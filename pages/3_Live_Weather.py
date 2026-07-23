import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

st.set_page_config(
    page_title="Live Weather",
    page_icon="🌦",
    layout="wide"
)

# ----------------------------
# API Configuration
# ----------------------------

API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ==========================================================
# Load CSS
# ==========================================================

css = Path("assets/style.css")

if css.exists():
    with open(css) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================================================
# Header
# ==========================================================

st.title("🌦 Live Weather")

st.write(
    "Fetch current weather conditions for any city."
)

st.divider()

# ==========================================================
# City Search
# ==========================================================

col1, col2 = st.columns([4,1])

with col1:
    city = st.text_input(
        "Enter City",
        placeholder="Example: Chennai"
    )

with col2:
    st.write("")
    st.write("")
    search = st.button(
        "Get Weather",
        use_container_width=True
    )

# ==========================================================
# Fetch Weather
# ==========================================================

if search:

    if city == "":
        st.warning("Please enter a city.")
        st.stop()

    if API_KEY == "":
        st.error("Weather API key is not configured.")
        st.stop()

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    with st.spinner("Fetching weather..."):

        try:

            response = requests.get(
                BASE_URL,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            weather = response.json()

        except Exception as e:

            st.error(f"Unable to fetch weather.\n\n{e}")
            st.stop()

    # ======================================================
    # Weather Data
    # ======================================================

    temp = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    pressure = weather["main"]["pressure"]
    wind = weather["wind"]["speed"]
    clouds = weather["clouds"]["all"]
    description = weather["weather"][0]["description"].title()
    sunrise = datetime.fromtimestamp(
        weather["sys"]["sunrise"]
    ).strftime("%H:%M")

    sunset = datetime.fromtimestamp(
        weather["sys"]["sunset"]
    ).strftime("%H:%M")

    st.success("Weather Retrieved Successfully")

    st.divider()

    # ======================================================
    # Weather Metrics
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🌡 Temperature",
            f"{temp} °C"
        )

    with c2:
        st.metric(
            "💧 Humidity",
            f"{humidity}%"
        )

    with c3:
        st.metric(
            "🌬 Wind Speed",
            f"{wind} m/s"
        )

    with c4:
        st.metric(
            "📈 Pressure",
            f"{pressure} hPa"
        )

    st.divider()

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric(
            "☁ Cloud Cover",
            f"{clouds}%"
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

    st.divider()

    # ======================================================
    # Description
    # ======================================================

    st.subheader("Weather Summary")

    st.info(description)

    st.divider()

    # ======================================================
    # Weather Table
    # ======================================================

    weather_df = pd.DataFrame({

        "Parameter":[
            "Temperature",
            "Humidity",
            "Pressure",
            "Wind Speed",
            "Cloud Cover",
            "Sunrise",
            "Sunset"
        ],

        "Value":[
            temp,
            humidity,
            pressure,
            wind,
            clouds,
            sunrise,
            sunset
        ]

    })

    st.dataframe(
        weather_df,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # Download
    # ======================================================

    st.download_button(
        "📥 Download Weather Report",
        weather_df.to_csv(index=False),
        "weather_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # Forecast Shortcut
    # ======================================================

    st.success(
        "Use these weather values on the Solar Forecast page to generate a prediction."
    )