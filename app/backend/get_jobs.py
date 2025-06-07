from typing import List
import pandas as pd

def get_jobs_endpoint(page: int, perPage: int) -> List[dict]:
    # Load data from CSV files
    jobs_data = pd.read_csv('./database/jobs.csv')
    companies_data = pd.read_csv('./database/companies.csv')

    # Merge jobs.csv and companies.csv on company_name and name
    merged_data = pd.merge(
        jobs_data,
        companies_data[['name', 'small_image']],
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
        'position_level', 'employment_type', 'technologies_used'
    ]]

    return jobs.to_dict(orient="records")