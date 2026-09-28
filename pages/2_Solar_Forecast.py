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
    "Predict solar power generation using current weather "
    "conditions and solar parameters."
)

st.divider()

# ==========================================================
# City Selection
# ==========================================================

st.subheader("📍 Weather Location")

city = st.text_input(
    "Enter City",
    placeholder="Example: Vijayawada"
)

# ==========================================================
# Get Current Weather
# ==========================================================

weather = None

if city:

    if OPENWEATHER_API_KEY == "":

        st.error(
            "Weather API key is not configured."
        )

    else:

        with st.spinner(
            "Fetching current weather..."
        ):

            try:

                params = {
                    "q": city,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric"
                }

                response = requests.get(
                    OPENWEATHER_URL,
                    params=params,
                    timeout=20
                )

                response.raise_for_status()

                weather = response.json()

            except Exception as e:

                st.error(
                    f"Unable to fetch weather.\n\n{e}"
                )

# ==========================================================
# Current Weather Values
# ==========================================================

now = datetime.now()

if weather:

    # ------------------------------------------------------
    # Values from OpenWeather
    # ------------------------------------------------------

    temperature = float(
        weather["main"]["temp"]
    )

    humidity = float(
        weather["main"]["humidity"]
    )

    pressure = float(
        weather["main"]["pressure"]
    )

    wind = float(
        weather["wind"]["speed"]
    )

    cloud_cover = float(
        weather["clouds"]["all"]
    )

    description = (
        weather["weather"][0]["description"]
        .title()
    )

    sunrise = datetime.fromtimestamp(
        weather["sys"]["sunrise"]
    ).strftime("%H:%M")

    sunset = datetime.fromtimestamp(
        weather["sys"]["sunset"]
    ).strftime("%H:%M")

    # ------------------------------------------------------
    # Current date/time
    # ------------------------------------------------------

    hour = now.hour
    day = now.day
    month = now.month

    st.success(
        f"Current weather loaded for {city}."
    )

    # ======================================================
    # Current Weather Display
    # ======================================================

    st.subheader("🌦 Current Weather")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🌡 Temperature",
            f"{temperature:.2f} °C"
        )

    with c2:

        st.metric(
            "💧 Humidity",
            f"{humidity:.0f}%"
        )

    with c3:

        st.metric(
            "🌬 Wind Speed",
            f"{wind:.1f} m/s"
        )

    with c4:

        st.metric(
            "📈 Air Pressure",
            f"{pressure:.0f} hPa"
        )

    c5, c6, c7 = st.columns(3)

    with c5:

        st.metric(
            "☁ Cloud Cover",
            f"{cloud_cover:.0f}%"
        )

    with c6:

        st.metric(
            "🌅 Sunrise",
            sunrise
        )

    with c7:

        st.metric(
            "🌇 Sunset",
            sunset
        )

    st.info(
        f"Weather condition: **{description}**"
    )

else:

    st.info(
        "Enter a city above to load current weather "
        "parameters."
    )

    # Default values are only used until weather is loaded.
    temperature = 28.0
    humidity = 60.0
    pressure = 1013.0
    wind = 3.5
    cloud_cover = 0.0

    hour = now.hour
    day = now.day
    month = now.month

st.divider()

# ==========================================================
# Weather Parameters
# ==========================================================

st.subheader("🌦 Weather Parameters")

st.caption(
    "Temperature, humidity, wind speed and air pressure "
    "are automatically synchronized with the current weather."
)

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
        step=0.1,
        help=(
            "OpenWeather current-weather endpoint does not "
            "provide sunshine duration."
        )
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
        step=1.0,
        help=(
            "OpenWeather current-weather endpoint does not "
            "provide solar radiation."
        )
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
        value=int(hour)
    )

    day_input = st.slider(
        "Day",
        min_value=1,
        max_value=31,
        value=int(day)
    )

    month_input = st.slider(
        "Month",
        min_value=1,
        max_value=12,
        value=int(month)
    )

st.divider()

# ==========================================================
# Synchronization Notice
# ==========================================================

st.subheader("🔄 Weather Synchronization")

st.success(
    "The following values are synchronized with Live Weather: "
    "Temperature, Humidity, Wind Speed and Air Pressure."
)

st.warning(
    "Solar Radiation and Sunshine Duration are currently "
    "manual inputs because the OpenWeather endpoint used "
    "by this application does not provide those values."
)

st.divider()

# ==========================================================
# Forecast Button
# ==========================================================

if st.button(
    "🚀 Forecast Solar Power",
    use_container_width=True
):

    # ------------------------------------------------------
    # Prediction Payload
    # ------------------------------------------------------

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
    # Prediction Completed
    # ======================================================

    st.success(
        "Prediction Completed Successfully"
    )

    st.divider()

    # ======================================================
    # Forecast Result
    # ======================================================

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
    # Dynamic AI Insight
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

            "Air Temperature",

            "Relative Humidity",

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
    # Download Prediction Report
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
