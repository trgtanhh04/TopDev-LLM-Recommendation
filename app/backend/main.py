from fastapi import FastAPI, Query
from typing import List
from get_jobs import get_jobs_endpoint

app = FastAPI()

@app.get("/jobs")
def get_jobs(page: int = Query(1, ge=1), perPage: int = Query(10, ge=1)) -> List[dict]:
    return get_jobs_endpoint(page, perPage)