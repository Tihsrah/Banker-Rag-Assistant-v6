# import os
# import json
# from datetime import datetime, timedelta
# from app.salesforce import get_opportunities
# from app.documents import read_documents_for_opportunity
# from app.task_generator import generate_tasks
# from app.gmail_utils import send_email
# from app.calendar_utils import create_meeting
# from app.update_salesforce import update_next_step

# banker_email = input("Enter your (banker's) Gmail address: ").strip()

# opportunities = get_opportunities()
# print("\nAvailable Opportunities:")
# for i, opp in enumerate(opportunities):
#     print(f"{i + 1}. {opp['Name']}")

# selected = int(input("\nSelect an opportunity by number: ")) - 1
# opportunity = opportunities[selected]

# username = opportunity.get("OwnerUsername", "banker1")
# opportunity_name = opportunity["Name"]
# docs_text = read_documents_for_opportunity(username, opportunity_name)

# task_result = generate_tasks(opportunity, docs_text, banker_email)

# print("\n===== AI Summary (for Next Step) =====")
# print(task_result.get("summary", "No summary"))

# print("\n===== Missing Fields =====")
# print(", ".join(task_result.get("missing_fields", [])))

# print("\n===== Suggested Actions =====")
# for action in task_result.get("actions", []):
#     if action["type"] == "email":
#         print(f"📧 Email to: {action['to']}")
#         print(f"Subject: {action['subject']}")
#         print(f"Body: {action['body']}")
#         confirm = input("Send this email? (y/n): ").strip().lower()
#         if confirm == 'y':
#             result = send_email(
#                 to=action["to"],
#                 subject=action["subject"],
#                 body=action["body"],
#                 sender_email=banker_email
#             )
#             print("Email Status:", result)
#     elif action["type"] == "meeting":
#         print(f"📅 Meeting: {action['title']}")
#         print(f"Details: {action['description']}")
#         meeting_time = input("Enter meeting start time (YYYY-MM-DD HH:MM): ")
#         dt = datetime.strptime(meeting_time, "%Y-%m-%d %H:%M")
#         confirm = input("Schedule this meeting? (y/n): ").strip().lower()
#         if confirm == 'y':
#             result = create_meeting(
#                 banker_email=banker_email,
#                 title=action["title"],
#                 description=action["description"],
#                 start_time=dt,
#                 duration_minutes=action.get("duration_minutes", 30)
#             )
#             print("Meeting Status:", result)

# update_confirm = input("\nDo you want to update Salesforce 'Next Step' with this summary? (y/n): ").strip().lower()
# if update_confirm == 'y':
#     update_result = update_next_step(opportunity["Id"], task_result.get("summary", ""))
#     print("Salesforce Update Result:", update_result)

# print(task_result.get("summary", "No summary available."))

# import os
# import json
# from datetime import datetime
# from app.salesforce import get_opportunities
# from app.task_generator import generate_tasks
# from app.gmail_utils import send_email
# from app.calendar_utils import create_meeting
# from app.update_salesforce import update_next_step
# from app.rag_orchestrator import search_documents_for_user

# # 👤 Input banker identity
# banker_email = input("Enter your (banker's) Gmail address: ").strip()

# # 📂 Load opportunities
# opportunities = get_opportunities()
# print("\nAvailable Opportunities:")
# for i, opp in enumerate(opportunities):
#     print(f"{i + 1}. {opp['Name']}")

# # 🎯 Select one
# selected = int(input("\nSelect an opportunity by number: ")) - 1
# opportunity = opportunities[selected]

# username = opportunity.get("OwnerUsername", "banker1")
# opportunity_name = opportunity["Name"]

# # 🧠 Get document chunks from Azure Search
# chunks = search_documents_for_user(username, opportunity_name, "*")
# combined_text = "\n\n".join(chunks)

# # 🚀 Generate action plan
# task_result = generate_tasks(opportunity, combined_text, banker_email)

# # 📌 Output results
# print("\n===== AI Summary (for Next Step) =====")
# print(task_result.get("summary", "No summary"))

# print("\n===== Missing Fields =====")
# print(", ".join(task_result.get("missing_fields", [])))

# print("\n===== Suggested Actions =====")
# for action in task_result.get("actions", []):
#     if action["type"] == "email":
#         print(f"📧 Email to: {action['to']}")
#         print(f"Subject: {action['subject']}")
#         print(f"Body: {action['body']}")
#         confirm = input("Send this email? (y/n): ").strip().lower()
#         if confirm == 'y':
#             result = send_email(
#                 to=action["to"],
#                 subject=action["subject"],
#                 body=action["body"],
#                 sender_email=banker_email
#             )
#             print("Email Status:", result)

