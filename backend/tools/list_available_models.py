"""List available Gemini models for local diagnostics."""

import os

from dotenv import load_dotenv
from google import genai


load_dotenv(".env")
key = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY set:", bool(key))
if not key:
    raise SystemExit("Missing GEMINI_API_KEY")

client = genai.Client(api_key=key)
models = list(client.models.list())
print("Found", len(models), "models")
for model in models[:80]:
    print(model.name)
