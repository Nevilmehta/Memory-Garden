from app.groq_client import GroqClient

class MemoryExtractor:
    def __init__(self):
        self.llm = GroqClient(model_name="llama-3.1-8b-instant")

    def extract(self, message: str) -> dict:
        system_prompt = """
You are the memory extraction system for an AI called Memory Garden.

Your job is to extract useful long-term memories from the user's message.

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
- technical decisions for a project

Do NOT store:
- greetings
- random small talk
- temporary commands
- meaningless messages like "ok", "nice", "lets go"
- one-time debugging messages unless they reveal a project decision or repeated problem

Return ONLY valid JSON.

JSON schema:
{
  "memories": [
    {
      "memory_text": "clean third-person memory sentence",
      "category": "project",
      "importance": 8,
      "reason": "short reason"
    }
  ]
}

Allowed categories:
project, goal, learning, interest, preference, idea, experience, general

Rules:
- Extract zero, one, or multiple memories.
- Each memory should contain only one clear fact, goal, preference, or decision.
- Use third person: "User wants...", "User is learning...", "User prefers..."
- Do not combine unrelated ideas into one memory.
- Importance must be a number from 1 to 10.
- Importance 8-10 means important for long-term projects or Jarvis.
- Importance 5-7 means useful but not critical.
- Importance 1-4 means minor.
- If there is no useful long-term memory, return: {"memories": []}
- Return JSON only.
"""

        user_prompt = f"""
User message:
{message}
"""

        result = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        memories = result.get("memories", [])

        cleaned_memories = []

        for memory in memories:
            memory_text = memory.get("memory_text", "").strip()

            if not memory_text:
                continue

            cleaned_memories.append(
                {
                    "text": memory_text,
                    "category": memory.get("category", "general"),
                    "importance": memory.get("importance", 5),
                    "reason": memory.get("reason", ""),
                }
            )

        return {
            "memories": cleaned_memories
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

        