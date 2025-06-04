# # import streamlit as st
# # import os
# # import sys
# # import pandas as pd
# # from datetime import datetime, timedelta
# # from dotenv import load_dotenv
# # import plotly.express as px
# # import tiktoken

# # # Set environment
# # sys.path.append(os.path.abspath("app"))

# # from salesforce import get_opportunities, update_next_step
# # from salesforce_blob_dump import dump_all_salesforce_opportunities_to_blob
# # from rag_orchestrator import answer_user_query, search_documents_for_user
# # from task_generator import generate_tasks
# # from gmail_utils import send_email
# # from calendar_utils import create_meeting

# # load_dotenv()

# # # Static banker login
# # user_email = "harshlf4@gmail.com"

# # # Layout config
# # st.set_page_config(page_title="Barclays Banker Assistant", layout="wide")
# # st.markdown("""
# #     <style>
# #     .block-container { padding-top: 2rem; }
# #     h1, h2, h3 { color: #002c5f; font-weight: 700; }
# #     </style>
# # """, unsafe_allow_html=True)

# # st.title("💼 Barclays Banker Assistant")

# # # Data sync
# # with st.spinner("🔍 Loading Salesforce opportunities..."):
# #     opportunities = get_opportunities(user_email)

# # with st.spinner("☁️ Uploading to Azure Blob..."):
# #     dump_all_salesforce_opportunities_to_blob(user_email)

# # if not opportunities:
# #     st.warning("No opportunities available.")
# #     st.stop()

# # # GPT-4 Q&A
# # st.markdown("### 🤖 GPT-4 Opportunity Assistant")
# # selected_opp = st.selectbox("🎯 Select an opportunity", [opp["Name"] for opp in opportunities])
# # user_question = st.text_input("💬 Ask a question about this opportunity:")

# # if st.button("Ask GPT") and selected_opp and user_question:
# #     with st.spinner("🤖 Thinking..."):
# #         try:
# #             answer = answer_user_query(user_email, selected_opp, user_question)
# #             st.subheader("📈 GPT-4's Answer")
# #             st.markdown(f"```\n{answer}\n```")
# #         except Exception as e:
# #             st.error(f"GPT-4 failed to answer: {str(e)}")

# # # Truncate helper
# # def truncate_to_token_limit(text, max_tokens=500):
# #     enc = tiktoken.encoding_for_model("gpt-4")
# #     tokens = enc.encode(text)
# #     return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# # # Analyze Opportunity
# # st.markdown("### 📘 Analyze Pitchbook & Recommend Actions")

# # if st.button("🧠 Analyze This Opportunity"):
# #     with st.spinner("Reading documents and generating tasks..."):
# #         selected_data = next((opp for opp in opportunities if opp["Name"] == selected_opp), None)
# #         if not selected_data:
# #             st.error("No data found for selected opportunity.")
# #             st.stop()

# #         semantic_query = (
# #             "What is missing from the opportunity documentation in terms of legal, team, financials, "
# #             "investor readiness, and what actions the banker should take next?"
# #         )
# #         chunks = search_documents_for_user(user_email, selected_opp, semantic_query)
# #         combined_text = "\n\n".join(chunks)
# #         st.subheader("📄 Preview of Document Context Sent to GPT")
# #         st.code(combined_text[:1000], language="text")  # Truncated for readability
# #         combined_text = truncate_to_token_limit(combined_text)

# #         task_data = generate_tasks(selected_data, combined_text, user_email)

# #         st.subheader("📌 Suggested Next Step (AI)")
# #         st.success(task_data.get("summary", "No summary available"))

# #         if st.button("✅ Update 'Next Step' in Salesforce"):
# #             result = update_next_step(selected_data["Id"], task_data.get("summary", ""))
# #             if result["status"] == "success":
# #                 st.success("Updated in Salesforce successfully!")
# #             else:
# #                 st.error(f"Failed to update: {result['details']}")

# #         st.subheader("🧩 Missing Fields")
# #         for item in task_data.get("missing_fields", []):
# #             st.markdown(f"- {item}")

# #         st.subheader("📬 Suggested Actions")
# #         for idx, action in enumerate(task_data.get("actions", [])):
# #             if action["type"] == "email":
# #                 with st.expander(f"📧 Email Draft {idx + 1}"):
# #                     st.code(f"To: {action['to']}\nSubject: {action['subject']}\n\n{action['body']}")
# #                     if st.button(f"Send Email {idx + 1}"):
# #                         email_result = send_email(
# #                             to=action["to"],
# #                             subject=action["subject"],
# #                             body=action["body"],
# #                             sender_email=user_email
# #                         )
# #                         if email_result["status"] == "success":
# #                             st.success(f"Email sent! ID: {email_result['message_id']}")
# #                         else:
# #                             st.error(f"Email failed: {email_result['error']}")

