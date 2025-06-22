import faiss
import numpy as np
import json
from typing import List, Dict, Any

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

class MongoDBVectorDB:
    def __init__(self, mongo_collection):
        self.mongo_collection = mongo_collection

    def search(self, query_vector, k=5):
        # Chỉ lấy trường cần thiết
        jobs = list(self.mongo_collection.find(
            {'embedding': {'$exists': True}},
            {'_id': 0}
        ))
        results = []
        for job in jobs:
            emb = job.get('embedding')
            if emb:
                sim = cosine_similarity(query_vector, emb)
                job['similarity'] = sim
                results.append(job)

        results = sorted(results, key=lambda x: x['similarity'], reverse=True)
        return results[:k]
