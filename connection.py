from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
# Define your MongoDB connection and database/collection
client = MongoClient(f'mongodb+srv://okaforchidubem7:{os.getenv("PASSWORD")}@cluster0.coflu6v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['test']