# #             elif action["type"] == "meeting":
# #                 with st.expander(f"📅 Meeting Suggestion {idx + 1}"):
# #                     st.markdown(f"**Title:** {action['title']}")
# #                     st.markdown(f"**Description:** {action['description']}")
# #                     date_part = st.date_input("📅 Select meeting date", value=datetime.now().date())
# #                     time_part = st.time_input("⏰ Select meeting time", value=datetime.now().time())
# #                     date_input = datetime.combine(date_part, time_part)
# #                     if st.button(f"Create Meeting {idx + 1}"):
# #                         meeting_result = create_meeting(
# #                             banker_email=user_email,
# #                             title=action["title"],
# #                             description=action["description"],
# #                             start_time=date_input,
# #                             duration_minutes=action.get("duration_minutes", 30)
# #                         )
# #                         if meeting_result["status"] == "success":
# #                             st.success(f"Meeting created! [View in Calendar]({meeting_result['event_link']})")
# #                         else:
# #                             st.error(f"Failed to create meeting: {meeting_result['error']}")

# # # 3D Plot
# # st.markdown("### 📊 Visual Opportunity Overview")

# # stage_order = {
# #     "Qualify": 1,
# #     "Meet & Present": 2,
# #     "Propose": 3,
# #     "Negotiate": 4,
# #     "Closed Won": 5,
# #     "Closed Lost": 0
# # }

# # df = pd.DataFrame(opportunities)
# # df["CloseDate"] = pd.to_datetime(df["CloseDate"], errors="coerce")
# # df["CloseDateNum"] = df["CloseDate"].map(lambda x: x.timestamp() if pd.notnull(x) else 0)
# # df["StageNum"] = df["StageName"].map(stage_order)
# # df = df[df["StageNum"].notnull()]

# # fig = px.scatter_3d(
# #     df,
# #     x="CloseDateNum",
# #     y="Amount",
# #     z="StageNum",
# #     color="StageName",
# #     hover_name="Name",
# #     hover_data={"CloseDate": True, "Amount": True, "StageName": True},
# #     title="Opportunities by Close Date, Amount, and Stage"
# # )

# # fig.update_layout(
# #     scene=dict(
# #         xaxis_title="Close Date",
# #         yaxis_title="Deal Amount ($)",
# #         zaxis_title="Stage",
# #         xaxis=dict(tickangle=-35, gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
# #         yaxis=dict(gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
# #         zaxis=dict(
# #             tickvals=list(stage_order.values()),
# #             ticktext=list(stage_order.keys()),
# #             gridcolor="rgba(200,200,200,0.3)",
# #             tickfont=dict(color="white")
# #         ),
# #         bgcolor="rgb(20,24,35)"
# #     ),
# #     margin=dict(l=10, r=10, b=10, t=40),
# #     height=600,
# #     paper_bgcolor="rgb(20,24,35)",
# #     font=dict(color="white")
# # )

# # st.plotly_chart(fig, use_container_width=True)

# # # working
# # import streamlit as st
# # import os
# # import sys
# # import pandas as pd
# # from datetime import datetime, timedelta
# # from dotenv import load_dotenv
# # import plotly.express as px
# # import tiktoken

# # # Paths and modules
# # sys.path.append(os.path.abspath("app"))

# # from salesforce import get_opportunities, update_next_step
# # from salesforce_blob_dump import dump_all_salesforce_opportunities_to_blob
# # from rag_orchestrator import search_documents_for_user
# # from task_generator import generate_email_task, generate_meeting_task
# # from gmail_utils import send_email
# # from calendar_utils import create_meeting

# # # Load environment
# # load_dotenv()
# # user_email = "harshlf4@gmail.com"  # Static banker login

# # # Layout
# # st.set_page_config(page_title="Barclays Banker Assistant", layout="wide")
# # st.markdown("""
# #     <style>
# #     .block-container { padding-top: 2rem; }
# #     h1, h2, h3 { color: #002c5f; font-weight: 700; }
# #     </style>
# # """, unsafe_allow_html=True)
# # st.title("💼 Barclays Banker Assistant")

# # # Load opportunities and sync storage
# # with st.spinner("🔍 Loading Salesforce opportunities..."):
# #     opportunities = get_opportunities(user_email)
# # with st.spinner("☁️ Uploading to Azure Blob..."):
# #     dump_all_salesforce_opportunities_to_blob(user_email)

# # if not opportunities:
# #     st.warning("No opportunities available.")
# #     st.stop()

# # # Select opportunity
# # selected_opp = st.selectbox("🎯 Select an opportunity", [opp["Name"] for opp in opportunities])
# # selected_data = next((opp for opp in opportunities if opp["Name"] == selected_opp), None)

# # # Token helper
# # def truncate_to_token_limit(text, max_tokens=500):
# #     enc = tiktoken.encoding_for_model("gpt-4")
# #     tokens = enc.encode(text)
# #     return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# # # Load relevant docs
# # semantic_query = "pitchbook or salesforce summary for banker task planning"
# # doc_chunks = search_documents_for_user(user_email, selected_opp, semantic_query)
# # combined_text = "\n\n".join(doc_chunks)
# # combined_text = truncate_to_token_limit(combined_text)

