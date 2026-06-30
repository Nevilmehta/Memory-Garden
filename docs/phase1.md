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

Important Concept: Memory Extraction(Rule based)

Right now we are sending this,
Hey bro today I was working on Memory Garden and I think I want to use Qdrant only, not ChromaDB.
Would be stored as raw memory

But a real memory system should extract the actual memory,
User wants to use Qdrant only for the Memory Garden project, not ChromaDB.

So this is the flow,
User Message
   ↓
Memory Extractor
   ↓
Clean Memory
   ↓
Embedding
   ↓
Qdrant


Next step: LLM Based Memory Extractor with Ollama

Right now your extractor is rule based.
That is useful for learning, but its not intelligent.

Now we want this,
User message
↓
Ollama LLM
↓
Extract clean memory
↓
Return structured JSON
↓
Store in Qdrant

This teaches a very important AI engineering idea:
LLMs are not only for chatting.
They can act as structured information extractors.

----------------------------------------------------------------------------------

Memory Garden’s job is to decide what matters long-term.
Primary: Groq / hosted LLM
Fallback: Ollama local model
Sensitive memories: local-only mode

-----------------------------------------------------------------------------------

Multiple memory:
Example:

I am learning LangGraph for Jarvis, but before going deep into agents, I want to improve my RAG basics. Also, I prefer using Qdrant over ChromaDB.

This should become three memories:

1. User is learning LangGraph for Jarvis.
2. User wants to improve RAG basics before going deep into agents.
3. User prefers Qdrant over ChromaDB.

This is important because Memory Garden should not treat a whole paragraph as one messy memory. It should break it into clean memory units.

New Architecture:
FastAPI
↓
MessageInput
↓
Groq MemoryExtractor
↓
Multiple atomic memories
↓
For each memory:
    Qdrant semantic duplicate check
    embedding
    vector storage
↓
Search API

-------------------------------------------------------------------------------------

Answer Generation:
Until now, Memory Garden can:

Store memories
Search memories
Extract clean memories
Avoid some duplicates

But now we want it to answer questions using stored memories.

This is the first complete RAG loop:
User Question
↓
Embed question
↓
Retrieve relevant memories from Qdrant
↓
Send question + memories to Groq
↓
Generate personalized answer

-----------------------------------------------------------------------------------

Current Architecture:
FastAPI
│
├── /memories
│     └── Direct memory storage
│
├── /memories/search
│     └── Vector search
│
├── /memories/extract-and-store
│     └── Groq extractor → atomic memories → Qdrant
│
└── /chat
      └── Question → Qdrant retrieval → Groq answer
      