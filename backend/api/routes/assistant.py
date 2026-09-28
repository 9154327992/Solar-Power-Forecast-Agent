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
    Check for complete words or phrases.

    Using word boundaries prevents:
        hi -> matching high
    """

    for phrase in phrases:

        pattern = rf"\b{re.escape(phrase.lower())}\b"

        if re.search(pattern, text):
            return True

    return False


def is_greeting(text: str) -> bool:
    """
    Detect greetings without treating 'high' as 'hi'.
    """

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
# Backend Request Helper
# ==========================================================

def safe_get(url: str) -> Optional[Any]:
    """
    Safely request JSON data from the backend.
    """

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


# ==========================================================
# History
# ==========================================================

def get_history() -> Optional[Any]:
    """
    Retrieve prediction history.
    """

    return safe_get(
        f"{API_BASE_URL}/api/history"
    )


# ==========================================================
# Weather
# ==========================================================

def get_weather() -> Optional[Any]:
    """
    Try the available weather endpoints.
    """

    weather_urls = [
        f"{API_BASE_URL}/api/weather",
        f"{API_BASE_URL}/api/weather/current",
    ]

    for url in weather_urls:

        data = safe_get(url)

        if data is not None:
            return data

    return None


# ==========================================================
# Extract History Records
# ==========================================================

def extract_records(data: Any) -> list:
    """
    Extract prediction records from common API formats.
    """

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        possible_keys = [
            "history",
            "data",
            "records",
            "predictions",
            "results"
        ]

        for key in possible_keys:

            value = data.get(key)

            if isinstance(value, list):
                return value

    return []


# ==========================================================
# Extract Prediction
# ==========================================================

def extract_prediction(history: Any) -> Optional[float]:
    """
    Extract the latest prediction from history.
    """

    records = extract_records(history)

    if not records:
        return None

    latest = records[-1]

    if not isinstance(latest, dict):
        return None

    prediction_keys = [
        "prediction",
        "predicted_power",
        "solar_power",
        "power",
        "value"
    ]

    for key in prediction_keys:

        value = latest.get(key)

        if value is None:
            continue

        try:

            return float(value)

        except (ValueError, TypeError):

            continue

    return None


# ==========================================================
# Extract Weather Values
# ==========================================================

def extract_weather_value(
    weather: Any,
    keys: list[str]
) -> Optional[Any]:
    """
    Extract a weather value from common response formats.
    """

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


# ==========================================================
# Get Current Application Data
# ==========================================================

def get_current_data() -> dict:
    """
    Collect currently available prediction and weather data.
    """

    history = get_history()
    weather = get_weather()

    data = {
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

    return data


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
# Greeting
# ==========================================================

def greeting_answer() -> str:

    return (
        "Hello! ☀️ I'm your Solar Energy Assistant.\n\n"
        "You can ask me questions about:\n\n"
        "• Solar generation\n"
        "• Today's forecast\n"
        "• Weather conditions\n"
        "• Battery charging\n"
        "• Appliance scheduling\n"
        "• Energy saving\n"
        "• Solar panel efficiency\n"
        "• Solar panel maintenance\n"
        "• XGBoost and machine learning\n"
        "• Daily reports\n\n"
        "You are not limited to the quick questions shown above."
    )


# ==========================================================
# Forecast Prediction Answer
# ==========================================================

def forecast_prediction_answer(data: dict) -> str:
    """
    Answer questions such as:

    Will solar generation be high today?
    Is solar generation good today?
    How much solar power will be generated?
    """

    prediction = data.get("prediction")

    if prediction is None:

        return (
            "☀️ **Today's Solar Generation**\n\n"
            "I can't determine whether today's solar generation "
            "will be High, Moderate, or Low because the latest "
            "prediction is currently unavailable from the backend.\n\n"
            "Please check the **Solar Forecast** page for the "
            "current prediction."
        )

    level = prediction_level(prediction)

    if level == "High":

        recommendation = (
            "This indicates favorable conditions for solar "
            "generation. You can consider charging the battery "
            "and using flexible high-power appliances while "
            "generation is strong."
        )

    elif level == "Moderate":

        recommendation = (
            "This indicates reasonable generation conditions. "
            "Flexible appliances can be used when solar output "
            "is strongest."
        )

    else:

        recommendation = (
            "This indicates relatively low generation. If your "
            "schedule is flexible, consider waiting for a period "
            "with stronger solar output."
        )

    return (
        "☀️ **Today's Solar Generation**\n\n"
        f"Latest available prediction: "
        f"**{prediction:.2f} kW**\n\n"
        f"Generation level: **{level}**\n\n"
        f"{recommendation}"
    )


# ==========================================================
# Forecast Explanation Answer
# ==========================================================

def forecast_explanation_answer(data: dict) -> str:
    """
    Explain why the forecast has its current characteristics.
    """

    prediction = data.get("prediction")
    radiation = data.get("radiation")
    sunshine = data.get("sunshine")
    clouds = data.get("clouds")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    wind = data.get("wind")

    response = (
        "☀️ **Today's Forecast Explanation**\n\n"
    )

    if prediction is not None:

        level = prediction_level(prediction)

        response += (
            f"The latest available prediction is "
            f"**{prediction:.2f} kW ({level})**.\n\n"
        )

    else:

        response += (
            "The latest numerical prediction is currently "
            "unavailable from the backend.\n\n"
        )

    response += (
        "The forecasting system considers several weather "
        "and time-related factors:\n\n"
        "☀️ **Solar radiation** — indicates the amount of "
        "solar energy available to the panels.\n\n"
        "🌞 **Sunshine duration** — represents how long "
        "sunlight is available.\n\n"
        "☁️ **Cloud conditions** — increased cloud cover "
        "can reduce sunlight reaching the panels.\n\n"
        "🌡️ **Air temperature** — temperature is included "
        "as one of the model features.\n\n"
        "💧 **Relative humidity** — provides additional "
        "information about atmospheric conditions.\n\n"
        "💨 **Wind speed** — provides another weather "
        "indicator used by the forecasting model.\n\n"
        "🕐 **Time features** — hour, day, and month help "
        "the model account for changes in solar availability "
        "throughout the day and year.\n\n"
        "The application combines these inputs using an "
        "**XGBoost Regressor** to estimate solar power."
    )

    # Add available current values.

    available = []

    if radiation is not None:
        available.append(
            f"☀️ Solar radiation: **{radiation}**"
        )

    if sunshine is not None:
        available.append(
            f"🌞 Sunshine duration: **{sunshine}**"
        )

    if clouds is not None:
        available.append(
            f"☁️ Cloud cover: **{clouds}**"
        )

    if temperature is not None:
        available.append(
            f"🌡️ Temperature: **{temperature}**"
        )

    if humidity is not None:
        available.append(
            f"💧 Humidity: **{humidity}**"
        )

    if wind is not None:
        available.append(
            f"💨 Wind: **{wind}**"
        )

    if available:

        response += (
            "\n\n**Available current conditions:**\n\n"
            + "\n\n".join(available)
        )

    return response


# ==========================================================
# General Forecast Answer
# ==========================================================

def general_forecast_answer(data: dict) -> str:

    prediction = data.get("prediction")

    response = (
        "☀️ **Solar Forecast**\n\n"
    )

    if prediction is not None:

        level = prediction_level(prediction)

        response += (
            f"Latest available prediction: "
            f"**{prediction:.2f} kW ({level})**.\n\n"
        )

    else:

        response += (
            "The latest numerical prediction is currently "
            "unavailable.\n\n"
        )

    response += (
        "Solar generation is influenced by solar radiation, "
        "sunshine duration, cloud cover, temperature, "
        "humidity, wind conditions, and time of day.\n\n"
        "The forecasting system uses these weather and "
        "time-based features with an XGBoost model."
    )

    return response


# ==========================================================
# Weather Answer
# ==========================================================

def weather_answer(data: dict) -> str:

    values = []

    if data.get("temperature") is not None:
        values.append(
            f"🌡️ Temperature: **{data['temperature']}**"
        )

    if data.get("humidity") is not None:
        values.append(
            f"💧 Humidity: **{data['humidity']}**"
        )

    if data.get("pressure") is not None:
        values.append(
            f"🧭 Pressure: **{data['pressure']}**"
        )

    if data.get("wind") is not None:
        values.append(
            f"💨 Wind: **{data['wind']}**"
        )

    if data.get("clouds") is not None:
        values.append(
            f"☁️ Cloud cover: **{data['clouds']}**"
        )

    if data.get("radiation") is not None:
        values.append(
            f"☀️ Solar radiation: **{data['radiation']}**"
        )

    if not values:

        return (
            "🌤️ **Current Weather**\n\n"
            "I couldn't retrieve the current weather data "
            "from the backend right now.\n\n"
            "Please check the **Live Weather** page for "
            "the latest available conditions."
        )

    return (
        "🌤️ **Current Weather Information**\n\n"
        + "\n\n".join(values)
        + "\n\n"
        "These weather conditions can affect solar power "
        "generation."
    )


# ==========================================================
# Battery Answer
# ==========================================================

def battery_answer(data: dict) -> str:

    prediction = data.get("prediction")

    if prediction is None:

        return (
            "🔋 **Battery Recommendation**\n\n"
            "The latest solar prediction is currently "
            "unavailable.\n\n"
            "In general, battery charging is most useful "
            "during periods of strong solar generation. "
            "For this application, approximately **10 AM–3 PM** "
            "is a useful daytime window to consider.\n\n"
            "Check the **Solar Forecast** page for the latest "
            "prediction."
        )

    level = prediction_level(prediction)

    if level == "High":

        return (
            "🔋 **Battery Recommendation**\n\n"
            f"The latest solar prediction is "
            f"**{prediction:.2f} kW ({level})**.\n\n"
            "This indicates strong generation conditions. "
            "If your battery needs charging, this is generally "
            "a suitable period to prioritize charging."
        )

    if level == "Moderate":

        return (
            "🔋 **Battery Recommendation**\n\n"
            f"The latest solar prediction is "
            f"**{prediction:.2f} kW ({level})**.\n\n"
            "Battery charging may be reasonable, but available "
            "solar generation should be monitored."
        )

    return (
        "🔋 **Battery Recommendation**\n\n"
        f"The latest solar prediction is "
        f"**{prediction:.2f} kW ({level})**.\n\n"
        "Solar generation is relatively low. If your schedule "
        "is flexible, consider waiting for stronger generation "
        "before prioritizing battery charging."
    )


# ==========================================================
# Appliance Answer
# ==========================================================

def appliance_answer(data: dict) -> str:

    prediction = data.get("prediction")

    if prediction is None:

        return (
            "⚡ **Appliance Scheduling**\n\n"
            "The latest solar prediction isn't available right "
            "now.\n\n"
            "In general, flexible high-power appliances such as "
            "washing machines, water pumps, and EV chargers are "
            "better scheduled during periods of strong solar "
            "generation.\n\n"
            "For this application, the suggested daytime window "
            "is approximately **10 AM–3 PM**."
        )

    level = prediction_level(prediction)

    if level == "High":

        return (
            "⚡ **Appliance Recommendation**\n\n"
            f"The latest solar prediction is "
            f"**{prediction:.2f} kW ({level})**.\n\n"
            "This indicates favorable conditions for running "
            "flexible high-power appliances such as washing "
            "machines, water pumps, or EV chargers."
        )

    return (
        "⚡ **Appliance Recommendation**\n\n"
        f"The latest solar prediction is "
        f"**{prediction:.2f} kW ({level})**.\n\n"
        "Consider scheduling flexible high-power appliances "
        "for a period when solar generation is stronger."
    )


# ==========================================================
# Machine Learning Answer
# ==========================================================

def ml_answer() -> str:

    return (
        "🤖 **Machine Learning Model**\n\n"
        "The Solar Power Forecast Agent uses an "
        "**XGBoost Regressor** for solar power forecasting.\n\n"
        "The model uses weather and time-based features "
        "including:\n\n"
        "• Wind speed\n"
        "• Sunshine duration\n"
        "• Air pressure\n"
        "• Solar radiation\n"
        "• Air temperature\n"
        "• Relative humidity\n"
        "• Hour\n"
        "• Day\n"
        "• Month\n\n"
        "The model learns relationships between these inputs "
        "and solar power generation to produce a forecast."
    )


# ==========================================================
# Solar Efficiency Answer
# ==========================================================

def efficiency_answer() -> str:

    return (
        "⚡ **Solar Panel Efficiency**\n\n"
        "Solar panel performance can be affected by several "
        "conditions:\n\n"
        "☀️ **Solar radiation:** More available sunlight "
        "generally supports greater generation.\n\n"
        "🌡️ **Temperature:** Panel electrical characteristics "
        "can change as temperature changes.\n\n"
        "☁️ **Cloud cover:** Clouds can reduce sunlight reaching "
        "the panels.\n\n"
        "🧹 **Dust and dirt:** Surface contamination can reduce "
        "the available sunlight.\n\n"
        "🌳 **Shading:** Buildings, trees, and other obstructions "
        "can reduce output.\n\n"
        "Monitoring generation over time can help identify "
        "unusual performance changes."
    )


# ==========================================================
# Cloud Answer
# ==========================================================

def cloudy_answer() -> str:

    return (
        "☁️ **Cloudy Weather and Solar Generation**\n\n"
        "Cloud cover generally reduces the amount of direct "
        "sunlight reaching solar panels.\n\n"
        "Panels can still generate electricity under cloudy "
        "conditions because some diffuse sunlight reaches them, "
        "but output is generally lower than during strong "
        "clear-sky conditions."
    )


# ==========================================================
# Solar Radiation Answer
# ==========================================================

def radiation_answer() -> str:

    return (
        "☀️ **Solar Radiation**\n\n"
        "Solar radiation represents the solar energy reaching "
        "the Earth's surface.\n\n"
        "It is one of the important factors affecting "
        "photovoltaic power generation.\n\n"
        "Your XGBoost forecasting model uses solar radiation "
        "as one of its input features."
    )


# ==========================================================
# Humidity Answer
# ==========================================================

def humidity_answer() -> str:

    return (
        "💧 **Humidity and Solar Generation**\n\n"
        "Relative humidity describes the amount of water vapor "
        "in the atmosphere.\n\n"
        "It provides additional atmospheric information that "
        "can help a forecasting model distinguish between "
        "different weather conditions.\n\n"
        "Your XGBoost model includes relative humidity as "
        "one of its input features."
    )


# ==========================================================
# Temperature Answer
# ==========================================================

def temperature_answer() -> str:

    return (
        "🌡️ **Temperature and Solar Generation**\n\n"
        "Temperature is one of the weather variables used "
        "by the forecasting model.\n\n"
        "Solar panel electrical characteristics can change "
        "with temperature, so temperature can contribute "
        "to the prediction of solar generation.\n\n"
        "The model combines temperature with other weather "
        "and time-based features rather than relying on "
        "temperature alone."
    )


# ==========================================================
# Energy Saving Answer
# ==========================================================

def energy_saving_answer() -> str:

    return (
        "💡 **Energy-Saving Recommendations**\n\n"
        "1. Use high-power appliances during strong solar "
        "generation periods.\n\n"
        "2. Reduce unnecessary standby power consumption.\n\n"
        "3. Use stored battery energy when solar generation "
        "is low.\n\n"
        "4. Keep solar panels reasonably clean.\n\n"
        "5. Avoid unnecessary shading and obstructions.\n\n"
        "6. Monitor historical solar generation.\n\n"
        "7. Shift flexible electricity consumption toward "
        "strong daytime solar production."
    )


# ==========================================================
# Maintenance Answer
# ==========================================================

def maintenance_answer() -> str:

    return (
        "🔧 **Solar Panel Maintenance**\n\n"
        "Regular maintenance can help maintain effective "
        "solar system operation.\n\n"
        "• Keep panels reasonably clean.\n"
        "• Remove dust, leaves, and visible obstructions.\n"
        "• Check for unnecessary shading.\n"
        "• Monitor changes in solar generation.\n"
        "• Investigate unusual drops in output.\n"
        "• Check for visible physical damage.\n\n"
        "For electrical or physical faults, use qualified "
        "professional inspection."
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

    response = (
        "📊 **Daily Solar Energy Report**\n\n"
    )

    if prediction is not None:

        level = prediction_level(prediction)

        response += (
            f"☀️ **Solar Prediction:** "
            f"{prediction:.2f} kW ({level})\n\n"
        )

    else:

        response += (
            "☀️ **Solar Prediction:** "
            "Currently unavailable\n\n"
        )

    if temperature is not None:
        response += (
            f"🌡️ **Temperature:** "
            f"{temperature}\n\n"
        )

    if humidity is not None:
        response += (
            f"💧 **Humidity:** "
            f"{humidity}\n\n"
        )

    if clouds is not None:
        response += (
            f"☁️ **Cloud Cover:** "
            f"{clouds}\n\n"
        )

    if radiation is not None:
        response += (
            f"☀️ **Solar Radiation:** "
            f"{radiation}\n\n"
        )

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
# General Solar Answer
# ==========================================================

def solar_answer() -> str:

    return (
        "☀️ **Solar Energy**\n\n"
        "Solar photovoltaic systems convert sunlight into "
        "electrical energy.\n\n"
        "Solar generation is affected by factors including:\n\n"
        "• Solar radiation\n"
        "• Sunshine duration\n"
        "• Cloud cover\n"
        "• Temperature\n"
        "• Humidity\n"
        "• Wind conditions\n"
        "• Time of day\n\n"
        "Your Solar Power Forecast Agent uses weather and "
        "time-based features with an XGBoost model to "
        "estimate solar power generation."
    )


# ==========================================================
# Project Answer
# ==========================================================

def project_answer() -> str:

    return (
        "☀️ **Solar Power Forecast Agent**\n\n"
        "This application forecasts solar power generation "
        "and provides energy recommendations.\n\n"
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
        "The forecasting system uses an XGBoost model."
    )


# ==========================================================
# Main Assistant Logic
# ==========================================================

def generate_answer(question: str) -> str:

    q = clean_text(question)

    # ======================================================
    # Greeting
    # ======================================================

    if is_greeting(q):

        return greeting_answer()

    # ======================================================
    # Thanks
    # ======================================================

    if contains_any(
        q,
        [
            "thank you",
            "thanks",
            "thank"
        ]
    ):

        return (
            "You're welcome! ☀️\n\n"
            "Feel free to ask another solar or energy question."
        )

    # ======================================================
    # Specific Forecast Prediction
    #
    # IMPORTANT:
    # This MUST come BEFORE general forecast detection.
    # ======================================================

    if contains_any(
        q,
        [
            "will solar generation be high",
            "will solar generation be low",
            "will solar generation be good",
            "is solar generation high",
            "is solar generation low",
            "is solar generation good",
            "how much solar will",
            "how much power will",
            "what will solar generation",
            "solar generation today",
            "solar output today",
            "power generation today",
            "will solar power be high",
            "will solar power be low"
        ]
    ):

        return forecast_prediction_answer(
            get_current_data()
        )

    # ======================================================
    # Forecast Explanation
    #
    # Separate from prediction questions.
    # ======================================================

    if contains_any(
        q,
        [
            "explain today's forecast",
            "explain todays forecast",
            "explain the forecast",
            "explain today's solar forecast",
            "explain todays solar forecast",
            "why is the forecast",
            "why is solar generation",
            "what affects today's forecast",
            "what affects todays forecast",
            "what factors affect solar generation",
            "what factors affect the forecast",
            "how is the forecast calculated",
            "how is solar generation forecast",
            "how does solar forecasting work"
        ]
    ):

        return forecast_explanation_answer(
            get_current_data()
        )

    # ======================================================
    # Machine Learning / XGBoost
    # ======================================================

    if contains_any(
        q,
        [
            "xgboost",
            "machine learning",
            "machine learning model",
            "ml model",
            "machine model",
            "algorithm",
            "how does the model work",
            "what model do you use",
            "what ml model do you use"
        ]
    ):

        return ml_answer()

    # ======================================================
    # Solar Panel Efficiency
    # ======================================================

    if contains_any(
        q,
        [
            "efficiency",
            "panel efficiency",
            "solar panel efficiency",
            "improve efficiency",
            "improve solar",
            "improve generation",
            "solar performance",
            "panel performance"
        ]
    ):

        return efficiency_answer()

    # ======================================================
    # Cloud Conditions
    # ======================================================

    if contains_any(
        q,
        [
            "cloudy",
            "cloudy day",
            "cloudy weather",
            "cloud cover",
            "clouds",
            "what happens on a cloudy day",
            "solar on cloudy day"
        ]
    ):

        return cloudy_answer()

    # ======================================================
    # Solar Radiation
    # ======================================================

    if contains_any(
        q,
        [
            "solar radiation",
            "what is radiation",
            "radiation"
        ]
    ):

        return radiation_answer()

    # ======================================================
    # Humidity
    # ======================================================

    if contains_any(
        q,
        [
            "humidity",
            "relative humidity",
            "what is humidity",
            "how does humidity affect solar"
        ]
    ):

        return humidity_answer()

    # ======================================================
    # Temperature
    # ======================================================

    if contains_any(
        q,
        [
            "temperature",
            "hot weather",
            "heat",
            "how does temperature affect solar",
            "does temperature affect solar"
        ]
    ):

        return temperature_answer()

    # ======================================================
    # Battery
    # ======================================================

    if contains_any(
        q,
        [
            "battery",
            "charge battery",
            "charging battery",
            "battery charging",
            "store energy",
            "when should i charge",
            "should i charge"
        ]
    ):

        return battery_answer(
            get_current_data()
        )

    # ======================================================
    # Appliances
    # ======================================================

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
            "high power appliances",
            "can i run"
        ]
    ):

        return appliance_answer(
            get_current_data()
        )

    # ======================================================
    # Weather
    # ======================================================

    if contains_any(
        q,
        [
            "weather",
            "current weather",
            "weather today",
            "what is the weather",
            "how is the weather"
        ]
    ):

        return weather_answer(
            get_current_data()
        )

    # ======================================================
    # Energy Saving
    # ======================================================

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
            "save power",
            "how can i save energy",
            "how to save energy"
        ]
    ):

        return energy_saving_answer()

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
            "panel cleaning",
            "panel care",
            "solar panel maintenance",
            "how to maintain solar panels"
        ]
    ):

        return maintenance_answer()

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
            "give me a report",
            "report"
        ]
    ):

        return daily_report_answer(
            get_current_data()
        )

    # ======================================================
    # Project Information
    # ======================================================

    if contains_any(
        q,
        [
            "what is this project",
            "what does this project do",
            "about this project",
            "project features",
            "what can you do",
            "your capabilities",
            "what is solar power forecast agent"
        ]
    ):

        return project_answer()

    # ======================================================
    # General Forecast
    #
    # This comes AFTER specific forecast questions.
    # ======================================================

    if contains_any(
        q,
        [
            "forecast",
            "solar forecast",
            "solar generation",
            "solar output",
            "power generation",
            "solar power today",
            "forecasting"
        ]
    ):

        return general_forecast_answer(
            get_current_data()
        )

    # ======================================================
    # General Solar
    # ======================================================

    if contains_any(
        q,
        [
            "solar",
            "photovoltaic",
            "photovoltaics",
            "pv",
            "pv panels",
            "pv system",
            "sunlight",
            "sun"
        ]
    ):

        return solar_answer()

    # ======================================================
    # Unknown
    # ======================================================

    return (
        "☀️ **Solar Energy Assistant**\n\n"
        "I can answer a wide range of questions about "
        "solar energy and this application.\n\n"
        "You can ask about:\n\n"
        "• Today's solar generation\n"
        "• Forecast explanations\n"
        "• Weather conditions\n"
        "• Solar radiation\n"
        "• Temperature and humidity\n"
        "• Cloudy conditions\n"
        "• Battery charging\n"
        "• Appliance scheduling\n"
        "• Energy saving\n"
        "• Solar panel efficiency\n"
        "• Solar panel maintenance\n"
        "• XGBoost and machine learning\n"
        "• Daily reports\n"
        "• How this project works\n\n"
        "You don't have to choose one of the six quick "
        "questions. Type your own question below."
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