# # st.subheader("📄 Document Context for AI")
# # st.code(combined_text[:1000] or "No document content available.", language="text")

# # # ---- 📧 Generate Email ----
# # st.markdown("### 📬 Generate Follow-up Email")

# # if st.button("✉️ Generate Follow-Up Email"):
# #     with st.spinner("Generating email content..."):
# #         result = generate_email_task(selected_data, combined_text)

# #         if not result:
# #             st.error("Failed to generate email.")
# #         else:
# #             st.success(result.get("summary", "No summary provided."))
# #             st.subheader("📧 Email Draft")
# #             email = result.get("email", {})
# #             st.code(f"To: {email.get('to')}\nSubject: {email.get('subject')}\n\n{email.get('body')}")
# #             if st.button("Send Email"):
# #                 response = send_email(
# #                     to=email.get("to"),
# #                     subject=email.get("subject"),
# #                     body=email.get("body"),
# #                     sender_email=user_email
# #                 )
# #                 if response["status"] == "success":
# #                     st.success("Email sent successfully!")
# #                 else:
# #                     st.error(f"Email failed: {response['error']}")

# # # ---- 📅 Generate Meeting ----
# # st.markdown("### 📅 Generate Suggested Meeting")

# # if st.button("📅 Suggest Meeting"):
# #     with st.spinner("Creating meeting plan..."):
# #         result = generate_meeting_task(selected_data, combined_text)

# #         if not result:
# #             st.error("No meeting suggestion returned.")
# #         else:
# #             st.subheader("🗓️ Suggested Meeting Details")
# #             st.markdown(f"**Purpose:** {result.get('purpose')}")
# #             st.markdown(f"**Agenda:** {result.get('agenda')}")
# #             st.markdown(f"**Description:** {result.get('description')}")
# #             date = st.date_input("📅 Date", value=datetime.now().date())
# #             time = st.time_input("⏰ Time", value=datetime.now().time())
# #             start_dt = datetime.combine(date, time)

# #             if st.button("Create Meeting"):
# #                 response = create_meeting(
# #                     banker_email=user_email,
# #                     title=result.get("suggested_title", "Client Meeting"),
# #                     description=result.get("description", ""),
# #                     start_time=start_dt,
# #                     duration_minutes=result.get("duration_minutes", 30)
# #                 )
# #                 if response["status"] == "success":
# #                     st.success(f"Meeting created: [Open]({response['event_link']})")
# #                 else:
# #                     st.error(f"Failed to create meeting: {response['error']}")

# # # ---- 📊 Visualization ----
# # st.markdown("### 📊 Visual Opportunity Overview")

# # stage_order = {
# #     "Qualify": 1,
# #     "Meet & Present": 2,
# #     "Propose": 3,
# #     "Negotiate": 4,
# #     "Closed Won": 5,
# #     "Closed Lost": 0
# # }

# # df = pd.DataFrame(opportunities)
# # df["CloseDate"] = pd.to_datetime(df["CloseDate"], errors="coerce")
# # df["CloseDateNum"] = df["CloseDate"].map(lambda x: x.timestamp() if pd.notnull(x) else 0)
# # df["StageNum"] = df["StageName"].map(stage_order)
# # df = df[df["StageNum"].notnull()]

# # fig = px.scatter_3d(
# #     df,
# #     x="CloseDateNum",
# #     y="Amount",
# #     z="StageNum",
# #     color="StageName",
# #     hover_name="Name",
# #     title="Opportunities by Close Date, Amount, and Stage",
# #     hover_data={"CloseDate": True, "Amount": True}
# # )

# # fig.update_layout(
# #     scene=dict(
# #         xaxis_title="Close Date",
# #         yaxis_title="Deal Amount ($)",
# #         zaxis_title="Stage",
# #         zaxis=dict(tickvals=list(stage_order.values()), ticktext=list(stage_order.keys()))
# #     ),
# #     margin=dict(l=0, r=0, b=0, t=40),
# #     height=600
# # )

# # st.plotly_chart(fig, use_container_width=True)

# import streamlit as st
# import os
# import sys
# import pandas as pd
# from datetime import datetime
# from dotenv import load_dotenv
# import plotly.express as px
# import tiktoken

# # Set environment
# sys.path.append(os.path.abspath("app"))

# from salesforce import get_opportunities, update_next_step
# from salesforce_blob_dump import dump_all_salesforce_opportunities_to_blob
# from rag_orchestrator import answer_user_query, search_documents_for_user
# from task_generator import generate_email_task, generate_meeting_task
# from gmail_utils import send_email
# from calendar_utils import create_meeting

# load_dotenv()
# user_email = "harshlf4@gmail.com"

