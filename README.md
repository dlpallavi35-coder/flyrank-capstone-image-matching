# AI Image Understanding and Content Matching Engine

An AI-powered backend service that analyzes uploaded images using Google Gemini, generates semantic embeddings, matches images with relevant posts, and provides human-review workflows.

## Features

- Image upload through FastAPI
- AI image analysis using Google Gemini
- Structured image metadata:
  - Subject
  - Category
  - Attributes
  - Caption
  - Confidence score
- Semantic embeddings using `gemini-embedding-001`
- Image-to-post matching
- Image-to-post similarity suggestions
- Human approval/rejection workflow
- Batch embedding processing
- Retry handling for embedding generation
- PostgreSQL persistence
- Docker and Docker Compose support
- AI usage tracking and estimated cost reporting
- REST API with automatically generated OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Google Gemini API
- Docker
- Docker Compose
- Pytest

## Project Structure

```text
flyrank-capstone-image-matching/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── database/
│   │   └── database.py
│   ├── models/
│   │   ├── ai_usage.py
│   │   ├── image.py
│   │   ├── post.py
│   │   └── suggestion.py
│   ├── schemas/
│   │   └── post_schema.py
│   ├── services/
│   │   ├── batch_service.py
│   │   ├── embedding_service.py
│   │   ├── matching_service.py
│   │   └── vision_service.py
│   └── main.py
│
├── uploads/
├── test_gemini.py
├── test_image.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── capstone.yaml
├── BUILDLOG.md
├── EVIDENCE.md
└── README.md