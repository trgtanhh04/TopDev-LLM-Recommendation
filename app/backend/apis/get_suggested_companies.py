import pandas as pd
import numpy as np
import random

def get_suggested_companies_endpoint(perPage: int = 5, keyword: str = None):
    companies_data = pd.read_csv('./database/companies.csv')
    filtered = companies_data[
        companies_data['small_image'].notna() & companies_data['big_image'].notna() &
        (companies_data['small_image'].astype(str).str.strip() != '') &
        (companies_data['big_image'].astype(str).str.strip() != '')
    ]
    if keyword:
        filtered = filtered[
            filtered['name'].str.contains(keyword, case=False, na=False)
            | filtered['office_address'].str.contains(keyword, case=False, na=False)
            | filtered['industry'].str.contains(keyword, case=False, na=False)
        ]
    fields = [
        'name', 'tag_line', 'office_address', 'industry', 'small_image', 'big_image'
    ]
    suggested = filtered.sample(n=min(perPage, len(filtered)), random_state=None)
    companies = suggested[fields]
    companies = companies.replace([np.nan, np.inf, -np.inf], None)
    return {
        "suggested_companies": companies.to_dict(orient="records")
    }