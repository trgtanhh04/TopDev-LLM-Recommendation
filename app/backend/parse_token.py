import os
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = "HS256"
security = HTTPBearer()

def get_email_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("email") or payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token: no email found")
        return email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")