import os
import jwt
from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = "HS256"

@router.post("/dev-get-token")
def dev_get_token():
    payload = {
        "sub": "testuser@example.com",
        "name": "Test User",
        "exp": datetime.utcnow() + timedelta(days=60)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"token": token}