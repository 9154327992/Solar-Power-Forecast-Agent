from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def battery_home():

    return {
        "message": "Battery API"
    }


@router.get("/{city}")
def battery(city: str):

    return {
        "city": city,
        "battery": "Battery scheduling endpoint"
    }