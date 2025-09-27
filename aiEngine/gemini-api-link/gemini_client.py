import os
from google import genai
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

# === Step 1: Module descriptions ===
MODULES_DESCRIPTION = """
You are a classifier. Decide which advisory module to use for a farmer's query.

Modules:
1. yield_prediction - Return a list of yields from a list of crops.
2. pest_outbreak_risk
3. scheduling - Text-based input and recommending fertilizer, irrigation, harvesting, sowing schedules.
4. anomaly_detection -
5. pest_image_detection - Image-based pest detection and pesticide recommendation.
6. crop_disease - Image-based crop disease detection and fertilizer recommendation.
7. fallback_nlp - General chat or questions outside the above scope.

If the query contains an image of a pest, route it to pest_image_detection (inside PREDICTIVE_ADVISORY).
"""

# === Step 2: Schemas ===
import schema.response # router schema → { "module": str }
import schema.predictive # predictive schema → includes "sub_model"

def classify_and_extract(user_prompt: str, image: str = None) -> tuple:
    """
    Classify query → choose module → extract structured JSON.
    Supports text and optional image.
    """

    # First: classify into module
    router_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{MODULES_DESCRIPTION}\n\nFarmer Query: {user_prompt}",
        config={
            "response_mime_type": "application/json",
            "response_schema": schema.response, # → { "module": str }
        },
    )

    chosen_module = router_response.parsed["module"]
    print(f"Router chose module: {chosen_module}")

    # TODO: Implement individual functions for modules 1, 5, 6, 7

    return chosen_module, {}
