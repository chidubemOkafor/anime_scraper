import aiohttp
from bs4 import BeautifulSoup
from pymongo import MongoClient
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Define your MongoDB connection and database/collection
client = MongoClient(f'mongodb+srv://okaforchidubem7:{os.getenv("PASSWORD")}@cluster0.coflu6v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['anime_database']
collection = db['anime_collection']

# Clear the collection before inserting new data


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_anime_data(url):
    anime_list = []
    async with aiohttp.ClientSession() as session:
        response_text = await fetch_url(session, url)
        soup = BeautifulSoup(response_text, 'html.parser')

        # Debugging: print the fetched HTML
        print(f"Scraping URL: {url}")

        latest_anime = soup.find_all("div", class_="anime-tile lozad")
        
        for anime in latest_anime:
            anime_dict = {}
            name = anime.find("h2", class_="anime-tile-title").text if anime.find("h2", class_="anime-tile-title") else "N/A"
            rating = anime.find("strong", class_="anime-tile-rating-score")
            description = anime.find("p", class_="anime-tile-description").text if anime.find("p", class_="anime-tile-description") else "N/A"
            genres = anime.find_all("a", class_="anime-tile-genre")
            episodes = anime.find_all("div", class_="anime-tile-bottom-item")
            genre_texts = [genre.text for genre in genres]
            date = anime.find("time", class_="anime-tile-bottom-item anime-tile-datetime").text if anime.find("time", class_="anime-tile-bottom-item anime-tile-datetime") else "N/A"
            duration = anime.find_all("div", class_="anime-tile-bottom-item anime-tile-bottom-item-length")

            new_url = "https://animeschedule.net" + anime.find("a")["href"] if anime.find("a") else ""
            anime_response_text = await fetch_url(session, new_url)
            anime_soup = BeautifulSoup(anime_response_text, 'html.parser')
            
            anime_url = anime_soup.find("div", id="page-content-wrapper")
            thumbnail = anime_url.find("img", id="anime-poster")["src"] if anime_url.find("img", id="anime-poster") else "N/A"
            show_type = anime_url.find_all("a", class_="information-link")
            status = anime_url.find_all("div", class_="information-content-wrapper")
            main_status = status[3].find("div") if len(status) > 3 else None
            alternative_name = anime_url.find("div", class_="alternative-name")
            anime_website_element = anime_url.find("a", class_="anime-link official-link")
            anime_website = anime_website_element["href"] if anime_website_element else "N/A"
            release_time_sub = anime_url.find("time", id="release-time-subs")
            anime_link_container = anime_url.find("div", class_="links-container")
            streaming_sites = [link["href"] for link in anime_link_container.find_all("a", class_="anime-link")] if anime_link_container else []

            anime_dict["name"] = name
            anime_dict["alt_name"] = alternative_name.text if alternative_name else "N/A"
            anime_dict["description"] = description
            anime_dict["thumbnail"] = thumbnail
            anime_dict["genre"] = genre_texts
            anime_dict["rating"] = rating.text if rating else "N/A"
            anime_dict["episodes"] = episodes[1].text if len(episodes) > 1 else "N/A"
            anime_dict["duration"] = duration[1].text if len(duration) > 1 else "N/A"
            anime_dict["launch_date"] = date.strip() if date else "N/A"
            anime_dict["type"] = show_type[0].text if len(show_type) > 0 else "N/A"
            anime_dict["season"] = show_type[1].text if len(show_type) > 1 else "N/A"
            anime_dict["source"] = show_type[2].text if len(show_type) > 2 else "N/A"
            anime_dict["release_time(sub)"] = release_time_sub.text if release_time_sub else "N/A"
            anime_dict["streaming_sites"] = streaming_sites
            anime_dict["official_website"] = anime_website

            anime_list.append(anime_dict)
            collection.insert_one(anime_dict)  # Insert each anime_dict into MongoDB

    print("Scraping and insertion complete")
    return anime_list

def update_collection():
    result = collection.delete_many({})
    print(f"Documents deleted: {result.deleted_count}")

    current_year = datetime.now().year

    seasons = ["spring", "summer", "fall"]

    for season in seasons:
        result = asyncio.run(scrape_anime_data(f"https://animeschedule.net/seasons/{season}-{current_year}"))

update_collection()

