import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Load .env
load_dotenv()

# Azure Search setup
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
)

# def search_azure_index(query: str, user_email: str = "", opportunity_name: str = "") -> list:
#     print(f"\n🔍 [AZURE_SEARCH] Querying vector index for: '{query}'")

#     # ✅ Use only valid index fields: "chunk", "storage_path", "title"
#     raw_results = search_client.search(
#         search_text=query,
#         select=["chunk", "storage_path", "title"]
#     )

#     expected_folder = f"{user_email.strip().lower()}/{opportunity_name.strip().lower()}/"
#     filtered = []

#     print(f"\n📂 [FILTER] Filtering chunks for folder: {expected_folder}\n")

#     for doc in raw_results:
#         path = doc.get("storage_path", "").lower()
#         title = doc.get("title", "[Untitled]")
#         text = doc.get("chunk", "").strip()

#         print(f"📄 Title: {title}")
#         print(f"📁 Path: {path[:120]}")
#         print(f"📝 Preview: {text[:200]}")

#         if expected_folder in path:
#             print(f"✅ Keeping: {title} ({path})")
#             filtered.append({
#                 "title": title,
#                 "path": path,
#                 "content": text
#             })
#         else:
#             print(f"⛔ Skipping: {title} — path doesn't match {expected_folder}")

#     print(f"\n✅ Total relevant chunks: {len(filtered)}\n")
#     return filtered

def search_azure_index(query: str, user_email: str = "", opportunity_name: str = "") -> list:
    print(f"\n🔍 [AZURE_SEARCH] Querying vector index for: '{query}'")

    raw_results = search_client.search(
        search_text=query,
        select=["chunk", "storage_path", "title"]
    )

    expected_folder = f"{user_email.strip().lower()}/{opportunity_name.strip().lower()}/"
    important_keywords = ["salesforce_summary", "pitchbook"]
    filtered = []

    print(f"\n📂 [FILTER] Filtering chunks for folder: {expected_folder}")
    print(f"🔎 Only keeping files containing: {important_keywords}\n")

    for doc in raw_results:
        path = doc.get("storage_path", "").lower()
        title = doc.get("title", "[Untitled]").lower()
        text = doc.get("chunk", "").strip()

        print(f"📄 Title: {title}")
        print(f"📁 Path: {path[:120]}")
        print(f"📝 Preview: {text[:200]}")

        if expected_folder in path:
            if any(keyword in path or keyword in title for keyword in important_keywords):
                print(f"✅ Keeping: {title} ({path})")
                filtered.append({
                    "title": title,
                    "path": path,
                    "content": text
                })
            else:
                print(f"⛔ Skipping non-key file: {title}")
        else:
            print(f"⛔ Skipping unrelated folder: {title} — doesn't match {expected_folder}")

    print(f"\n✅ Total relevant chunks kept: {len(filtered)}\n")
    return filtered

def extract_user_and_opportunity_from_path(storage_path):
    try:
        parts = storage_path.split("/banker-updates/")[1].split("/")
        if len(parts) >= 2:
            return parts[0].lower(), parts[1].lower()
    except Exception:
        pass
    return None, None

def search_documents_for_user(username, opportunity_name, query_text):
    print(f"\n🔍 [DEBUG] Running Azure Search for:")
    print(f"   Query: '{query_text}'")
    print(f"   Username: '{username}'")
    print(f"   Opportunity: '{opportunity_name}'")

    results = search_azure_index(query=query_text, user_email=username, opportunity_name=opportunity_name)
    matched_chunks = [doc["content"] for doc in results]

    print(f"\n✅ [RESULT] Matched Chunks Count: {len(matched_chunks)}")
    return matched_chunks
