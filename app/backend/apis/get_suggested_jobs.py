from typing import Dict
import pandas as pd
import numpy as np
import random

def get_suggested_jobs_endpoint(perPage: int = 5, keyword: str = None) -> Dict:
    jobs_data = pd.read_csv('./database/jobs.csv')
    companies_data = pd.read_csv('./database/companies.csv')

    merged_data = pd.merge(
        jobs_data,
        companies_data[['name', 'small_image']],
        left_on='company_name',
        right_on='name',
        how='left'
    )
    if keyword:
        merged_data = merged_data[
            merged_data['job_title'].str.contains(keyword, case=False, na=False)
            | merged_data['company_name'].str.contains(keyword, case=False, na=False)
            | merged_data['technologies_used'].str.contains(keyword, case=False, na=False)
        ]
    suggested_data = merged_data.sample(n=min(perPage, len(merged_data)), random_state=None)

    jobs = suggested_data[[
        'job_title', 'company_name', 'small_image', 'technologies_used'
    ]]
    jobs = jobs.replace([np.nan, np.inf, -np.inf], None)

    return {
        "suggested-jobs": jobs.to_dict(orient="records")
    }