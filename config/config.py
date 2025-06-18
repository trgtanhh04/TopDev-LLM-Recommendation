import os
from dotenv import load_dotenv
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", '8h738jV32gjV9nO7l2nphveXhkhsKao5')
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "mistral-embed")
MONGO_URL = os.getenv("MONGO_URI", "mongodb+srv://tienanh:tienanh@tienanh.mdznrij.mongodb.net/?retryWrites=true&w=majority&appName=Tienanh")