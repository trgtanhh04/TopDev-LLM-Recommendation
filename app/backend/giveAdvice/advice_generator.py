import os
import json
import requests
import re
from dotenv import load_dotenv

# Load Mistral API key
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY", "8h738jV32gjV9nO7l2nphveXhkhsKao5")
API_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL_NAME = "mistral-medium"

# Hàm gọi API
def get_advice_from_cv_and_job(cv_info: dict, job_info: dict) -> dict:
    prompt_template = """
        You are a professional career advisor. Based on the candidate's CV and the job description, analyze and return structured feedback:

        CV:
        {cv_json}

        Job Description:
        {job_json}

        Return a JSON response in this format:
        {{
        "match_score": 0-100,
        "missing_skills": ["skill1", "skill2", "..."],
        "recommendations": [
            {{
            "skill": "skill name",
            "course": "course name",
            "link": "course url"
            }}
        ],
        "summary": "Short advice summary (3-4 lines)"
        }}

        Only return valid JSON. Do not include explanation or code block markers.
    """


    prompt = prompt_template.format(
        cv_json=json.dumps(cv_info, ensure_ascii=False),
        job_json=json.dumps(job_info, ensure_ascii=False)
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        content = re.sub(r"^```(?:json)?|```$", "", content.strip())
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "raw_response": response.text if 'response' in locals() else None
        }

cv_info = {
    "full_name": "HOANG HUU TUYEN",
    "email": "hoanghuutuyen06022004@gmail.com",
    "phone": "0392159388",
    "job_title": None,
    "education": [
        {
            "degree": "Information technology",
            "university": "Academy Of Cryptography Techniques"
        }
    ],
    "experience": [],
    "skills": [
        "Java(Spring Boot)", "JavaScript(React)", "HTML", "CSS", "SQLServer", "MySQL",
        "MongoDB", "Spring Security", "Spring Cloud", "Kafka", "Redis", "AWS S3", "Brevo",
        "Problem-solving", "Teamwork", "Effective communication"
    ],
    "certifications": [],
    "languages": ["English"]
}

job_info = {
    "job_title": "UX/UI Designer (Game)",
    "company_name": "CÔNG TY CỔ PHẦN SUNTEK",
    "salary": "Thương lượng",
    "address": ["Thành phố Thủ Đức, Hồ Chí Minh"],
    "date_posted": ["Đăng 1 giờ trước"],
    "industry": ["Giải trí/ Game"],
    "company_size": ["25-99 Nhân viên"],
    "company_nationality": ["Thailand"],
    "experience_years": ["Từ 2 năm"],
    "position_level": ["Junior", "Middle"],
    "employment_type": ["In Office"],
    "contract_type": ["Fulltime"],
    "technologies_used": ["UX/UI Design", "HTML & CSS", "UI/UX"],
    "job_description": [
        "Trách nhiệm công việc",
        "1. General task",
        "Have aesthetic thinking, color coordination and layout...",
        "Can use one of the product design tools such as: Figma, Adobe Illustrator, Photoshop...",
        "Ability to take clear notes in design files.",
        "Ability to organize design documents scientifically.",
        "Design the interface of menus, buttons, tabs, pop-ups, and graphical user interface elements.",
        "Create user interface mockups and prototypes that clearly demonstrate how the website works and looks.",
        "Make unique designs that improve the user experience and match game themes."
    ]
}

if __name__ == "__main__":
    advice = get_advice_from_cv_and_job(cv_info, job_info)
    print(json.dumps(advice, indent=2, ensure_ascii=False))
