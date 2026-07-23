"""
API Schemas Package
"""

from .auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)

from .prediction import (
    PredictionRequest,
    PredictionResponse,
)

from .weather import (
    WeatherRequest,
    WeatherResponse,
    ForecastResponse,
)