from typing import Dict
import pandas as pd
from .get_suggested_jobs import get_suggested_jobs_endpoint

def get_jobs_endpoint(page: int, perPage: int) -> Dict:
    # Load data from CSV files
    jobs_data = pd.read_csv('./database/jobs.csv')
    companies_data = pd.read_csv('./database/companies.csv')

    # Merge jobs.csv and companies.csv on company_name and name
    merged_data = pd.merge(
        jobs_data,
        companies_data[['name', 'small_image', 'company_profile']],
        left_on='company_name',
        right_on='name',
        how='left'
    )

    # Paginate the merged data
    start = (page - 1) * perPage
    end = start + perPage
    paginated_data = merged_data.iloc[start:end]

    # Select relevant columns
    jobs = paginated_data[[
        'job_title', 'company_name', 'salary', 'address', 'date_posted', 'small_image',
        'position_level', 'employment_type', 'technologies_used', 'company_profile'
    ]]

    # Get suggested jobs (always perPage=5)
    suggested_jobs = get_suggested_jobs_endpoint(perPage=5)["suggested-jobs"]

    # Return paginated jobs, total count, and suggested jobs
    return {
        "total_jobs": len(merged_data),
        "jobs": jobs.to_dict(orient="records"),
        "suggested_jobs": suggested_jobs
    }