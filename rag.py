import json
import uuid
from openai import OpenAI
import os
import numpy as np
import faiss
from core.db import SessionLocal
from core.db_models import LogMemory

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

index = None
documents = []

def save_document(new_doc):
    db = SessionLocal()

    embedding = get_embedding(new_doc)

    db_log = LogMemory(
        id=str(uuid.uuid4()),
        log=new_doc,
        embedding=json.dumps(embedding)  # store as JSON
    )

    db.add(db_log)
    db.commit()
    db.close()

def load_documents():
    db = SessionLocal()
    rows = db.query(LogMemory).all()
    db.close()

    docs = [row.log for row in rows]
    embeddings = [json.loads(row.embedding) for row in rows]

    return docs, embeddings

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def initialize_index():
    global index, documents

    try:
        documents, embeddings = load_documents()

        if not documents:
            index = None
            return

        vectors = np.array(embeddings).astype("float32")

        dimension = len(vectors[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)

        print("Vector index ready (from DB embeddings)")

    except Exception as e:
        print("⚠️ Failed to initialize vector index:", str(e))
        index = None
        documents = []

def search_similar(query, threshold=0.7, k=5):
    global index, documents

    if index is None or not documents:
        return []

    query_vector = np.array([get_embedding(query)]).astype("float32")
    distances, indices = index.search(query_vector, k=min(k, len(documents)))

    results = []

    for dist, idx in zip(distances[0], indices[0]):
        similarity = 1 / (1 + dist)

        if similarity >= threshold:
            results.append(documents[idx])

    return results