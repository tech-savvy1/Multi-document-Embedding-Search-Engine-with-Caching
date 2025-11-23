import os
import re
from sentence_transformers import SentenceTransformer
from cache_manager import CacheManager

class Embedder: # Handles document embedding with caching
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        print(f"Loading model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.cache_manager = CacheManager()
        self.docs_path = "data/docs"

    def preprocess_text(self, text): # Text Preprocessing
        text = text.lower() # Lowercase
        text = re.sub(r'<[^>]+>', '', text) # Remove HTML tags
        text = re.sub(r'\s+', ' ', text).strip() # Remove extra spaces
        return text

    def process_documents(self): # Embed documents with caching
        embeddings = []
        doc_ids = []
        metadata = []

        files = sorted(os.listdir(self.docs_path))
        
        for filename in files:
            if not filename.endswith(".txt"): # Only process .txt files
                continue
                
            file_path = os.path.join(self.docs_path, filename) # Full file path
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read() # Read raw text
            
            cleaned_text = self.preprocess_text(raw_text) # Preprocess text
            current_hash = self.cache_manager.compute_hash(cleaned_text) # Text hash
            doc_id = filename

            cached_entry = self.cache_manager.get_entry(doc_id) # retrieve cache entry

            # Check if cache is valid (hash match)
            if cached_entry and cached_entry['hash'] == current_hash:
                embedding = cached_entry['embedding']
            else:
                # Generate new embedding
                embedding = self.model.encode(cleaned_text).tolist()
                self.cache_manager.update_entry(doc_id, embedding, current_hash)
            
            embeddings.append(embedding)
            doc_ids.append(doc_id)
            metadata.append({
                "doc_id": doc_id, # Document ID
                "original_text": raw_text[:200] + "...", # Preview of original text
                "full_text": cleaned_text, # Store full cleaned text
                "length": len(cleaned_text) # Length of cleaned text
            })

        return doc_ids, embeddings, metadata # Return lists of doc IDs, embeddings, and metadata

    def embed_query(self, query): # Embed a search query
        clean_query = self.preprocess_text(query)
        return self.model.encode(clean_query)