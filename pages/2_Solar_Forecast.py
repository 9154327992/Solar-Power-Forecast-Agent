import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

OPENWEATHER_API_KEY = st.secrets.get(
    "OPENWEATHER_API_KEY",
    ""
)

OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

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
# Header
# ==========================================================

st.title("☀ Solar Power Forecast")

st.write(
    "Predict solar power generation using weather parameters."
)

st.divider()

# ==========================================================
# Live Weather
# ==========================================================

st.subheader("🌦 Live Weather")

# Get city from previous Live Weather page
live_weather = st.session_state.get(
    "live_weather",
    None
)

# If Live Weather data exists, use it
if live_weather:

    temperature = float(
        live_weather["temperature"]
    )

    humidity = float(
        live_weather["humidity"]
    )

    wind = float(
        live_weather["wind"]
    )

    pressure = float(
        live_weather["pressure"]
    )

    cloud_cover = float(
        live_weather["cloud_cover"]
    )

else:

    # ------------------------------------------------------
    # No previous Live Weather data
    # ------------------------------------------------------

    temperature = None
    humidity = None
    wind = None
    pressure = None
    cloud_cover = None

# ==========================================================
# Live Weather Display
# ==========================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "🌡 Temperature",
        f"{temperature:.2f} °C"
        if temperature is not None
        else "--"
    )

with c2:

    st.metric(
        "💧 Humidity",
        f"{humidity:.0f}%"
        if humidity is not None
        else "--"
    )

with c3:

    st.metric(
        "🌬 Wind Speed",
        f"{wind:.1f} m/s"
        if wind is not None
        else "--"
    )

with c4:

    st.metric(
        "📈 Air Pressure",
        f"{pressure:.0f} hPa"
        if pressure is not None
        else "--"
    )

with c5:

    st.metric(
        "☁ Cloud Cover",
        f"{cloud_cover:.0f}%"
        if cloud_cover is not None
        else "--"
    )

st.divider()

# ==========================================================
# Weather Parameters
# ==========================================================

st.subheader("🌦 Weather Parameters")

# ==========================================================
# Fallback Values
# ==========================================================

if wind is None:
    wind = 3.5

if temperature is None:
    temperature = 28.0

if humidity is None:
    humidity = 60.0

if pressure is None:
    pressure = 1013.0

# Current date/time
now = datetime.now()

# ==========================================================
# Parameter Inputs
# ==========================================================

left, right = st.columns(2)

# ==========================================================
# Left Column
# ==========================================================

with left:

    wind_input = st.number_input(
        "Wind Speed (m/s)",
        min_value=0.0,
        max_value=50.0,
        value=float(wind),
        step=0.1
    )

    sunshine = st.number_input(
        "Sunshine Duration (Hours)",
        min_value=0.0,
        max_value=24.0,
        value=6.0,
        step=0.1
    )

    pressure_input = st.number_input(
        "Air Pressure (hPa)",
        min_value=800.0,
        max_value=1100.0,
        value=float(pressure),
        step=0.1
    )

    radiation = st.number_input(
        "Solar Radiation (W/m²)",
        min_value=0.0,
        max_value=1500.0,
        value=450.0,
        step=1.0
    )

# ==========================================================
# Right Column
# ==========================================================

with right:

    temperature_input = st.number_input(
        "Air Temperature (°C)",
        value=float(temperature),
        step=0.1
    )

    humidity_input = st.number_input(
        "Relative Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(humidity),
        step=1.0
    )

    hour_input = st.slider(
        "Hour",
        min_value=0,
        max_value=23,
        value=now.hour
    )

    day_input = st.slider(
        "Day",
        min_value=1,
        max_value=31,
        value=now.day
    )

    month_input = st.slider(
        "Month",
        min_value=1,
        max_value=12,
        value=now.month
    )

st.divider()

# ==========================================================
# Forecast Button
# ==========================================================

if st.button(
    "🚀 Forecast Solar Power",
    use_container_width=True
):

    payload = {

        "wind_speed": wind_input,

        "sunshine_duration": sunshine,

        "air_pressure": pressure_input,

        "solar_radiation": radiation,

        "air_temperature": temperature_input,

        "relative_humidity": humidity_input,

        "hour": hour_input,

        "day": day_input,

        "month": month_input

    }

    with st.spinner(
        "Predicting Solar Power..."
    ):

        try:

            response = requests.post(

                f"{API_URL}/api/predict/forecast",

                json=payload,

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
    # Result
    # ======================================================

    st.success(
        "Prediction Completed Successfully"
    )

    st.divider()

    st.subheader("☀️ Forecast Result")

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
            "☀️ High solar generation expected."
        )

    elif "Moderate" in level:

        st.warning(
            "⛅ Moderate solar generation expected."
        )

    else:

        st.error(
            "🌧️ Low solar generation expected."
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

    prediction = float(
        result["prediction"]
    )

    if prediction >= 6:

        st.success(
            f"Solar generation is strong at "
            f"**{prediction:.2f} kW**. "
            "This is a suitable period for battery charging "
            "and flexible high-power usage."
        )

    elif prediction >= 3:

        st.warning(
            f"Solar generation is moderate at "
            f"**{prediction:.2f} kW**. "
            "Monitor generation before using high-power "
            "appliances."
        )

    else:

        st.error(
            f"Solar generation is relatively low at "
            f"**{prediction:.2f} kW**. "
            "Consider reducing or delaying flexible "
            "high-power usage."
        )

    st.divider()

    # ======================================================
    # Prediction Summary
    # ======================================================

    st.subheader("📋 Prediction Summary")

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

            f"{wind_input:.2f} m/s",
            f"{sunshine:.2f} hours",
            f"{pressure_input:.2f} hPa",
            f"{radiation:.2f} W/m²",
            f"{temperature_input:.2f} °C",
            f"{humidity_input:.0f}%",
            hour_input,
            day_input,
            month_input

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
