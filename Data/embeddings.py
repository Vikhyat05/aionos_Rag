import os
from pathlib import Path
from markdown_it import MarkdownIt
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

openai_client = OpenAI(api_key=openai_key)
supabase = create_client(supabase_url, supabase_service_role_key)


md_parser = MarkdownIt()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)


def get_text_chunks(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("\n", " ")  # optional: normalize line breaks
    return splitter.split_text(text)


def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [e.embedding for e in response.data]


def upload_to_supabase(chunks, embeddings, source_file):
    """
    Uploads text chunks and their embeddings to Supabase with metadata like 'page_1'.
    """
    page_parts = Path(source_file).stem.split("_")
    page_name = "_".join(page_parts[:2])

    for chunk, embed in zip(chunks, embeddings):
        supabase.table("markdown_docs").insert(
            {"content": chunk, "embedding": embed, "metadata": {"source": page_name}}
        ).execute()


def process_file(file_path: str):
    chunks = get_text_chunks(file_path)
    embeddings = get_embeddings(chunks)
    upload_to_supabase(chunks, embeddings, os.path.basename(file_path))


MARKDOWN_DIR = Path(__file__).parent / "markdowns"

for fname in os.listdir(MARKDOWN_DIR):
    if fname.endswith(".md"):
        print(f"📄 Processing {fname}...")
        process_file(str(MARKDOWN_DIR / fname))