# st.set_page_config(page_title="Barclays Banker Assistant", layout="wide")
# st.markdown("""
#     <style>
#     .block-container { padding-top: 2rem; }
#     h1, h2, h3 { color: #002c5f; font-weight: 700; }
#     </style>
# """, unsafe_allow_html=True)

# st.title("💼 Barclays Banker Assistant")

# with st.spinner("🔍 Loading Salesforce opportunities..."):
#     opportunities = get_opportunities(user_email)

# with st.spinner("☁️ Uploading to Azure Blob..."):
#     dump_all_salesforce_opportunities_to_blob(user_email)

# if not opportunities:
#     st.warning("No opportunities available.")
#     st.stop()

# selected_opp = st.selectbox("🎯 Select an opportunity", [opp["Name"] for opp in opportunities])
# selected_data = next((opp for opp in opportunities if opp["Name"] == selected_opp), None)

# # GPT-4 Q&A Section
# st.markdown("### 🤖 GPT-4 Opportunity Assistant")
# user_question = st.text_input("💬 Ask a question about this opportunity:")

# if st.button("Ask GPT") and selected_opp and user_question:
#     with st.spinner("🤖 Thinking..."):
#         try:
#             answer = answer_user_query(user_email, selected_opp, user_question)
#             st.subheader("📈 GPT-4's Answer")
#             st.markdown(f"```\n{answer}\n```")
#         except Exception as e:
#             st.error(f"GPT-4 failed to answer: {str(e)}")

# def truncate_to_token_limit(text, max_tokens=500):
#     enc = tiktoken.encoding_for_model("gpt-4")
#     tokens = enc.encode(text)
#     return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# # Get relevant context chunks
# semantic_query = (
#     "What is missing from the opportunity documentation in terms of legal, team, financials, "
#     "investor readiness, and what actions the banker should take next?"
# )
# chunks = search_documents_for_user(user_email, selected_opp, semantic_query)
# combined_text = truncate_to_token_limit("\n\n".join(chunks), 2000)

# # Analyze (all in one)
# st.markdown("### 🧠 Analyze Pitchbook & Generate Tasks")

# if st.button("🔍 Generate All Tasks"):
#     with st.spinner("Reading documents and generating tasks..."):
#         task_data = generate_tasks(selected_data, combined_text, user_email)

#         st.subheader("📌 Suggested Next Step (AI)")
#         st.success(task_data.get("summary", "No summary available"))

#         if st.button("✅ Update 'Next Step' in Salesforce"):
#             result = update_next_step(selected_data["Id"], task_data.get("summary", ""))
#             if result["status"] == "success":
#                 st.success("Updated in Salesforce successfully!")
#             else:
#                 st.error(f"Failed to update: {result['details']}")

#         st.subheader("🧩 Missing Fields")
#         for item in task_data.get("missing_fields", []):
#             st.markdown(f"- {item}")

#         st.subheader("📬 Suggested Actions")
#         for idx, action in enumerate(task_data.get("actions", [])):
#             if action["type"] == "email":
#                 with st.expander(f"📧 Email Draft {idx + 1}"):
#                     st.code(f"To: {action['to']}\nSubject: {action['subject']}\n\n{action['body']}")
#                     if st.button(f"Send Email {idx + 1}"):
#                         result = send_email(
#                             to=action["to"],
#                             subject=action["subject"],
#                             body=action["body"],
#                             sender_email=user_email
#                         )
#                         if result["status"] == "success":
#                             st.success(f"Email sent! Message ID: {result['message_id']}")
#                         else:
#                             st.error(f"Email failed: {result['error']}")
                    
#             elif action["type"] == "meeting":
#                 with st.expander(f"📅 Meeting Suggestion {idx + 1}"):
#                     st.markdown(f"**Title:** {action['title']}")
#                     st.markdown(f"**Description:** {action['description']}")
#                     date_part = st.date_input("📅 Meeting date", value=datetime.now().date())
#                     time_part = st.time_input("⏰ Meeting time", value=datetime.now().time())
#                     start_time = datetime.combine(date_part, time_part)
#                     if st.button(f"Create Meeting {idx + 1}"):
#                         result = create_meeting(
#                             banker_email=user_email,
#                             title=action["title"],
#                             description=action["description"],
#                             start_time=start_time,
#                             duration_minutes=action.get("duration_minutes", 30)
#                         )
#                         if result["status"] == "success":
#                             st.success(f"Meeting created! [View]({result['event_link']})")
#                         else:
#                             st.error(f"Meeting failed: {result['error']}")

# # Email-only path
# st.markdown("### ✉️ Generate Follow-Up Email Only")

# if st.button("📤 Generate Email"):
#     with st.spinner("Working..."):
#         result = generate_email_task(selected_data, combined_text)
#         print("result :",result)
#         email = result.get("email", {})
#         print("email :",email)
#         st.success(result.get("summary", "No summary"))
#         st.code(f"To: {email.get('to')}\nSubject: {email.get('subject')}\n\n{email.get('body')}")
#         if st.button("Send Email"):
#             outcome = send_email(
#                 to=email.get("to"),
#                 subject=email.get("subject"),
#                 body=email.get("body"),
#                 sender_email=user_email
#             )
#             if outcome["status"] == "success":
#                 st.success(f"Email sent! ID: {outcome['message_id']}")
#             else:
#                 st.error(f"Failed to send email: {outcome['error']}")
#             print("we are passed send email button ")

