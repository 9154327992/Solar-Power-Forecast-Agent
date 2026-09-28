from fastapi import APIRouter
from pydantic import BaseModel
import requests
import re
from typing import Any, Optional

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
# Utility Functions
# ==========================================================

def clean_text(text: str) -> str:
    """Normalize user input."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def contains_any(text: str, words: list[str]) -> bool:
    """Check whether any complete word/phrase exists."""
    return any(
        re.search(rf"\b{re.escape(word)}\b", text)
        for word in words
    )


def is_greeting(text: str) -> bool:
    """
    Prevent the 'hi' inside 'high' bug.
    """
    text = text.strip()

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
# Backend Data Helpers
# ==========================================================

def get_history() -> Optional[Any]:
    """
    Try to retrieve prediction history from the backend.
    Returns None if the endpoint is unavailable.
    """

    try:
        response = requests.get(
            f"{API_BASE_URL}/api/history",
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response.json()

    except Exception:
        pass

    return None


def get_weather() -> Optional[Any]:
    """
    Try to retrieve live weather from the backend.

    The weather router may have different response structures,
    so this function safely handles unavailable data.
    """

    possible_urls = [
        f"{API_BASE_URL}/api/weather",
        f"{API_BASE_URL}/api/weather/current",
    ]

    for url in possible_urls:

        try:
            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                return response.json()

        except Exception:
            continue

    return None


def extract_latest_prediction(history: Any) -> Optional[float]:
    """
    Extract the latest prediction from several possible
    history response formats.
    """

    if history is None:
        return None

    records = history

    if isinstance(history, dict):

        for key in [
            "history",
            "data",
            "records",
            "predictions",
            "results"
        ]:
            if key in history:
                records = history[key]
                break

    if not isinstance(records, list):
        return None

    if not records:
        return None

    latest = records[-1]

    if isinstance(latest, dict):

        for key in [
            "prediction",
            "predicted_power",
            "solar_power",
            "power",
            "value"
        ]:

            value = latest.get(key)

            if value is not None:

                try:
                    return float(value)

                except (ValueError, TypeError):
                    pass

    return None


def extract_weather_value(
    weather: Any,
    keys: list[str]
) -> Optional[Any]:
    """
    Find a weather value from common response structures.
    """

    if weather is None:
        return None

    objects = []

    if isinstance(weather, dict):
        objects.append(weather)

        for key in [
            "weather",
            "data",
            "current",
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


# ==========================================================
# Data Summary
# ==========================================================

def get_current_data() -> dict:
    """
    Collect whatever current information is available
    from the existing backend.
    """

    history = get_history()
    weather = get_weather()

    prediction = extract_latest_prediction(history)

    temperature = extract_weather_value(
        weather,
        [
            "temperature",
            "temp",
            "air_temperature"
        ]
    )

    humidity = extract_weather_value(
        weather,
        [
            "humidity",
            "relative_humidity"
        ]
    )

    pressure = extract_weather_value(
        weather,
        [
            "pressure",
            "air_pressure"
        ]
    )

    wind = extract_weather_value(
        weather,
        [
            "wind_speed",
            "wind"
        ]
    )

    clouds = extract_weather_value(
        weather,
        [
            "cloud_cover",
            "clouds",
            "cloud"
        ]
    )

    radiation = extract_weather_value(
        weather,
        [
            "solar_radiation",
            "radiation"
        ]
    )

    return {
        "prediction": prediction,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "wind": wind,
        "clouds": clouds,
        "radiation": radiation,
    }


# ==========================================================
# Forecast Response
# ==========================================================

def forecast_answer(data: dict) -> str:

    prediction = data.get("prediction")
    temperature = data.get("temperature")
    clouds = data.get("clouds")
    radiation = data.get("radiation")

    parts = []

    if prediction is not None:

        if prediction >= 6:
            level = "high"
        elif prediction >= 3:
            level = "moderate"
        else:
            level = "low"

        parts.append(
            f"☀️ **Current solar prediction: {prediction:.2f} kW ({level.title()})**."
        )

    if temperature is not None:
        parts.append(f"🌡️ Temperature: {temperature}")

    if clouds is not None:
        parts.append(f"☁️ Cloud cover: {clouds}")

    if radiation is not None:
        parts.append(f"☀️ Solar radiation: {radiation}")

    if parts:

        return (
            "\n\n".join(parts)
            + "\n\n"
            "Higher solar radiation and longer sunshine duration "
            "generally support stronger solar generation."
        )

    return (
        "☀️ **Solar Generation Forecast**\n\n"
        "Solar generation depends mainly on solar radiation, "
        "sunshine duration, cloud conditions, temperature, "
        "humidity, wind, and time of day.\n\n"
        "The application uses an XGBoost forecasting model "
        "to estimate solar power generation."
    )


# ==========================================================
# Weather Response
# ==========================================================

def weather_answer(data: dict) -> str:

    temperature = data.get("temperature")
    humidity = data.get("humidity")
    pressure = data.get("pressure")
    wind = data.get("wind")
    clouds = data.get("clouds")
    radiation = data.get("radiation")

    values = []

    if temperature is not None:
        values.append(f"🌡️ Temperature: **{temperature}**")

    if humidity is not None:
        values.append(f"💧 Humidity: **{humidity}**")

    if pressure is not None:
        values.append(f"🧭 Pressure: **{pressure}**")

    if wind is not None:
        values.append(f"💨 Wind: **{wind}**")

    if clouds is not None:
        values.append(f"☁️ Cloud cover: **{clouds}**")

    if radiation is not None:
        values.append(f"☀️ Solar radiation: **{radiation}**")

    if values:

        return (
            "🌤️ **Current Weather Information**\n\n"
            + "\n".join(values)
            + "\n\n"
            "These conditions can influence solar generation."
        )

    return (
        "🌤️ I couldn't retrieve the current weather data "
        "from the backend right now.\n\n"
        "Please open the **Live Weather** page to check the "
        "latest available weather information."
    )


# ==========================================================
# Main AI Logic
# ==========================================================

def generate_answer(question: str) -> str:

    q = clean_text(question)

    # ======================================================
    # Greeting
    # ======================================================

    if is_greeting(q):

        return (
            "Hello! ☀️ I'm your Solar Energy Assistant.\n\n"
            "I can help you with:\n"
            "• Solar generation forecasts\n"
            "• Live weather\n"
            "• Battery charging\n"
            "• Appliance scheduling\n"
            "• Energy saving\n"
            "• Solar panel maintenance\n"
            "• XGBoost and machine learning\n"
            "• Daily energy reports\n\n"
            "What would you like to know?"
        )

    # ======================================================
    # Thanks
    # ======================================================

    if contains_any(
        q,
        ["thank you", "thanks", "thank"]
    ):

        return (
            "You're welcome! ☀️\n\n"
            "I'm here whenever you need help with "
            "solar forecasting, weather, batteries, "
            "or energy optimization."
        )

    # ======================================================
    # ML Model
    # ======================================================

    if contains_any(
        q,
        [
            "xgboost",
            "machine learning",
            "ml model",
            "machine model",
            "algorithm",
            "model",
            "how does the model work"
        ]
    ):

        return (
            "🤖 **Machine Learning Model**\n\n"
            "This project uses an **XGBoost Regressor** "
            "for solar power forecasting.\n\n"
            "The model uses weather and time-based features "
            "such as:\n\n"
            "• Wind speed\n"
            "• Sunshine duration\n"
            "• Air pressure\n"
            "• Solar radiation\n"
            "• Air temperature\n"
            "• Relative humidity\n"
            "• Hour\n"
            "• Day\n"
            "• Month\n\n"
            "These features are used to estimate solar power "
            "generation."
        )

    # ======================================================
    # Battery
    # ======================================================

    if contains_any(
        q,
        [
            "battery",
            "charge battery",
            "charging battery",
            "store energy",
            "battery charging"
        ]
    ):

        data = get_current_data()
        prediction = data.get("prediction")

        if prediction is not None:

            if prediction >= 6:

                return (
                    "🔋 **Battery Recommendation**\n\n"
                    f"The latest available solar prediction is "
                    f"**{prediction:.2f} kW**, which indicates "
                    "strong generation.\n\n"
                    "This is generally a suitable period to "
                    "prioritize battery charging if your system "
                    "supports it."
                )

            elif prediction >= 3:

                return (
                    "🔋 **Battery Recommendation**\n\n"
                    f"The latest available prediction is "
                    f"**{prediction:.2f} kW**, indicating "
                    "moderate solar generation.\n\n"
                    "Battery charging may be reasonable, but "
                    "available solar power should be monitored."
                )

            else:

                return (
                    "🔋 **Battery Recommendation**\n\n"
                    f"The latest available prediction is "
                    f"**{prediction:.2f} kW**, indicating "
                    "relatively low generation.\n\n"
                    "If possible, consider waiting for stronger "
                    "solar generation before prioritizing charging."
                )

        return (
            "🔋 **Battery Recommendation**\n\n"
            "Battery charging is generally most effective when "
            "solar generation is strong.\n\n"
            "For this application, the recommended daytime "
            "window is approximately **10 AM–3 PM**.\n\n"
            "For the actual current prediction, check the "
            "**Solar Forecast** page."
        )

    # ======================================================
    # Heavy Appliances
    # ======================================================

    if contains_any(
        q,
        [
            "heavy appliance",
            "heavy appliances",
            "washing machine",
            "washing machines",
            "water pump",
            "water pumps",
            "ev charger",
            "ev charging",
            "run appliances",
            "run appliance"
        ]
    ):

        data = get_current_data()
        prediction = data.get("prediction")

        if prediction is not None and prediction >= 6:

            return (
                "⚡ **Appliance Recommendation**\n\n"
                f"The latest available solar prediction is "
                f"**{prediction:.2f} kW**, indicating strong "
                "generation.\n\n"
                "This is generally a favorable condition for "
                "running flexible high-power appliances such as "
                "washing machines, water pumps, or EV chargers."
            )

        if prediction is not None:

            return (
                "⚡ **Appliance Recommendation**\n\n"
                f"The latest available solar prediction is "
                f"**{prediction:.2f} kW**.\n\n"
                "For better direct solar utilization, consider "
                "scheduling flexible high-power appliances during "
                "periods of stronger daytime generation."
            )

        return (
            "⚡ **Appliance Scheduling**\n\n"
            "High-power appliances are generally better scheduled "
            "during periods of strong solar generation.\n\n"
            "The recommended daytime window for this application "
            "is approximately **10 AM–3 PM**."
        )

    # ======================================================
    # Forecast
    # ======================================================

    if contains_any(
        q,
        [
            "forecast",
            "solar generation",
            "solar power",
            "power generation",
            "generation today",
            "solar output",
            "will solar",
            "how much solar",
            "high today",
            "low today"
        ]
    ):

        data = get_current_data()

        return forecast_answer(data)

    # ======================================================
    # Weather
    # ======================================================

    if contains_any(
        q,
        [
            "weather",
            "temperature",
            "humidity",
            "pressure",
            "wind",
            "cloud",
            "clouds",
            "sunshine",
            "sunlight",
            "radiation"
        ]
    ):

        data = get_current_data()

        return weather_answer(data)

    # ======================================================
    # Energy Saving
    # ======================================================

    if contains_any(
        q,
        [
            "saving",
            "save energy",
            "energy saving",
            "reduce electricity",
            "reduce power",
            "electricity bill",
            "save electricity"
        ]
    ):

        return (
            "💡 **Energy-Saving Recommendations**\n\n"
            "1. Use high-power appliances during periods of "
            "strong solar generation.\n\n"
            "2. Reduce unnecessary standby consumption.\n\n"
            "3. Use stored battery energy when solar generation "
            "is low.\n\n"
            "4. Keep solar panels clean and free from unnecessary "
            "obstructions.\n\n"
            "5. Monitor your historical solar generation.\n\n"
            "6. Shift flexible electricity consumption toward "
            "strong daytime solar production."
        )

    # ======================================================
    # Maintenance
    # ======================================================

    if contains_any(
        q,
        [
            "maintenance",
            "maintain",
            "clean panel",
            "clean panels",
            "solar panel",
            "solar panels",
            "panel cleaning",
            "panel care"
        ]
    ):

        return (
            "🔧 **Solar Panel Maintenance**\n\n"
            "Regular maintenance can help keep a solar system "
            "operating effectively.\n\n"
            "Recommended practices include:\n\n"
            "• Keep panels reasonably clean.\n"
            "• Remove dust, leaves, and visible obstructions.\n"
            "• Check for unnecessary shading.\n"
            "• Monitor changes in generation.\n"
            "• Investigate unusual drops in output.\n\n"
            "For electrical or physical faults, use qualified "
            "professional inspection."
        )

    # ======================================================
    # Daily Report
    # ======================================================

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

        data = get_current_data()

        prediction = data.get("prediction")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        clouds = data.get("clouds")

        report = "📊 **Daily Solar Energy Report**\n\n"

        if prediction is not None:

            if prediction >= 6:
                level = "High"
            elif prediction >= 3:
                level = "Moderate"
            else:
                level = "Low"

            report += (
                f"☀️ **Solar Prediction:** "
                f"{prediction:.2f} kW ({level})\n\n"
            )

        else:

            report += (
                "☀️ **Solar Prediction:** "
                "Current prediction unavailable\n\n"
            )

        if temperature is not None:
            report += f"🌡️ **Temperature:** {temperature}\n\n"

        if humidity is not None:
            report += f"💧 **Humidity:** {humidity}\n\n"

        if clouds is not None:
            report += f"☁️ **Cloud Cover:** {clouds}\n\n"

        report += (
            "🔋 **Battery:** Charge when solar generation "
            "is strong.\n\n"
            "⚡ **Appliances:** Prefer flexible high-power "
            "loads during strong daytime generation.\n\n"
            "💡 **Energy Saving:** Reduce standby consumption "
            "and maximize direct solar usage."
        )

        return report

    # ======================================================
    # Project Information
    # ======================================================

    if contains_any(
        q,
        [
            "what is this project",
            "what does this project do",
            "about this project",
            "what can you do",
            "your capabilities",
            "features"
        ]
    ):

        return (
            "☀️ **Solar Power Forecast Agent**\n\n"
            "This application forecasts solar power generation "
            "and provides energy recommendations.\n\n"
            "It includes:\n\n"
            "• XGBoost solar forecasting\n"
            "• Live weather information\n"
            "• Prediction history\n"
            "• Analytics\n"
            "• AI Energy Assistant\n"
            "• Battery recommendations\n"
            "• Appliance scheduling\n"
            "• Maintenance guidance\n"
            "• Daily reports\n"
            "• Administrative tools"
        )

    # ======================================================
    # General Solar
    # ======================================================

    if contains_any(
        q,
        [
            "solar",
            "photovoltaic",
            "pv",
            "sun"
        ]
    ):

        return (
            "☀️ **Solar Energy**\n\n"
            "Solar power generation depends mainly on the "
            "sunlight reaching the panels and the operating "
            "conditions of the system.\n\n"
            "In this application, weather and time-based "
            "features are used by an XGBoost model to forecast "
            "solar power generation.\n\n"
            "You can also explore the **Solar Forecast**, "
            "**Live Weather**, and **Analytics** pages."
        )

    # ======================================================
    # Unknown Question
    # ======================================================

    return (
        "I'm your Solar Energy Assistant. ☀️\n\n"
        "I can help you with:\n\n"
        "• Solar power forecasts\n"
        "• Current weather\n"
        "• Battery charging\n"
        "• Appliance scheduling\n"
        "• Energy-saving strategies\n"
        "• Solar panel maintenance\n"
        "• XGBoost and machine learning\n"
        "• Daily solar reports\n\n"
        "Try asking:\n\n"
        "\"Will solar generation be high today?\"\n"
        "\"Should I charge my battery now?\"\n"
        "\"Can I run my washing machine?\"\n"
        "\"What is your ML model?\"\n"
        "\"Give me today's weather.\"\n"
        "\"Generate a daily report.\""
    )


# ==========================================================
# API Endpoint
# ==========================================================

@router.post("/ai-assistant")
def ai_assistant(request: AssistantRequest):

    answer = generate_answer(request.question)

    return {
        "response": answer
    }
