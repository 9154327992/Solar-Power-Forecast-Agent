from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def recommendation_home():

    return {
        "message": "Recommendation API"
    }


@router.get("/{city}")
def recommendation(city: str):

    return {
        "city": city,
        "recommendation": "Energy recommendation endpoint"
    }