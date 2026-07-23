import streamlit as st
import requests
import pandas as pd
from pathlib import Path

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
    with open(css) as f:
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
# Weather Input
# ==========================================================

st.subheader("🌦 Weather Parameters")

left, right = st.columns(2)

with left:

    wind = st.number_input(
        "Wind Speed (m/s)",
        min_value=0.0,
        max_value=50.0,
        value=3.5
    )

    sunshine = st.number_input(
        "Sunshine Duration (Hours)",
        min_value=0.0,
        max_value=24.0,
        value=6.0
    )

    pressure = st.number_input(
        "Air Pressure (hPa)",
        min_value=800.0,
        max_value=1100.0,
        value=1013.0
    )

    radiation = st.number_input(
        "Solar Radiation (W/m²)",
        min_value=0.0,
        value=450.0
    )

with right:

    temperature = st.number_input(
        "Air Temperature (°C)",
        value=28.0
    )

    humidity = st.number_input(
        "Relative Humidity (%)",
        value=60.0
    )

    hour = st.slider(
        "Hour",
        0,
        23,
        12
    )

    day = st.slider(
        "Day",
        1,
        31,
        15
    )

    month = st.slider(
        "Month",
        1,
        12,
        6
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

                f"{API_URL}/forecast",

                json={

                    "wind": wind,

                    "sunshine": sunshine,

                    "pressure": pressure,

                    "radiation": radiation,

                    "temperature": temperature,

                    "humidity": humidity,

                    "hour": hour,

                    "day": day,

                    "month": month

                },

                timeout=20

            )

            response.raise_for_status()

            result = response.json()

        except Exception as e:

            st.error(f"Prediction Failed\n\n{e}")

            st.stop()

    st.success("Prediction Completed Successfully")

    st.divider()

    # ======================================================
    # Result Cards
    # ======================================================

    st.subheader("Forecast Result")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Predicted Power",

            f"{result['prediction']/1000:.2f} kW"

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

    st.info(result["recommendation"])

    st.divider()

    # ======================================================
    # AI Insight
    # ======================================================

    st.subheader("💡 AI Insight")

    st.success(result["insight"])

    st.divider()

    # ======================================================
    # Prediction Summary
    # ======================================================

    st.subheader("Prediction Summary")

    summary = pd.DataFrame({

        "Weather Parameter":[

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

        "Value":[

            wind,

            sunshine,

            pressure,

            radiation,

            temperature,

            humidity,

            hour,

            day,

            month

        ]

    })

    st.dataframe(

        summary,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # Download Report
    # ======================================================

    csv = summary.to_csv(index=False)

    st.download_button(

        "📥 Download Prediction Report",

        data=csv,

        file_name="solar_prediction.csv",

        mime="text/csv",

        use_container_width=True

    )