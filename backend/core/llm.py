import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Required environment setup
openai_key = os.getenv("OPENAI_API_KEY")

global_client = AsyncOpenAI(api_key=openai_key)
