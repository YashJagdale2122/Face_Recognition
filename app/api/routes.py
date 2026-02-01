from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.post("/recognize")
def recognize_face():
    return {"message": "endpoint stub"}