# # Meeting-only path
# st.markdown("### 📅 Propose Meeting Only")

# if st.button("📆 Generate Meeting Suggestion"):
#     with st.spinner("Planning meeting..."):
#         result = generate_meeting_task(selected_data, combined_text)
#         meeting = result.get("meeting", {})
#         st.success(result.get("summary", "No summary"))
#         st.markdown(f"**Title:** {meeting.get('title')}  \n**Description:** {meeting.get('description')}")
#         date_part = st.date_input("📅 Meeting date", value=datetime.now().date())
#         time_part = st.time_input("⏰ Meeting time", value=datetime.now().time())
#         start_time = datetime.combine(date_part, time_part)
#         if st.button("Create Meeting"):
#             outcome = create_meeting(
#                 banker_email=user_email,
#                 title=meeting.get("title"),
#                 description=meeting.get("description"),
#                 start_time=start_time,
#                 duration_minutes=meeting.get("duration_minutes", 30)
#             )
#             if outcome["status"] == "success":
#                 st.success(f"Meeting created! [Open]({outcome['event_link']})")
#             else:
#                 st.error(f"Failed to create: {outcome['error']}")

# # 3D Plot Section
# st.markdown("### 📊 Visual Opportunity Overview")

# stage_order = {
#     "Qualify": 1, "Meet & Present": 2, "Propose": 3,
#     "Negotiate": 4, "Closed Won": 5, "Closed Lost": 0
# }

# df = pd.DataFrame(opportunities)
# df["CloseDate"] = pd.to_datetime(df["CloseDate"], errors="coerce")
# df["CloseDateNum"] = df["CloseDate"].map(lambda x: x.timestamp() if pd.notnull(x) else 0)
# df["StageNum"] = df["StageName"].map(stage_order)
# df = df[df["StageNum"].notnull()]

# fig = px.scatter_3d(
#     df, x="CloseDateNum", y="Amount", z="StageNum", color="StageName",
#     hover_name="Name", hover_data={"CloseDate": True, "Amount": True, "StageName": True},
#     title="Opportunities by Close Date, Amount, and Stage"
# )

# fig.update_layout(
#     scene=dict(
#         xaxis_title="Close Date", yaxis_title="Deal Amount ($)", zaxis_title="Stage",
#         bgcolor="rgb(20,24,35)",
#         xaxis=dict(tickangle=-35, gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
#         yaxis=dict(gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
#         zaxis=dict(
#             tickvals=list(stage_order.values()),
#             ticktext=list(stage_order.keys()),
#             gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")
#         )
#     ),
#     margin=dict(l=10, r=10, b=10, t=40), height=600,
#     paper_bgcolor="rgb(20,24,35)", font=dict(color="white")
# )

# st.plotly_chart(fig, use_container_width=True)

# import os
# from datetime import datetime
# import pandas as pd
# import plotly.express as px
# import tiktoken
# import streamlit as st

# import sys
# import pandas as pd
# from datetime import datetime
# from dotenv import load_dotenv
# import plotly.express as px
# import tiktoken

# # Set environment
# sys.path.append(os.path.abspath("app"))
# from dotenv import load_dotenv
# from salesforce import get_opportunities, update_next_step
# from salesforce_blob_dump import dump_all_salesforce_opportunities_to_blob
# from rag_orchestrator import answer_user_query, search_documents_for_user
# from task_generator import generate_email_task, generate_meeting_task
# from gmail_utils import send_email
# from calendar_utils import create_meeting

# load_dotenv()

# # Static user
# user_email = "harshlf4@gmail.com"

# st.set_page_config(page_title="Barclays Banker Assistant", layout="wide")
# st.markdown("""
#     <style>
#     .block-container { padding-top: 2rem; }
#     h1, h2, h3 { color: #002c5f; font-weight: 700; }
#     </style>
# """, unsafe_allow_html=True)

# st.title("💼 Barclays Banker Assistant")

# # Load and sync opportunities
# with st.spinner("🔍 Loading Salesforce opportunities..."):
#     opportunities = get_opportunities(user_email)

# with st.spinner("☁️ Syncing with Azure Blob..."):
#     dump_all_salesforce_opportunities_to_blob(user_email)

# if not opportunities:
#     st.warning("No opportunities available.")
#     st.stop()

# selected_opp = st.selectbox("🎯 Select an opportunity", [opp["Name"] for opp in opportunities])
# selected_data = next((opp for opp in opportunities if opp["Name"] == selected_opp), None)

# # GPT-4 Q&A Section
# st.markdown("### 🤖 GPT-4 Opportunity Assistant")
# user_question = st.text_input("💬 Ask a question about this opportunity:")

