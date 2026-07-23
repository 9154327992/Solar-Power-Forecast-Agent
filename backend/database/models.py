# ============================================================
# models.py
# Pydantic Models
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================================
# Weather Input Model
# ============================================================

class WeatherInput(BaseModel):

    temperature: float = Field(..., gt=-50, lt=60)

    humidity: float = Field(..., ge=0, le=100)

    pressure: float = Field(..., gt=800, lt=1200)

    wind_speed: float = Field(..., ge=0)

    cloud_cover: float = Field(..., ge=0, le=100)


# ============================================================
# Prediction Response
# ============================================================

class PredictionResponse(BaseModel):

    prediction: float

    efficiency: float

    level: str

    recommendation: str

    insight: str


# ============================================================
# Prediction Record
# ============================================================

class PredictionRecord(BaseModel):

    id: Optional[int] = None

    timestamp: str

    temperature: float

    humidity: float

    pressure: float

    wind_speed: float

    cloud_cover: float

    prediction: float

    efficiency: float

    generation_level: str


# ============================================================
# AI Chat Request
# ============================================================

class ChatRequest(BaseModel):

    message: str


# ============================================================
# AI Chat Response
# ============================================================

class ChatResponse(BaseModel):

    response: str


# ============================================================
# Weather Response
# ============================================================

class WeatherResponse(BaseModel):

    city: str

    temperature: float

    humidity: float

    pressure: float

    wind_speed: float

    cloud_cover: float

    description: str


# ============================================================
# History Response
# ============================================================

class HistoryResponse(BaseModel):

    history: List[PredictionRecord]


# ============================================================
# Database Statistics
# ============================================================

class DatabaseStatistics(BaseModel):

    total_predictions: int

    average_prediction: float


# ============================================================
# Health Check
# ============================================================

class HealthResponse(BaseModel):

    status: str

    model_loaded: bool

    database_connected: bool