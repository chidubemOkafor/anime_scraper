from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def email_transporter(reciever: str, subject: str, body: str, type: str, anime_name: str):
    sender_email = "anickal167@gmail.com"
    reciever_email = reciever
    password = "skgryteigqcagcxl"

    if type == "html":
        with open(body, 'r') as file:
            html_content = file.read()
        html_content = html_content.format(anime_name=anime_name)
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