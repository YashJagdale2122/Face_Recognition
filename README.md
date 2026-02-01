# Face Recognition Backend

![CI](https://github.com/YashJagdale2122/Face_Recognition/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


A production-oriented **Face Recognition Backend** built using **FastAPI** and the `face_recognition` library.
The system detects multiple faces in an uploaded image, identifies known individuals, and returns structured bounding box data via a REST API.

This project demonstrates how an **experimental ML script** can be evolved into a **clean backend service** using proper architecture and separation of concerns.

---

## Problem Statement

Face recognition is often demonstrated through standalone scripts, which are:

* tightly coupled,
* hard to extend,
* unsuitable for real backend systems.

This project addresses that gap by converting face recognition logic into a **service-driven backend** that can be consumed by other systems (web, mobile, analytics pipelines).

---

## Solution Overview

The backend exposes an API that:

1. Accepts an image upload
2. Detects all faces present
3. Matches detected faces against a known set
4. Returns recognized names and bounding boxes as JSON

The system is structured to be **extensible**, **testable**, and **production-ready**.

---

## Architecture

```text
Client
  │
  ▼
FastAPI Route
  │
  ▼
FaceRecognitionService
  │
  ▼
face_recognition (dlib)
```

### Key Design Decisions

* **Service Layer** handles all ML logic
* **API Layer** only manages HTTP concerns
* Known faces are loaded at application startup
* No business logic inside routes

---

## Features

* Multi-face detection in a single image
* Known vs unknown face classification
* Bounding box extraction per face
* Clean service abstraction
* Dockerized deployment
* OpenAPI / Swagger support

---

## Tech Stack

* **Backend**: FastAPI (Python 3.10+)
* **Face Recognition**: `face_recognition` (dlib)
* **Image Processing**: OpenCV, NumPy
* **Containerization**: Docker
* **API Docs**: Swagger UI

---

## API Usage

### Recognize Faces

**Endpoint**

```http
POST /recognize
```

**Request**

* Multipart form upload
* Field: `file` (image)

**Response**

```json
{
  "results": [
    {
      "name": "amir",
      "box": {
        "top": 206,
        "right": 1133,
        "bottom": 527,
        "left": 812
      }
    }
  ]
}
```

If a face is not recognized, the name is returned as `"Unknown"`.

---

## Running Locally

### Using Docker (Recommended)

```bash
docker build -t face-recognition-backend .
docker run -p 8000:8000 face-recognition-backend
```

API available at:

```
http://localhost:8000
http://localhost:8000/docs
```

---

## Known Faces Handling

* Known identities are loaded from an `images/` directory at startup
* Image filenames are used as identity labels (e.g. `amir.jpg → amir`)
* This keeps the initial system simple and transparent

> In production, this can be replaced with database-backed identity management.

---

## Project Evolution

* **Phase 1**: Standalone face recognition script (experimental)
* **Phase 2**: Service abstraction and backend architecture
* **Phase 3**: Dockerized API with clean separation of concerns

This mirrors real-world ML system evolution.

---

## Future Improvements

* Database-backed identity storage
* Confidence scoring for matches
* Batch image processing
* Async job handling
* Authentication and rate limiting
