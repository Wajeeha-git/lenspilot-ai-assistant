from dotenv import load_dotenv
import os
from google import genai

load_dotenv('.env')
key = os.getenv('GEMINI_API_KEY')
print('GEMINI_API_KEY set:', bool(key))
client = genai.Client(api_key=key)
print('client.models obj:', type(client.models))
print('client.models attributes:')
for name in dir(client.models):
    if not name.startswith('_'):
        print(name)
