

class MemoryExtractor:
    def extract(self, message: str):
        """
        Phase 1C rule-based memory extractor.

        Later this will be replaced with an LLM-based extractor.
        For now, it teaches us:
        - what should become memory
        - what category it belongs to
        - how important it is
        """
        cleaned_message = message.strip()

        category = self._classify_category(cleaned_message)
        importance = self._score_importance(cleaned_message, category)
        memory_text = self._rewrite_as_memory(cleaned_message)

        return {
            "text": memory_text,
            "category": category,
            "importance": importance
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

        