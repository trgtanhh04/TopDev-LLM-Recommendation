from typing import Dict
import pandas as pd

def get_job_detail_endpoint(job_title: str, company_name: str) -> Dict:
    jobs_data = pd.read_csv('./database/jobs.csv')
    companies_data = pd.read_csv('./database/companies.csv')

    job_row = jobs_data[
        (jobs_data['job_title'] == job_title) &
        (jobs_data['company_name'] == company_name)
    ]

    if job_row.empty:
        return {"error": "Job not found"}

    # Merge with company info to get additional fields
    merged = pd.merge(
        job_row,
        companies_data[['name', 'small_image', 'company_profile', 'image_galleries']],
        left_on='company_name',
        right_on='name',
        how='left'
    )

    # Select only the required fields
    fields = [
        'job_title', 'company_name', 'salary', 'address', 'date_posted', 'industry',
        'company_size', 'company_nationality', 'experience_years', 'position_level',
        'employment_type', 'contract_type', 'technologies_used', 'job_description',
        'small_image', 'company_profile', 'image_galleries'
    ]
    job_detail = merged[fields].iloc[0].to_dict()

    return {"job_detail": job_detail}