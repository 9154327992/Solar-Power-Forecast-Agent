import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

API_URL = "https://solar-power-forecast-agent.onrender.com"

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
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

st.title("📜 Prediction History")

st.write(
    "View, search, filter, and export previous solar power predictions."
)

st.divider()

# ==========================================================
# Load History
# ==========================================================

try:

    response = requests.get(
        f"{API_URL}/history",
        timeout=20
    )

    response.raise_for_status()

    history = pd.DataFrame(response.json())

except Exception as e:

    st.error(f"Unable to load prediction history.\n\n{e}")

    st.stop()

# ==========================================================
# Empty History
# ==========================================================

if history.empty:

    st.warning("No prediction history available.")

    st.stop()

# ==========================================================
# Dashboard Statistics
# ==========================================================

st.subheader("📊 Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Predictions",
        len(history)
    )

with c2:

    st.metric(
        "Average Power",
        f"{history['predicted_power'].mean()/1000:.2f} kW"
    )

with c3:

    st.metric(
        "Maximum Power",
        f"{history['predicted_power'].max()/1000:.2f} kW"
    )

with c4:

    st.metric(
        "Minimum Power",
        f"{history['predicted_power'].min()/1000:.2f} kW"
    )

st.divider()

# ==========================================================
# Search & Filter
# ==========================================================

st.subheader("🔍 Search")

left, right = st.columns(2)

with left:

    keyword = st.text_input(
        "Search"
    )

with right:

    levels = ["All"] + sorted(
        history["generation_level"].unique().tolist()
    )

    selected = st.selectbox(
        "Generation Level",
        levels
    )

filtered = history.copy()

if keyword:

    filtered = filtered[
        filtered.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                keyword,
                case=False
            ).any(),
            axis=1
        )
    ]

if selected != "All":

    filtered = filtered[
        filtered["generation_level"] == selected
    ]

st.divider()

# ==========================================================
# Prediction Table
# ==========================================================

st.subheader("📋 Prediction Records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# Last Five Predictions
# ==========================================================

st.subheader("🕒 Last Five Predictions")

st.dataframe(

    history.tail(5),

    use_container_width=True,

    hide_index=True

)

st.divider()

# ==========================================================
# Download History
# ==========================================================

st.subheader("⬇ Download")

csv = filtered.to_csv(index=False)

st.download_button(

    "Download CSV",

    csv,

    "prediction_history.csv",

    "text/csv",

    use_container_width=True

)

st.divider()

# ==========================================================
# Delete History
# ==========================================================

st.subheader("🗑 Delete History")

confirm = st.checkbox(
    "I understand this action cannot be undone."
)

if confirm:

    if st.button(
        "Delete All History",
        type="primary",
        use_container_width=True
    ):

        try:

            response = requests.delete(

                f"{API_URL}/history"

            )

            response.raise_for_status()

            st.success(
                "Prediction history deleted successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(e)

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.caption(
    "Solar Power Forecast Agent • Prediction History"
)