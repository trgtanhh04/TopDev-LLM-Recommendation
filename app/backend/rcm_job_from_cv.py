import math
from fastapi import UploadFile, File, HTTPException
from pymongo import MongoClient
from config.config import MONGO_URL
from process_cv.info_extract import extract_text_from_pdf, extract_info
from process_cv.embedding import get_embedding
from process_cv.vector_db import MongoDBVectorDB

EMBED_DIM = 1536
mongo = MongoClient(MONGO_URL)['JobInfo']['jobs']

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

async def process_cv_logic(file: UploadFile = File(...)):
    temp_path = f"database/{file.filename}"
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
