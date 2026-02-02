# Face Recognition Backend

![CI](https://github.com/YashJagdale2122/Face_Recognition/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


A production-oriented **Face Recognition Backend** built using **FastAPI** and the `face_recognition` library.
The system detects multiple faces in an uploaded image, identifies known individuals, and returns structured bounding box data via a REST API.

This project demonstrates how an **experimental ML script** can be evolved into a **clean backend service** using proper architecture and separation of concerns.


## Problem Statement

Face recognition is often demonstrated through standalone scripts, which are:

* tightly coupled,
* hard to extend,
* unsuitable for real backend systems.

This project addresses that gap by converting face recognition logic into a **service-driven backend** that can be consumed by other systems (web, mobile, analytics pipelines).


## Solution Overview

The backend exposes an API that:

1. Accepts an image upload
2. Detects all faces present
3. Matches detected faces against a known set
4. Returns recognized names and bounding boxes as JSON

The system is structured to be **extensible**, **testable**, and **production-ready**.


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


## Features

* Multi-face detection in a single image
* Known vs unknown face classification
* Bounding box extraction per face
* Clean service abstraction
* Dockerized deployment
* OpenAPI / Swagger support


## Tech Stack

* **Backend**: FastAPI (Python 3.10+)
* **Face Recognition**: `face_recognition` (dlib)
* **Image Processing**: OpenCV, NumPy
* **Containerization**: Docker
* **API Docs**: Swagger UI


## Quick Start

### Prerequisites

- Docker installed (recommended)
- Python 3.10+ (for local development without Docker)
- Webcam or test images (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/YashJagdale2122/Face_Recognition.git
cd Face_Recognition
```

### 2. Prepare Known Faces

Add reference images to the `images/` directory:
```bash
# Each image filename becomes the person's identity
images/
  ├── john.jpg      # Will be recognized as "john"
  ├── sarah.jpg     # Will be recognized as "sarah"
  └── alex.png      # Will be recognized as "alex"
```

**Image Requirements:**
- Clear, front-facing photos
- Good lighting
- Single person per image
- Supported formats: .jpg, .jpeg, .png

### 3. Run with Docker (Recommended)
```bash
docker build -t face-recognition-backend .
docker run -p 8000:8000 face-recognition-backend
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

### 4. Test the API

#### Using curl:
```bash
# Upload an image for recognition
curl -X POST "http://localhost:8000/recognize" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/test_image.jpg"
```

#### Using Swagger UI:

1. Navigate to http://localhost:8000/docs
2. Click on `/recognize` endpoint
3. Click "Try it out"
4. Upload an image file
5. Click "Execute"

#### Expected Response:
```json
{
  "results": [
    {
      "name": "john",
      "box": {
        "top": 150,
        "right": 450,
        "bottom": 380,
        "left": 220
      }
    }
  ]
}
```

### 5. Run Locally (Without Docker)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Stop the Service

Docker:
```bash
docker stop <container_id>
```

Local:
```bash
# Press Ctrl+C in the terminal
```


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


## Known Faces Handling

* Known identities are loaded from an `images/` directory at startup
* Image filenames are used as identity labels (e.g. `amir.jpg → amir`)
* This keeps the initial system simple and transparent

> In production, this can be replaced with database-backed identity management.


## Project Evolution

* **Phase 1**: Standalone face recognition script (experimental)
* **Phase 2**: Service abstraction and backend architecture
* **Phase 3**: Dockerized API with clean separation of concerns

This mirrors real-world ML system evolution.


## Future Improvements

* Database-backed identity storage
* Confidence scoring for matches
* Batch image processing
* Async job handling
* Authentication and rate limiting
