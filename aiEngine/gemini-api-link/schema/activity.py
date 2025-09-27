"""
"activity_id": "A567",
"farmer_id" : "F123",
"crop": "Rice",
"action_type": "Irrigation", // irrigation, sowing, fertilizer, pesticide, harvest
"amount": "NA", // e.g., 20kg fertilizer OR NA for irrigation
"unit": "litres/kg/NA", // optional (helps in fertilizers/pesticides)
"date": "2025-09-27"
"location": "Field 1", // optional, if farmer has multiple plots(will not be used in making the prototype)
"""

from .unit import Unit
import pydantic

class Activity(pydantic.BaseModel):
    activity_id: str
    farmer_id: str
    crop: str
    action_type: str
    amount: str
    unit: Unit
    date: str
