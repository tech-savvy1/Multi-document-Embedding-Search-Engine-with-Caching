# 🔍 Multi-document Embedding Search Engine (with Caching)

A lightweight semantic search engine that:

- Embeds multiple documents with **Sentence Transformers**
- Uses **content-hash caching** to avoid recomputing embeddings
- Builds a **FAISS index** for fast nearest-neighbor search
- Exposes both **Streamlit UI** and **FastAPI API**
- Provides simple and transparent **search explanations**

---

## 📸 Preview

![Web App](Preview1.png)
![Web App](Preview2.png)

---

## 🚀 Live Demo

🔗 **Live Streamlit App:**  
[https://multi-document-embedding-search-engine-with-caching.streamlit.app/]

---

## 📂 Folder Structure
```
├── api.py # FastAPI backend
├── app.py # Streamlit UI
├── embedder.py # Embedding + caching logic
├── search_engine.py # FAISS index and search functions
├── cache_manager.py # Handles hashing and embedding_cache.json
├── embedding_cache.json # Auto-generated cache file
├── data/
│ └── docs/ # Place your .txt documents here
└── README.md
```

---

## ⚙️ How Caching Works

Caching is implemented using **SHA-256 hashes** of cleaned document content.

### 🔄 Caching Process

1. Document text is cleaned (lowercasing, HTML removal, whitespace normalization).
2. A **SHA-256 hash** of the cleaned text is generated.
3. `embedding_cache.json` stores:
   - `doc_id`
   - `hash` (content hash)
   - `embedding`
   - `metadata` (filename, timestamp)
4. When loading documents:
   - If hash **matches** → **reuse embedding**
   - If hash **differs** or absent → **regenerate embedding**

### ✅ Why this method?

- Avoids re-running expensive embedding operations  
- Auto-invalidates when file content changes  
- JSON format is simple and version-friendly  
- Fast and predictable

### 🔧 Forcing a regeneration

Delete the cache:

```bash
rm embedding_cache.json
```

# Multi-document Embedding Search Engine (with Caching)

## 🧠 How to Run Embedding Generation

The system generates embeddings in three ways.

### 1. Manual Generation (recommended for debugging)
```
python -c "from embedder import Embedder; Embedder().process_documents()"
```

### 2. Streamlit UI (auto generates embeddings)
```
streamlit run app.py
```

### 3. API Startup (auto generates embeddings)
```
uvicorn api:app --host 0.0.0.0 --port 8000
```

All three will:
- Read documents from `data/docs/`
- Check cache
- Generate missing embeddings
- Save the updated cache

---

## 🌐 How to Start the API

Start the FastAPI backend:
```
uvicorn api:app --host 0.0.0.0 --port 8000
```

### ➤ Endpoint: /search

POST request:
```json
{
  "query": "machine learning",
  "top_k": 5
}
```

Example CURL:
```
curl -X POST "http://localhost:8000/search"   -H "Content-Type: application/json"   -d '{"query": "deep learning", "top_k": 3}'
```

---

## 🖥️ How to Start the Streamlit UI
```
streamlit run app.py
```

The UI:
- Loads embeddings (using caching)
- Builds FAISS index
- Lets you run semantic search interactively

---

## 🧱 Design Choices

### 1. SHA-256 Content Hashing for Caching
- Guarantees accurate invalidation
- Simple and deterministic
- Avoids timestamp inconsistencies

### 2. Sentence Transformer Model
Default: `all-MiniLM-L6-v2`
- Fast on CPU
- Memory-efficient
- High semantic quality

### 3. FAISS: IndexFlatIP
- Cosine similarity (with normalized vectors)
- Extremely fast nearest-neighbor search
- Scalable and flexible

### 4. Search Explanation
- Token overlap
- Overlap ratio
- Human-readable 'why this result'

### 5. Modular Architecture
- Embedder → preprocessing + embedding + caching
- CacheManager → load/save cache
- SearchEngine → FAISS search + explanations
- api.py → backend
- app.py → UI

---

## 📦 Requirements
```
sentence-transformers
faiss-cpu
numpy
fastapi
uvicorn
pydantic
streamlit
```

---

## 🛠 Troubleshooting

| Problem | Solution |
|--------|----------|
| Embeddings not updating | Delete `embedding_cache.json` |
| No documents loaded | Add `.txt` files in `data/docs/` |
| Slow embedding generation | Use GPU or batching |
| FAISS index empty | Ensure `process_documents()` ran |

---

## 🚀 Optional Improvements
- Document chunking
- Hybrid BM25 + Vector search
- GPU FAISS
- Docker support
- Redis/SQLite cache backend
