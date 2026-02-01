from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import uuid
import os

from app.services.face_service import FaceRecognitionService

app = FastAPI(title="Face Recognition Backend")

KNOWN_FACES_DIR = "images"
TEMP_DIR = "tmp"

os.makedirs(TEMP_DIR, exist_ok=True)


@app.on_event("startup")
def startup_event():
    app.state.face_service = FaceRecognitionService(KNOWN_FACES_DIR)


@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        results = app.state.face_service.recognize_faces(temp_path)
        return {"results": results}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
