import pandas as pd
from pymongo import MongoClient
import ast
from embedding import get_embedding
from tqdm import tqdm
import os
import sys
import re
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import MISTRAL_API_KEY, EMBEDDING_MODEL_NAME, MONGO_URL

client = MongoClient(MONGO_URL)
db = client["tienanh"]
job_collection = db["jobs"]

df = pd.read_csv("E:/test-project/data/preprocessed_data.csv")

# process the DataFrame
list_columns = [
    "industry", "company_nationality", "position_level",
    "employment_type", "contract_type", "technologies_used"
]

def clean_list_string(val):
    if pd.isna(val):
        return []
    if isinstance(val, list):
        return val
    try:
        val = str(val)
        val = re.sub(r"[\[\]]", "", val) 
        parts = [x.strip(" '\"") for x in val.split(",") if x.strip(" '\"")]
        return parts
    except Exception:
        return []

for col in list_columns:
    if col in df.columns:
        df[col] = df[col].apply(clean_list_string)

def fix_address(val):
    if isinstance(val, list) and len(val) == 1:
        return val[0] 
    elif isinstance(val, str):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list) and len(parsed) == 1:
                return parsed[0]
        except:
            pass
    return val

df['address'] = df['address'].apply(fix_address)

if "company_size" in df.columns:
    df["company_size"] = pd.to_numeric(df["company_size"], errors="coerce")

df = df.drop(columns=['no'])

# embedding + push to MongoDB
def text_emb(job_title, technologies_used):
    query = f'job title: {job_title}, skills: {", ".join(technologies_used)}'
    return get_embedding(query)

docs = []
for _, row in tqdm(df.iterrows(), total=len(df), desc="Embedding & build docs"):
    job_title = row.get('job_title', '')
    techs = row.get('technologies_used', '')

    doc = row.to_dict()
    emd = text_emb(job_title, techs)
    doc['embedding'] = emd
    docs.append(doc)
    time.sleep(1.1)

# Insert documents into MongoDB
if docs:
    job_collection.insert_many(docs)
    print(f"Inserted {len(docs)} documents into MongoDB.")
else:
    print("No documents to insert into MongoDB.")