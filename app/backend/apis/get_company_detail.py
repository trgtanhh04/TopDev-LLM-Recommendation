import pandas as pd

def get_company_detail_endpoint(company_name: str):
    companies_data = pd.read_csv('./database/companies.csv')
    company_row = companies_data[companies_data['name'] == company_name]
    if company_row.empty:
        return {"error": "Company not found"}
    fields = [
        'name', 'url', 'tag_line', 'industry', 'company_size', 'nationality',
        'tech_stack', 'website', 'office_address', 'company_profile',
        'small_image', 'big_image', 'image_galleries'
    ]
    company_detail = company_row.iloc[0][fields].to_dict()
    return {"company_detail": company_detail}