Goal of this step====>

Build the smallest working memory system:
User writes memory
↓
Convert memory into embedding
↓
Store vector + text + metadata in Qdrant
↓
Search memory later using natural language

This teaches you the real founcation of RAG

-----------------------------------------------
Why Qdrant exists here

A normal database stores exact information:
Find row where topic = "LangGraph"
But a vector database stores meaning.

So this query:
"What framework am I studying for Jarvis?"

can still find:
"I am learning LangGraph for my Jarvis project."

Even though the words are different.
That happens because both texts become vectors that are close in embedding space.

---------------------------------------------------------------------------------
Important concept:

all-MiniLM-L6-v2 converts text into a 384-dimensional vector.

So this:
"I am learning LangGraph."

becomes something like:
[0.12, -0.04, 0.88, ... 384 numbers total]

Qdrant stores and searches these vectors.

----------------------------------------------------------------------------------
You built this:

Memory text
↓
Embedding model
↓
384-dimensional vector
↓
Qdrant collection
↓
Cosine similarity search
↓
Relevant memory result

This is the real base of memory RAG.

No LangGraph yet.
No multi-agent yet.
No knowledge graph yet.

Just the foundation.

----------------------------------------------------------------
So Qdrant now has duplicate memories.

This is actually an important real-world memory-system lesson:
Long-term memory systems need duplicate detection.

But we will not fix that yet. That becomes important in a later phase called Memory Growth / Merge / Duplicate Detection.

----------------------------------------------------------------
Duplication:
Before adding a memory, we will search Qdrant with the same text.
If a very similar memory already exists, we will not store it again.

New memory comes in
↓
Embed new memory
↓
Search existing memories
↓
If top similarity score is very high, example >= 0.92
    → treat as duplicate
    → do not store
Else
    → store as new memory

----------------------------------------------------------------

