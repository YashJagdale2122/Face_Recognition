from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

from app.services.face_service import FaceRecognitionService

app = FastAPI(title="Face Recognition Backend")


@app.on_event("startup")
def startup():
    app.state.face_service = FaceRecognitionService(
        known_faces_dir="images"
    )


@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    contents = await file.read()

    np_img = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Invalid image"}

    results = app.state.face_service.recognize_faces(image)
    return {"results": results}
