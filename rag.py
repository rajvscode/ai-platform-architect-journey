from openai import OpenAI
import os
import numpy as np
import faiss

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory store
documents = [
    "Kafka timeout usually happens due to broker overload",
    "Database connection pool exhaustion occurs due to high concurrency",
    "NullPointerException occurs when object is not initialized"
]

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# Create vector index
dimension = 1536
index = faiss.IndexFlatL2(dimension)

vectors = np.array([get_embedding(doc) for doc in documents]).astype("float32")
index.add(vectors)


def search_similar(query):
    query_vector = np.array([get_embedding(query)]).astype("float32")
    distances, indices = index.search(query_vector, k=2)
    return [documents[i] for i in indices[0]]