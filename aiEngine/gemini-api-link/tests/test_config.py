"""
Test Configuration and Utilities
"""

import os
import tempfile

# Test data
SAMPLE_QUERIES = {
    "yield_prediction": [
        "What will be the yield of rice in Punjab?",
        "Predict wheat yield for winter season",
        "Expected yield of sugarcane in 5-acre farm"
    ],
    "pest_detection": [
        "Found insects on my cotton plants",
        "Small holes in cabbage leaves",
        "Aphids on tomato plants"
    ],
    "disease_detection": [
        "Yellow spots on tomato leaves",
        "Brown lesions on rice plants",
        "Wilting in potato plants"
    ],
    "general_chat": [
        "What are organic farming practices?",
        "How to improve soil health?",
        "Best time to plant vegetables?"
    ]
}

def create_test_image():
    """Create a test image for testing purposes"""
    try:
        from PIL import Image
        import io

        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='green')

        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        img.save(temp_file.name, 'JPEG')

        return temp_file.name
    except ImportError:
        return None

def cleanup_test_files():
    """Clean up temporary test files"""
    # Add cleanup logic here
    pass
