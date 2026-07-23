from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def maintenance_home():

    return {
        "message": "Maintenance API"
    }


@router.get("/{city}")
def maintenance(city: str):

    return {
        "city": city,
        "maintenance": "Maintenance advice endpoint"
    }