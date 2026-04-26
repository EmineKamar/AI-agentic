import os
from openai import OpenAI

import os
from dotenv import load_dotenv
from openai import OpenAI

# .env dosyasını yükler
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

# Basit bir chat completion örneği
resp = client.chat.completions.create(
    model="gpt-4.1-turbo",
    messages=[
        {"role": "user", "content": "Merhaba, nasılsın?"}
    ]
)

print(resp.choices[0].message.content)
