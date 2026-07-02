# ============================================================
# Solar Power Forecast Agent
# Machine Learning + AI Agent
# Part 1 - Imports, UI and User Inputs
# ============================================================

# -----------------------------
# Import Libraries
# -----------------------------

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Solar Power Forecast Agent",
    page_icon="☀️",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

.block-container{
    padding-top:2rem;
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

# -----------------------------
# Load Model
# -----------------------------

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# -----------------------------
# Header
# -----------------------------

st.title("☀ Solar Power Forecast Agent")

st.write(
"""
Predict solar power generation using weather conditions and receive intelligent AI recommendations.
"""
)

st.markdown("---")

# -----------------------------
# Dashboard Cards
# -----------------------------

card1, card2, card3 = st.columns(3)

with card1:
    st.metric("Model", "XGBoost")

with card2:
    st.metric("Prediction", "Regression")

with card3:
    st.metric("Input Features", "9")

st.markdown("---")

# -----------------------------
# Weather Inputs
# -----------------------------

st.subheader("🌦 Weather Parameters")

left, right = st.columns(2)

with left:

    wind = st.number_input(
        "Wind Speed",
        min_value=0.0,
        max_value=50.0,
        value=3.5
    )

    sunshine = st.number_input(
        "Sunshine Duration",
        min_value=0.0,
        max_value=24.0,
        value=6.0
    )

    pressure = st.number_input(
        "Air Pressure",
        min_value=800.0,
        max_value=1100.0,
        value=1013.0
    )

    radiation = st.number_input(
        "Solar Radiation",
        min_value=0.0,
        value=450.0
    )

with right:

    temperature = st.number_input(
        "Air Temperature",
        value=28.0
    )

    humidity = st.number_input(
        "Relative Humidity",
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

# -----------------------------
# Predict Button
# -----------------------------

if st.button("🚀 Predict Solar Power"):

    # Create Input DataFrame
    input_data = pd.DataFrame({

        "WindSpeed":[wind],
        "Sunshine":[sunshine],
        "AirPressure":[pressure],
        "Radiation":[radiation],
        "AirTemperature":[temperature],
        "RelativeAirHumidity":[humidity],
        "Hour":[hour],
        "Day":[day],
        "Month":[month]

    })

    # Scale Data
    scaled_data = scaler.transform(input_data)

    # Predict
    prediction = model.predict(scaled_data)[0]

    st.markdown("---")

        # ============================================================
    # Dashboard Metrics
    # ============================================================

    metric1, metric2, metric3 = st.columns(3)

    # Predicted Power
    with metric1:

        st.metric(
            label="☀ Predicted Power",
            value=f"{prediction/1000:.2f} kW"
        )

    # Generation Level
    with metric2:

        if prediction >= 5000:

            level = "Excellent 🌞"

            status = "Excellent"

        elif prediction >= 2000:

            level = "High ☀"

            status = "High"

        elif prediction >= 500:

            level = "Moderate ⛅"

            status = "Moderate"

        else:

            level = "Low 🌙"

            status = "Low"

        st.metric(
            label="Generation Level",
            value=level
        )

    # Estimated Efficiency
    with metric3:

        efficiency = (prediction / 7701) * 100

        st.metric(
            label="Estimated Efficiency",
            value=f"{efficiency:.1f}%"
        )

    st.markdown("---")

    # ============================================================
    # AI Recommendation
    # ============================================================

    st.subheader("🤖 AI Recommendation")

    if prediction >= 5000:

        recommendation = """
### 🌞 Excellent Solar Generation

Recommendations

✅ Charge batteries to full capacity

✅ Export electricity to the power grid

✅ Charge electric vehicles

✅ Run washing machines

✅ Operate water heaters

✅ Schedule heavy electrical appliances
"""

    elif prediction >= 2000:

        recommendation = """
### ☀ High Solar Generation

Recommendations

✅ Charge battery storage

✅ Run household appliances

✅ Use air conditioning

✅ Export surplus electricity
"""

    elif prediction >= 500:

        recommendation = """
### ⛅ Moderate Solar Generation

Recommendations

✅ Use solar energy for daily household loads

✅ Charge electronic devices

✅ Store extra energy if possible

✅ Avoid multiple heavy appliances together
"""

    else:

        recommendation = """
### 🌙 Low Solar Generation

Recommendations

⚠ Reduce heavy electrical loads

⚠ Use battery backup

⚠ Import electricity from the grid

⚠ Delay high-power appliances
"""

    st.info(recommendation)

    # ============================================================
    # AI Insight
    # ============================================================

    st.subheader("🧠 AI Insight")

    if prediction >= 5000:

        st.success(
            "Excellent weather conditions detected. This is an ideal time to maximize solar energy generation and export excess electricity."
        )

    elif prediction >= 2000:

        st.info(
            "Good weather conditions detected. Solar generation should satisfy most household energy requirements."
        )

    elif prediction >= 500:

        st.warning(
            "Moderate solar generation expected. Consider avoiding multiple heavy electrical appliances simultaneously."
        )

    else:

        st.error(
            "Low solar generation expected due to weather conditions or time of day. Consider using stored battery power."
        )

    st.markdown("---")

    # ============================================================
    # Save Prediction History
    # ============================================================

    history_record = pd.DataFrame({

        "Date":[datetime.now().strftime("%Y-%m-%d")],

        "Time":[datetime.now().strftime("%H:%M:%S")],

        "Prediction (W)":[round(prediction,2)],

        "Generation Level":[status]

    })

    filename = "prediction_logs.csv"

    if os.path.exists(filename):

        history_record.to_csv(

            filename,

            mode="a",

            header=False,

            index=False

        )

    else:

        history_record.to_csv(

            filename,

            index=False

        )

    st.success("✅ Prediction saved successfully.")

    st.markdown("---")

        # ============================================================
    # Prediction Summary
    # ============================================================

    st.subheader("📋 Prediction Summary")

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

    st.markdown("---")

# ============================================================
# Prediction History
# ============================================================

st.subheader("📈 Prediction History")

filename = "prediction_logs.csv"

if os.path.exists(filename):

    history = pd.read_csv(filename)

    st.dataframe(
        history,
        use_container_width=True
    )

    st.markdown("---")

    # ============================================================
    # Dashboard Statistics
    # ============================================================

    st.subheader("📊 Dashboard Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Predictions",
            len(history)
        )

    with col2:

        avg_prediction = history["Prediction (W)"].mean()

        st.metric(
            "Average Prediction",
            f"{avg_prediction/1000:.2f} kW"
        )

    with col3:

        max_prediction = history["Prediction (W)"].max()

        st.metric(
            "Maximum Prediction",
            f"{max_prediction/1000:.2f} kW"
        )

    st.markdown("---")

    # ============================================================
    # Prediction Trend
    # ============================================================

    st.subheader("📉 Prediction Trend")

    trend = history.copy()

    trend.index = range(1, len(trend)+1)

    st.line_chart(
        trend["Prediction (W)"]
    )

    st.markdown("---")

    # ============================================================
    # Generation Level Distribution
    # ============================================================

    st.subheader("📊 Generation Level Distribution")

    level_counts = history["Generation Level"].value_counts()

    st.bar_chart(level_counts)

    st.markdown("---")

    # ============================================================
    # Recent Predictions
    # ============================================================

    st.subheader("🕒 Last Five Predictions")

    st.dataframe(

        history.tail(5),

        use_container_width=True

    )

    st.markdown("---")

    # ============================================================
    # Download CSV
    # ============================================================

    st.download_button(

        label="📥 Download Prediction History",

        data=history.to_csv(index=False),

        file_name="prediction_logs.csv",

        mime="text/csv"

    )

else:

    st.warning(
        "No prediction history available."
    )

st.markdown("---")

# ============================================================
# Project Information
# ============================================================

st.subheader("📚 Project Information")

left_info, right_info = st.columns(2)

with left_info:

    st.info("""
### Solar Power Forecast Agent

**Project Type**

Machine Learning + AI Agent

**Algorithm**

XGBoost Regressor

**Prediction**

Solar Power Generation

**Dataset**

8760 Hourly Records

**Target Variable**

SystemProduction
""")

with right_info:

    st.success("""
### Technologies Used

- Python
- Streamlit
- XGBoost
- Scikit-Learn
- Pandas
- NumPy
- Joblib
- Matplotlib
""")

st.markdown("---")

# ============================================================
# Model Performance
# ============================================================

st.subheader("📈 Model Summary")

performance = pd.DataFrame({

    "Property":[

        "Algorithm",

        "Problem Type",

        "Input Features",

        "Dataset Size",

        "Prediction Target"

    ],

    "Value":[

        "XGBoost",

        "Regression",

        "9",

        "8760",

        "SystemProduction"

    ]

})

st.dataframe(

    performance,

    use_container_width=True

)

st.markdown("---")

# ============================================================
# Weather Tips
# ============================================================

st.subheader("🌤 Weather Tips")

tip1, tip2 = st.columns(2)

with tip1:

    st.warning("""

☀ Higher Solar Radiation

➡ Higher Solar Generation

☀ Longer Sunshine Duration

➡ Better Energy Production

☀ Midday Hours

➡ Maximum Solar Output

""")

with tip2:

    st.info("""

🌧 Rainy Weather

➡ Lower Generation

☁ Heavy Cloud Cover

➡ Reduced Output

🌙 Night Time

➡ Zero Solar Production

""")

st.markdown("---")

# ============================================================
# AI Agent Capabilities
# ============================================================

st.subheader("🤖 AI Agent Features")

features = pd.DataFrame({

    "Capability":[

        "Solar Power Prediction",

        "Generation Level Detection",

        "AI Recommendation",

        "Prediction History",

        "Trend Visualization",

        "CSV Export"

    ],

    "Status":[

        "✅",

        "✅",

        "✅",

        "✅",

        "✅",

        "✅"

    ]

})

st.dataframe(

    features,

    use_container_width=True,

    hide_index=True

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
Machine Learning • Artificial Intelligence • Streamlit Dashboard
</h4>

<hr>

<p>

Developed using

<b>Python</b> |

<b>XGBoost</b> |

<b>Scikit-Learn</b> |

<b>Streamlit</b>

</p>

</div>
""",

unsafe_allow_html=True

)

st.caption(

"© 2026 Solar Power Forecast Agent | Developed using Machine Learning and Artificial Intelligence"

)
