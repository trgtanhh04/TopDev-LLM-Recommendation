from mistralai import Mistral
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import MISTRAL_API_KEY, EMBEDDING_MODEL_NAME  
import pandas as pd
import time

client = Mistral(api_key=MISTRAL_API_KEY)

def get_embedding(text: str) -> list[float]:
    res = client.embeddings.create(
        model=EMBEDDING_MODEL_NAME,
        inputs=[text]       
    )
    return res.data[0].embedding 

