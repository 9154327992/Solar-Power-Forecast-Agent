from fastapi import APIRouter
from pydantic import BaseModel
import requests
import re
from typing import Optional, Any

router = APIRouter()


# ==========================================================
# Configuration
# ==========================================================

API_BASE_URL = "https://solar-power-forecast-agent.onrender.com"
REQUEST_TIMEOUT = 10


# ==========================================================
# Request Model
# ==========================================================

class AssistantRequest(BaseModel):
    question: str


# ==========================================================
# Text Utilities
# ==========================================================

def clean_text(text: str) -> str:
    """Normalize the user's question."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text: str, phrases: list[str]) -> bool:
    """
    Detect complete words or phrases without substring mistakes.

    This prevents:
        'hi' from matching 'high'
    """
    for phrase in phrases:
        pattern = rf"\b{re.escape(phrase.lower())}\b"

        if re.search(pattern, text):
            return True

    return False


def is_greeting(text: str) -> bool:
    """Detect greetings without confusing 'high' with 'hi'."""

    greetings = {
        "hi",
        "hello",
        "hey",
        "hi!",
        "hello!",
        "hey!",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if text in greetings:
        return True

    return (
        text.startswith("hi ")
        or text.startswith("hello ")
        or text.startswith("hey ")
        or text.startswith("good morning ")
        or text.startswith("good afternoon ")
        or text.startswith("good evening ")
    )


# ==========================================================
# Backend Data
# ==========================================================

def safe_get(url: str) -> Optional[Any]:
    """Safely request JSON data from the backend."""

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response.json()

    except Exception:
        pass

    return None


def get_history() -> Optional[Any]:
    return safe_get(
        f"{API_BASE_URL}/api/history"
    )


def get_weather() -> Optional[Any]:
    """
    Try the available weather endpoints.
    """

    urls = [
        f"{API_BASE_URL}/api/weather",
        f"{API_BASE_URL}/api/weather/current",
    ]

    for url in urls:

        data = safe_get(url)

        if data is not None:
            return data

    return None


def extract_records(data: Any) -> list:
    """Extract list records from common API response formats."""

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        for key in [
            "history",
            "data",
            "records",
            "predictions",
            "results"
        ]:

            value = data.get(key)

            if isinstance(value, list):
                return value

    return []


def extract_prediction(history: Any) -> Optional[float]:
    """Extract latest prediction."""

    records = extract_records(history)

    if not records:
        return None

    latest = records[-1]

    if not isinstance(latest, dict):
        return None

    possible_keys = [
        "prediction",
        "predicted_power",
        "solar_power",
        "power",
        "value"
    ]

    for key in possible_keys:

        value = latest.get(key)

        if value is None:
            continue

        try:
            return float(value)

        except (TypeError, ValueError):
            continue

    return None


def extract_weather_value(
    weather: Any,
    keys: list[str]
) -> Optional[Any]:
    """Extract weather values from common response structures."""

    if weather is None:
        return None

    objects = []

    if isinstance(weather, dict):

        objects.append(weather)

        for key in [
            "weather",
            "current",
            "data",
            "result"
        ]:

            value = weather.get(key)

            if isinstance(value, dict):
                objects.append(value)

    for obj in objects:

        for key in keys:

            if key in obj:
                return obj[key]

    return None


def get_current_data() -> dict:
    """Collect available prediction and weather information."""

    history = get_history()
    weather = get_weather()

    return {
        "prediction": extract_prediction(history),

        "temperature": extract_weather_value(
            weather,
            [
                "temperature",
                "temp",
                "air_temperature"
            ]
        ),

        "humidity": extract_weather_value(
            weather,
            [
                "humidity",
                "relative_humidity"
            ]
        ),

        "pressure": extract_weather_value(
            weather,
            [
                "pressure",
                "air_pressure"
            ]
        ),

        "wind": extract_weather_value(
            weather,
            [
                "wind_speed",
                "wind"
            ]
        ),

        "clouds": extract_weather_value(
            weather,
            [
                "cloud_cover",
                "clouds",
                "cloud"
            ]
        ),

        "radiation": extract_weather_value(
            weather,
            [
                "solar_radiation",
                "radiation"
            ]
        ),

        "sunshine": extract_weather_value(
            weather,
            [
                "sunshine_duration",
                "sunshine"
            ]
        )
    }


# ==========================================================
# Prediction Level
# ==========================================================

def prediction_level(value: float) -> str:

    if value >= 6:
        return "High"

    if value >= 3:
        return "Moderate"

    return "Low"


# ==========================================================
# Forecast Answer
# ==========================================================

def forecast_answer(data: dict) -> str:

    prediction = data.get("prediction")
    temperature = data.get("temperature")
    clouds = data.get("clouds")
    radiation = data.get("radiation")
    sunshine = data.get("sunshine")

    response = "☀️ **Solar Generation Forecast**\n\n"

    if prediction is not None:

        level = prediction_level(prediction)

        response += (
            f"**Latest available prediction:** "
            f"{prediction:.2f} kW ({level})\n\n"
        )

    else:

        response += (
            "The current solar prediction is not available "
            "from the backend right now.\n\n"
        )

    if radiation is not None:
        response += f"☀️ Solar radiation: **{radiation}**\n\n"

    if sunshine is not None:
        response += f"🌞 Sunshine duration: **{sunshine}**\n\n"

    if clouds is not None:
        response += f"☁️ Cloud cover: **{clouds}**\n\n"

    if temperature is not None:
        response += f"🌡️ Temperature: **{temperature}**\n\n"

    response += (
        "Solar generation is influenced by solar radiation, "
        "sunshine duration, cloud conditions, temperature, "
        "humidity, wind, and time of day.\n\n"
        "The application uses an **XGBoost forecasting model** "
        "to estimate solar power generation."
    )

    return response


# ==========================================================
# Weather Answer
# ==========================================================

def weather_answer(data: dict) -> str:

    response = "🌤️ **Current Weather Information**\n\n"

    found = False

    values = [
        ("🌡️ Temperature", data.get("temperature")),
        ("💧 Humidity", data.get("humidity")),
        ("🧭 Pressure", data.get("pressure")),
        ("💨 Wind", data.get("wind")),
        ("☁️ Cloud cover", data.get("clouds")),
        ("☀️ Solar radiation", data.get("radiation")),
    ]

    for label, value in values:

        if value is not None:

            response += f"{label}: **{value}**\n\n"
            found = True

    if not found:

        return (
            "🌤️ I couldn't retrieve the current weather "
            "data from the backend right now.\n\n"
            "Please check the **Live Weather** page for "
            "the latest weather information."
        )

    response += (
        "These weather conditions can directly affect "
        "solar power generation."
    )

    return response


# ==========================================================
# Battery Answer
# ==========================================================

def battery_answer(data: dict) -> str:

    prediction = data.get("prediction")

    if prediction is not None:

        level = prediction_level(prediction)

        if level == "High":

            return (
                "🔋 **Battery Recommendation**\n\n"
                f"The latest available solar prediction is "
                f"**{prediction:.2f} kW ({level})**.\n\n"
                "This indicates strong generation conditions. "
                "If your battery needs charging, this can be "
                "a suitable period to prioritize charging.\n\n"
                "For this application, the suggested daytime "
                "window is approximately **10 AM–3 PM**."
            )

        if level == "Moderate":

            return (
                "🔋 **Battery Recommendation**\n\n"
                f"The latest available solar prediction is "
                f"**{prediction:.2f} kW ({level})**.\n\n"
                "Battery charging may be reasonable, but "
                "available solar generation should be monitored."
            )

        return (
            "🔋 **Battery Recommendation**\n\n"
            f"The latest available solar prediction is "
            f"**{prediction:.2f} kW ({level})**.\n\n"
            "Solar generation is currently relatively low. "
            "If possible, consider waiting for stronger "
            "generation before prioritizing battery charging."
        )

    return (
        "🔋 **Battery Recommendation**\n\n"
        "Battery charging is generally most effective when "
        "solar generation is strong.\n\n"
        "For this application, the suggested daytime window "
        "is approximately **10 AM–3 PM**.\n\n"
        "The current prediction is unavailable, so check the "
        "**Solar Forecast** page for the latest value."
    )


# ==========================================================
# Appliance Answer
# ==========================================================

def appliance_answer(data: dict) -> str:

    prediction = data.get("prediction")

    if prediction is not None:

        level = prediction_level(prediction)

        if level == "High":

            return (
                "⚡ **Appliance Recommendation**\n\n"
                f"The latest solar prediction is "
                f"**{prediction:.2f} kW ({level})**.\n\n"
                "This indicates favorable generation conditions "
                "for flexible high-power appliances such as "
                "washing machines, water pumps, and EV charging.\n\n"
                "If possible, use these appliances while solar "
                "generation is strong."
            )

        return (
            "⚡ **Appliance Recommendation**\n\n"
            f"The latest solar prediction is "
            f"**{prediction:.2f} kW ({level})**.\n\n"
            "Consider delaying flexible high-power appliances "
            "until solar generation becomes stronger."
        )

    return (
        "⚡ **Appliance Scheduling**\n\n"
        "High-power appliances such as washing machines, "
        "water pumps, and EV chargers are generally better "
        "scheduled during strong solar generation.\n\n"
        "For this application, the suggested daytime window "
        "is approximately **10 AM–3 PM**."
    )


# ==========================================================
# Energy Saving
# ==========================================================

def energy_saving_answer() -> str:

    return (
        "💡 **Energy-Saving Recommendations**\n\n"
        "1. Use high-power appliances when solar generation "
        "is strong.\n\n"
        "2. Reduce unnecessary standby power consumption.\n\n"
        "3. Use stored battery energy when solar generation "
        "is low.\n\n"
        "4. Keep solar panels clean and free from unnecessary "
        "obstructions.\n\n"
        "5. Monitor your historical solar generation.\n\n"
        "6. Shift flexible electricity consumption toward "
        "strong daytime solar production.\n\n"
        "7. Avoid using several high-power appliances "
        "simultaneously when solar generation is low."
    )


# ==========================================================
# Maintenance
# ==========================================================

def maintenance_answer() -> str:

    return (
        "🔧 **Solar Panel Maintenance**\n\n"
        "Regular maintenance helps keep a solar system "
        "operating effectively.\n\n"
        "• Keep panels reasonably clean.\n"
        "• Remove dust, leaves, and visible obstructions.\n"
        "• Check for unnecessary shading.\n"
        "• Monitor changes in solar generation.\n"
        "• Look for unusual drops in output.\n"
        "• Check the system for visible damage.\n\n"
        "For electrical or physical faults, use qualified "
        "professional inspection."
    )


# ==========================================================
# ML Answer
# ==========================================================

def ml_answer() -> str:

    return (
        "🤖 **Machine Learning Model**\n\n"
        "The Solar Power Forecast Agent uses an "
        "**XGBoost Regressor** for solar power forecasting.\n\n"
        "The forecasting features include:\n\n"
        "• Wind speed\n"
        "• Sunshine duration\n"
        "• Air pressure\n"
        "• Solar radiation\n"
        "• Air temperature\n"
        "• Relative humidity\n"
        "• Hour\n"
        "• Day\n"
        "• Month\n\n"
        "The model learns relationships between these "
        "weather/time features and solar power generation "
        "to produce a forecast."
    )


# ==========================================================
# Solar Panel Efficiency
# ==========================================================

def efficiency_answer() -> str:

    return (
        "⚡ **Solar Panel Efficiency**\n\n"
        "Solar panel performance can be affected by several "
        "conditions:\n\n"
        "☀️ **Solar radiation:** More available sunlight "
        "generally provides more energy.\n\n"
        "🌡️ **Temperature:** Panel electrical performance "
        "can change as temperature increases.\n\n"
        "☁️ **Cloud cover:** Clouds reduce the sunlight "
        "reaching the panels.\n\n"
        "🧹 **Dust and dirt:** Surface contamination can "
        "reduce the available sunlight.\n\n"
        "🌳 **Shading:** Trees, buildings, and other "
        "obstructions can reduce output.\n\n"
        "Regular monitoring can help identify unusual "
        "performance changes."
    )


# ==========================================================
# Cloudy Weather
# ==========================================================

def cloudy_answer() -> str:

    return (
        "☁️ **Cloudy Weather and Solar Generation**\n\n"
        "Cloud cover generally reduces the amount of direct "
        "sunlight reaching solar panels.\n\n"
        "Solar panels can still generate electricity under "
        "cloudy conditions because some diffuse sunlight "
        "reaches the panels, but output is usually lower "
        "than under strong clear-sky conditions."
    )


# ==========================================================
# Solar Radiation
# ==========================================================

def radiation_answer() -> str:

    return (
        "☀️ **Solar Radiation**\n\n"
        "Solar radiation is the sunlight energy reaching "
        "the Earth's surface and is an important factor "
        "in solar power generation.\n\n"
        "Higher available solar radiation generally provides "
        "better conditions for photovoltaic electricity "
        "generation.\n\n"
        "Your forecasting system uses solar radiation as "
        "one of its model features."
    )


# ==========================================================
# Humidity
# ==========================================================

def humidity_answer() -> str:

    return (
        "💧 **Humidity and Solar Generation**\n\n"
        "Humidity describes the amount of water vapor in "
        "the atmosphere.\n\n"
        "It can be useful as a weather feature because "
        "atmospheric conditions often occur together with "
        "clouds, haze, and other factors that influence "
        "the sunlight reaching solar panels.\n\n"
        "Your XGBoost model uses relative humidity as one "
        "of its forecasting features."
    )


# ==========================================================
# Temperature
# ==========================================================

def temperature_answer() -> str:

    return (
        "🌡️ **Temperature and Solar Panels**\n\n"
        "Temperature is one of the weather variables used "
        "by your forecasting model.\n\n"
        "Solar panel electrical characteristics can change "
        "with temperature, so temperature can be useful "
        "when estimating solar generation.\n\n"
        "The model combines temperature with other features "
        "rather than relying on temperature alone."
    )


# ==========================================================
# General Solar Answer
# ==========================================================

def solar_answer() -> str:

    return (
        "☀️ **Solar Energy**\n\n"
        "Solar photovoltaic systems convert sunlight into "
        "electrical energy.\n\n"
        "Solar generation varies according to conditions "
        "such as:\n\n"
        "• Solar radiation\n"
        "• Sunshine duration\n"
        "• Cloud cover\n"
        "• Temperature\n"
        "• Humidity\n"
        "• Wind conditions\n"
        "• Time of day\n\n"
        "Your Solar Power Forecast Agent uses these types "
        "of weather and time features with an XGBoost "
        "model to estimate solar power generation."
    )


# ==========================================================
# Project Answer
# ==========================================================

def project_answer() -> str:

    return (
        "☀️ **Solar Power Forecast Agent**\n\n"
        "This application is designed to forecast solar "
        "power generation and provide energy recommendations.\n\n"
        "**Main features:**\n\n"
        "• Solar power forecasting\n"
        "• Live weather integration\n"
        "• AI Energy Assistant\n"
        "• Prediction history\n"
        "• Analytics dashboard\n"
        "• Battery recommendations\n"
        "• Appliance scheduling\n"
        "• Energy-saving advice\n"
        "• Solar panel maintenance guidance\n"
        "• Daily reports\n"
        "• Admin dashboard\n\n"
        "The forecasting model uses XGBoost."
    )


# ==========================================================
# Daily Report
# ==========================================================

def daily_report_answer(data: dict) -> str:

    prediction = data.get("prediction")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    clouds = data.get("clouds")
    radiation = data.get("radiation")

    response = "📊 **Daily Solar Energy Report**\n\n"

    if prediction is not None:

        level = prediction_level(prediction)

        response += (
            f"☀️ **Solar Prediction:** "
            f"{prediction:.2f} kW ({level})\n\n"
        )

    else:

        response += (
            "☀️ **Solar Prediction:** "
            "Current prediction unavailable\n\n"
        )

    if temperature is not None:
        response += f"🌡️ **Temperature:** {temperature}\n\n"

    if humidity is not None:
        response += f"💧 **Humidity:** {humidity}\n\n"

    if clouds is not None:
        response += f"☁️ **Cloud Cover:** {clouds}\n\n"

    if radiation is not None:
        response += f"☀️ **Solar Radiation:** {radiation}\n\n"

    response += (
        "🔋 **Battery:** Prioritize charging when solar "
        "generation is strong.\n\n"
        "⚡ **Appliances:** Schedule flexible high-power "
        "loads during stronger daytime generation.\n\n"
        "💡 **Energy Saving:** Reduce standby consumption "
        "and maximize direct solar usage."
    )

    return response


# ==========================================================
# Main Assistant
# ==========================================================

def generate_answer(question: str) -> str:

    q = clean_text(question)

    # ------------------------------------------------------
    # Greeting
    # ------------------------------------------------------

    if is_greeting(q):

        return (
            "Hello! ☀️ I'm your Solar Energy Assistant.\n\n"
            "You can ask me any question about solar energy, "
            "weather, batteries, appliances, maintenance, "
            "energy saving, or the forecasting model.\n\n"
            "You are not limited to the quick questions above."
        )

    # ------------------------------------------------------
    # Thanks
    # ------------------------------------------------------

    if contains_any(
        q,
        ["thank", "thanks", "thank you"]
    ):

        return (
            "You're welcome! ☀️\n\n"
            "Feel free to ask another solar or energy question."
        )

    # ------------------------------------------------------
    # ML / XGBoost
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "xgboost",
            "machine learning",
            "ml model",
            "machine model",
            "model",
            "algorithm",
            "how does the model work"
        ]
    ):

        return ml_answer()

    # ------------------------------------------------------
    # Efficiency
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "efficiency",
            "panel efficiency",
            "improve efficiency",
            "performance",
            "improve solar",
            "improve generation"
        ]
    ):

        return efficiency_answer()

    # ------------------------------------------------------
    # Cloudy / cloudy day
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "cloudy",
            "cloudy day",
            "cloudy weather",
            "cloud cover",
            "clouds"
        ]
    ):

        return cloudy_answer()

    # ------------------------------------------------------
    # Solar Radiation
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "solar radiation",
            "radiation"
        ]
    ):

        return radiation_answer()

    # ------------------------------------------------------
    # Humidity
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "humidity",
            "relative humidity"
        ]
    ):

        return humidity_answer()

    # ------------------------------------------------------
    # Temperature
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "temperature",
            "hot weather",
            "heat"
        ]
    ):

        return temperature_answer()

    # ------------------------------------------------------
    # Battery
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "battery",
            "charge battery",
            "charging battery",
            "battery charging",
            "store energy"
        ]
    ):

        return battery_answer(
            get_current_data()
        )

    # ------------------------------------------------------
    # Appliances
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "washing machine",
            "washing machines",
            "water pump",
            "water pumps",
            "ev charger",
            "ev charging",
            "heavy appliance",
            "heavy appliances",
            "run appliance",
            "run appliances",
            "high power appliance",
            "high power appliances"
        ]
    ):

        return appliance_answer(
            get_current_data()
        )

    # ------------------------------------------------------
    # Forecast
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "forecast",
            "solar generation",
            "solar output",
            "power generation",
            "generation today",
            "solar power today",
            "will solar",
            "how much solar",
            "high today",
            "low today"
        ]
    ):

        return forecast_answer(
            get_current_data()
        )

    # ------------------------------------------------------
    # Weather
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "weather",
            "current weather",
            "weather today"
        ]
    ):

        return weather_answer(
            get_current_data()
        )

    # ------------------------------------------------------
    # Energy Saving
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "energy saving",
            "save energy",
            "save electricity",
            "saving electricity",
            "reduce electricity",
            "reduce power",
            "electricity bill",
            "energy consumption",
            "save power"
        ]
    ):

        return energy_saving_answer()

    # ------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "maintenance",
            "maintain",
            "clean panel",
            "clean panels",
            "panel cleaning",
            "panel care",
            "solar panel maintenance"
        ]
    ):

        return maintenance_answer()

    # ------------------------------------------------------
    # Daily Report
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "daily report",
            "today report",
            "solar report",
            "energy report",
            "generate report",
            "report"
        ]
    ):

        return daily_report_answer(
            get_current_data()
        )

    # ------------------------------------------------------
    # Project
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "what is this project",
            "what does this project do",
            "about this project",
            "project features",
            "what can you do",
            "your capabilities"
        ]
    ):

        return project_answer()

    # ------------------------------------------------------
    # General Solar
    # ------------------------------------------------------

    if contains_any(
        q,
        [
            "solar",
            "photovoltaic",
            "photovoltaics",
            "pv panels",
            "pv system",
            "sunlight",
            "sun"
        ]
    ):

        return solar_answer()

    # ------------------------------------------------------
    # Unknown
    # ------------------------------------------------------

    return (
        "☀️ I can help with a wide range of solar-energy "
        "questions.\n\n"
        "Try asking me about:\n\n"
        "• Solar forecasting\n"
        "• Weather\n"
        "• Solar radiation\n"
        "• Temperature\n"
        "• Humidity\n"
        "• Cloudy conditions\n"
        "• Battery charging\n"
        "• Appliance scheduling\n"
        "• Energy saving\n"
        "• Solar panel efficiency\n"
        "• Maintenance\n"
        "• XGBoost / machine learning\n"
        "• Daily reports\n\n"
        "You don't have to use one of the six quick questions."
    )


# ==========================================================
# API Endpoint
# ==========================================================

@router.post("/ai-assistant")
def ai_assistant(request: AssistantRequest):

    answer = generate_answer(
        request.question
    )

    return {
        "response": answer
    }