# if st.button("Ask GPT") and selected_opp and user_question:
#     with st.spinner("🤖 Thinking..."):
#         try:
#             answer = answer_user_query(user_email, selected_opp, user_question)
#             st.subheader("📈 GPT-4's Answer")
#             st.markdown(f"```\n{answer}\n```")
#         except Exception as e:
#             st.error(f"GPT-4 failed to answer: {str(e)}")

# # Helper
# def truncate_to_token_limit(text, max_tokens=500):
#     enc = tiktoken.encoding_for_model("gpt-4")
#     tokens = enc.encode(text)
#     return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# semantic_query = (
#     "What is missing from the opportunity documentation in terms of legal, team, financials, "
#     "investor readiness, and what actions the banker should take next?"
# )

# chunks = search_documents_for_user(user_email, selected_opp, semantic_query)
# combined_text = truncate_to_token_limit("\n\n".join(chunks), 2000)

# # Analyze All
# st.markdown("### 🧠 Analyze Pitchbook & Generate Tasks")
# if st.button("🔍 Generate All Tasks"):
#     with st.spinner("Reading documents and generating tasks..."):
#         task_data = generate_tasks(selected_data, combined_text, user_email)
#         st.subheader("📌 Suggested Next Step (AI)")
#         st.success(task_data.get("summary", "No summary available"))

#         if st.button("✅ Update 'Next Step' in Salesforce"):
#             result = update_next_step(selected_data["Id"], task_data.get("summary", ""))
#             if result["status"] == "success":
#                 st.success("Updated in Salesforce successfully!")
#             else:
#                 st.error(f"Failed to update: {result['details']}")

#         st.subheader("🧩 Missing Fields")
#         for item in task_data.get("missing_fields", []):
#             st.markdown(f"- {item}")

#         st.subheader("📬 Suggested Actions")
#         for idx, action in enumerate(task_data.get("actions", [])):
#             if action["type"] == "email":
#                 with st.expander(f"📧 Email Draft {idx + 1}"):
#                     st.code(f"To: {action['to']}\nSubject: {action['subject']}\n\n{action['body']}")
#                     if st.button(f"Send Email {idx + 1}"):
#                         result = send_email(
#                             to=action["to"],
#                             subject=action["subject"],
#                             body=action["body"],
#                             sender_email=user_email
#                         )
#                         if result["status"] == "success":
#                             st.success(f"Email sent! Message ID: {result['message_id']}")
#                         else:
#                             st.error(f"Email failed: {result['error']}")
#             elif action["type"] == "meeting":
#                 with st.expander(f"📅 Meeting Suggestion {idx + 1}"):
#                     st.markdown(f"**Title:** {action['title']}")
#                     st.markdown(f"**Description:** {action['description']}")
#                     date_part = st.date_input("📅 Meeting date", value=datetime.now().date())
#                     time_part = st.time_input("⏰ Meeting time", value=datetime.now().time())
#                     start_time = datetime.combine(date_part, time_part)
#                     if st.button(f"Create Meeting {idx + 1}"):
#                         result = create_meeting(
#                             banker_email=user_email,
#                             title=action["title"],
#                             description=action["description"],
#                             start_time=start_time,
#                             duration_minutes=action.get("duration_minutes", 30)
#                         )
#                         if result["status"] == "success":
#                             st.success(f"Meeting created! [View]({result['event_link']})")
#                         else:
#                             st.error(f"Meeting failed: {result['error']}")

# # Email Only
# st.markdown("### ✉️ Generate Follow-Up Email Only")

# if st.button("📤 Generate Email"):
#     with st.spinner("Working..."):
#         result = generate_email_task(selected_data, combined_text)
#         st.session_state.generated_email = result

# if "generated_email" in st.session_state:
#     result = st.session_state.generated_email
#     email = result.get("email", {})
#     st.success(result.get("summary", "No summary"))
#     st.code(f"To: {email.get('to')}\nSubject: {email.get('subject')}\n\n{email.get('body')}")
#     if st.button("Send Email"):
#         outcome = send_email(
#             to=email.get("to"),
#             subject=email.get("subject"),
#             body=email.get("body"),
#             sender_email=user_email
#         )
#         if outcome["status"] == "success":
#             st.success(f"✅ Email sent! ID: {outcome['message_id']}")
#         else:
#             st.error(f"❌ Failed to send email: {outcome['error']}")

# # Meeting Only
# st.markdown("### 📅 Propose Meeting Only")

# # if st.button("📆 Generate Meeting Suggestion"):
# #     with st.spinner("Planning meeting..."):
# #         result = generate_meeting_task(selected_data, combined_text)
# #         st.session_state.generated_meeting = result
# if st.button("📆 Generate Meeting Suggestion"):
#     with st.spinner("Planning meeting..."):
#         result = generate_meeting_task(selected_data, combined_text)

