from azure_search_client import search_documents_for_user
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Azure OpenAI configuration
openai_client = AzureOpenAI(
    api_version="2024-04-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

def generate_answer_from_context(user_question, context_text):
    prompt = f"""
You are a senior investment banking assistant.
You will ONLY answer based on the provided document context.
If the answer is not in the documents, respond with: "I don't have that information."

Context:
{context_text}

Question:
{user_question}
""".strip()

    print("\n🧠 [OPENAI] Sending prompt to GPT...")
    print(f"📋 Prompt Preview:\n{prompt[:1000]}")

    response = openai_client.chat.completions.create(
        model=openai_deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a financial assistant using internal opportunity documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
        temperature=0
    )

    return response.choices[0].message.content.strip()

def answer_user_query(username: str, opportunity_name: str, user_question: str) -> str:
    print(f"\n🔍 [RAG] Searching Azure for relevant documents for: {username}/{opportunity_name}")
    docs = search_documents_for_user(username, opportunity_name, user_question)

    if not docs:
        return "No relevant documents found for this opportunity and user."

    context_text = "\n\n".join(docs)
    return generate_answer_from_context(user_question, context_text)
