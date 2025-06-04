# import msal
# import requests

# # ------------------ Configuration ------------------
# client_id = "240734d5-6462-4ef7-b0cb-69a28c2cd9da"
# client_secret = "eY48Q~gZ.HB0eYZJkhbN6eTYoONSBQ8OJLLQNa_k"
# tenant_id = "91cc1fb6-1275-4acf-b3ea-c213ec16257b"
# authority = f"https://login.microsoftonline.com/{tenant_id}"
# redirect_uri = "http://localhost"
# scopes = ["User.Read", "Mail.Send"]

# # ------------------ MSAL App Setup ------------------
# app = msal.ConfidentialClientApplication(
#     client_id,
#     authority=authority,
#     client_credential=client_secret
# )

# # ------------------ Get Authorization URL ------------------
# flow = app.initiate_auth_code_flow(scopes=scopes, redirect_uri=redirect_uri)
# print("Please go to this URL and authorize the app:")
# print(flow["auth_uri"])

# # ------------------ Paste the auth code ------------------
# auth_response_code = input("Paste the full URL you were redirected to: ")

# # Extract the code from the redirect response
# from urllib.parse import urlparse, parse_qs
# query = urlparse(auth_response_code).query
# code = parse_qs(query).get("code")[0]

# # ------------------ Exchange code for access token ------------------
# result = app.acquire_token_by_authorization_code(
#     code,
#     scopes=scopes,
#     redirect_uri=redirect_uri
# )

# if "access_token" not in result:
#     print("Failed to get access token:", result.get("error_description"))
#     exit()

# access_token = result["access_token"]

# # ------------------ Send Email via Microsoft Graph ------------------
# email_payload = {
#     "message": {
#         "subject": "🎉 Test Email from Graph API!",
#         "body": {
#             "contentType": "Text",
#             "content": "Hello! This email was sent using Microsoft Graph API and delegated user login."
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

# response = requests.post(
#     "https://graph.microsoft.com/v1.0/me/sendMail",
#     headers=headers,
#     json=email_payload
# )

# # ------------------ Response Check ------------------
# if response.status_code == 202:
#     print("✅ Email sent successfully!")
# else:
#     print("❌ Failed to send email:")
#     print("Status:", response.status_code)
#     print("Details:", response.text)
