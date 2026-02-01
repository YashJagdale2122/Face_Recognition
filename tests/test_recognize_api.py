import numpy as np
import pytest

from app.services.face_service import FaceRecognitionService


@pytest.fixture
def service(tmp_path):
    """
    Create service with empty known faces.
    We mock face_recognition internals anyway.
    """
    return FaceRecognitionService(known_faces_dir=str(tmp_path))


def test_recognize_faces_returns_expected_structure(mocker, service):
    # --- Mock face_recognition ---
    mocker.patch(
        "face_recognition.load_image_file",
        return_value=np.zeros((100, 100, 3))
    )

    mocker.patch(
        "face_recognition.face_locations",
        return_value=[(10, 50, 60, 5)]
    )

    mocker.patch(
        "face_recognition.face_encodings",
        return_value=[np.array([0.1] * 128)]
    )

    mocker.patch(
        "face_recognition.face_distance",
        return_value=np.array([0.2])
    )

    service.known_encodings = [np.array([0.1] * 128)]
    service.known_names = ["test_person"]

    results = service.recognize_faces("dummy.jpg")

    assert isinstance(results, list)
    assert len(results) == 1

    face = results[0]

    assert "name" in face
    assert "confidence" in face
    assert "box" in face

    assert face["name"] == "test_person"
    assert 0.0 <= face["confidence"] <= 1.0

def test_distance_to_confidence(service):
    assert service._distance_to_confidence(0.0) == 1.0
    assert service._distance_to_confidence(0.3) == 0.5
    assert service._distance_to_confidence(0.6) == 0.0
    assert service._distance_to_confidence(0.8) == 0.0
