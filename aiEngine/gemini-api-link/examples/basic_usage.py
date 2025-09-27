"""
Basic Usage Examples for Enhanced Gemini Client
"""

from enhanced_gemini_client import process_query

def example_yield_prediction():
    """Example of yield prediction functionality"""
    print("=== Yield Prediction Example ===")

    query = "What will be the yield of rice in Punjab during winter season?"
    result = process_query(query)

    print(f"Query: {query}")
    print(f"Module: {result['module']}")

    if 'predictions' in result:
        for pred in result['predictions']:
            print(f"  - {pred.get('crop', 'Unknown')}: {pred.get('yield_estimate', 'N/A')} {pred.get('unit', '')}")

def example_fallback_nlp():
    """Example of fallback NLP functionality"""
    print("\n=== Fallback NLP Example ===")

    query = "What are the best practices for organic farming?"
    result = process_query(query)

    print(f"Query: {query}")
    print(f"Module: {result['module']}")

    if 'response' in result:
        print(f"Response: {result['response'][:150]}...")

if __name__ == "__main__":
    print("Enhanced Gemini Client - Basic Examples")
    print("=" * 50)

    example_yield_prediction()
    example_fallback_nlp()

    print("\n" + "=" * 50)
    print("Examples completed!")
