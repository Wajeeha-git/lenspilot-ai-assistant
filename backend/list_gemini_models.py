from dotenv import load_dotenv
import os
from google import genai

load_dotenv('.env')
key = os.getenv('GEMINI_API_KEY')
print('GEMINI_API_KEY set:', bool(key))
if not key:
    raise SystemExit('Missing GEMINI_API_KEY')
client = genai.Client(api_key=key)
models = client.models.list_models()
print('Found', len(models), 'models')
for m in models[:60]:
    print(m.name)
