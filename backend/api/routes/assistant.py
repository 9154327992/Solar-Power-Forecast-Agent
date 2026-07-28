from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AssistantRequest(BaseModel):
    question: str

@router.post("/ai-assistant")
def ai_assistant(request: AssistantRequest):

    question = request.question.lower()

    if "battery" in question:
        answer = (
            "Charge your battery during peak solar generation "
            "(10 AM–3 PM) to maximize stored energy."
        )

    elif (
        "forecast" in question
        or "solar generation" in question
        or "high today" in question
    ):
        answer = (
            "If solar radiation is high and cloud cover is low, "
            "solar generation is expected to be high today. "
            "Use battery charging and heavy appliances during "
            "peak sunlight hours (10 AM–3 PM)."
        )
    elif "heavy" in question:
        answer = (
            "Run heavy appliances like washing machines, water pumps, "
            "or EV chargers during peak sunlight hours."
        )

    elif "saving" in question:
        answer = (
            "Reduce standby power, clean solar panels regularly, "
            "and schedule high-energy appliances during the daytime."
        )

    elif "weather" in question:
        answer = (
            "Clear skies and high solar radiation generally produce "
            "the highest solar power output."
        )

    elif "report" in question:
        answer = (
            "Daily Solar Report\n\n"
            "• Weather: Normal\n"
            "• Solar Generation: Good\n"
            "• Battery: Charge between 10 AM and 3 PM\n"
            "• Recommendation: Use heavy appliances during daylight."
        )

    elif "model" in question or "ml" in question:
        answer = (
            "This project uses the XGBoost Machine Learning model "
            "for solar power forecasting."
        )

    else:
        answer = (
            "I'm your AI Energy Assistant. "
            "Ask me about solar forecasting, battery usage, "
            "weather, maintenance, or energy optimization."
        )

    return {
        "response": answer
    }
