# ============================================================
# dashboard.py
# Streamlit Dashboard Components
# ============================================================

import streamlit as st


class Dashboard:

    @staticmethod
    def page_config():

        st.set_page_config(
            page_title="Solar Power Forecast Agent",
            page_icon="☀️",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    @staticmethod
    def header():

        st.markdown(
            """
            <h1 class="main-title">
            ☀️ Solar Power Forecast Agent
            </h1>

            <p class="subtitle">
            AI-Based Solar Energy Forecasting System
            </p>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def metric(title, value):

        st.markdown(
            f"""
            <div class="metric">
                <h2>{value}</h2>
                <p>{title}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    @staticmethod
    def prediction_card(result):

        st.markdown("### Prediction Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Solar Power",
                f"{result['prediction']:.2f} W"
            )

        with col2:
            st.metric(
                "Efficiency",
                f"{result['efficiency']}%"
            )

        with col3:
            st.metric(
                "Level",
                result["level"]
            )

        st.success(result["recommendation"])

    @staticmethod
    def weather_card(weather):

        st.markdown("### Current Weather")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Temperature",
                f"{weather['temperature']} °C"
            )

            st.metric(
                "Humidity",
                f"{weather['humidity']} %"
            )

        with col2:
            st.metric(
                "Pressure",
                f"{weather['pressure']} hPa"
            )

            st.metric(
                "Wind",
                f"{weather['wind_speed']} m/s"
            )

        with col3:
            st.metric(
                "Cloud Cover",
                f"{weather['cloud_cover']} %"
            )

            st.metric(
                "Condition",
                weather["description"]
            )

    @staticmethod
    def footer():

        st.markdown(
            """
            <hr>

            <div class="footer">
            © 2026 Solar Power Forecast Agent |
            Powered by AI & Machine Learning
            </div>
            """,
            unsafe_allow_html=True
        )


dashboard = Dashboard()