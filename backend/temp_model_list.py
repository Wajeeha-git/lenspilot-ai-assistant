from dotenv import load_dotenv
import os
from google import genai

load_dotenv('.env')
key = os.getenv('GEMINI_API_KEY')
print('GEMINI_API_KEY set:', bool(key))
client = genai.Client(api_key=key)
models = client.models.list()
print('Found', len(models), 'models')
for model in models[:80]:
    print(model.name)
