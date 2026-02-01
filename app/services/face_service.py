import os
from typing import List, Dict

import face_recognition


class FaceRecognitionService:
    """
    Core service responsible for loading known faces and
    performing face recognition on input images.
    """

    def __init__(self, known_faces_dir: str):
        self.known_encodings: List = []
        self.known_names: List[str] = []
        self._load_known_faces(known_faces_dir)

    def _load_known_faces(self, dir_path: str) -> None:
        """
        Loads all images from a directory and stores
        face encodings with corresponding names.
        """
        for file in os.listdir(dir_path):
            if not file.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            name = os.path.splitext(file)[0]
            image_path = os.path.join(dir_path, file)

            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if not encodings:
                continue

            self.known_encodings.append(encodings[0])
            self.known_names.append(name)

    def recognize_faces(self, image_path: str) -> List[Dict]:
        """
        Recognizes faces in the given image.

        Returns:
            List of dicts with name and bounding box.
        """
        image = face_recognition.load_image_file(image_path)
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)

        results = []

        for (top, right, bottom, left), encoding in zip(locations, encodings):
            matches = face_recognition.compare_faces(
                self.known_encodings, encoding
            )

            name = "Unknown"
            if True in matches:
                idx = matches.index(True)
                name = self.known_names[idx]

            results.append({
                "name": name,
                "box": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left,
                }
            })

        return results
