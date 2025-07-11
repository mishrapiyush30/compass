import json
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from tqdm import tqdm

class IndexBuilder:
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """Initialize IndexBuilder with the specified sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.batch_size = 32
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=str(self.data_dir / "chroma"))
        
    def load_corpus(self, json_path: str) -> List[Dict[str, Any]]:
        """Load the Q&A corpus from JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def build_index(self, corpus_path: str) -> None:
        """Build ChromaDB collection from corpus."""
        print("Loading corpus...")
        corpus = self.load_corpus(corpus_path)
        
        # Create or get collection
        collection = self.chroma_client.get_or_create_collection(
            name="compass",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        # Prepare data for batch insertion
        ids = []
        texts = []
        metadatas = []
        
        print("Processing documents...")
        for idx, item in enumerate(tqdm(corpus)):
            ids.append(str(idx))
            texts.append(item['embedding_text'])
            metadatas.append({
                'question': item.get('question', ''),
                'answer': item.get('answer', ''),
                'source': item.get('source', ''),
                'category': item.get('category', ''),
                'subcategory': item.get('subcategory', '')
            })
        
        # Add documents in batches
        print("Adding documents to ChromaDB...")
        for i in tqdm(range(0, len(texts), self.batch_size)):
            batch_ids = ids[i:i + self.batch_size]
            batch_texts = texts[i:i + self.batch_size]
            batch_metadatas = metadatas[i:i + self.batch_size]
            
            collection.add(
                ids=batch_ids,
                documents=batch_texts,
                metadatas=batch_metadatas,
                embeddings=self.model.encode(batch_texts).tolist()
            )
            
        print(f"Index built successfully! Stats:")
        print(f"- Corpus size: {len(corpus)} Q&A pairs")
        print(f"- Collection name: compass")
        print(f"- Files saved to: {self.data_dir}/chroma")

if __name__ == "__main__":
    builder = IndexBuilder()
    builder.build_index("data/combined_dataset.json") 