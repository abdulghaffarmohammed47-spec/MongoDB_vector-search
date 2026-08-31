# Vector Search with MongoDB & Voyage AI

This project demonstrates how to connect to MongoDB Atlas, generate dense vector embeddings for movie plots using Voyage AI (`voyage-4`), and store them in MongoDB for vector search workflows.

---

## Features

* **MongoDB Connection**: Connects to the `sample_mflix` database and accesses the `movies` collection.


* **Voyage AI Integration**: Generates vector embeddings using the `voyage-4` model.


* **Batch Processing**: Processes documents in configurable batches with exponential backoff for handling HTTP 429 rate limits.


* **Incremental Updates**: Detects and updates only movies where `plot_embedding` is missing.



---

## Prerequisites

* Python 3.8+
* A MongoDB Atlas account with the `sample_mflix` dataset loaded


* A Voyage AI API key



---

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/mongodb-vector-search.git
cd mongodb-vector-search

```


2. **Install dependencies**:
```bash
pip install requests pymongo python-dotenv

```


3. **Configure environment variables**:
Create a `.env` file in the root directory:


```env
VOYAGE_API_KEY=your_voyage_api_key_here
MONGODB_URI=your_mongodb_connection_string_here

```



---

## Usage

### 1. Test MongoDB Connection

Verify connectivity to your MongoDB database:

```bash
python test_connection.py

```

### 2. Test Single Embedding Generation

Generate a sample vector embedding using Voyage AI to inspect dimensions and vector output:

```bash
python single_embedding.py

```

### 3. Generate & Store Single Movie Embedding

Fetch a single movie from MongoDB, create its embedding, and store it back into the database:

```bash
python store_single.py

```

### 4. Run Batch Embedding Pipeline

Batch process all movies that currently lack embeddings with rate-limit handling and progress tracking:

```bash
python batch_embeddings.py

```

---

## Vector Search Index Setup (MongoDB Atlas)

To query these vectors in MongoDB Atlas, create a Vector Search Index on the `sample_mflix.movies` collection:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "plot_embedding",
      "numDimensions": 1024,
      "similarity": "cosine"
    }
  ]
}

```

---

## Environment Variables

| Variable | Description |
| --- | --- |
| `VOYAGE_API_KEY` | API key from Voyage AI for embedding endpoints

 |
| `MONGODB_URI` | MongoDB Atlas connection string

 |
