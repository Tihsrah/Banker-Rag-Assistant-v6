# # # app/salesforce.py
# # import requests
# # import os
# # # from auth import get_aad_token
# # from dotenv import load_dotenv

# # load_dotenv()

# # def get_salesforce_headers():
# #     token = get_aad_token()["access_token"]
# #     return {
# #         "Authorization": f"Bearer {token}",
# #         "Content-Type": "application/json",
# #         "X-PrettyPrint": "1"
# #     }

# # def get_opportunities(user_email):
# #     instance_url = os.getenv("SF_INSTANCE_URL")
# #     query = f"""
# #     SELECT Id, Name, StageName, Amount, CloseDate, Owner.Username, 
# #            (SELECT Subject, ActivityDate FROM Tasks) 
# #     FROM Opportunity 
# #     WHERE Owner.Username = '{user_email}'
# #     """
# #     url = f"{instance_url}/services/data/v58.0/query/?q={query}"
# #     response = requests.get(url, headers=get_salesforce_headers())
# #     response.raise_for_status()
# #     return response.json().get("records", [])
# # app/salesforce.py
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# def get_salesforce_headers():
#     # Get credentials from environment
#     client_id = os.getenv("CLIENT_ID")
#     client_secret = os.getenv("CLIENT_SECRET")
#     username = os.getenv("USERNAME")
#     password = os.getenv("PASSWORD")
#     security_token = os.getenv("SECURITY_TOKEN")

#     # Compose login URL
#     login_url = "https://login.salesforce.com/services/oauth2/token"
#     payload = {
#         "grant_type": "password",
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "username": username,
#         "password": password + security_token
#     }

#     # Authenticate
#     response = requests.post(login_url, data=payload)
#     response.raise_for_status()

#     access_token = response.json().get("access_token")
#     instance_url = response.json().get("instance_url")

#     return {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#         "X-PrettyPrint": "1"
#     }, instance_url

# def get_opportunities(user_email):
#     headers, instance_url = get_salesforce_headers()

#     query = f"""
#     SELECT Id, Name, StageName, Amount, CloseDate, Owner.Username, 
#            (SELECT Subject, ActivityDate FROM Tasks) 
#     FROM Opportunity 
#     WHERE Owner.Username = '{user_email}'
#     """
#     url = f"{instance_url}/services/data/v58.0/query/?q={query}"
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     return response.json().get("records", [])

# app/salesforce.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 🔐 Get Salesforce Access Token using Refresh Token
def get_salesforce_token_with_refresh():
    token_url = "https://login.salesforce.com/services/oauth2/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# ✅ Get headers for authenticated request
def get_salesforce_headers():
    access_token = get_salesforce_token_with_refresh()
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-PrettyPrint": "1"
    }

# ✅ Get opportunities for a user from Salesforce
def get_opportunities(user_email):
    instance_url = os.getenv("INSTANCE_URL")
    headers = get_salesforce_headers()

    query = f"""
    SELECT Id, Name, StageName, Amount, CloseDate, Owner.Username,
           (SELECT Subject, ActivityDate FROM Tasks)
    FROM Opportunity
    WHERE Owner.Username = '{user_email}'
    """
    query_url = f"{instance_url}/services/data/v58.0/query/?q={query}"

    response = requests.get(query_url, headers=headers)
    response.raise_for_status()
    return response.json().get("records", [])

def update_next_step(opportunity_id, summary_text):
    url = f"{SF_INSTANCE}/services/data/{SF_API_VERSION}/sobjects/Opportunity/{opportunity_id}"
    
    headers = {
        "Authorization": f"Bearer {SF_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "NextStep": summary_text
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 204:
        return {"status": "success", "message": "Next Step updated."}
    else:
        return {
            "status": "error",
            "code": response.status_code,
            "details": response.text
        }
