import os
import pandas as pd
import json
import fitz
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import requests
import re

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY", "8h738jV32gjV9nO7l2nphveXhkhsKao5")
API_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL_NAME = "mistral-medium"

prompt_template = """
Extract the following candidate information fields from the CV content (as plain text) below in the exact JSON format:
{{
"full_name": "...",
"email": "...",
"phone": "...",
"job_title": "...",
"education": [
    {{
    "degree": "...",
    "university": "..."
    }}
],
"experience": [
    {{
    "job_title": "...",
    "company": "...",
    "description": "..."
    }}
],

"years_of_experience": "...",
"skills": ["...", "..."],
"certifications": [
    {{
    "certificate_name": "...",
    "organization": "..."
    }}
],
"languages": ["...", "..."]
}}

Only include **real work experience** (e.g. internships, jobs at companies, freelance work) in the "experience" field.  
**Do not include personal, academic, or side projects** in the experience section.

Only return the JSON content. Do not include any explanation.  
If any field cannot be found, set it to null or empty array.

CV content:
{text}
"""

# Process info user after extraction
def safe_get(value, default='Unknown'):
    if value is None:
        return default
    if isinstance(value, list) and value.strip() == "":
        return "Unknown"
    
    return value if value else default


# Extract info from CVs or resumes in PDF format
def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def extract_info(text: str) -> dict:
    prompt = prompt_template.format(text=text)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()

        match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", content)
        if match:
            json_str = match.group(1)
        else:
            json_str = content
        return json.loads(json_str)
    except Exception as e:
        error_msg = str(e)
        raw_response = None
        if 'response' in locals():
            try:
                raw_response = response.text
            except Exception:
                raw_response = None
        return {"error": error_msg, "raw_response": raw_response}
    
if __name__ == "__main__":
    # Example usage
    pdf_text = extract_text_from_pdf("E:\\test-project\\data\\CV1 - Copy.pdf")
    candidate_info = extract_info(pdf_text)
    print(candidate_info)