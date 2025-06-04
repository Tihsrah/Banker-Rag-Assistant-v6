# # import base64
# # from email.message import EmailMessage
# # from googleapiclient.discovery import build
# # from google.oauth2.credentials import Credentials

# # def send_email(to, subject, body, sender_email, token_path='token.json'):
# #     creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/gmail.send'])
# #     service = build('gmail', 'v1', credentials=creds)

# #     message = EmailMessage()
# #     message.set_content(body)
# #     message['To'] = to
# #     message['From'] = sender_email
# #     message['Subject'] = subject

# #     raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
# #     try:
# #         sent_message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
# #         return {
# #             'status': 'success',
# #             'message_id': sent_message['id']
# #         }
# #     except Exception as e:
# #         return {
# #             'status': 'error',
# #             'error': str(e)
# #         }

# # Here is an updated version of the Gmail utility module (`gmail_utils.py`)
# # to integrate properly with your app and return results correctly.

# import os
# import base64
# from email.message import EmailMessage
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# # Required scopes
# SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# def authenticate_gmail():
#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     return build('gmail', 'v1', credentials=creds)

# def create_message(sender, to, subject, message_text):
#     message = EmailMessage()
#     message.set_content(message_text)
#     message['To'] = to
#     message['From'] = sender
#     message['Subject'] = subject
#     raw_message = base64.urlsafe_b64encode(message.as_bytes())
#     return {'raw': raw_message.decode()}

# def send_email(to, subject, body, sender_email):
#     try:
#         service = authenticate_gmail()
#         message = create_message(sender_email, to, subject, body)
#         send_result = service.users().messages().send(userId="me", body=message).execute()
#         return {"status": "success", "message_id": send_result["id"]}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail send scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authenticate and return Gmail service"""
    creds = None
    token_path = 'token.json'
    client_secret_path = 'client_secret.json'

    # Load existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or generate new token if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the new token
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    """Construct the email message"""
    message = EmailMessage()
    message.set_content(message_text)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(to, subject, body, sender_email="harshlf4@gmail.com"):
    """Send an email using Gmail API"""
    try:
        service = authenticate_gmail()
        message = create_message(sender_email, to, subject, body)
        sent = service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent to {to}. Message ID: {sent['id']}")
        return {"status": "success", "message_id": sent['id']}
    except Exception as e:
        print("❌ Failed to send email:", str(e))
        return {"status": "error", "error": str(e)}
