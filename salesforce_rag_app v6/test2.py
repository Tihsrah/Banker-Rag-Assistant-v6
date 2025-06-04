import os
from openai import AzureOpenAI

# Based on your Azure resource settings
endpoint = "https://salesforce-gen-hackathon.openai.azure.com/"
api_key = "1r8CbI9eiYIfnRrVaEKdkskcLGHYqTttApxFl6revHbtFjF2ODT7JQQJ99BEACfhMk5XJ3w3AAABACOGFf7m"
deployment = "gpt-4"  # ✅ this is your actual Azure deployment name
api_version = "2024-04-01-preview"  # ✅ current valid preview version

# Create AzureOpenAI client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version,
)
print("📡 Sending request to Azure OpenAI...")
# Example chat
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I am going to Paris, what should I see?"}
    ],
    max_tokens=100,
    temperature=1.0,
    top_p=1.0
)   
print("✅ Response received.")

# Print result
print("\n🧠 GPT-4 says:\n")
print(response.choices[0].message.content)

# from azure.storage.blob import BlobServiceClient

# def upload_text_to_blob(container: str, blob_path: str, content: str):
#     print("📦 Connecting to Azure Blob...")
    
#     connection_string = (
#         "DefaultEndpointsProtocol=https;"
#         "AccountName=bankerdata;"
#         "AccountKey=D9jNfoESvBZ+OvQdoYBJjBqsSxbAgLklq95jN3oZzHfV0JADvmsjwC46+drJkk32ua0cnjKot2mb+AStv45Ldw==;"
#         "EndpointSuffix=core.windows.net"
#     )

#     blob_service = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service.get_blob_client(container=container, blob=blob_path)
#     blob_client.upload_blob(content, overwrite=True)

#     print(f"✅ Uploaded to blob: {blob_path}")

