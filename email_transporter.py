from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def email_transporter(reciever: str, subject: str, body: str, type: str, anime_name: str | list):
    sender_email = "anickal167@gmail.com"
    reciever_email = reciever
    password = os.getenv("EMAIL_PASSWORD")

    if type == "html":
        with open(body, 'r') as file:
            html_content = file.read()
        
        anime_list_items = "\n".join(f"<li>name: {anime['anime_name']}  time: {anime['release_time']}</li>" for anime in anime_name)
        if isinstance(anime_name, str):
            anime_name_to_use = anime_name
        else:
            anime_name_to_use = anime_list_items

        # Format the html_content
        html_content = html_content.format(anime_list=anime_name_to_use)
        print(html_content)
    else:
        html_content = body

    #message body
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = reciever

    #message body
    part1 = MIMEText(html_content,type)

    #Attach the email body
    message.attach(part1)

    #send the email using gmail's SMTP server

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")