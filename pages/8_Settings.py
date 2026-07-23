import streamlit as st
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
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
# Session State Defaults
# ==========================================================

defaults = {
    "theme": "Light",
    "units": "Metric",
    "notifications": True,
    "auto_refresh": False,
    "refresh_interval": 30,
    "api_url": "https://solar-power-forecast-agent.onrender.com"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# Header
# ==========================================================

st.title("⚙️ Settings")

st.write(
    "Customize your Solar Power Forecast Agent experience."
)

st.divider()

# ==========================================================
# Appearance
# ==========================================================

st.subheader("🎨 Appearance")

theme = st.selectbox(
    "Application Theme",
    ["Light", "Dark", "System"],
    index=["Light", "Dark", "System"].index(st.session_state.theme)
)

units = st.selectbox(
    "Measurement Units",
    ["Metric", "Imperial"],
    index=["Metric", "Imperial"].index(st.session_state.units)
)

st.divider()

# ==========================================================
# Notifications
# ==========================================================

st.subheader("🔔 Notifications")

notifications = st.toggle(
    "Enable Notifications",
    value=st.session_state.notifications
)

auto_refresh = st.toggle(
    "Enable Auto Refresh",
    value=st.session_state.auto_refresh
)

refresh_interval = st.slider(
    "Refresh Interval (seconds)",
    10,
    300,
    st.session_state.refresh_interval,
    step=10
)

st.divider()

# ==========================================================
# API Configuration
# ==========================================================

st.subheader("🌐 Backend Configuration")

api_url = st.text_input(
    "Backend API URL",
    value=st.session_state.api_url
)

st.caption(
    "Example: https://solar-power-forecast-agent.onrender.com"
)

st.divider()

# ==========================================================
# About Application
# ==========================================================

st.subheader("ℹ️ Application Information")

st.info("""
**Solar Power Forecast Agent**

Version: **1.0.0**

Machine Learning Model: **XGBoost Regressor**

Frameworks:
- Streamlit
- FastAPI
- XGBoost
- SQLite
- Plotly
""")

st.divider()

# ==========================================================
# Save Settings
# ==========================================================

if st.button(
    "💾 Save Settings",
    use_container_width=True
):

    st.session_state.theme = theme
    st.session_state.units = units
    st.session_state.notifications = notifications
    st.session_state.auto_refresh = auto_refresh
    st.session_state.refresh_interval = refresh_interval
    st.session_state.api_url = api_url

    st.success("Settings saved successfully!")

st.divider()

# ==========================================================
# Reset Settings
# ==========================================================

if st.button(
    "🔄 Reset to Default",
    use_container_width=True
):

    for key, value in defaults.items():
        st.session_state[key] = value

    st.success("Settings restored to default values.")
    st.rerun()

st.divider()

# ==========================================================
# Current Settings
# ==========================================================

st.subheader("📋 Current Configuration")

st.json({
    "Theme": st.session_state.theme,
    "Units": st.session_state.units,
    "Notifications": st.session_state.notifications,
    "Auto Refresh": st.session_state.auto_refresh,
    "Refresh Interval": st.session_state.refresh_interval,
    "API URL": st.session_state.api_url
})

st.divider()

# ==========================================================
# Footer
# ==========================================================

st.caption(
    "Solar Power Forecast Agent • Settings"
)