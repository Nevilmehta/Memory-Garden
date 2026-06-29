from app.ollama_client import OllamaClient

class MemoryExtractor:
    def __init__(self):
        self.llm = OllamaClient(model_name="llama3.2:3b")

    def extract(self, message: str) -> dict:
        prompt = f"""
You are the memory extraction system for an AI called Memory Garden.

Your job is to decide whether the user's message contains useful long-term memory.

A useful long-term memory includes:
- projects the user is building
- goals
- skills the user is learning
- interests
- preferences
- important decisions
- plans
- personal workflow preferences
- ideas that may matter later

Do NOT store:
- greetings
- random small talk
- temporary commands
- one-time debugging messages unless they reveal a project decision
- meaningless messages like "ok", "nice", "lets go"

Return ONLY valid JSON.

JSON schema:
{{
  "should_store": true or false,
  "memory_text": "clean third-person memory sentence",
  "category": "project | goal | learning | interest | preference | idea | experience | general",
  "importance": number from 1 to 10,
  "reason": "short reason why this should or should not be stored"
}}

Rules:
- Use third person: "User wants...", "User is learning...", "User prefers..."
- If should_store is false, memory_text should be an empty string.
- Importance 8-10 means important for long-term projects or Jarvis.
- Importance 5-7 means useful but not critical.
- Importance 1-4 means minor.
- Return JSON only. No markdown. No explanation outside JSON.

User message:
{message}
"""

        result = self.llm.generate_json(prompt)

        return {
            "should_store": result.get("should_store", False),
            "text": result.get("memory_text", ""),
            "category": result.get("category", "general"),
            "importance": result.get("importance", 5),
            "reason": result.get("reason", ""),
        }

    def _classify_category(self, text: str) -> str:
        lower_text = text.lower()

        if any(word in lower_text for word in ["project", "build", "building", "app", "system"]):
            return "project"

        if any(word in lower_text for word in ["learn", "learning", "study", "understand"]):
            return "learning"

        if any(word in lower_text for word in ["goal", "want to", "plan to", "aim"]):
            return "goal"

        if any(word in lower_text for word in ["like", "prefer", "preference", "use qdrant", "not chromadb"]):
            return "preference"

        if any(word in lower_text for word in ["idea", "thinking", "concept"]):
            return "idea"

        return "general"

    def _score_importance(self, text: str, category: str) -> int:
        lower_text = text.lower()

        score = 5

        if category in ["project", "goal"]:
            score += 2

        if category == "learning":
            score += 1

        if any(word in lower_text for word in ["jarvis", "memory garden", "long-term", "future"]):
            score += 2

        if any(word in lower_text for word in ["important", "must", "only", "remember"]):
            score += 1

        return min(score, 10)

    def _rewrite_as_memory(self, text: str) -> str:
        lower_text = text.lower()

        if lower_text.startswith("i am "):
            return "User is " + text[5:]

        if lower_text.startswith("i'm "):
            return "User is " + text[4:]

        if lower_text.startswith("i want "):
            return "User wants " + text[7:]

        if lower_text.startswith("i prefer "):
            return "User prefers " + text[9:]

        if lower_text.startswith("my "):
            return "User's " + text[3:]

        return f"User said: {text}"

        