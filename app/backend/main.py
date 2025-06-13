from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from get_jobs import get_jobs_endpoint
from get_suggested_jobs import get_suggested_jobs_endpoint
from get_job_detail import get_job_detail_endpoint

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs")
def get_jobs(page: int = Query(1, ge=1), perPage: int = Query(10, ge=1)) -> Dict:
    return get_jobs_endpoint(page, perPage)

@app.get("/suggested-jobs")
def get_suggested_jobs(perPage: int = Query(5, ge=1)) -> Dict:
    return get_suggested_jobs_endpoint(perPage)

@app.get("/job-detail")
def get_job_detail(job_title: str, company_name: str) -> Dict:
    return get_job_detail_endpoint(job_title, company_name)