#         if result is None:
#             st.error("❌ Failed to generate meeting suggestion. Please check logs or try again.")
#         else:
#             meeting = result.get("meeting", {})
#             st.success(result.get("summary", "No summary"))
#             st.markdown(f"**Title:** {meeting.get('title')}  \n**Description:** {meeting.get('description')}")

#             date_part = st.date_input("📅 Meeting date", value=datetime.now().date())
#             time_part = st.time_input("⏰ Meeting time", value=datetime.now().time())
#             start_time = datetime.combine(date_part, time_part)

#             if st.button("Create Meeting"):
#                 outcome = create_meeting(
#                     banker_email=user_email,
#                     title=meeting.get("title"),
#                     description=meeting.get("description"),
#                     start_time=start_time,
#                     duration_minutes=meeting.get("duration_minutes", 30)
#                 )
#                 if outcome["status"] == "success":
#                     st.success(f"Meeting created! [Open]({outcome['event_link']})")
#                 else:
#                     st.error(f"Failed to create: {outcome['error']}")

# if "generated_meeting" in st.session_state:
#     result = st.session_state.generated_meeting
#     meeting = result.get("meeting", {})
#     st.success(result.get("summary", "No summary"))
#     st.markdown(f"**Title:** {meeting.get('title')}  \n**Description:** {meeting.get('description')}")
#     date_part = st.date_input("📅 Meeting date", value=datetime.now().date(), key="meet_date")
#     time_part = st.time_input("⏰ Meeting time", value=datetime.now().time(), key="meet_time")
#     start_time = datetime.combine(date_part, time_part)
#     if st.button("Create Meeting"):
#         outcome = create_meeting(
#             banker_email=user_email,
#             title=meeting.get("title"),
#             description=meeting.get("description"),
#             start_time=start_time,
#             duration_minutes=meeting.get("duration_minutes", 30)
#         )
#         if outcome["status"] == "success":
#             st.success(f"Meeting created! [Open]({outcome['event_link']})")
#         else:
#             st.error(f"Failed to create: {outcome['error']}")

# # 3D Visualization
# st.markdown("### 📊 Visual Opportunity Overview")

# stage_order = {
#     "Qualify": 1, "Meet & Present": 2, "Propose": 3,
#     "Negotiate": 4, "Closed Won": 5, "Closed Lost": 0
# }

# df = pd.DataFrame(opportunities)
# df["CloseDate"] = pd.to_datetime(df["CloseDate"], errors="coerce")
# df["CloseDateNum"] = df["CloseDate"].map(lambda x: x.timestamp() if pd.notnull(x) else 0)
# df["StageNum"] = df["StageName"].map(stage_order)
# df = df[df["StageNum"].notnull()]

# fig = px.scatter_3d(
#     df, x="CloseDateNum", y="Amount", z="StageNum", color="StageName",
#     hover_name="Name", hover_data={"CloseDate": True, "Amount": True, "StageName": True},
#     title="Opportunities by Close Date, Amount, and Stage"
# )

# fig.update_layout(
#     scene=dict(
#         xaxis_title="Close Date", yaxis_title="Deal Amount ($)", zaxis_title="Stage",
#         bgcolor="rgb(20,24,35)",
#         xaxis=dict(tickangle=-35, gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
#         yaxis=dict(gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
#         zaxis=dict(
#             tickvals=list(stage_order.values()),
#             ticktext=list(stage_order.keys()),
#             gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")
#         )
#     ),
#     margin=dict(l=10, r=10, b=10, t=40), height=600,
#     paper_bgcolor="rgb(20,24,35)", font=dict(color="white")
# )

# st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import plotly.express as px
import tiktoken

# Path setup
sys.path.append(os.path.abspath("app"))

# Internal imports
from salesforce import get_opportunities, update_next_step
from salesforce_blob_dump import dump_all_salesforce_opportunities_to_blob
from rag_orchestrator import answer_user_query, search_documents_for_user
from task_generator import generate_email_task, generate_meeting_task
from gmail_utils import send_email
from calendar_utils import create_meeting

# Load environment variables
load_dotenv()
user_email = "harshlf4@gmail.com"

