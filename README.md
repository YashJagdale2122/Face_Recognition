# Vision Processing Backend
![CI](https://github.com/YashJagdale2122/vision-processing-backend/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Status](https://img.shields.io/badge/Status-Actively%20Maintained-brightgreen)


## Overview

**Vision Processing Backend** is a **backend-oriented REST service** that exposes
computer vision capabilities through a clean API.

The project demonstrates how **applied AI / ML logic (face recognition)** can be
integrated into a **structured backend service**, with clear separation between:
- API layer
- Service layer
- Vision processing logic

This repository focuses on **backend design and service structure**, not on model
training or research experimentation.


## Problem Statement

Applications often need to perform **vision-based analysis** (e.g. face recognition)
while keeping the system:
- API-driven
- Maintainable
- Replaceable in terms of models and algorithms

Embedding vision logic directly inside scripts or UI layers makes systems hard to
scale and evolve.


## Solution Overview

This project provides a **FastAPI-based backend service** that:
- Accepts image input via HTTP
- Executes face recognition inside a service layer
- Returns structured, machine-readable results
- Keeps AI logic isolated from request handling

The design allows the vision logic to evolve independently of the API contract.


## Architecture Overview

The service follows a **simple, backend-first layered architecture**.

```text
Client
  ↓
FastAPI API Layer
  ↓
Service Layer
  ↓
Vision Processing Logic
````

### Design Principles

* **Thin API layer**: routes only validate input and format responses
* **Service abstraction**: vision logic is not embedded in routes
* **Replaceable AI components**: models and libraries can be swapped
* **Clear contracts**: predictable request/response behavior


## Core Components

### API Layer

* FastAPI endpoints
* Handles HTTP requests and file uploads
* Returns structured JSON responses

### Service Layer

* Orchestrates vision processing
* Handles business logic
* Acts as the boundary between API and AI logic

### Vision Processing

* Uses OpenCV and `face_recognition`
* Performs face detection and recognition
* Returns bounding box and identity information


## API Usage

### Base URL

```
http://localhost:8000
```

### Health Check

**GET** `/health`

```json
{
  "status": "ok"
}
```


## API Examples

### Recognize Faces (Image Upload)

**Request**

```bash
curl -X POST "http://localhost:8000/recognize" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@person.jpg"
```

**Successful Response**

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

**Unknown Face Response**

```json
{
  "results": [
    {
      "name": "Unknown",
      "box": {
        "top": 210,
        "right": 390,
        "bottom": 420,
        "left": 180
      }
    }
  ]
}
```

**Notes**

* Multiple faces in a single image are supported
* Bounding boxes are returned in pixel coordinates
* Vision logic is executed inside the service layer, not the API routes


## Tech Stack

* **Backend Framework**: FastAPI
* **Language**: Python 3.12
* **Computer Vision**: OpenCV, face_recognition
* **Server**: Uvicorn
* **Containerization**: Docker


## Running Locally

### Prerequisites

* Python 3.12+
* Docker (optional)

### Run without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run with Docker

```bash
docker build -t vision-processing-backend .
docker run -p 8000:8000 vision-processing-backend
```


## Scope & Limitations

This project intentionally does **not** include:

* Asynchronous job queues
* Persistent storage
* Authentication or authorization
* Distributed workers

Those concerns are explored in other backend-focused repositories.


## Why This Repo Exists

This repository exists to demonstrate:

* How AI/ML logic fits inside backend services
* Clean separation between API and processing logic
* Practical backend application of computer vision

It complements larger, system-level backend projects in this profile.


## Future Improvements

* Async job execution for large images
* Model abstraction layer
* Result persistence
* Authentication
