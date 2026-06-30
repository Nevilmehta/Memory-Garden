from app.groq_client import GroqClient

class AnswerGenerator:
    def __init__(self):
        self.llm = GroqClient(model_name="llama-3.1-8b-instant")

    def generate_answer(self, question: str, memories: list[dict]):
        if not memories:
            return(
                "I could not find any relevant memories for that yet. "
                "You may need to store more memories first."
            )

        memory_context = self._format_memories(memories)

        system_prompt = """
You are the answer generation system for AI Memory Garden.

Your job is to answer the user's question using ONLY the provided memories.

Rules:
- Be clear and helpful.
- Do not invent facts that are not present in the memories.
- If the memories are not enough, say that clearly.
- Refer to the user as "you".
- Keep the answer concise but useful.
- Use the memories to personalize the answer.
"""

        user_prompt = f"""
User question:
{question}

Relevant memories:
{memory_context}

Answer the user's question based only on these memories.
"""

        return self.llm.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

    def _format_memories(self, memories: list[dict]) -> str:
        formatted = []

        for index, memory in enumerate(memories, start=1):
            formatted.append(
                f"""
Memory {index}:
Text: {memory.get("text")}
Category: {memory.get("category")}
Importance: {memory.get("importance")}
Similarity Score: {memory.get("score")}
Created At: {memory.get("created_at")}
"""
            )

        return "\n".join(formatted)