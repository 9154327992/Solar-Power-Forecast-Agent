# ------------------------------------------------------------
# Import Streamlit Library
# ------------------------------------------------------------

import streamlit as st

# ------------------------------------------------------------
# Import Requests Library
# ------------------------------------------------------------

import requests

# ------------------------------------------------------------
# Import Pandas Library
# ------------------------------------------------------------

import pandas as pd

API_URL = "https://solar-power-forecast-agent.onrender.com"

# ============================================================
# Configure Streamlit Page
# ============================================================

st.set_page_config(

    page_title="Solar Power Forecast Agent",

    page_icon="☀️",

    layout="wide"

)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""

<style>

.block-container{

    padding-top:1rem;

}

h1{

    color:#FDB813;

}

[data-testid="stMetric"]{

    background-color:#1c1f26;

    padding:15px;

    border-radius:12px;

    border:1px solid #333333;

}

</style>

""", unsafe_allow_html=True)

# ============================================================
# Page Title
# ============================================================

st.title("☀ Solar Power Forecast Agent")

# ============================================================
# Page Description
# ============================================================

st.write(

    "AI-powered Solar Power Forecasting and Energy Recommendation System."

)

st.markdown("---")

# ============================================================
# Dashboard Cards
# ============================================================

card1, card2, card3 = st.columns(3)

with card1:

    st.metric(

        "Model",

        "XGBoost"

    )

with card2:

    st.metric(

        "Prediction",

        "Regression"

    )

with card3:

    st.metric(

        "Input Features",

        "9"

    )

st.markdown("---")

# ============================================================
# Weather Parameters
# ============================================================

st.subheader("🌦 Weather Parameters")

left, right = st.columns(2)

# ------------------------------------------------------------
# Left Column Inputs
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Right Column Inputs
# ------------------------------------------------------------

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

st.markdown("---")

# ============================================================
# Forecast Solar Power
# ============================================================

if st.button("🚀 Forecast Solar Power"):

    # --------------------------------------------------------
    # Send Data to FastAPI Backend
    # --------------------------------------------------------

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

        }

    )

    # --------------------------------------------------------
    # Check API Response
    # --------------------------------------------------------

    if response.status_code == 200:

        result = response.json()

    else:

        st.error("Unable to connect to FastAPI Backend.")

        st.write(response.text)

        st.stop()

    # --------------------------------------------------------
    # Forecast Report
    # --------------------------------------------------------

    st.subheader("Forecast Report")

    col1, col2, col3 = st.columns(3)

    # Predicted Power

    with col1:

        st.metric(

            "Predicted Power",

            f"{result['prediction']/1000:.2f} kW"

        )

    # Generation Level

    with col2:

        st.metric(

            "Generation Level",

            result["level"]

        )

    # Estimated Efficiency

    with col3:

        st.metric(

            "Estimated Efficiency",

            f"{result['efficiency']:.2f}%"

        )

    # --------------------------------------------------------
    # Generation Status
    # --------------------------------------------------------

    if result["level"] == "Excellent 🌞":

        st.success(

            "Excellent solar power generation is expected."

        )

    elif result["level"] == "High ☀":

        st.info(

            "High solar power generation is expected."

        )

    elif result["level"] == "Moderate ⛅":

        st.warning(

            "Moderate solar power generation is expected."

        )

    else:

        st.error(

            "Low solar power generation is expected."

        )

    st.markdown("---")

    # --------------------------------------------------------
    # AI Recommendation
    # --------------------------------------------------------

    st.subheader("AI Recommendation")

    st.info(

        result["recommendation"]

    )

    st.markdown("---")

    # --------------------------------------------------------
    # AI Insight
    # --------------------------------------------------------

    st.subheader("AI Insight")

    st.success(

        result["insight"]

    )

    st.markdown("---")

    # --------------------------------------------------------
    # Prediction Summary
    # --------------------------------------------------------

    st.subheader("Prediction Summary")

    summary = pd.DataFrame({

        "Weather Parameter":[

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

        "Input Value":[

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

    st.success(

        "Prediction completed successfully."

    )

st.markdown("---")

# ============================================================
# View Prediction History
# ============================================================

st.subheader("Prediction History")

if st.button("View Prediction History"):

    # --------------------------------------------------------
    # Retrieve Prediction History
    # --------------------------------------------------------

    response = requests.get(

        f"{API_URL}/history"

    )

    # Check Response

    if response.status_code == 200:

        history = pd.DataFrame(

            response.json()

        )

    else:

        st.error(

            "Unable to retrieve prediction history."

        )

        st.write(

            response.text

        )

        st.stop()

    # --------------------------------------------------------
    # Check History Availability
    # --------------------------------------------------------

    if len(history) > 0:

        # Display History

        st.dataframe(

            history,

            use_container_width=True

        )

        st.markdown("---")

        # ====================================================
        # Dashboard Statistics
        # ====================================================

        st.subheader("Dashboard Statistics")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Total Predictions",

                len(history)

            )

        with c2:

            st.metric(

                "Average Prediction",

                f"{history['predicted_power'].mean()/1000:.2f} kW"

            )

        with c3:

            st.metric(

                "Maximum Prediction",

                f"{history['predicted_power'].max()/1000:.2f} kW"

            )

        st.markdown("---")

        # ====================================================
        # Prediction Trend
        # ====================================================

        st.subheader("Prediction Trend")

        trend = history.copy()

        trend.index = range(

            1,

            len(trend)+1

        )

        st.line_chart(

            trend["predicted_power"]

        )

        st.markdown("---")

        # ====================================================
        # Generation Level Distribution
        # ====================================================

        st.subheader("Generation Level Distribution")

        st.bar_chart(

            history["generation_level"].value_counts()

        )

        st.markdown("---")

        # ====================================================
        # Last Five Predictions
        # ====================================================

        st.subheader("Last Five Predictions")

        st.dataframe(

            history.tail(

                5

            ),

            use_container_width=True

        )

        st.markdown("---")

        # ====================================================
        # Download Prediction History
        # ====================================================

        st.download_button(

            label="Download Prediction History",

            data=history.to_csv(

                index=False

            ),

            file_name="prediction_history.csv",

            mime="text/csv"

        )

    else:

        st.warning(

            "No prediction history available."

        )

st.markdown("---")

# ============================================================
# Footer
# ============================================================

st.markdown(

"""

<div style="text-align:center">

<h2>☀ Solar Power Forecast Agent</h2>

<h4>

Machine Learning • Artificial Intelligence • FastAPI • Streamlit

</h4>

<hr>

<p>

Developed using

<b>Python</b> |

<b>FastAPI</b> |

<b>XGBoost</b> |

<b>SQLite</b> |

<b>Streamlit</b>

</p>

</div>

""",

unsafe_allow_html=True

)

st.caption(

"© 2026 Solar Power Forecast Agent | Developed using Machine Learning, FastAPI and Artificial Intelligence"

)
