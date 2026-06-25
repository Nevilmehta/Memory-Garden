from app.qdrant_store import QdrantMemoryStore

store = QdrantMemoryStore()

print("Adding memories...")

store.add_memory(
    text="I am learning LangGraph for my future Jarvis AI system.",
    category="learning",
    importance=9,
)

store.add_memory(
    text="I want to build AI Memory Garden as a long-term memory subsystem.",
    category="project",
    importance=10,
)

store.add_memory(
    text="I am interested in agents, tool calling, and advanced RAG.",
    category="interest",
    importance=8,
)

print("\nSearching memories...")

results = store.search_memories(
    query="What am I learning for Jarvis?",
    limit=3,
)

for memory in results:
    print("\n---")
    print("Score:", memory["score"])
    print("Text:", memory["text"])
    print("Category:", memory["category"])
    print("Importance:", memory["importance"])