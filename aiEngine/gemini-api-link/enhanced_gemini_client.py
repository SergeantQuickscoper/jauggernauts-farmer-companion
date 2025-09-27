import os
import json
import base64
from typing import Dict, List, Any, Optional, Union
from google import genai
import dotenv
from datetime import datetime
import logging

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini client
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is required")

client = genai.Client(api_key=api_key)

# === Step 1: Module descriptions ===
MODULES_DESCRIPTION = """
You are a classifier. Decide which advisory module to use for a farmer's query.

Modules:
1. yield_prediction - Return a list of yields from a list of crops.
2. pest_outbreak_risk - Predict pest outbreak risks for crops.
3. scheduling - Text-based input and recommending fertilizer, irrigation, harvesting, sowing schedules.
4. anomaly_detection - Detect anomalies in crop growth or farming activities.
5. pest_image_detection - Image-based pest detection and pesticide recommendation.
6. crop_disease - Image-based crop disease detection and fertilizer recommendation.
7. fallback_nlp - General chat or questions outside the above scope.

If the query contains an image of a pest, route it to pest_image_detection (inside PREDICTIVE_ADVISORY).
If the query contains an image of diseased crops, route it to crop_disease.
"""

# === Step 2: Import Schemas ===
try:
    from schema.response import Response
    from schema.activity import Activity
    from schema.unit import Unit
except ImportError as e:
    logger.warning(f"Schema import error: {e}. Using basic schemas.")

