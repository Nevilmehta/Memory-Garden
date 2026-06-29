import os 
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

class GroqClient:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        return json.loads(content)