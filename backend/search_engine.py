import chromadb
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Set
import re

class SearchEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """Initialize search engine with model and load necessary files."""
        self.model = SentenceTransformer(model_name)
        self.data_dir = Path("data")
        self.mental_health_terms: Set[str] = {
            "depress", "anxiety", "anxious", "sad", "stress", "therapy",
            "trauma", "grief", "panic", "mood", "mental", "emotion",
            "counseling", "crisis", "support", "help", "cope", "healing"
        }
        self.crisis_keywords: Set[str] = {
            "suicide", "kill", "die", "death", "hurt", "harm", "pain",
            "overdose", "cut", "cutting", "end it all", "give up"
        }
        self._load_resources()
        
    def _load_resources(self) -> None:
        """Load ChromaDB collection."""
        client = chromadb.PersistentClient(path=str(self.data_dir / "chroma"))
        self.collection = client.get_or_create_collection(
            name="compass",
            metadata={"hnsw:space": "cosine"}
        )
            
    def _compute_keyword_score(self, query: str, text: str) -> float:
        """Compute keyword-based score between query and text."""
        query_words = set(re.findall(r'\w+', query.lower()))
        text_words = set(re.findall(r'\w+', text.lower()))
        
        # Coverage score
        coverage = len(query_words & text_words) / len(query_words) if query_words else 0
        
        # Mental health terms boost
        query_mh_terms = query_words & self.mental_health_terms
        text_mh_terms = text_words & self.mental_health_terms
        boost = len(text_mh_terms) / len(query_mh_terms) if query_mh_terms else 0
        
        # Combine scores
        return (0.6 * coverage + 0.4 * boost) * 100
        
    def check_crisis(self, text: str) -> bool:
        """Check if text contains crisis keywords."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.crisis_keywords)
        
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform hybrid search combining semantic and keyword matching."""
        # Get semantic search results
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k * 3  # Get more candidates for reranking and deduplication
        )
        
        # Process and rerank results
        processed_results = []
        seen_contexts = set()  # For deduplication based on question content
        
        for idx, (text, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # Skip if we've seen this question before
            question = metadata['question'].strip().lower()
            if question in seen_contexts:
                continue
            seen_contexts.add(question)
            
            # Compute keyword score
            keyword_score = self._compute_keyword_score(query, text)
            
            # Convert distance to similarity score (ChromaDB returns distances)
            semantic_score = 1 - distance
            
            # Compute hybrid score (75% semantic, 25% keyword)
            hybrid_score = round(0.75 * semantic_score * 100 + 0.25 * keyword_score, 1)
            
            processed_results.append({
                'Context': metadata['question'],
                'Response': metadata['answer'],
                'score': hybrid_score
            })
            
            if len(processed_results) >= k:
                break
                
        # Sort by hybrid score
        processed_results.sort(key=lambda x: x['score'], reverse=True)
        return processed_results[:k] 