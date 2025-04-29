import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_report(notes):
    instructions = """Write a leadership consulting report based on these notes. Use professional tone and provide clear, structured insights."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": notes}
        ]
    )
    return response.choices[0].message.content.strip()
