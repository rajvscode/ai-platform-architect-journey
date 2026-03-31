from openai import OpenAI
import os
import numpy as np
import faiss
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MEMORY_FILE = "memory.json"


def load_documents():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_document(new_doc):
    docs = load_documents()
    docs.append(new_doc)

    with open(MEMORY_FILE, "w") as f:
        json.dump(docs, f, indent=2)


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_index(docs):
    vectors = np.array([get_embedding(doc) for doc in docs]).astype("float32")
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)
    return index, docs


def search_similar(query):
    docs = load_documents()
    index, docs = build_index(docs)

    query_vector = np.array([get_embedding(query)]).astype("float32")
    distances, indices = index.search(query_vector, k=2)

    return [docs[i] for i in indices[0]]