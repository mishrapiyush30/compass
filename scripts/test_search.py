from search_engine import SearchEngine
from pprint import pprint

def test_search():
    # Initialize search engine
    search = SearchEngine()
    
    # Test queries
    test_queries = [
        "How do I deal with anxiety?",
        "What are some coping mechanisms for stress?",
        "I'm feeling depressed, what should I do?",
        "How to improve mental health?",
        "Ways to practice self-care"
    ]
    
    # Try each query
    for query in test_queries:
        print("\nQuery:", query)
        print("-" * 50)
        
        # Get results with default weights (75% semantic, 25% keyword)
        results = search.hybrid_search(query, k=3)
        
        # Print results
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (Score: {result['score']:.3f}):")
            print(f"Q: {result['question']}")
            print(f"A: {result['answer']}")
            
        print("\n" + "="*80)

if __name__ == "__main__":
    test_search() 