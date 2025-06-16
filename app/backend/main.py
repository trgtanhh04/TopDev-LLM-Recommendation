from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from typing import Dict
from get_jobs import get_jobs_endpoint
from get_suggested_jobs import get_suggested_jobs_endpoint
from get_job_detail import get_job_detail_endpoint
from oauth import router as oauth_router
import os

app = FastAPI()

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")

# Determine cookie settings based on redirect URI scheme
if GOOGLE_REDIRECT_URI.startswith("https"):
    COOKIE_SAMESITE = "none"
    COOKIE_SECURE = True
else:
    COOKIE_SAMESITE = "lax"
    COOKIE_SECURE = False

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    same_site=COOKIE_SAMESITE,
    https_only=COOKIE_SECURE
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oauth_router)

@app.get("/jobs")
def get_jobs(page: int = Query(1, ge=1), perPage: int = Query(10, ge=1)) -> Dict:
    return get_jobs_endpoint(page, perPage)

@app.get("/suggested-jobs")
def get_suggested_jobs(perPage: int = Query(5, ge=1)) -> Dict:
    return get_suggested_jobs_endpoint(perPage)

@app.get("/job-detail")
def get_job_detail(job_title: str, company_name: str) -> Dict:
    return get_job_detail_endpoint(job_title, company_name)