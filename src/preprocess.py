import pandas as pd
import ast 
import re
import os
import pandas as pd
import json
from dotenv import load_dotenv
from tqdm import tqdm
import sys

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.backend.config.config import OPEN_API_KEY, LLM_MODEL_NAME

def upload_csv(file_path: str):
    df = pd.read_csv(file_path)
    return df

# ========== Preprocessing Functions ==========
def literal_eval(val):
    if isinstance(val, str):
        try:
            if not val.strip():
                return []
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return [] 
    elif pd.isna(val):
        return []
    if isinstance(val, list):
        return val
    return []

def clean_text(text, default_val=""):
    if not isinstance(text, (str, list)) or not text:
        return default_val

    if isinstance(text, str):
        items = [item.strip() for item in text.split(",") if item.strip()]
    else:
        items = [str(item).strip() for item in text if item is not None and str(item).strip()]
    if not items:
        return default_val

    cleaned_text = items[0] 
    for item in items[1:]:
        cleaned_text += f", {item}"

    return cleaned_text


def preprocess_data(input_path):
    df = pd.read_csv(input_path)

    cols = ['job_title', 'company_name', 'job_description', 'industry', 'address', 'technologies_used']
    for col in cols:
        df[col] = df[col].fillna('')

    df = df[df['job_title'].astype(str).str.strip() != '']
    df = df[df['job_description'].astype(str).str.strip() != '']

    list_cols = ['address', 'industry', 'technologies_used', 'position_level']
    for col in list_cols:
        df[col] = df[col].apply(literal_eval)

    df['processed_industry'] = df['industry'].apply(
        lambda x: x[0] if isinstance(x, list) and x and isinstance(x[0], str) and x[0].strip() else "Không xác định"
    )

    df['cleaned_job_description'] = df['job_description'].astype(str).apply(
        lambda x: re.sub(r'\\n', ' ', x)
    )
    df['cleaned_job_description'] = df['cleaned_job_description'].apply(
        lambda x: re.sub(r'\s+', ' ', x.replace('\n', ' ')).strip()
    )

    job_title = df['job_title'].astype(str).str.strip()
    company_name = "Công ty: " + df['company_name'].astype(str).str.strip()
    industry = "Ngành nghề: " + df['processed_industry'].astype(str).str.strip()

    address = df['address'].apply(lambda x: clean_text(x, default_val=""))
    address = address.apply(lambda x: "Địa điểm: " + x if x else "")

    tech = df['technologies_used'].apply(lambda x: clean_text(x, default_val=""))
    tech = tech.apply(lambda x: "Công nghệ sử dụng: " + x if x else "")

    description = "Mô tả công việc: " + df['cleaned_job_description']

    job_texts = []
    for i in range(len(df)):
        parts = [
            job_title.iat[i],
            company_name.iat[i],
            industry.iat[i],
            address.iat[i],
            tech.iat[i],
            description.iat[i]
        ]
        filtered_parts = [part for part in parts if part]
        job_text = ". ".join(filtered_parts)
        job_texts.append(job_text)

    df['job_text'] = job_texts

    df['job_text'] = df['job_text'].str.replace(r'\.\s*\.(?=\s|$)', '.', regex=True)\
                                   .str.replace(r'^\.\s*', '', regex=True).str.strip()

    df.drop_duplicates(subset=['job_text'], keep='first', inplace=True)

    return df

def save_data(df, output_path):
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    input_path = 'data/preprocessed_data.csv'
    output_path = 'data/test.csv'
    
    df = preprocess_data(input_path)
    save_data(df, output_path)


