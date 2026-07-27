from fastapi import APIRouter

router = APIRouter()

# Temporary in-memory history
prediction_history = []


@router.get("/")
def get_history():
    return prediction_history


@router.post("/")
def add_history(data: dict):
    prediction_history.append(data)
    return {
        "message": "Prediction saved successfully."
    }


@router.delete("/")
def clear_history():
    prediction_history.clear()
    return {
        "message": "Prediction history cleared."
    }


@router.delete("/{prediction_id}")
def delete_history(prediction_id: int):

    if 0 <= prediction_id < len(prediction_history):
        deleted = prediction_history.pop(prediction_id)
        return {
            "message": "Prediction deleted.",
            "data": deleted
        }

    return {
        "message": "Prediction not found."
    }
