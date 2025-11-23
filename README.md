🧠 Multi-document Embedding Search Engine (with Caching)

A lightweight semantic search engine that:

Embeds multiple documents using Sentence Transformers

Uses content-based caching to avoid recomputing embeddings

Builds a FAISS vector index for fast similarity search

Exposes Streamlit UI + FastAPI backend

Provides transparent search explanations

🚀 Features

📄 Multi-document ingestion (data/docs/)

⚡ Caching using per-document SHA-256 content hashes

🔎 Fast FAISS-based similarity search

🧰 Clean modular structure (Embedder, CacheManager, SearchEngine)

🌐 API + UI supported

📦 Folder Structure
.
├── api.py                  # FastAPI server
├── app.py                  # Streamlit UI
├── embedder.py             # Embedding + caching logic
├── search_engine.py        # FAISS index and search functions
├── cache_manager.py        # Cache load, save, hashing
├── embedding_cache.json    # Auto-generated cache
├── data/
│   └── docs/               # Add your .txt documents here
└── README.md

🧩 How Caching Works

Caching is handled entirely by CacheManager + Embedder.

🔍 Caching Workflow

Each document is cleaned and preprocessed.

Its cleaned text is hashed using SHA-256.

Cache file: embedding_cache.json. Each entry includes:

doc_id

hash (content hash)

embedding (vector)

metadata (filename + timestamp)

When loading documents:

If a document's hash matches the cached hash → reuse embedding

If hash changes or no entry exists → regenerate embedding

✅ Benefits

No unnecessary model calls

Cache automatically invalidates when document content changes

Simple, portable JSON-based cache

📄 How to Run Embedding Generation

There are three ways to generate embeddings:

1. Manual generation (recommended during development)
python -c "from embedder import Embedder; Embedder().process_documents()"

2. Streamlit autogeneration

Running the UI automatically generates/reuses cached embeddings:

streamlit run app.py

3. FastAPI autogeneration

The API loads embeddings and builds FAISS index on startup:

uvicorn api:app --host 0.0.0.0 --port 8000

🌐 How to Start the API

Start FastAPI server:

uvicorn api:app --host 0.0.0.0 --port 8000

API Endpoint

POST /search

Example request:
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 5}'

Example response:
[
  {
    "doc_id": "doc1",
    "score": 0.82,
    "preview": "first few lines of the doc...",
    "explanation": {
      "overlap_tokens": ["learning", "model"],
      "overlap_ratio": 0.22,
      "why_this": "Document shares semantic and keyword similarity."
    }
  }
]

🖥️ Start the Streamlit UI
streamlit run app.py


This loads embeddings (with caching) and builds the search interface.

🏗️ Design Choices
1. Content-Hash Based Caching

Avoids re-computation by using SHA-256 hashes

JSON cache for transparency and debugging

Clear invalidation rules

2. Sentence-Transformer Model

Default: all-MiniLM-L6-v2
Chosen because:

Fast

Lightweight (good for CPU)

High semantic quality for small projects

3. FAISS Index

Used FAISS IndexFlatIP with vector normalization → Cosine similarity.
Reasons:

Extremely fast nearest neighbor search

Swappable with GPU FAISS or vector DBs (Pinecone/Milvus)

4. Transparent Search Explanation

Instead of a heavy LLM explanation, the score explanation comes from:

token overlap

overlap ratio

short “why this result” message

5. Clean Modularity

Embedder handles preprocessing + embeddings + caching

CacheManager handles persistence

SearchEngine handles FAISS + ranking + explanations

api.py and app.py are thin wrappers

🛠️ Requirements

Add this as your requirements.txt:

sentence-transformers
faiss-cpu
numpy
fastapi
uvicorn
pydantic
streamlit

🧪 Troubleshooting
Issue	Fix
Cache not updating	Delete embedding_cache.json
No documents found	Place .txt files in data/docs/
Slow embedding generation	Use GPU or batch encoding
Index returns no results	Ensure FAISS index is built on startup
🎯 Future Enhancements (Optional)

Chunk-based document splitting

GPU FAISS index

Redis-based caching

Hybrid search (BM25 + vectors)

LLM-based answer generation
