import faiss
import numpy as np
import re

class SearchEngine: # Embedding-based search engine using FAISS
    def __init__(self):
        self.index = None
        self.doc_ids = []
        self.metadata = []
        self.embeddings = None

    def build_index(self, doc_ids, embeddings, metadata): # Build FAISS index
        self.doc_ids = doc_ids
        self.metadata = metadata
        # Convert list to numpy array
        self.embeddings = np.array(embeddings).astype('float32')
        
        # Normalize for Cosine Similarity using FAISS (IndexFlatIP)
        faiss.normalize_L2(self.embeddings)
        
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings)

    def search(self, query_text, query_vector, top_k=5): # Search for similar documents
        query_vector = np.array([query_vector]).astype('float32')
        faiss.normalize_L2(query_vector)
        
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]): # Iterate over top_k results
            if idx == -1: continue
            
            doc_meta = self.metadata[idx] # Retrieve metadata
            score = float(distances[0][i]) # Similarity score
            
            # Generate detailed explanation using the query text
            explanation = self._generate_explanation(doc_meta, score, query_text)
            
            results.append({ 
                "doc_id": doc_meta['doc_id'],
                "score": round(score, 4),
                "preview": doc_meta['original_text'],
                "explanation": explanation
            })
            
        return results 

    def _generate_explanation(self, doc_meta, score, query_text):
        # 1. Simple Tokenization (split by non-word characters)
        # Using set() to get unique words
        query_tokens = set(re.findall(r'\w+', query_text.lower()))
        doc_tokens = set(re.findall(r'\w+', doc_meta['full_text'].lower()))
        
        # 2. Find Overlap
        # Intersection of words in query and words in document
        common_tokens = query_tokens.intersection(doc_tokens)
        
        # 3. Calculate Ratio
        if len(query_tokens) > 0:
            overlap_ratio = len(common_tokens) / len(query_tokens)
        else:
            overlap_ratio = 0.0
            
        # 4. Construct Explanation Object
        return {
            "why_this": f"High semantic match ({score:.2f}) with {len(common_tokens)} keyword overlaps.",
            "overlapped_keywords": list(common_tokens),
            "overlap_ratio": round(overlap_ratio, 2)
        }