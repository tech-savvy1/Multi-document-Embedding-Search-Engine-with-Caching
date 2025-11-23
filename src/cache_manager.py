import json
import os
import hashlib
from datetime import datetime

CACHE_FILE = "embedding_cache.json" # Cache file path

class CacheManager: # Manages caching of embeddings
    def __init__(self):
        self.cache_file = CACHE_FILE
        self.cache = self._load_cache()

    def _load_cache(self): # Load existing cache from file
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self): # Save cache to file
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get_entry(self, doc_id): # Retrieve cache entry by document ID
        return self.cache.get(doc_id)

    def update_entry(self, doc_id, embedding, text_hash): # Update or add cache entry
        self.cache[doc_id] = {
            "embedding": embedding,
            "hash": text_hash,
            "updated_at": datetime.now().isoformat()
        }
        self.save_cache()

    @staticmethod
    def compute_hash(text): # Compute SHA256 hash of the text
        return hashlib.sha256(text.encode('utf-8')).hexdigest()