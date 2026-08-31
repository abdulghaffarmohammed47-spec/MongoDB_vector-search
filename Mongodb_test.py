import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")
# creating mongodb connection
client = MongoClient(mongodb_uri) #represents your connection to the MongoDB deployment.

db = client["sample_mflix"] # from clint connection give me this data base 
movies = db["movies"]

movie = movies.find_one()
#check if your mongodb connection is successful
print("MongoDB connection successful!")
print("Movie title:", movie["title"])
print("Movie plot:", movie.get("plot"))