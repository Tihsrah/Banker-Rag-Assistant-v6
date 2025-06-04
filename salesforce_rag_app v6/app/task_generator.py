
# import json
# import os
# from openai import AzureOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# openai_client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_version="2024-04-01-preview"
# )

# openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

# import tiktoken
# def truncate_to_token_limit(text, max_tokens=5000, model="gpt-4"):
#     enc = tiktoken.encoding_for_model(model)
#     tokens = enc.encode(text)
#     return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# def generate_tasks(opportunity_data, document_text, banker_email):
#     print("\n🚀 [TASK_GENERATOR] Starting task generation")
#     print(f"📌 Opportunity: {opportunity_data.get('Name', 'Unknown')}")
#     print(f"📨 Banker Email: {banker_email}")
#     print(f"📄 Document Text Length: {len(document_text)} characters")

#     # Truncate to avoid token overload
#     document_text = truncate_to_token_limit(document_text, max_tokens=5000)

#     # GPT Prompt
#     prompt = f"""
# You are a senior investment banking assistant helping a banker on the opportunity "{opportunity_data.get('Name', '')}".
# Based only on the provided documents, perform the following:

# 1. Identify missing information in these categories: legal, financials, team, investor readiness.
# 2. Suggest next steps for the banker (e.g., send email, schedule a meeting).
# 3. Return a JSON response with:
#     - summary: concise update for CRM
#     - missing_fields: list of strings
#     - actions: a maximum of one email (to harshlf4@gmail.com) and optional meeting

# Documents:
# \"\"\"
# {document_text}
# \"\"\"
# """.strip()

#     print("\n🧠 [TASK_GENERATOR] Sending prompt to GPT-4...")

#     try:
#         response = openai_client.chat.completions.create(
#             model=openai_deployment,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant generating banker tasks."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300,
#             temperature=0.2
#         )

#         raw_reply = response.choices[0].message.content.strip()
#         print("\n📝 [TASK_GENERATOR] Raw GPT Response:")
#         print(raw_reply)

#         try:
#             parsed = json.loads(raw_reply)
#             print("✅ [TASK_GENERATOR] Successfully parsed JSON.")

#             # ✅ Post-process: Combine emails
#             email_actions = [a for a in parsed.get("actions", []) if a["type"] == "email"]
#             meeting_actions = [a for a in parsed.get("actions", []) if a["type"] == "meeting"]

#             if email_actions:
#                 combined_body = "\n\n".join(a.get("body", "") for a in email_actions)
#                 subject = email_actions[0].get("subject", "Follow-up on missing information")

#                 parsed["actions"] = [
#                     {
#                         "type": "email",
#                         "to": "harshlf4@gmail.com",
#                         "subject": subject,
#                         "body": combined_body
#                     }
#                 ]
#                 if meeting_actions:
#                     parsed["actions"].extend(meeting_actions)

#                 print("✉️ [TASK_GENERATOR] Consolidated multiple emails into one.")

#             return parsed

#         except json.JSONDecodeError as je:
#             print("❌ [TASK_GENERATOR] JSON parsing failed:")
#             print(je)
#             return {
#                 "summary": "GPT response was not valid JSON.",
#                 "missing_fields": [],
#                 "actions": []
#             }

#     except Exception as e:
#         print("\n❌ [TASK_GENERATOR] Unexpected error during GPT response")
#         print("Error:", str(e))
#         return {
#             "summary": f"OpenAI error: {str(e)}",
#             "missing_fields": [],
#             "actions": []
#         }

import json
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import tiktoken

# Load environment variables
load_dotenv()

# Azure OpenAI setup
openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-04-01-preview"
)
openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

