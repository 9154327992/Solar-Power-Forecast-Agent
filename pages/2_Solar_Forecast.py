import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

st.set_page_config(
    page_title="Solar Forecast",
    page_icon="☀️",
    layout="wide"
)

# ==========================================================
# Load CSS
# ==========================================================

css = Path("assets/style.css")

if css.exists():
    with open(css, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================================================
# Helper Functions
# ==========================================================

def get_live_weather():
    """
    Get current weather data from the backend.
    Tries the main weather endpoint first, then the
    current-weather endpoint.
    """

    endpoints = [
        f"{API_URL}/api/weather",
        f"{API_URL}/api/weather/current"
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(
                endpoint,
                timeout=15
            )

            if response.ok:
                data = response.json()

                # Handle APIs that wrap the weather object
                if isinstance(data, dict):
                    if "data" in data and isinstance(data["data"], dict):
                        return data["data"]

                    if "weather" in data and isinstance(data["weather"], dict):
                        return data["weather"]

                    return data

        except Exception:
            continue

    return None


def get_value(data, *keys):
    """
    Return the first available value from possible API keys.
    """

    if not isinstance(data, dict):
        return None

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    return None


# ==========================================================
# Header
# ==========================================================

st.title("☀ Solar Power Forecast")

st.write(
    "Predict solar power generation using current weather parameters."
)

st.divider()

# ==========================================================
# Get Current Weather
# ==========================================================

weather = get_live_weather()

# Current date/time fallback
now = datetime.now()

# Default values
wind_default = 3.5
pressure_default = 1013.0
temperature_default = 28.0
humidity_default = 60.0

# Values from Live Weather API
if weather:

    wind_api = get_value(
        weather,
        "wind_speed",
        "windSpeed",
        "wind"
    )

    pressure_api = get_value(
        weather,
        "air_pressure",
        "pressure",
        "airPressure"
    )

    temperature_api = get_value(
        weather,
        "air_temperature",
        "temperature",
        "temp"
    )

    humidity_api = get_value(
        weather,
        "relative_humidity",
        "humidity",
        "relativeHumidity"
    )

    if wind_api is not None:
        wind_default = float(wind_api)

    if pressure_api is not None:
        pressure_default = float(pressure_api)

    if temperature_api is not None:
        temperature_default = float(temperature_api)

    if humidity_api is not None:
        humidity_default = float(humidity_api)

# ==========================================================
# Weather Status
# ==========================================================

if weather:

    st.success(
        "🌤 Current weather data loaded from Live Weather."
    )

else:

    st.warning(
        "⚠️ Live Weather data could not be loaded. "
        "Default values are being used."
    )

# ==========================================================
# Weather Input
# ==========================================================

st.subheader("🌦 Weather Parameters")

left, right = st.columns(2)

with left:

    wind = st.number_input(
        "Wind Speed (m/s)",
        min_value=0.0,
        max_value=50.0,
        value=wind_default,
        step=0.1
    )

    sunshine = st.number_input(
        "Sunshine Duration (Hours)",
        min_value=0.0,
        max_value=24.0,
        value=6.0,
        step=0.1
    )

    pressure = st.number_input(
        "Air Pressure (hPa)",
        min_value=800.0,
        max_value=1100.0,
        value=pressure_default,
        step=0.1
    )

    radiation = st.number_input(
        "Solar Radiation (W/m²)",
        min_value=0.0,
        max_value=1500.0,
        value=450.0,
        step=1.0
    )

with right:

    temperature = st.number_input(
        "Air Temperature (°C)",
        value=temperature_default,
        step=0.1
    )

    humidity = st.number_input(
        "Relative Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=humidity_default,
        step=1.0
    )

    hour = st.slider(
        "Hour",
        0,
        23,
        now.hour
    )

    day = st.slider(
        "Day",
        1,
        31,
        now.day
    )

    month = st.slider(
        "Month",
        1,
        12,
        now.month
    )

st.divider()

# ==========================================================
# Forecast Button
# ==========================================================

if st.button(
    "🚀 Forecast Solar Power",
    use_container_width=True
):

    with st.spinner("Predicting Solar Power..."):

        try:

            response = requests.post(

                f"{API_URL}/api/predict/forecast",

                json={

                    "wind_speed": wind,

                    "sunshine_duration": sunshine,

                    "air_pressure": pressure,

                    "solar_radiation": radiation,

                    "air_temperature": temperature,

                    "relative_humidity": humidity,

                    "hour": hour,

                    "day": day,

                    "month": month

                },

                timeout=20

            )

            response.raise_for_status()

            result = response.json()

        except Exception as e:

            st.error(
                f"Prediction Failed\n\n{e}"
            )

            st.stop()

    # ======================================================
    # Prediction Result
    # ======================================================

    st.success(
        "Prediction Completed Successfully"
    )

    st.divider()

    st.subheader("Forecast Result")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Predicted Power",
            f"{result['prediction']:.2f} kW"
        )

    with c2:

        st.metric(
            "Generation Level",
            result["level"]
        )

    with c3:

        st.metric(
            "Efficiency",
            f"{result['efficiency']:.2f}%"
        )

    st.divider()

    # ======================================================
    # Generation Status
    # ======================================================

    level = result["level"]

    if "Excellent" in level:

        st.success(
            "🌞 Excellent solar generation expected."
        )

    elif "High" in level:

        st.info(
            "☀ High solar generation expected."
        )

    elif "Moderate" in level:

        st.warning(
            "⛅ Moderate solar generation expected."
        )

    else:

        st.error(
            "🌧 Low solar generation expected."
        )

    st.divider()

    # ======================================================
    # AI Recommendation
    # ======================================================

    st.subheader("🤖 AI Recommendation")

    st.info(
        result["recommendation"]
    )

    st.divider()

    # ======================================================
    # AI Insight
    # ======================================================

    st.subheader("💡 AI Insight")

    prediction = result["prediction"]

    if prediction >= 6:

        st.info(
            f"Solar generation is currently strong at "
            f"{prediction:.2f} kW. This is a suitable period "
            f"for battery charging and flexible high-power usage."
        )

    elif prediction >= 3:

        st.info(
            f"Solar generation is moderate at "
            f"{prediction:.2f} kW. Monitor generation before "
            f"using high-power appliances."
        )

    else:

        st.info(
            f"Solar generation is relatively low at "
            f"{prediction:.2f} kW. Consider reducing or "
            f"delaying flexible high-power usage."
        )

    st.divider()

    # ======================================================
    # Prediction Summary
    # ======================================================

    st.subheader("Prediction Summary")

    summary = pd.DataFrame({

        "Weather Parameter": [

            "Wind Speed",

            "Sunshine Duration",

            "Air Pressure",

            "Solar Radiation",

            "Temperature",

            "Humidity",

            "Hour",

            "Day",

            "Month"

        ],

        "Value": [

            f"{wind:.2f} m/s",

            f"{sunshine:.2f} hours",

            f"{pressure:.2f} hPa",

            f"{radiation:.2f} W/m²",

            f"{temperature:.2f} °C",

            f"{humidity:.0f}%",

            hour,

            day,

            month

        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================================
    # Download Report
    # ======================================================

    csv = summary.to_csv(
        index=False
    )

    st.download_button(

        "📥 Download Prediction Report",

        data=csv,

        file_name="solar_prediction.csv",

        mime="text/csv",

        use_container_width=True

    )
