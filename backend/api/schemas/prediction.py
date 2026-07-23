"""
Prediction Schemas
"""

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    city: str


class PredictionResponse(BaseModel):
    prediction: float
    level: str
    efficiency: float
    recommendation: str


class PredictionHistory(BaseModel):
    id: int
    city: str
    prediction: float
    created_at: str