# Token helper
def truncate_to_token_limit(text, max_tokens=500, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# ✅ Email Task Generator
def generate_email_task(opportunity_data, document_text):
    print("\n📧 [EMAIL_GENERATOR] Generating follow-up email")
    print(f"📌 Opportunity: {opportunity_data.get('Name')}")
    print(f"📄 Document Length: {len(document_text)} characters")

    document_text = truncate_to_token_limit(document_text, max_tokens=5000)

    prompt = f"""
You are a senior investment banking assistant.

Given the opportunity named "{opportunity_data.get('Name', '')}", and based only on the documents below:
1. Identify missing information in legal, financials, team, and investor readiness.
2. Draft a single follow-up email to the client requesting all of that info.
3. Return JSON with:
    - summary
    - missing_fields (list of strings)
    - email: {{ to, subject, body }}
4. make it really short and crisp and try to write things in 100 words only.

Documents:
\"\"\"{document_text}\"\"\"
""".strip()

    print("\n🧠 [EMAIL_GENERATOR] Sending to GPT...")

    try:
        response = openai_client.chat.completions.create(
            model=openai_deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant generating follow-up emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.2
        )

        raw = response.choices[0].message.content.strip()
        print("\n📝 [EMAIL_GENERATOR] GPT Raw Response:")
        print(raw)

        parsed = json.loads(raw)
        parsed["email"]["to"] = "harshlf4@gmail.com"  # Force target email
        return parsed

    except json.JSONDecodeError as je:
        print("❌ [EMAIL_GENERATOR] JSON parsing failed:", je)
        return None
    except Exception as e:
        print("❌ [EMAIL_GENERATOR] GPT failed:", e)
        return None

# ✅ Meeting Suggestion Generator
# def generate_meeting_task(opportunity_data, document_text):
#     print("\n📅 [MEETING_GENERATOR] Generating meeting suggestion")
#     print(f"📌 Opportunity: {opportunity_data.get('Name')}")
#     print(f"📄 Document Length: {len(document_text)} characters")

#     document_text = truncate_to_token_limit(document_text, max_tokens=5000)

#     prompt = f"""
# You are a senior investment banking assistant.

# Based on the provided documents for opportunity "{opportunity_data.get('Name', '')}":
# 1. Determine if a meeting should be scheduled.
# 2. If yes, return JSON with:
#     - purpose
#     - agenda
#     - suggested_title
#     - description
#     - duration_minutes (optional)
# 3. make it really short and crisp and try to write things in 100 words only.

# Documents:
# \"\"\"{document_text}\"\"\"
# """.strip()

#     print("\n🧠 [MEETING_GENERATOR] Sending to GPT...")

#     try:
#         response = openai_client.chat.completions.create(
#             model=openai_deployment,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant scheduling meetings."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=400,
#             temperature=0.2
#         )

#         raw = response.choices[0].message.content.strip()
#         print("\n📝 [MEETING_GENERATOR] GPT Raw Response:")
#         print(raw)

#         return json.loads(raw)

#     except json.JSONDecodeError as je:
#         print("❌ [MEETING_GENERATOR] JSON parsing failed:", je)
#         return None
#     except Exception as e:
#         print("❌ [MEETING_GENERATOR] GPT failed:", e)
#         return None

# def generate_meeting_task(opportunity_data, document_text):
#     from openai import AzureOpenAI
#     import os
#     import json
#     from dotenv import load_dotenv
#     import tiktoken

#     load_dotenv()

#     openai_client = AzureOpenAI(
#         api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#         api_version="2024-04-01-preview"
#     )

#     deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

#     try:
#         prompt = f"""
# You are an AI assistant helping an investment banker plan meetings.
# Based only on the provided opportunity documents, suggest a meeting with:
# - title
# - description
# - proposed duration in minutes

# Respond strictly in JSON format:
# {{
#   "summary": "...",
#   "meeting": {{
#     "title": "...",
#     "description": "...",
#     "duration_minutes": 30
#   }}
# }}

# Documents:
# \"\"\"
# {document_text}
# \"\"\"
# """

#         print("📅 [MEETING_GENERATOR] Sending prompt to GPT-4")

#         response = openai_client.chat.completions.create(
#             model=deployment,
#             messages=[
#                 {"role": "system", "content": "You are helping organize banker meetings."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=400,
#             temperature=0.3
#         )

#         raw = response.choices[0].message.content.strip()
#         print("📨 [MEETING_GENERATOR] Raw response:", raw)

#         data = json.loads(raw)
#         return data

#     except Exception as e:
#         print("❌ [MEETING_GENERATOR] Error:", str(e))
#         return {
#             "summary": f"Error occurred: {str(e)}",
#             "meeting": {
#                 "title": "Meeting Planning Failed",
#                 "description": "Could not generate meeting suggestion.",
#                 "duration_minutes": 30
#             }
#         }

def generate_meeting_task(opportunity_data, document_text):
    try:
        print("📅 [MEETING_GENERATOR] Generating meeting from docs...")
        document_text = truncate_to_token_limit(document_text, 2000)

        prompt = f"""
You are a virtual banking assistant helping prepare client meetings.
Read the following opportunity documents and suggest one meeting bankers should schedule.
Your response must strictly follow this JSON format:
{{
  "summary": "...",
  "meeting": {{
    "title": "...",
    "description": "...",
    "duration_minutes": 30
  }}
}}

Documents:
\"\"\"{document_text}\"\"\"
""".strip()

        response = openai_client.chat.completions.create(
            model=openai_deployment,
            messages=[
                {"role": "system", "content": "You help bankers organize meetings based on client documentation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        print("🧠 [MEETING_GENERATOR] GPT Raw Response:")
        print(content)

        parsed = json.loads(content)

        if "meeting" not in parsed:
            raise ValueError("No 'meeting' key in GPT output.")

        return parsed

    except Exception as e:
        print("❌ [MEETING_GENERATOR] Failed to generate meeting:", str(e))
        return {
            "summary": f"Failed to generate meeting suggestion: {str(e)}",
            "meeting": {
                "title": "N/A",
                "description": "Meeting generation failed.",
                "duration_minutes": 30
            }
        }