# Layout
st.set_page_config(page_title="Barclays Banker Assistant", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: #002c5f; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Barclays Banker Assistant")

# Load data
with st.spinner("🔍 Loading Salesforce opportunities..."):
    opportunities = get_opportunities(user_email)

with st.spinner("☁️ Uploading to Azure Blob..."):
    dump_all_salesforce_opportunities_to_blob(user_email)

if not opportunities:
    st.warning("No opportunities available.")
    st.stop()

# Select Opportunity
selected_opp = st.selectbox("🎯 Select an opportunity", [opp["Name"] for opp in opportunities])
selected_data = next((opp for opp in opportunities if opp["Name"] == selected_opp), None)

# GPT-4 Q&A Section
st.markdown("### 🤖 GPT-4 Opportunity Assistant")
user_question = st.text_input("💬 Ask a question about this opportunity:")

if st.button("Ask GPT"):
    with st.spinner("🤖 Thinking..."):
        try:
            answer = answer_user_query(user_email, selected_opp, user_question)
            st.subheader("📈 GPT-4's Answer")
            st.markdown(f"```\n{answer}\n```")
        except Exception as e:
            st.error(f"GPT-4 failed to answer: {str(e)}")

# Truncate helper
def truncate_to_token_limit(text, max_tokens=500):
    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = enc.encode(text)
    return enc.decode(tokens[:max_tokens]) if len(tokens) > max_tokens else text

# Semantic context
semantic_query = (
    "What is missing from the opportunity documentation in terms of legal, team, financials, "
    "investor readiness, and what actions the banker should take next?"
)
chunks = search_documents_for_user(user_email, selected_opp, semantic_query)
combined_text = truncate_to_token_limit("\n\n".join(chunks), 2000)

# Email Generation Section
st.markdown("### ✉️ Generate Follow-Up Email Only")
if "email_generated" not in st.session_state:
    st.session_state.email_generated = False
    st.session_state.email_data = {}

if st.button("📤 Generate Email"):
    with st.spinner("Working..."):
        result = generate_email_task(selected_data, combined_text)
        if result:
            st.session_state.email_generated = True
            st.session_state.email_data = result

if st.session_state.email_generated:
    email = st.session_state.email_data.get("email", {})
    st.success(st.session_state.email_data.get("summary", "No summary available"))
    st.code(f"To: {email.get('to')}\nSubject: {email.get('subject')}\n\n{email.get('body')}")
    if st.button("📨 Send Email"):
        send_result = send_email(
            to=email.get("to"),
            subject=email.get("subject"),
            body=email.get("body"),
            sender_email=user_email
        )
        if send_result["status"] == "success":
            st.success(f"✅ Email sent! Message ID: {send_result['message_id']}")
        else:
            st.error(f"❌ Email failed: {send_result['error']}")

# Meeting Generation Section
st.markdown("### 📅 Propose Meeting Only")
if "meeting_generated" not in st.session_state:
    st.session_state.meeting_generated = False
    st.session_state.meeting_data = {}

if st.button("📆 Generate Meeting Suggestion"):
    with st.spinner("Planning meeting..."):
        result = generate_meeting_task(selected_data, combined_text)
        if result:
            st.session_state.meeting_generated = True
            st.session_state.meeting_data = result

if st.session_state.meeting_generated:
    meeting = st.session_state.meeting_data.get("meeting", {})
    st.success(st.session_state.meeting_data.get("summary", "No summary available"))
    st.markdown(f"**Title:** {meeting.get('title')}  \n**Description:** {meeting.get('description')}")
    date_part = st.date_input("📅 Meeting date", value=datetime.now().date(), key="meeting_date")
    time_part = st.time_input("⏰ Meeting time", value=datetime.now().time(), key="meeting_time")
    start_time = datetime.combine(date_part, time_part)
    if st.button("📲 Create Meeting"):
        result = create_meeting(
            banker_email=user_email,
            title=meeting.get("title"),
            description=meeting.get("description"),
            start_time=start_time,
            duration_minutes=meeting.get("duration_minutes", 30)
        )
        if result["status"] == "success":
            st.success(f"✅ Meeting created! [Join Meeting]({result['event_link']})")
        else:
            st.error(f"❌ Failed to create meeting: {result['error']}")

# 3D Opportunity Plot
st.markdown("### 📊 Visual Opportunity Overview")

stage_order = {
    "Qualify": 1, "Meet & Present": 2, "Propose": 3,
    "Negotiate": 4, "Closed Won": 5, "Closed Lost": 0
}

df = pd.DataFrame(opportunities)
df["CloseDate"] = pd.to_datetime(df["CloseDate"], errors="coerce")
df["CloseDateNum"] = df["CloseDate"].map(lambda x: x.timestamp() if pd.notnull(x) else 0)
df["StageNum"] = df["StageName"].map(stage_order)
df = df[df["StageNum"].notnull()]

fig = px.scatter_3d(
    df, x="CloseDateNum", y="Amount", z="StageNum", color="StageName",
    hover_name="Name", hover_data={"CloseDate": True, "Amount": True, "StageName": True},
    title="Opportunities by Close Date, Amount, and Stage"
)

fig.update_layout(
    scene=dict(
        xaxis_title="Close Date", yaxis_title="Deal Amount ($)", zaxis_title="Stage",
        bgcolor="rgb(20,24,35)",
        xaxis=dict(tickangle=-35, gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
        yaxis=dict(gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")),
        zaxis=dict(
            tickvals=list(stage_order.values()),
            ticktext=list(stage_order.keys()),
            gridcolor="rgba(200,200,200,0.3)", tickfont=dict(color="white")
        )
    ),
    margin=dict(l=10, r=10, b=10, t=40), height=600,
    paper_bgcolor="rgb(20,24,35)", font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)
