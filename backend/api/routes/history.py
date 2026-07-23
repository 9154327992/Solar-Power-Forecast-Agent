from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def history():

    return {
        "message": "Prediction history"
    }


@router.delete("/{prediction_id}")
def delete_history(prediction_id: int):

    return {
        "deleted": prediction_id
    }