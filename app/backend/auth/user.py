import os
import pandas as pd

USERS_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'users.csv')

def get_user_by_email(email):
    if not os.path.exists(USERS_CSV_PATH):
        return None
    df = pd.read_csv(USERS_CSV_PATH)
    user_row = df[df['email'] == email]
    if not user_row.empty:
        return user_row.iloc[0].to_dict()
    return None

def add_user(email, name):
    if os.path.exists(USERS_CSV_PATH):
        df = pd.read_csv(USERS_CSV_PATH)
    else:
        df = pd.DataFrame(columns=['email', 'name'])
    if email in df['email'].values:
        return df[df['email'] == email].iloc[0].to_dict()
    new_row = {'email': email, 'name': name}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(USERS_CSV_PATH, index=False)
    return new_row