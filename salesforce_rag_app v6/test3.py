# import requests

# access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ik40WnJYZXdCWTJzcFB4NTlJcnQyQ1U0Z3YxN19oTHdmU2pZUGhwcE9seG8iLCJhbGciOiJSUzI1NiIsIng1dCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSIsImtpZCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC85MWNjMWZiNi0xMjc1LTRhY2YtYjNlYS1jMjEzZWMxNjI1N2IvIiwiaWF0IjoxNzQ4OTQ2NTE5LCJuYmYiOjE3NDg5NDY1MTksImV4cCI6MTc0ODk1MDQxOSwiYWlvIjoiazJSZ1lQaXN6UFIrSzM5Zjh2SDlXWWtpNGpibEFBPT0iLCJhcHBfZGlzcGxheW5hbWUiOiJCYW5rZXJzIE91dGxvb2sgVGFzayIsImFwcGlkIjoiMjQwNzM0ZDUtNjQ2Mi00ZWY3LWIwY2ItNjlhMjhjMmNkOWRhIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvOTFjYzFmYjYtMTI3NS00YWNmLWIzZWEtYzIxM2VjMTYyNTdiLyIsImlkdHlwIjoiYXBwIiwib2lkIjoiZDg2ZGUxN2QtZDhkZS00ZmIwLTljMGMtYjkzYjFhZTJkMTYzIiwicmgiOiIxLkFVb0F0aF9Na1hVU3owcXo2c0lUN0JZbGV3TUFBQUFBQUFBQXdBQUFBQUFBQUFCS0FBQktBQS4iLCJzdWIiOiJkODZkZTE3ZC1kOGRlLTRmYjAtOWMwYy1iOTNiMWFlMmQxNjMiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiQVMiLCJ0aWQiOiI5MWNjMWZiNi0xMjc1LTRhY2YtYjNlYS1jMjEzZWMxNjI1N2IiLCJ1dGkiOiJ3UExtMFNPUUZreWlhWHp4Y0tVc0FnIiwidmVyIjoiMS4wIiwid2lkcyI6WyIwOTk3YTFkMC0wZDFkLTRhY2ItYjQwOC1kNWNhNzMxMjFlOTAiXSwieG1zX2Z0ZCI6ImFqUUxTcTFTcENUTDAwTHZxUUlXSm44TUFWdXYzSUtYbUpoSTJrYldnR1lCYTI5eVpXRnpiM1YwYUMxa2MyMXoiLCJ4bXNfaWRyZWwiOiIxMCA3IiwieG1zX3JkIjoiMC40MkxsWUJKaTlCSVM0V0FYRXVoZV9lZTBhUGdLM183ZnloZFhGTC1UQjRweUNnbGNUc2ppZXBHWDR6TDNpT0JXODdPX0Z3SkZPWVFFbUJrZzRBQ1VCZ0EiLCJ4bXNfdGNkdCI6MTU4NTgyMjgyN30.ceLt_VGq9A1_6Ddg9sYX9abBFPzrW_VPwk4KlNLae9N12WEiELJZAbufI-s-_ExEFunhVXtf2FAy7Quy17tPZiFPyTlF_ft5ifp9AB15sm5orVuY7K1H7AV-yaqlrBd87IKiE3rhlTNAsDebwTMXYbnHDNkQQLJFGO6FpCo4qjvsmBvbxc0zf33hE6UhnJ78qRZ3YQ8akQVMj-tqxxT6OtQmBXe_BBkIdTYdsYQNh4IY7Dx9-SfcarmOww6uZfTNn0tNDspi4YMQbEMDLfZRJMQ3kQgz8OjIHExNqlU_2Wi4mX2AXGK4afJlt0a54zJAaceXeb9xJCYNCR21a-j45A"

# url = "https://graph.microsoft.com/v1.0/me/sendMail"

# payload = {
#     "message": {
#         "subject": "Hello from Microsoft Graph API (Delegated Flow)!",
#         "body": {
#             "contentType": "Text",
#             "content": "This email was sent using the delegated flow with Microsoft Graph API via Python."
#         },
#         "toRecipients": [
#             {
#                 "emailAddress": {
#                     "address": "harshlf4@gmail.com"
#                 }
#             }
#         ]
#     },
#     "saveToSentItems": "true"
# }

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# response = requests.post(url, headers=headers, json=payload)

# if response.status_code == 202:
#     print("Email sent successfully!")
# else:
#     print("Error sending email:", response.status_code, response.text)

# gmail:
import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message = EmailMessage()
    message.set_content(message_text)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw_message.decode()}

def send_email():
    service = authenticate_gmail()
    message = create_message("your_email@gmail.com", "harshlf4@gmail.com",
                             "Test Email from Gmail API",
                             "This is a demo email sent via Gmail API and Python.")
    send = service.users().messages().send(userId="me", body=message).execute()
    print("✅ Email sent! Message ID:", send['id'])

send_email()
