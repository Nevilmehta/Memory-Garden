import json
import requests

class OllamaClient:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"

    def generate(self, prompt: str):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        return response.json()["response"]

    def generate_json(self, prompt: str):
        raw_response = self.generate(prompt)

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            start = raw_response.find("{")
            end = raw_response.rfind("}") + 1

            if start == -1 or end == 0:
                raise ValueError(f"Could not parse JSON from model response: {raw_response}")

            json_text = raw_response[start:end]
            return json.loads(json_text)