#     elif action["type"] == "meeting":
#         print(f"📅 Meeting: {action['title']}")
#         print(f"Details: {action['description']}")
#         meeting_time = input("Enter meeting start time (YYYY-MM-DD HH:MM): ")
#         dt = datetime.strptime(meeting_time, "%Y-%m-%d %H:%M")
#         confirm = input("Schedule this meeting? (y/n): ").strip().lower()
#         if confirm == 'y':
#             result = create_meeting(
#                 banker_email=banker_email,
#                 title=action["title"],
#                 description=action["description"],
#                 start_time=dt,
#                 duration_minutes=action.get("duration_minutes", 30)
#             )
#             print("Meeting Status:", result)

# # 🔁 Salesforce Update
# update_confirm = input("\nDo you want to update Salesforce 'Next Step' with this summary? (y/n): ").strip().lower()
# if update_confirm == 'y':
#     update_result = update_next_step(opportunity["Id"], task_result.get("summary", ""))
#     print("Salesforce Update Result:", update_result)

# print(task_result.get("summary", "No summary available."))

import os
from datetime import datetime
from app.salesforce import get_opportunities
from app.task_generator import generate_tasks
from app.gmail_utils import send_email
from app.calendar_utils import create_meeting
from app.update_salesforce import update_next_step
from app.rag_orchestrator import search_documents_for_user
import tiktoken

def truncate_to_token_limit(text, max_tokens=7000):
    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = enc.encode(text)
    return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# 🧑 Banker identity
banker_email = input("Enter your (banker's) Gmail address: ").strip()

# 📄 Fetch opportunities
opportunities = get_opportunities()
print("\nAvailable Opportunities:")
for i, opp in enumerate(opportunities):
    print(f"{i + 1}. {opp['Name']}")

# 🎯 Choose one
selected = int(input("\nSelect an opportunity by number: ")) - 1
opportunity = opportunities[selected]

username = opportunity.get("OwnerUsername", "banker1")
opportunity_name = opportunity["Name"]

# 🧠 Semantic query for relevant content
semantic_query = (
    "What information is missing from the documents in terms of legal setup, financials, "
    "team details, investor readiness, or what actions the banker should take?"
)

chunks = search_documents_for_user(username, opportunity_name, semantic_query)
combined_text = "\n\n".join(chunks)
combined_text = truncate_to_token_limit(combined_text)

# 🤖 Task generation
task_result = generate_tasks(opportunity, combined_text, banker_email)

# 💡 Output
print("\n===== AI Summary (for Next Step) =====")
print(task_result.get("summary", "No summary"))

print("\n===== Missing Fields =====")
print(", ".join(task_result.get("missing_fields", [])))

print("\n===== Suggested Actions =====")
for action in task_result.get("actions", []):
    if action["type"] == "email":
        print(f"\n📧 Email to: {action['to']}")
        print(f"Subject: {action['subject']}")
        print(f"Body:\n{action['body']}")
        confirm = input("Send this email? (y/n): ").strip().lower()
        if confirm == 'y':
            result = send_email(
                to=action["to"],
                subject=action["subject"],
                body=action["body"],
                sender_email=banker_email
            )
            print("Email Status:", result)

    elif action["type"] == "meeting":
        print(f"\n📅 Meeting: {action['title']}")
        print(f"Details: {action['description']}")
        meeting_time = input("Enter meeting start time (YYYY-MM-DD HH:MM): ").strip()
        dt = datetime.strptime(meeting_time, "%Y-%m-%d %H:%M")
        confirm = input("Schedule this meeting? (y/n): ").strip().lower()
        if confirm == 'y':
            result = create_meeting(
                banker_email=banker_email,
                title=action["title"],
                description=action["description"],
                start_time=dt,
                duration_minutes=action.get("duration_minutes", 30)
            )
            print("Meeting Status:", result)

# ✅ Optional: Update in Salesforce
update_confirm = input("\nDo you want to update Salesforce 'Next Step' with this summary? (y/n): ").strip().lower()
if update_confirm == 'y':
    update_result = update_next_step(opportunity["Id"], task_result.get("summary", ""))
    print("Salesforce Update Result:", update_result)

print("\nDone.")
