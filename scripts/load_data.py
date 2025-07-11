import pandas as pd
import json
from pathlib import Path

def convert_csv_to_json():
    """Convert Dataset.csv to combined_dataset.json with proper formatting."""
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Read CSV file
    df = pd.read_csv("dataset/Dataset.csv")
    
    # Convert DataFrame to list of dictionaries
    corpus = []
    for _, row in df.iterrows():
        # Combine context and response for embedding
        embedding_text = f"{row['Context']} {row['Response']}"
        
        # Create document entry
        doc = {
            'question': row['Context'],
            'answer': row['Response'],
            'embedding_text': embedding_text,
            'source': 'Dataset.csv',  # Original source
            'category': '',  # Can be filled in later if categories are added
            'subcategory': ''  # Can be filled in later if subcategories are added
        }
        corpus.append(doc)
    
    # Save as JSON
    output_path = data_dir / "combined_dataset.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {len(corpus)} Q&A pairs")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    convert_csv_to_json() 