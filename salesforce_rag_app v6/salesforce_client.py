import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_salesforce_access_token():
    url = "https://login.salesforce.com/services/oauth2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def get_user_opportunities(user_email):
    token = get_salesforce_access_token()
    instance_url = os.getenv("INSTANCE_URL")
    query = f"""
    SELECT Id, Name, StageName, Amount, CloseDate 
    FROM Opportunity 
    WHERE Owner.Email = '{user_email}'
    """
    url = f"{instance_url}/services/data/v58.0/query/"
    params = {"q": query}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("records", [])

# Test example
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = "your-user@example.com"
    opportunities = get_user_opportunities(email)
    for opp in opportunities:
        print(f"{opp['Name']} - {opp['StageName']} - ${opp['Amount']}")
