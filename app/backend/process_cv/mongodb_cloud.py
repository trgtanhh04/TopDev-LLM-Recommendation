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
db = client["JobInfo"]
job_collection = db["jobs"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
jobs_path = os.path.join(BASE_DIR, '..', 'database', 'jobs.csv')
companies_path = os.path.join(BASE_DIR, '..', 'database', 'companies.csv')

jobs_df = pd.read_csv(jobs_path)
companies_df = pd.read_csv(companies_path)

def merge_job(jobs_df: pd.DataFrame, companies_df: pd.DataFrame) -> pd.DataFrame:
    company_images = companies_df[['name', 'small_image']]

    merged_df = pd.merge(
        jobs_df,
        company_images,
        left_on='company_name',
        right_on='name',
        how='left'
    )

    merged_df = merged_df.drop(columns=['name'])

    return merged_df

df_merge = merge_job(jobs_df, companies_df)

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
    if col in df_merge.columns:
        df_merge[col] = df_merge[col].apply(clean_list_string)

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

df_merge['address'] = df_merge['address'].apply(fix_address)

if "company_size" in df_merge.columns:
    df_merge["company_size"] = pd.to_numeric(df_merge["company_size"], errors="coerce")

# df = df.drop(columns=['no'])

# embedding + push to MongoDB
def text_emb(job_title, technologies_used):
    query = f'job title: {job_title}, skills: {", ".join(technologies_used)}'
    return get_embedding(query)

docs = []
for _, row in tqdm(df_merge.iterrows(), total=len(df_merge), desc="Embedding & build docs"):
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