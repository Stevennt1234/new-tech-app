import openai
import os

def ask_chatgpt(question: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an HVAC expert."},
                      {"role": "user", "content": question}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {e}"