class FarmingAdvisor:
    """Main class for farming advisory system using Gemini AI"""

    def __init__(self):
        self.client = client
        self.current_session = {}

    def classify_and_extract(self, user_prompt: str, image: str = None) -> tuple:
        """
        Classify query → choose module → extract structured JSON.
        Supports text and optional image.
        """
        try:
            # First: classify into module
            router_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{MODULES_DESCRIPTION}\n\nFarmer Query: {user_prompt}",
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {"type": "object", "properties": {"module": {"type": "string"}}},
                },
            )

            chosen_module = router_response.parsed["module"]
            logger.info(f"Router chose module: {chosen_module}")

            # Route to appropriate function
            if chosen_module == "yield_prediction" or "yield" in chosen_module.lower():
                return self.yield_prediction(user_prompt)
            elif chosen_module == "pest_image_detection" or ("pest" in chosen_module.lower() and image):
                return self.pest_image_detection(user_prompt, image)
            elif chosen_module == "crop_disease" or ("disease" in chosen_module.lower() and image):
                return self.crop_disease(user_prompt, image)
            elif chosen_module == "fallback_nlp" or "fallback" in chosen_module.lower():
                return self.fallback_nlp(user_prompt)
            else:
                return self.fallback_nlp(user_prompt)

        except Exception as e:
            logger.error(f"Error in classify_and_extract: {e}")
            return self.fallback_nlp(user_prompt)

    def yield_prediction(self, user_prompt: str) -> Dict[str, Any]:
        """Function 1: Yield prediction for crops"""
        try:
            prediction_prompt = f"""
            You are an agricultural expert. Analyze the farmer's query and provide yield predictions.

            Farmer Query: {user_prompt}

            Extract the following information and provide yield predictions:
            - Crop types mentioned
            - Location/region if specified
            - Season/timing if mentioned
            - Area/acreage if specified

            Provide realistic yield predictions based on:
            - Crop type and variety
            - Regional averages
            - Seasonal factors
            - Best practices implementation
            """

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prediction_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "module": {"type": "string"},
                            "crops": {"type": "array", "items": {"type": "string"}},
                            "predictions": {"type": "array", "items": {
                                "type": "object", 
                                "properties": {
                                    "crop": {"type": "string"},
                                    "yield_estimate": {"type": "string"},
                                    "unit": {"type": "string"},
                                    "yield_range": {"type": "string"}
                                }
                            }},
                            "confidence_scores": {"type": "array", "items": {"type": "number"}},
                            "factors_considered": {"type": "array", "items": {"type": "string"}},
                            "recommendations": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            )

            result = response.parsed
            result["module"] = "yield_prediction"
            result["timestamp"] = datetime.now().isoformat()

            logger.info(f"Yield prediction completed for query: {user_prompt[:50]}...")
            return result

        except Exception as e:
            logger.error(f"Error in yield_prediction: {e}")
            return {
                "module": "yield_prediction",
                "error": str(e),
                "crops": [],
                "predictions": [],
                "confidence_scores": [],
                "timestamp": datetime.now().isoformat()
            }

    def pest_image_detection(self, user_prompt: str, image: str = None) -> Dict[str, Any]:
        """Function 5: Pest detection from images with pesticide recommendations"""
        try:
            if not image:
                return {
                    "module": "pest_image_detection",
                    "error": "Image is required for pest detection",
                    "timestamp": datetime.now().isoformat()
                }

            detection_prompt = f"""
            You are an expert entomologist and agricultural pest specialist. Analyze the provided image to detect pests.

            Farmer Query: {user_prompt}

            Analyze the image and identify:
            1. Any pests present in the image
            2. Pest species and characteristics
            3. Severity level of infestation
            4. Crop type being affected (if visible)
            5. Recommended pesticides and treatments
            6. Preventive measures
            7. Application timing and methods
            """

            contents = [detection_prompt]
            if image:
                if image.startswith('data:image'):
                    contents.append(image)
                elif os.path.exists(image):
                    with open(image, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                        contents.append(f"data:image/jpeg;base64,{img_data}")
                else:
                    contents.append(image)

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "module": {"type": "string"},
                            "detected_pests": {"type": "array", "items": {
                                "type": "object",
                                "properties": {
                                    "pest_name": {"type": "string"},
                                    "scientific_name": {"type": "string"},
                                    "confidence": {"type": "number"},
                                    "severity": {"type": "string"},
                                    "description": {"type": "string"}
                                }
                            }},
                            "crop_type": {"type": "string"},
                            "pesticide_recommendations": {"type": "array", "items": {
                                "type": "object",
                                "properties": {
                                    "pesticide_name": {"type": "string"},
                                    "active_ingredient": {"type": "string"},
                                    "application_rate": {"type": "string"},
                                    "application_method": {"type": "string"},
                                    "safety_notes": {"type": "string"}
                                }
                            }},
                            "preventive_measures": {"type": "array", "items": {"type": "string"}},
                            "treatment_urgency": {"type": "string"},
                            "estimated_damage": {"type": "string"}
                        }
                    }
                }
            )

            result = response.parsed
            result["module"] = "pest_image_detection"
            result["timestamp"] = datetime.now().isoformat()

            logger.info("Pest image detection completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in pest_image_detection: {e}")
            return {
                "module": "pest_image_detection",
                "error": str(e),
                "detected_pests": [],
                "pesticide_recommendations": [],
                "timestamp": datetime.now().isoformat()
            }

    def crop_disease(self, user_prompt: str, image: str = None) -> Dict[str, Any]:
        """Function 6: Crop disease detection from images with treatment recommendations"""
        try:
            if not image:
                return {
                    "module": "crop_disease",
                    "error": "Image is required for disease detection",
                    "timestamp": datetime.now().isoformat()
                }

            disease_prompt = f"""
            You are an expert plant pathologist and agricultural disease specialist. Analyze the provided image to detect crop diseases.

            Farmer Query: {user_prompt}

            Analyze the image and identify:
            1. Any diseases present in the crop
            2. Disease type and pathogen (fungal, bacterial, viral, etc.)
            3. Severity and progression stage
            4. Crop type and affected parts
            5. Environmental factors that may contribute
            6. Treatment recommendations (fungicides, bactericides, etc.)
            7. Preventive measures and management practices
            8. Expected recovery timeline
            """

            contents = [disease_prompt]
            if image:
                if image.startswith('data:image'):
                    contents.append(image)
                elif os.path.exists(image):
                    with open(image, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                        contents.append(f"data:image/jpeg;base64,{img_data}")
                else:
                    contents.append(image)

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "module": {"type": "string"},
                            "disease_diagnosis": {"type": "array", "items": {
                                "type": "object",
                                "properties": {
                                    "disease_name": {"type": "string"},
                                    "pathogen_type": {"type": "string"},
                                    "confidence": {"type": "number"},
                                    "severity": {"type": "string"},
                                    "affected_parts": {"type": "array", "items": {"type": "string"}},
                                    "symptoms": {"type": "array", "items": {"type": "string"}}
                                }
                            }},
                            "crop_type": {"type": "string"},
                            "treatment_recommendations": {"type": "array", "items": {
                                "type": "object",
                                "properties": {
                                    "treatment_type": {"type": "string"},
                                    "product_name": {"type": "string"},
                                    "active_ingredient": {"type": "string"},
                                    "application_rate": {"type": "string"},
                                    "frequency": {"type": "string"},
                                    "timing": {"type": "string"}
                                }
                            }},
                            "cultural_practices": {"type": "array", "items": {"type": "string"}},
                            "prevention_strategies": {"type": "array", "items": {"type": "string"}},
                            "prognosis": {"type": "string"},
                            "estimated_yield_impact": {"type": "string"}
                        }
                    }
                }
            )

            result = response.parsed
            result["module"] = "crop_disease"
            result["timestamp"] = datetime.now().isoformat()

            logger.info("Crop disease detection completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error in crop_disease: {e}")
            return {
                "module": "crop_disease",
                "error": str(e),
                "disease_diagnosis": [],
                "treatment_recommendations": [],
                "timestamp": datetime.now().isoformat()
            }

    def fallback_nlp(self, user_prompt: str) -> Dict[str, Any]:
        """Function 7: Fallback NLP for general agricultural queries and chat"""
        try:
            fallback_prompt = f"""
            You are a knowledgeable agricultural assistant. The farmer's query doesn't fit into specific categories 
            like yield prediction, pest detection, or disease diagnosis, so provide general agricultural guidance.

            Farmer Query: {user_prompt}

            Provide helpful information about:
            - General farming practices
            - Agricultural advice and tips
            - Resource recommendations
            - Educational information
            - Answers to farming-related questions

            If the query is completely outside agricultural scope, politely redirect to farming topics while
            still being helpful. Always maintain a supportive and knowledgeable tone.
            """

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=fallback_prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "module": {"type": "string"},
                            "response": {"type": "string"},
                            "category": {"type": "string"},
                            "confidence": {"type": "number"},
                            "suggestions": {"type": "array", "items": {"type": "string"}},
                            "related_topics": {"type": "array", "items": {"type": "string"}},
                            "resources": {"type": "array", "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "type": {"type": "string"}
                                }
                            }},
                            "follow_up_questions": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            )

            result = response.parsed
            result["module"] = "fallback_nlp"
            result["timestamp"] = datetime.now().isoformat()

            logger.info(f"Fallback NLP response generated for query: {user_prompt[:50]}...")
            return result

        except Exception as e:
            logger.error(f"Error in fallback_nlp: {e}")
            return {
                "module": "fallback_nlp",
                "response": f"I apologize, but I encountered an error processing your request: {str(e)}. Could you please rephrase your question?",
                "error": str(e),
                "confidence": 0.0,
                "suggestions": ["Try rephrasing your question", "Check if all required information is provided"],
                "timestamp": datetime.now().isoformat()
            }

    def process_farmer_query(self, query: str, image: str = None, farmer_id: str = None) -> Dict[str, Any]:
        """Main method to process any farmer query"""
        try:
            logger.info(f"Processing query from farmer {farmer_id}: {query[:100]}...")

            if farmer_id:
                self.current_session["farmer_id"] = farmer_id
            self.current_session["last_query"] = query
            self.current_session["timestamp"] = datetime.now().isoformat()

            result = self.classify_and_extract(query, image)
            result["session_info"] = self.current_session.copy()

            return result

        except Exception as e:
            logger.error(f"Error in process_farmer_query: {e}")
            return {
                "module": "error",
                "error": str(e),
                "message": "An error occurred while processing your request.",
                "timestamp": datetime.now().isoformat()
            }

# Create global instance
farming_advisor = FarmingAdvisor()

# === Main Functions for External Use ===
def classify_and_extract(user_prompt: str, image: str = None):
    """Legacy function for backward compatibility"""
    return farming_advisor.classify_and_extract(user_prompt, image)

def process_query(query: str, image: str = None, farmer_id: str = None):
    """Main function to process farmer queries"""
    return farming_advisor.process_farmer_query(query, image, farmer_id)

# === Example usage ===
if __name__ == "__main__":
    print("=== Gemini Farming Advisory System ===")
    print("Available modules: yield_prediction, pest_image_detection, crop_disease, fallback_nlp")
    print()

    while True:
        try:
            query = input("Farmer query (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break

            image_path = input("Image path (optional, press Enter to skip): ").strip()
            if not image_path:
                image_path = None

            result = process_query(query, image_path)

            print("\n=== Result ===")
            print(json.dumps(result, indent=2, default=str))
            print("\n" + "="*50 + "\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
