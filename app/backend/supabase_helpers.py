import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_by_email(email):
    response = supabase.table("users").select("*").eq("email", email).limit(1).execute()
    data = response.data
    if data:
        return data[0]
    else:
        return None

def add_user(email, name):
    response = supabase.table("users").insert({"email": email, "name": name}).execute()
    return response.data[0] if response.data else None