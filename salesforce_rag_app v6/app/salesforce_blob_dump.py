# salesforce_blob_dump.py
from dotenv import load_dotenv
load_dotenv()
import sys
import os
sys.path.append(os.path.abspath("app"))

from azure.storage.blob import BlobServiceClient
from salesforce import get_opportunities  # or salesforce_client.get_user_opportunities


def generate_summary_text_from_opportunity(opp: dict) -> str:
    text_lines = []

    text_lines.append(f"Opportunity Name: {opp.get('Name', 'N/A')}")
    text_lines.append(f"Opportunity ID: {opp.get('Id', 'N/A')}")
    text_lines.append(f"Stage: {opp.get('StageName', 'N/A')}")
    text_lines.append(f"Amount: ${opp.get('Amount', 0):,.2f}")
    text_lines.append(f"Close Date: {opp.get('CloseDate', 'N/A')}")

    text_lines.append("\nTasks:")
    if "Tasks" in opp and isinstance(opp["Tasks"], dict):
        tasks = opp["Tasks"].get("records", [])
        if tasks:
            for t in tasks:
                subject = t.get("Subject", "N/A")
                date = t.get("ActivityDate", "N/A")
                text_lines.append(f"- {subject} on {date}")
        else:
            text_lines.append("- No tasks found.")
    else:
        text_lines.append("- No tasks available.")

    return "\n".join(text_lines)


# def upload_text_to_blob(container: str, blob_path: str, content: str):
#     connection_string = os.getenv("AZURE_STORAGE_CONN_STR")
#     blob_service = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service.get_blob_client(container=container, blob=blob_path)

#     blob_client.upload_blob(content, overwrite=True)
#     print(f"✅ Uploaded to blob: {blob_path}")
from azure.storage.blob import BlobServiceClient

def upload_text_to_blob(container: str, blob_path: str, content: str):
    print("📦 Connecting to Azure Blob...")
    
    # connection_string = (
    #     "DefaultEndpointsProtocol=https;"
    #     "AccountName=bankerdata;"
    #     "AccountKey=D9jNfoESvBZ+OvQdoYBJjBqsSxbAgLklq95jN3oZzHfV0JADvmsjwC46+drJkk32ua0cnjKot2mb+AStv45Ldw==;"
    #     "EndpointSuffix=core.windows.net"
    # )
    connection_string = os.getenv("AZURE_STORAGE_CONN_STR")

    blob_service = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service.get_blob_client(container=container, blob=blob_path)
    blob_client.upload_blob(content, overwrite=True)

    print(f"✅ Uploaded to blob: {blob_path}")

import requests

def run_azure_indexer():
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    indexer_name = "rag-email-indexer"
    api_key = os.getenv("AZURE_SEARCH_API_KEY")

    url = f"{endpoint}/indexers/{indexer_name}/run?api-version=2023-07-01-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        print("✅ Azure Search indexer triggered successfully.")
    else:
        print(f"❌ Failed to run indexer: {response.status_code}")
        print(response.text)

def dump_all_salesforce_opportunities_to_blob(user_email: str):
    print("📦 Dumping Salesforce opportunities to blob...")
    opportunities = get_opportunities(user_email)
    for opp in opportunities:
        summary_text = generate_summary_text_from_opportunity(opp)
        blob_path = f"{user_email}/{opp['Name']}/salesforce_summary.txt"
        upload_text_to_blob(container="banker-updates", blob_path=blob_path, content=summary_text)
        run_azure_indexer()
    print("✅ All opportunities uploaded.")
