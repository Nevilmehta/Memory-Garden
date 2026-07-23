Memory Garden’s job is to decide what matters long-term,

Phase 1 — Core Memory API
Qdrant + FastAPI + Groq + extraction + search + chat

Phase 2 — Structured Memory System
memory types, metadata, schemas, filters, update logic

Phase 3 — Reflection System
summary generation, pattern detection, learning insights

Phase 4 — LangGraph Workflow
turn messy backend pipeline into clean graph nodes

Phase 5 — Relationship Discovery
entity extraction, memory links, relationship table/graph

Phase 6 — Agent System
Memory Agent, Reflection Agent, Relationship Agent, Archivist Agent

Phase 7 — Kafka/Event-Driven Architecture
memory.created, memory.updated, memory.searched, reflection.requested events

Phase 8 — Knowledge Graph
Neo4j or graph layer for entities and relationships

Phase 9 — Production Backend
auth, users, background workers, observability, logging, tests

Phase 10 — Polished Frontend
real custom UI, not Streamlit

-----------------------------------------------------------------------------
Repository:

Only knows SQL.
create_memory()
update_memory()
delete_memory()
list_memories()

Qdrant Store:

Only knows vectors.
index()
search()
delete_vector()

Extractor

Only knows LLM.
extract()
classify()
later:
detect_updates()
detect_relationships()

