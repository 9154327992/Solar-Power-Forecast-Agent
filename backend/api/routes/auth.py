from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def auth_home():
    return {"message": "Authentication API"}


@router.post("/register")
def register():
    return {"message": "Register endpoint"}


@router.post("/login")
def login():
    return {"message": "Login endpoint"}


@router.get("/profile")
def profile():
    return {"message": "User profile"}