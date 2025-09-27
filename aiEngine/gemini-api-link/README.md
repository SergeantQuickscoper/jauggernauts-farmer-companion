# Enhanced Gemini Client for Agricultural Advisory

## Overview
This enhanced version of `gemini_client.py` implements four key functions for agricultural advisory services using Google's Gemini AI:

1. **yield_prediction** - Predicts crop yields based on farmer inputs
5. **pest_image_detection** - Detects pests from images and recommends pesticides
6. **crop_disease** - Detects crop diseases from images and suggests treatments  
7. **fallback_nlp** - Handles general agricultural queries and chat

## Project Structure
```
gemini-api-link/
├── gemini_client.py              # Original client
├── enhanced_gemini_client.py     # Enhanced version with 4 functions
├── models/                       # Empty models folder
├── schema/                       # Schema definitions
│   ├── activity.py               # Activity data model
│   ├── unit.py                   # Units enumeration
│   └── response.py               # Basic response schema
├── examples/                     # Usage examples
├── tests/                        # Test files
└── docs/                         # Documentation
```

## Installation

1. Install required dependencies:
```bash
pip install google-generativeai python-dotenv pydantic
```

2. Set up environment variables:
```bash
echo "API_KEY=your_gemini_api_key" > .env
```

## Usage

### Basic Usage
```python
from enhanced_gemini_client import process_query

# Text-only query
result = process_query("How to increase crop yield?")

# Query with image
result = process_query("Identify this pest", image="pest_image.jpg")

# Query with farmer ID for session management
result = process_query("What fertilizer should I use?", farmer_id="F12345")
```

## Features

### 1. Yield Prediction (Function 1)
- Predicts crop yields based on crop type, location, season
- Provides confidence scores and yield ranges
- Includes factors considered and recommendations
- Supports multiple crops in single query

### 2. Pest Image Detection (Function 5)
- Analyzes images to detect pests
- Identifies pest species with confidence scores
- Provides pesticide recommendations
- Includes application methods and safety notes

### 3. Crop Disease Detection (Function 6)
- Detects diseases from crop images
- Identifies pathogen types and severity
- Suggests treatments and cultural practices
- Estimates yield impact and recovery time

### 4. Fallback NLP (Function 7)
- Handles general agricultural questions
- Provides educational information
- Offers practical suggestions
- Maintains conversational context

## Response Format

All functions return structured JSON responses with:

```json
{
  "module": "function_name",
  "timestamp": "2024-01-01T12:00:00",
  "session_info": {...},
  "confidence": 0.95,
  "recommendations": [...],
  "error": null
}
```

## Error Handling

The system includes comprehensive error handling:
- Missing image validation for image-based functions
- API error handling and retries
- Graceful degradation to fallback responses
- Detailed error logging

## License

This project is part of the agricultural advisory system.
