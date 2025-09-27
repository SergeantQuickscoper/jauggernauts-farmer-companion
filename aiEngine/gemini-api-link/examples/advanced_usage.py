"""
Advanced Usage Examples with Image Processing
"""

from enhanced_gemini_client import process_query
import os

def example_pest_detection():
    """Example of pest detection with image"""
    print("=== Pest Detection Example ===")

    # Note: Replace with actual image path
    image_path = "sample_images/pest_damage.jpg"
    query = "I found insects on my cotton plants. Can you identify them?"

    if os.path.exists(image_path):
        result = process_query(query, image=image_path)

        print(f"Query: {query}")
        print(f"Image: {image_path}")
        print(f"Module: {result['module']}")

        if 'detected_pests' in result and result['detected_pests']:
            for pest in result['detected_pests']:
                print(f"  Detected: {pest.get('pest_name', 'Unknown')} (Confidence: {pest.get('confidence', 0)}%)")
    else:
        print(f"⚠️  Image file not found: {image_path}")
        print("Please add sample images to test image-based functions")

def example_disease_detection():
    """Example of crop disease detection"""
    print("\n=== Disease Detection Example ===")

    image_path = "sample_images/diseased_leaves.jpg"
    query = "My tomato plants have yellow spots on leaves. What disease is this?"

    if os.path.exists(image_path):
        result = process_query(query, image=image_path)

        print(f"Query: {query}")
        print(f"Image: {image_path}")
        print(f"Module: {result['module']}")

        if 'disease_diagnosis' in result and result['disease_diagnosis']:
            for disease in result['disease_diagnosis']:
                print(f"  Diagnosed: {disease.get('disease_name', 'Unknown')} (Confidence: {disease.get('confidence', 0)}%)")
    else:
        print(f"⚠️  Image file not found: {image_path}")
        print("Please add sample images to test image-based functions")

if __name__ == "__main__":
    print("Enhanced Gemini Client - Advanced Examples")
    print("=" * 50)

    # Create sample images directory
    os.makedirs("sample_images", exist_ok=True)

    example_pest_detection()
    example_disease_detection()

    print("\n" + "=" * 50)
    print("Advanced examples completed!")
    print("\nTo test with real images:")
    print("1. Add pest/disease images to sample_images/ directory")
    print("2. Update image paths in the examples")
    print("3. Run this script again")
