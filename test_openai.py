import os
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API anahtarını al
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Basit bir test öneri isteği
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Sen bir sürdürülebilirlik uzmanısın."},
        {"role": "user", "content": "Fosil yakıt tüketimini azaltmak için önerin nedir?"}
    ]
)

print(response.choices[0].message.content)
