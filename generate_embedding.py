import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Get credentials
api_key = os.getenv("VOYAGE_API_KEY")
mongodb_uri = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(mongodb_uri)

db = client["sample_mflix"]
movies = db["movies"]

# Get one movie
movie = movies.find_one({
    "plot": {"$exists": True}
})

print("Movie:", movie["title"])
print("Plot:", movie["plot"])

# Send plot to Voyage AI
url = "https://api.voyageai.com/v1/embeddings"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "input": [movie["plot"]],
    "model": "voyage-4",
    "input_type": "document"
}

response = requests.post(
    url,
    headers=headers,
    json=data
)

response.raise_for_status()

result = response.json()

# Get embedding
embedding = result["data"][0]["embedding"]

print("Number of dimensions:", len(embedding))
print("First 5 values:", embedding[:5])
                        
# Store embedding in MongoDB
movies.update_one(
    {"_id": movie["_id"]},
    {
        "$set": {
            "plot_embedding": embedding
        }
    }
)

print("Embedding stored successfully!")