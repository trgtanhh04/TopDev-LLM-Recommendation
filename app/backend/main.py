from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from typing import Dict
from get_jobs import get_jobs_endpoint
from get_suggested_jobs import get_suggested_jobs_endpoint
from get_job_detail import get_job_detail_endpoint
from oauth import router as oauth_router
from upload_cv import router as upload_cv_router
from dev_get_token import router as dev_get_token_router
from rcm_job_from_cv import process_cv_logic
from config.config import MONGO_URL
import os

app = FastAPI()

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS").split(",")

# Determine cookie settings based on redirect URI scheme
if GOOGLE_REDIRECT_URI and GOOGLE_REDIRECT_URI.startswith("https"):
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
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(oauth_router)
app.include_router(upload_cv_router)
app.include_router(dev_get_token_router)

@app.get("/jobs")
def get_jobs(page: int = Query(1, ge=1), perPage: int = Query(10, ge=1)) -> Dict:
    return get_jobs_endpoint(page, perPage)

@app.get("/suggested-jobs")
def get_suggested_jobs(perPage: int = Query(5, ge=1)) -> Dict:
    return get_suggested_jobs_endpoint(perPage)

@app.get("/job-detail")
def get_job_detail(job_title: str, company_name: str) -> Dict:
    return get_job_detail_endpoint(job_title, company_name)

@app.post("/process_cv")
async def process_cv(file: UploadFile = File(...)):
    return await process_cv_logic(file)

# uvicorn main:app --reload