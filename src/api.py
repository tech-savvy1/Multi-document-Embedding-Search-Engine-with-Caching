from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from embedder import Embedder
from search_engine import SearchEngine

app = FastAPI(
    title="Multi-Document Embedding Search API",
    description="Search Engine with Ranking Explanation",
    version="1.1.0"
)

# Global instances
embedder = Embedder()
engine = SearchEngine()

# Initialize data on startup
@app.on_event("startup")
def load_data():
    doc_ids, embeddings, metadata = embedder.process_documents()
    engine.build_index(doc_ids, embeddings, metadata)

# Models
class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query")
    top_k: int = Field(5, description="Number of results")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "ray tracing",
                    "top_k": 3
                }
            ]
        }
    }

class Explanation(BaseModel):
    why_this: str
    overlapped_keywords: List[str]  
    overlap_ratio: float

class SearchResult(BaseModel):
    doc_id: str
    score: float
    preview: str
    explanation: Explanation

class SearchResponse(BaseModel):
    results: List[SearchResult]

# Endpoint
@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    # 1. Embed Query
    query_vec = embedder.embed_query(request.query)
    
    # 2. Search Index
    results = engine.search(request.query, query_vec, request.top_k)
    
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)