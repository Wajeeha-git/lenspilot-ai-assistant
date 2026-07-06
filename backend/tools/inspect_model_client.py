"""Inspect the configured Gemini client object during local development."""

import os

from dotenv import load_dotenv
from google import genai


load_dotenv(".env")
key = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY set:", bool(key))

if not key:
    raise SystemExit("Missing GEMINI_API_KEY")

client = genai.Client(api_key=key)
print("client.models object:", type(client.models))
print("client.models attributes:")
for name in dir(client.models):
    if not name.startswith("_"):
        print(name)
