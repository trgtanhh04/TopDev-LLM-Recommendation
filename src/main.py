from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import math

from dotenv import load_dotenv
load_dotenv() 
import sys
import os
from dateutil import parser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
from config.config import MONGO_URL
from info_extract import extract_text_from_pdf, extract_info
from src.embedding import get_embedding
from pymongo import MongoClient
from src.vector_db import MongoDBVectorDB

app = FastAPI()
faiss_index = None
EMBED_DIM = 1536

def safe_get(value, default="Unknown"):
    if value is None:
        return default
    if isinstance(value, str) and value.strip() == "":
        return default
    return value

def clean_invalid_floats(doc):
    def fix_value(v):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v
    return {k: fix_value(v) for k, v in doc.items() if k not in ['_id', 'embedding']}

# def deduplicate_jobs(jobs):
#     seen = set()
#     unique_jobs = []
#     for job in jobs:
#         key = (job.get('job_title'), job.get('company_name'), job.get('location'))
#         if key not in seen:
#             seen.add(key)
#             unique_jobs.append(job)
#     return unique_jobs


mongo = MongoClient(MONGO_URL)['tienanh']['jobs']

@app.post("/process_cv/")
async def process_cv(
    file: UploadFile = File(...)
):
    temp_path = f"data/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    text = extract_text_from_pdf(temp_path)
    info = extract_info(text)
    if "error" in info:
        raise HTTPException(status_code=400, detail=info["error"])

    job_title = safe_get(info.get("job_title"))
    skills = safe_get(info.get("skills"), [])
    try:
        query = f'job title: {job_title}, skills: {", ".join(skills)}'
        query_emb = get_embedding(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    mongo_vector_db = MongoDBVectorDB(mongo)
    matcheds = mongo_vector_db.search(query_emb, k=10)

    return {
        'extracted_info': info,
        'matched_jobs': [clean_invalid_floats(doc) for doc in matcheds]
    }
