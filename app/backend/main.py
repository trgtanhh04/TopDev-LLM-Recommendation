from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from get_jobs import get_jobs_endpoint
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Get allowed origins from .env
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow origins from .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs")
def get_jobs(page: int = Query(1, ge=1), perPage: int = Query(10, ge=1)) -> List[dict]:
    return get_jobs_endpoint(page, perPage)