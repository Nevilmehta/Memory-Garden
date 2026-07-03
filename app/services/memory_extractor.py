from app.clients.groq_client import GroqClient


class MemoryExtractor:
    def __init__(self):
        self.llm = GroqClient()

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

        if "memories" in result:
            memories = result.get("memories", [])
        else:
            if result.get("should_store") and result.get("memory_text"):
                memories = [
                    {
                        "memory_text": result.get("memory_text"),
                        "category": result.get("category", "general"),
                        "importance": result.get("importance", 5),
                        "reason": result.get("reason", ""),
                    }
                ]
            else:
                memories = []

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