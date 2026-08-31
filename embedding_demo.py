import os# python interac with os
import requests     #used to send http requests
from dotenv import load_dotenv # allows python to read variables in .env file


load_dotenv()                          # 1 check if your api is working 
#loading variables from .env file
# Get Voyage API key
api_key = os.getenv("VOYAGE_API_KEY")

# Text that we want to convert into an embedding
text = "A group of people try to escape from a maximum security prison."

# Voyage AI endpoint
url = "https://api.voyageai.com/v1/embeddings"

# api request info
headers = {
    "Authorization": f"Bearer {api_key}",# use
    "Content-Type": "application/json"
}

# Data we send to Voyage AI
data = {
    "input": [text],
    "model": "voyage-4",
    "input_type": "document"
}

# talking to Voyage AI
response = requests.post(# http post req
    url,
    headers=headers,
    json=data
)

# Stop if the API returned an error
response.raise_for_status()

# Convert response into Python data
result = response.json()

# Extract the embedding
embedding = result["data"][0]["embedding"]


# Display information about the embedding
print("Number of dimensions:", len(embedding))
print("First 5 values:", embedding[:5])