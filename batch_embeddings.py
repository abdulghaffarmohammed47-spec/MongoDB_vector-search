import os
import time
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
                                 #batch embeddings for multiple data and store it in mongodb
load_dotenv()

# MongoDB
mongodb_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongodb_uri)

db = client["sample_mflix"]
movies = db["movies"]

# Voyage AI
api_key = os.getenv("VOYAGE_API_KEY")

url = "https://api.voyageai.com/v1/embeddings"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

BATCH_SIZE = 5


def generate_embeddings(plots):# accept plot (list of movie plots)

    data = {
        "input": plots,
        "model": "voyage-4",
        "input_type": "document"
    }

    wait_time = 30

    while True:

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        if response.status_code == 429:

            print(
                f"Rate limit reached. "
                f"Waiting {wait_time} seconds..."
            )

            time.sleep(wait_time)#pauses the Python program.

            wait_time *= 2# exponential backoff.

            continue

        response.raise_for_status()

        return response.json()#convert the JSON response into Python data


# Find movies that still need embeddings
cursor = movies.find({
    "plot": {"$exists": True},
    "plot_embedding": {"$exists": False}#Give me movies that have a plot but don't have a plot_embedding yet.
})

batch = []
total_processed = 0

for movie in cursor:

    batch.append(movie)#batch = [Movie1, Movie2, Movie3, Movie4, Movie5]

    if len(batch) == BATCH_SIZE:
        print( # just printing how many batches you are processing now
            f"\nProcessing batch of {len(batch)} movies..."
        )

#batch = [
   # {"title": "A", "plot": "Plot A"},
   # {"title": "B", "plot": "Plot B"},
    #{"title": "C", "plot": "Plot C"}
    #]
        plots = [    #Extract only the plots
            movie["plot"]
            for movie in batch
        ]
    # plots = [
    #       "Plot A",
    #       "Plot B",
    #       "Plot C"
    #    ]

        result = generate_embeddings(plots)

        embeddings = result["data"]#list of 5 embedding result

        for movie, embedding_data in zip(
            batch,
            embeddings
        ):
            #Movie 1 → Embedding 1
            #Movie 2 → Embedding 2
            #Movie 3 → Embedding 3
            #Movie 4 → Embedding 4
            #Movie 5 → Embedding 5

            embedding = embedding_data["embedding"]

            movies.update_one(
                {"_id": movie["_id"]},
                {
                    "$set": {
                        "plot_embedding": embedding
                    }
                }
            )

            total_processed += 1

        print(
            f"Batch completed. "
            f"Total processed: {total_processed}"
        )

        batch = []

        # Pause between batches
        time.sleep(5)


# Process remaining movies
if batch:

    print(
        f"\nProcessing final batch "
        f"of {len(batch)} movies..."
    )

    plots = [
        movie["plot"]
        for movie in batch
    ]

    result = generate_embeddings(plots)

    embeddings = result["data"]

    for movie, embedding_data in zip(
        batch,
        embeddings
    ):

        embedding = embedding_data["embedding"]

        movies.update_one(
            {"_id": movie["_id"]},
            {
                "$set": {
                    "plot_embedding": embedding
                }
            }
        )

        total_processed += 1


print("\nBatch job completed!")
print(
    "Total new embeddings generated:",
    total_processed
)