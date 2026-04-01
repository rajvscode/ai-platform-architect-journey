from core.db import SessionLocal
from core.db_models import LogMemory
from openai import OpenAI
import os
import numpy as np
import faiss
import json
import uuid

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_documents():
    db = SessionLocal()
    rows = db.query(LogMemory).all()
    db.close()

    return [row.log for row in rows]


def save_document(new_doc):
    db = SessionLocal()
    db_log = LogMemory(id=str(uuid.uuid4()), log=new_doc)
    db.add(db_log)
    db.commit()
    db.close()

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_index(docs):
    if not docs:
        return None, []

    vectors = np.array([get_embedding(doc) for doc in docs]).astype("float32")
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)
    return index, docs


def search_similar(query, threshold=0.7, k=5):
    docs = load_documents()

    if not docs:
        return []

    index, docs = build_index(docs)

    query_vector = np.array([get_embedding(query)]).astype("float32")
    distances, indices = index.search(query_vector, k=min(k, len(docs)))

    results = []

    for dist, idx in zip(distances[0], indices[0]):
        similarity = 1 / (1 + dist)  # safer than 1 - dist

        if similarity >= threshold:
            results.append(docs[idx])

    return results