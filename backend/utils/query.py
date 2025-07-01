from openai import OpenAI
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
openai_client = OpenAI(api_key=openai_key)
supabase = create_client(supabase_url, supabase_service_role_key)


def get_query_embedding(query: str):
    """
    Generates an embedding vector for a given query string using OpenAI's embedding model.

    Args:
        query (str): The user’s natural language query.

    Returns:
        list[float]: A dense vector embedding representing the query in semantic space.
    """
    response = openai_client.embeddings.create(
        model="text-embedding-3-small", input=query
    )
    return response.data[0].embedding


def semantic_search(query: str, top_k: int = 5):
    """
    Performs a semantic search over a Supabase vector store of markdown documents.

    The function:
    - Converts the query into an embedding.
    - Calls a Supabase stored procedure `match_markdown_chunks` that performs nearest-neighbor search.
    - Returns the top-matching text chunks with metadata and similarity.

    Args:
        query (str): The insurance-related question or phrase.
        top_k (int, optional): The number of top matches to retrieve. Defaults to 5.

    Returns:
        list[dict]: A list of matched chunks. Each contains `content`, `metadata`, and `similarity`.
    """
    query_embed = get_query_embedding(query)

    response = supabase.rpc(
        "match_markdown_chunks", {"query_embedding": query_embed, "match_count": top_k}
    ).execute()
    print(response)
    return response.data
