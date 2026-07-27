from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AssistantRequest(BaseModel):
    question: str


@router.post("/ai-assistant")
def ai_assistant(request: AssistantRequest):

    return {
        "response": (
            "AI Assistant received your question: "
            f"{request.question}"
        )
    }