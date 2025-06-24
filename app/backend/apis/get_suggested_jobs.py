from typing import Dict
import pandas as pd
import random

def get_suggested_jobs_endpoint(perPage: int = 5) -> Dict:
    jobs_data = pd.read_csv('./database/jobs.csv')
    companies_data = pd.read_csv('./database/companies.csv')

    merged_data = pd.merge(
        jobs_data,
        companies_data[['name', 'small_image']],
        left_on='company_name',
        right_on='name',
        how='left'
    )
    # Randomly sample jobs
    suggested_data = merged_data.sample(n=min(perPage, len(merged_data)), random_state=None)

    jobs = suggested_data[[
        'job_title', 'company_name', 'small_image', 'technologies_used'
    ]]

    return {
        "suggested-jobs": jobs.to_dict(orient="records")
    }