from fastapi import APIRouter
from pydantic import BaseModel
import re

router = APIRouter()


class AssistantRequest(BaseModel):
    question: str


def contains_any(text: str, words: list[str]) -> bool:
    return any(word in text for word in words)


def clean_question(question: str) -> str:
    question = question.lower().strip()
    question = re.sub(r"\s+", " ", question)
    return question


def generate_answer(question: str) -> str:
    q = clean_question(question)

    # ==========================================================
    # GREETING
    # ==========================================================

    if contains_any(q, [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return (
            "Hello! ☀️ I'm your Solar Energy Assistant.\n\n"
            "I can help you with:\n"
            "• Solar generation and forecasts\n"
            "• Battery charging\n"
            "• Weather conditions\n"
            "• Appliance scheduling\n"
            "• Energy-saving recommendations\n"
            "• Solar panel maintenance\n"
            "• The XGBoost forecasting model\n"
            "• Daily energy reports\n\n"
            "What would you like to know?"
        )

    # ==========================================================
    # THANK YOU
    # ==========================================================

    if contains_any(q, [
        "thank you",
        "thanks",
        "thank"
    ]):
        return (
            "You're welcome! ☀️\n\n"
            "I'm here whenever you need help with your solar "
            "forecast, battery, weather, or energy usage."
        )

    # ==========================================================
    # MACHINE LEARNING / MODEL
    # ==========================================================

    if contains_any(q, [
        "xgboost",
        "machine learning",
        "machine model",
        "ml model",
        "ml",
        "model",
        "algorithm",
        "how does the model work"
    ]):
        return (
            "🤖 **Machine Learning Model**\n\n"
            "This project uses an **XGBoost Regressor** for solar "
            "power forecasting.\n\n"
            "The model uses weather and time-related features such as:\n"
            "• Wind speed\n"
            "• Sunshine duration\n"
            "• Air pressure\n"
            "• Solar radiation\n"
            "• Air temperature\n"
            "• Relative humidity\n"
            "• Hour\n"
            "• Day\n"
            "• Month\n\n"
            "The model analyzes these features to estimate solar "
            "power generation."
        )

    # ==========================================================
    # BATTERY
    # ==========================================================

    if contains_any(q, [
        "battery",
        "charge battery",
        "charging battery",
        "store energy",
        "battery charging"
    ]):
        if contains_any(q, [
            "when",
            "now",
            "today",
            "time",
            "charge"
        ]):
            return (
                "🔋 **Battery Charging Recommendation**\n\n"
                "Battery charging is generally most effective when "
                "solar generation is strong.\n\n"
                "For this application, the recommended daytime window "
                "is approximately **10 AM–3 PM**, when sunlight is "
                "typically strongest.\n\n"
                "If your solar forecast is high during this period, "
                "prioritizing battery charging can help store available "
                "solar energy for later use."
            )

        return (
            "🔋 Battery storage can help you use solar energy after "
            "sunset or during periods of lower generation.\n\n"
            "A practical strategy is to charge the battery when solar "
            "generation is strong and use stored energy when generation "
            "falls."
        )

    # ==========================================================
    # HEAVY APPLIANCES
    # ==========================================================

    if contains_any(q, [
        "heavy appliance",
        "heavy appliances",
        "washing machine",
        "water pump",
        "ev charger",
        "ev charging",
        "run appliances",
        "run appliance"
    ]):
        return (
            "⚡ **Appliance Scheduling**\n\n"
            "High-power appliances such as washing machines, water "
            "pumps, and EV chargers are generally better scheduled "
            "during periods of strong solar generation.\n\n"
            "For this project, the recommended daytime window is "
            "**10 AM–3 PM**.\n\n"
            "This can increase direct use of solar energy and reduce "
            "the need to draw energy from storage or the grid."
        )

    # ==========================================================
    # SOLAR FORECAST
    # ==========================================================

    if contains_any(q, [
        "forecast",
        "solar generation",
        "solar power",
        "power generation",
        "generation today",
        "solar output",
        "will solar",
        "how much solar"
    ]):
        return (
            "☀️ **Solar Generation Forecast**\n\n"
            "Solar generation is influenced by several factors, "
            "especially:\n\n"
            "• Solar radiation\n"
            "• Sunshine duration\n"
            "• Cloud conditions\n"
            "• Air temperature\n"
            "• Relative humidity\n"
            "• Wind conditions\n\n"
            "Higher solar radiation and longer sunshine duration "
            "generally provide better conditions for solar generation.\n\n"
            "The forecasting model in this application uses these "
            "weather and time-related features to estimate solar power."
        )

    # ==========================================================
    # WEATHER
    # ==========================================================

    if contains_any(q, [
        "weather",
        "temperature",
        "humidity",
        "pressure",
        "wind",
        "cloud",
        "clouds",
        "sunshine",
        "sunlight",
        "radiation"
    ]):
        return (
            "🌤️ **Weather and Solar Generation**\n\n"
            "Weather conditions have a direct effect on solar power "
            "generation.\n\n"
            "☀️ High solar radiation → generally better generation\n"
            "☁️ Heavy cloud cover → generally lower generation\n"
            "🌡️ Temperature → can influence solar panel performance\n"
            "💧 Humidity → provides additional atmospheric information\n"
            "💨 Wind → contributes to the overall weather conditions\n\n"
            "You can use the **Live Weather** page to view the current "
            "weather information available to the application."
        )

    # ==========================================================
    # ENERGY SAVING
    # ==========================================================

    if contains_any(q, [
        "saving",
        "save energy",
        "energy saving",
        "reduce electricity",
        "reduce power",
        "electricity bill",
        "save electricity"
    ]):
        return (
            "💡 **Energy-Saving Tips**\n\n"
            "Here are some practical strategies:\n\n"
            "1. Use high-power appliances during strong daylight hours.\n"
            "2. Avoid unnecessary standby power consumption.\n"
            "3. Use stored battery energy when solar generation is low.\n"
            "4. Keep solar panels clean and unobstructed.\n"
            "5. Monitor your historical solar generation.\n"
            "6. Shift flexible electricity usage toward periods of "
            "strong solar production.\n\n"
            "The goal is to increase direct use of available solar "
            "energy while reducing unnecessary consumption."
        )

    # ==========================================================
    # MAINTENANCE
    # ==========================================================

    if contains_any(q, [
        "maintenance",
        "maintain",
        "clean panel",
        "clean panels",
        "solar panel",
        "solar panels",
        "panel cleaning",
        "panel care"
    ]):
        return (
            "🔧 **Solar Panel Maintenance**\n\n"
            "Regular maintenance can help keep a solar system operating "
            "effectively.\n\n"
            "Recommended practices include:\n"
            "• Keep panels reasonably clean.\n"
            "• Check for dust, leaves, and other obstructions.\n"
            "• Make sure panels are not shaded unnecessarily.\n"
            "• Monitor changes in solar generation.\n"
            "• Investigate unusual drops in output.\n\n"
            "For electrical or physical system faults, professional "
            "inspection should be used."
        )

    # ==========================================================
    # DAILY REPORT
    # ==========================================================

    if contains_any(q, [
        "daily report",
        "today report",
        "solar report",
        "energy report",
        "generate report",
        "report"
    ]):
        return (
            "📊 **Daily Solar Energy Report**\n\n"
            "**Forecast**\n"
            "Solar generation should be evaluated using the weather "
            "conditions and the XGBoost prediction.\n\n"
            "**Battery**\n"
            "Consider charging during periods of strong solar "
            "generation, particularly around 10 AM–3 PM.\n\n"
            "**Appliances**\n"
            "Consider scheduling flexible high-energy appliances "
            "during strong daytime generation.\n\n"
            "**Energy Saving**\n"
            "Reduce standby consumption and prioritize direct use "
            "of available solar energy.\n\n"
            "For the actual current prediction and weather values, "
            "use the Solar Forecast and Live Weather pages."
        )

    # ==========================================================
    # SYSTEM / PROJECT
    # ==========================================================

    if contains_any(q, [
        "what is this project",
        "what does this project do",
        "about this project",
        "what can you do",
        "your capabilities",
        "features"
    ]):
        return (
            "☀️ **Solar Power Forecast Agent**\n\n"
            "This application is designed to forecast solar power "
            "generation and provide energy recommendations.\n\n"
            "It includes:\n"
            "• XGBoost solar forecasting\n"
            "• Live weather information\n"
            "• Prediction history\n"
            "• Analytics dashboard\n"
            "• AI Energy Assistant\n"
            "• Battery recommendations\n"
            "• Appliance scheduling advice\n"
            "• Maintenance guidance\n"
            "• Daily reports\n"
            "• Admin tools"
        )

    # ==========================================================
    # GENERAL SOLAR QUESTIONS
    # ==========================================================

    if contains_any(q, [
        "solar",
        "photovoltaic",
        "pv",
        "sun"
    ]):
        return (
            "☀️ Solar power generation depends mainly on the amount "
            "of sunlight reaching the panels and the operating "
            "conditions of the system.\n\n"
            "In this application, weather and time-based features "
            "are used by an XGBoost model to forecast solar power.\n\n"
            "You can explore the **Solar Forecast**, **Live Weather**, "
            "and **Analytics** pages for more information."
        )

    # ==========================================================
    # UNKNOWN QUESTION
    # ==========================================================

    return (
        "I'm your Solar Energy Assistant. ☀️\n\n"
        "I can help with:\n"
        "• Solar power forecasts\n"
        "• Weather and solar conditions\n"
        "• Battery charging\n"
        "• Heavy appliance scheduling\n"
        "• Energy-saving strategies\n"
        "• Solar panel maintenance\n"
        "• XGBoost and machine learning\n"
        "• Daily solar reports\n\n"
        "Try asking something like:\n"
        "\"How does the ML model work?\"\n"
        "\"Should I charge my battery?\"\n"
        "\"Can I run my washing machine now?\"\n"
        "\"How can I save energy?\""
    )


# ==========================================================
# API ENDPOINT
# ==========================================================

@router.post("/ai-assistant")
def ai_assistant(request: AssistantRequest):

    answer = generate_answer(request.question)

    return {
        "response": answer
    }
