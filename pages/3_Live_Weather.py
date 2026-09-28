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

# ==========================================================
# API Configuration
# ==========================================================

API_KEY = st.secrets.get(
    "OPENWEATHER_API_KEY",
    ""
)

BASE_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

# ==========================================================
# Load CSS
# ==========================================================

css = Path("assets/style.css")

if css.exists():

    with open(
        css,
        encoding="utf-8"
    ) as f:

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

st.subheader("📍 City Search")

with st.form(
    "weather_search_form",
    clear_on_submit=False
):

    col1, col2 = st.columns(
        [4, 1]
    )

    with col1:

        city = st.text_input(
            "Enter City",
            placeholder="Example: Chennai",
            key="weather_city"
        )

    with col2:

        st.write("")
        st.write("")

        search = st.form_submit_button(
            "Get Weather",
            use_container_width=True
        )

# ==========================================================
# Fetch Weather
# ==========================================================

if search:

    city = city.strip()

    # ------------------------------------------------------
    # Validate City
    # ------------------------------------------------------

    if city == "":

        st.warning(
            "Please enter a city."
        )

        st.stop()

    # ------------------------------------------------------
    # Validate API Key
    # ------------------------------------------------------

    if API_KEY == "":

        st.error(
            "Weather API key is not configured."
        )

        st.stop()

    # ------------------------------------------------------
    # OpenWeather Parameters
    # ------------------------------------------------------

    params = {

        "q": city,

        "appid": API_KEY,

        "units": "metric"

    }

    # ------------------------------------------------------
    # API Request
    # ------------------------------------------------------

    with st.spinner(
        "Fetching weather..."
    ):

        try:

            response = requests.get(

                BASE_URL,

                params=params,

                timeout=20

            )

            response.raise_for_status()

            weather = response.json()

        except requests.exceptions.HTTPError:

            try:

                error_data = response.json()

                message = error_data.get(
                    "message",
                    "City not found."
                )

            except Exception:

                message = (
                    "Unable to find the requested city."
                )

            st.error(
                f"Weather request failed: {message}"
            )

            st.stop()

        except requests.exceptions.Timeout:

            st.error(
                "Weather service timed out. "
                "Please try again."
            )

            st.stop()

        except requests.exceptions.RequestException as e:

            st.error(
                f"Unable to fetch weather.\n\n{e}"
            )

            st.stop()

        except Exception as e:

            st.error(
                f"Unexpected error.\n\n{e}"
            )

            st.stop()

    # ======================================================
    # Weather Data
    # ======================================================

    try:

        temp = float(
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

        clouds = float(
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

    except (KeyError, TypeError, ValueError) as e:

        st.error(
            f"Weather data format was unexpected.\n\n{e}"
        )

        st.stop()

    # ======================================================
    # Save Weather Data
    # ======================================================

    st.session_state["live_weather"] = {

        "city": city,

        "temperature": temp,

        "humidity": humidity,

        "pressure": pressure,

        "wind": wind,

        "cloud_cover": clouds,

        "sunrise": sunrise,

        "sunset": sunset

    }

    # ======================================================
    # Success Message
    # ======================================================

    st.success(
        f"Weather Retrieved Successfully for {city}"
    )

    st.divider()

    # ======================================================
    # Weather Metrics
    # ======================================================

    st.subheader("🌦 Current Weather")

    c1, c2, c3, c4 = st.columns(4)

    # ------------------------------------------------------
    # Temperature
    # ------------------------------------------------------

    with c1:

        st.metric(
            "🌡 Temperature",
            f"{temp:.2f} °C"
        )

    # ------------------------------------------------------
    # Humidity
    # ------------------------------------------------------

    with c2:

        st.metric(
            "💧 Humidity",
            f"{humidity:.0f}%"
        )

    # ------------------------------------------------------
    # Wind
    # ------------------------------------------------------

    with c3:

        st.metric(
            "🌬 Wind Speed",
            f"{wind:.1f} m/s"
        )

    # ------------------------------------------------------
    # Pressure
    # ------------------------------------------------------

    with c4:

        st.metric(
            "📈 Pressure",
            f"{pressure:.0f} hPa"
        )

    st.divider()

    # ======================================================
    # Additional Weather Metrics
    # ======================================================

    c5, c6, c7 = st.columns(3)

    # ------------------------------------------------------
    # Cloud Cover
    # ------------------------------------------------------

    with c5:

        st.metric(
            "☁ Cloud Cover",
            f"{clouds:.0f}%"
        )

    # ------------------------------------------------------
    # Sunrise
    # ------------------------------------------------------

    with c6:

        st.metric(
            "🌅 Sunrise",
            sunrise
        )

    # ------------------------------------------------------
    # Sunset
    # ------------------------------------------------------

    with c7:

        st.metric(
            "🌇 Sunset",
            sunset
        )

    st.divider()

    # ======================================================
    # Weather Summary
    # ======================================================

    st.subheader("Weather Summary")

    st.info(
        description
    )

    st.divider()

    # ======================================================
    # Weather Table
    # ======================================================

    st.subheader("📋 Weather Details")

    weather_df = pd.DataFrame({

        "Parameter": [

            "Temperature",

            "Humidity",

            "Pressure",

            "Wind Speed",

            "Cloud Cover",

            "Sunrise",

            "Sunset"

        ],

        "Value": [

            f"{temp:.2f} °C",

            f"{humidity:.0f}%",

            f"{pressure:.0f} hPa",

            f"{wind:.1f} m/s",

            f"{clouds:.0f}%",

            sunrise,

            sunset

        ]

    })

    st.dataframe(

        weather_df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ======================================================
    # Download Weather Report
    # ======================================================

    st.download_button(

        "📥 Download Weather Report",

        data=weather_df.to_csv(
            index=False
        ),

        file_name="weather_report.csv",

        mime="text/csv",

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # Forecast Shortcut
    # ======================================================

    st.success(
        "Use these weather values on the Solar Forecast "
        "page to generate a prediction."
    )

# ==========================================================
# Existing Weather Data
# ==========================================================

elif "live_weather" in st.session_state:

    saved_weather = st.session_state[
        "live_weather"
    ]

    st.info(
        f"Showing the last retrieved weather for "
        f"**{saved_weather['city']}**."
    )
