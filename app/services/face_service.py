import os
from typing import List, Dict
import numpy as np
import face_recognition

from app.core.confidence import face_distance_to_confidence


class FaceRecognitionService:
    """
    Core service responsible for loading known faces and
    performing face recognition with confidence scoring.
    """

    def __init__(self, known_faces_dir: str):
        self.known_faces_dir = known_faces_dir
        self.known_encodings: List = []
        self.known_names: List[str] = []

        self._load_known_faces()

    def _load_known_faces(self) -> None:
        """
        Load known faces from directory and cache encodings.
        """
        for file in os.listdir(self.known_faces_dir):
            if not file.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            name = os.path.splitext(file)[0]
            image_path = os.path.join(self.known_faces_dir, file)

            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                continue

            self.known_encodings.append(encodings[0])
            self.known_names.append(name)

    def _distance_to_confidence(self, distance: float, threshold: float = 0.6) -> float:
        """
        Convert face distance to a normalized confidence score.
        Lower distance = higher confidence.
        """
        if distance > threshold:
            return 0.0
        return round(1 - (distance / threshold), 2)


    def recognize_faces(self, image_path: str) -> List[Dict]:
        image = face_recognition.load_image_file(image_path)
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)

        results = []

        for (top, right, bottom, left), encoding in zip(locations, encodings):
            distances = face_recognition.face_distance(
                self.known_encodings, encoding
            )

            best_idx = int(np.argmin(distances))
            best_distance = distances[best_idx]

            confidence = self._distance_to_confidence(best_distance)

            name = (
                self.known_names[best_idx]
                if confidence > 0
                else "Unknown"
            )

            results.append({
                "name": name,
                "confidence": confidence,
                "box": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left,
                }
            })

        return results
