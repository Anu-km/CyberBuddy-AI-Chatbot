from sentence_transformers import SentenceTransformer
import numpy as np
from db import knowledge_collection

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=3):
    q_vec = embed(query)
    results = []

    for doc in knowledge_collection.find():
        score = cosine(q_vec, np.array(doc["embedding"]))
        results.append((score, doc["text"], doc.get("source", "")))

    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_k]
