import os
from openai import OpenAI

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_chatgpt(question: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # fast & cost-effective
            messages=[
                {"role": "system", "content": "You are an HVAC expert. Answer clearly and concisely."},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Error: {e}"
