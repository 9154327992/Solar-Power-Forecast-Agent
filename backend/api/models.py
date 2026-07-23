"""
Common API response models.
"""

from typing import Any, Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str


class HealthResponse(BaseModel):
    status: str
    server: str


class PredictionResult(BaseModel):
    prediction: float
    level: str
    efficiency: float
    recommendation: str


class APIResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None