import json
from groq import Groq
from app.core.config import settings


class GroqClient:
    def __init__(self, model_name: str | None = None):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model_name = model_name or settings.GROQ_MODEL

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        return json.loads(content)

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content