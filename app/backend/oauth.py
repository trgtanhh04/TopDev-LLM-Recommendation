from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
import os

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get('/auth/google/login')
async def login_via_google(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_REDIRECT_URI,
        prompt="select_account"
    )

@router.get('/auth/google/callback')
async def auth_google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        print("Token:", token)
        user = None
        # Try to parse id_token, fallback to userinfo, fallback to token itself
        try:
            user = await oauth.google.parse_id_token(request, token)
        except Exception as e:
            print("parse_id_token error:", e)
        if not user and "userinfo" in token:
            user = token["userinfo"]
        if not user and "id_token" in token:
            import jwt
            user = jwt.decode(token["id_token"], options={"verify_signature": False})
        print("User:", user)
        email = user.get("email") if user else None
        if not email:
            return JSONResponse({"error": "No email found in user info"}, status_code=400)
        response = RedirectResponse(f"{FRONTEND_URL}/?user={email}")
        return response
    except Exception as e:
        print("Error in auth_google_callback:", e)
        return JSONResponse({"error": str(e)}, status_code=400)