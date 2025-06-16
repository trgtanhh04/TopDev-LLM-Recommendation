from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
import os
import csv
import jwt
from datetime import datetime, timedelta

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = "HS256"
USERS_CSV = os.path.join(os.path.dirname(__file__), "database", "users.csv")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS").split(",")

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

def get_user_by_email(email):
    if not os.path.exists(USERS_CSV):
        return None
    with open(USERS_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["email"].lower() == email.lower():
                return row
    return None

def add_user(email, name):
    file_exists = os.path.exists(USERS_CSV)
    with open(USERS_CSV, "a", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["email", "name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"email": email, "name": name})
    return {"email": email, "name": name}

@router.get('/auth/google/login')
async def login_via_google(request: Request, next: str = Query("/")):
    # Pass 'next' as the OAuth state parameter
    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_REDIRECT_URI,
        prompt="select_account",
        state=next
    )

@router.get('/auth/google/callback')
async def auth_google_callback(request: Request, state: str = Query("/")):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = None
        try:
            user = await oauth.google.parse_id_token(request, token)
        except Exception as e:
            print("parse_id_token error:", e)
        if not user and "userinfo" in token:
            user = token["userinfo"]
        if not user and "id_token" in token:
            user = jwt.decode(token["id_token"], options={"verify_signature": False})
        email = user.get("email") if user else None
        name = user.get("name") if user else None
        if not email:
            return JSONResponse({"error": "No email found in user info"}, status_code=400)

        db_user = get_user_by_email(email)
        if not db_user:
            db_user = add_user(email, name)

        payload = {
            "sub": email,
            "name": name,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Use ALLOW_ORIGINS for redirect security
        if state.startswith("http://") or state.startswith("https://"):
            if not any(state.startswith(origin) for origin in ALLOW_ORIGINS):
                state = "/"
            redirect_url = f"{state}?token={jwt_token}"
        else:
            redirect_url = f"{ALLOW_ORIGINS[0]}{state}?token={jwt_token}"

        return RedirectResponse(redirect_url)
    except Exception as e:
        print("Error in auth_google_callback:", e)
        return JSONResponse({"error": str(e)}, status_code=400)