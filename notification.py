import uuid
from connection import db
from datetime import datetime
import time
import json
from email_transporter import email_transporter

current_date = datetime.now().date()
print("current date",current_date)

release_array = []
filtered_array = []

date_format = "%A %d %b, %I:%M %p"

def get_tracking_anime_detail():

    user_collection = db["users"]
    anime_collection = db["animecollections"]
    users = user_collection.find({})

    for user in users:
        user_anime_array = user["trackingAnimes"]

        for anime in user["trackingAnimes"]:
                        
            release_dict = {
                "username": user["username"],
                "email": user["email"],
                "anime_name": anime
            }

            anime_detail = anime_collection.find_one({"name": anime})

            if anime_detail:
                release_dict["release_time"] = anime_detail["release_time(sub)"]
                release_array.append(release_dict)
            
            else:
                user_anime_array.remove(anime)
                user_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"trackingAnimes": user_anime_array}}
                )
                print(f"Anime '{anime}' removed and trackingAnimes updated.")

def filter_for_current_date(release_array):
    print("released array", release_array)
    for anime in release_array:
        if anime["release_time"] != 'N/A':
            launch_date = datetime.strptime(anime["release_time"], date_format)

            if launch_date.month == current_date.month and launch_date.day != current_date.day:

                new_dict = {
                    **anime,
                    "release_time": launch_date.strftime("%I:%M %p"),
                    "is_sent": False
                }
                filtered_array.append(new_dict)
    print(json.dumps(filtered_array, indent=4))

def send_email(mode: str):
    current_time = datetime.now().strftime("%I:%M %p")

    print("listening...")

    for anime in filtered_array:
        if anime["release_time"] >= current_time and anime["is_sent"] == False:
            email_transporter(
                anime["email"],
                "Show Update",
                "email_content.html" if mode == "worker" else "email_cron_content.html", 
                "html", 
                anime["anime_name"] if mode == "worker" else filtered_array
                )
            anime["is_sent"] = True
        
    print("listening...")


def email_notification(mode: str):
    get_tracking_anime_detail()
    filter_for_current_date(release_array)

    if mode == "worker":
        while True:
            send_email("worker")
            time.sleep(60)
    else:
        print("job ran!")
        send_email("job")

