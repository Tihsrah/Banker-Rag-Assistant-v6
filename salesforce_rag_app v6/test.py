from rag_orchestrator import answer_user_query

username = "harshlf4@gmail.com"
opportunity_name = "Testing"
question = "What are the terms of the NDA? who is borower, who is lender?"

response = answer_user_query(username, opportunity_name, question)
print("\n📣 Final Answer:\n", response)
