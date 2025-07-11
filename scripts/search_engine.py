import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import numpy as np

class SearchEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """Initialize SearchEngine with the specified sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.data_dir = Path("data")
        
        # Initialize ChromaDB client and get collection
        self.chroma_client = chromadb.PersistentClient(path=str(self.data_dir / "chroma"))
        self.collection = self.chroma_client.get_collection("compass")
        
    def hybrid_search(self, query: str, k: int = 5, semantic_weight: float = 0.75) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search.
        
        Args:
            query: The search query
            k: Number of results to return
            semantic_weight: Weight for semantic search (0.0 to 1.0)
            
        Returns:
            List of results with combined scores
        """
        # Get more results than needed to allow for hybrid reranking
        n_results = min(k * 2, self.collection.count())
        
        # Get results from ChromaDB (includes both semantic and keyword matches)
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["metadatas", "distances", "documents"]
        )
        
        # Extract results
        documents = results['documents'][0]  # First query's results
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        # Normalize distances to 0-1 range (ChromaDB returns cosine distance)
        semantic_scores = 1 - (np.array(distances) / 2)  # Convert cosine distance to similarity
        
        # Simple keyword matching score (TF-IDF like)
        query_terms = set(query.lower().split())
        keyword_scores = []
        
        for doc in documents:
            doc_terms = set(doc.lower().split())
            intersection = len(query_terms & doc_terms)
            union = len(query_terms | doc_terms)
            keyword_score = intersection / union if union > 0 else 0
            keyword_scores.append(keyword_score)
            
        keyword_scores = np.array(keyword_scores)
        
        # Combine scores
        combined_scores = (semantic_weight * semantic_scores + 
                         (1 - semantic_weight) * keyword_scores)
        
        # Sort by combined score
        sorted_indices = np.argsort(-combined_scores)  # Descending order
        
        # Prepare final results
        results = []
        for idx in sorted_indices[:k]:
            results.append({
                'question': metadatas[idx].get('question', ''),
                'answer': metadatas[idx].get('answer', ''),
                'source': metadatas[idx].get('source', ''),
                'category': metadatas[idx].get('category', ''),
                'subcategory': metadatas[idx].get('subcategory', ''),
                'score': float(combined_scores[idx])
            })
            
        return results 