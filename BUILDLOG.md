# FlyRank Capstone – Build Log

## Project

- Project: flyrank-capstone-image-matching
- Track: Backend
- Status: Completed
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- AI: Google Gemini
- Deployment: Docker Compose

## 1. Backend Foundation

Implemented the FastAPI backend with:

- Application entry point
- API routing
- Database connection
- SQLAlchemy models
- PostgreSQL persistence
- Health endpoint
- Root endpoint

Verified endpoints:

- `GET /`
- `GET /health`

## 2. Post Management

Implemented post management functionality.

Supported operations:

- Create a post
- Retrieve all posts
- Retrieve an individual post
- Retrieve matching images for a post

Endpoints:

- `POST /posts`
- `GET /posts`
- `GET /posts/{post_id}`
- `GET /posts/{post_id}/images`

Post embeddings are generated from the post title and content.

## 3. AI Image Analysis

Implemented Google Gemini image analysis.

When an image is uploaded, the application:

1. Validates the image format.
2. Saves the uploaded image.
3. Sends the image for AI analysis.
4. Generates structured image metadata.
5. Stores the generated description and confidence information.

Image metadata includes:

- Subject
- Category
- Attributes
- Caption
- Confidence

Supported image formats:

- JPEG
- PNG
- WEBP
- GIF

## 4. Semantic Embeddings

Implemented semantic embedding generation using:

`gemini-embedding-001`

Embeddings are generated for:

- Posts
- Uploaded images

The image embedding is generated from the AI-generated image description.

The embedding service also includes handling for embedding generation failures.

## 5. Image-to-Post Matching

Implemented semantic image-to-post matching.

The matching process:

1. Generates an image embedding.
2. Retrieves available post embeddings.
3. Calculates semantic similarity.
4. Selects the highest-ranked candidate.
5. Applies validation guards.
6. Accepts or rejects the candidate.
7. Creates a review suggestion.

The matching service uses cosine similarity.

## 6. Matching Validation Guards

Added validation safeguards to reduce incorrect matches.

Implemented protections include:

- Low-confidence image rejection
- Low-similarity rejection
- Subject compatibility validation
- Category compatibility validation
- Invalid embedding handling
- Zero-vector protection
- Embedding dimension validation
- Confidence normalization

Examples covered by automated tests include:

- Dog image matching a dog post
- Wolf image being rejected for a dog post
- Vehicle image being rejected for a dog post
- Low-confidence image rejection
- Low-similarity match rejection

## 7. Review Workflow

Implemented a human review workflow.

Suggestions can be:

- Pending
- Approved
- Rejected

Suggestion endpoints:

- `GET /suggestions`
- `GET /suggestions/{suggestion_id}`
- `POST /suggestions/{suggestion_id}/approve`
- `POST /suggestions/{suggestion_id}/reject`

Image review endpoints:

- `POST /images/{image_id}/approve`
- `POST /images/{image_id}/reject`
- `GET /images/{image_id}/review`

Approved suggestions can associate the image with the selected post.

## 8. Batch Processing

Implemented batch processing for images that do not have embeddings.

Endpoint:

`POST /images/process-batch`

The batch service:

- Finds images with missing embeddings.
- Generates embeddings.
- Retries failed operations.
- Records failures.
- Returns processing statistics.

The verified database currently contains:

- Total images: 12
- Images with embeddings: 12
- Images without embeddings: 0

## 9. AI Usage Tracking

Implemented AI operation tracking.

Tracked operations include:

- Image analysis
- Embedding generation

The application records:

- Operation
- Model
- Input tokens
- Output tokens
- Estimated cost
- Creation timestamp

The API exposes:

`GET /ai-usage`

Verified database records include:

- `gemini-3.6-flash` image analysis operations
- `gemini-embedding-001` embedding operations

## 10. Dockerization

Containerized the application using Docker.

The project contains:

- `Dockerfile`
- `docker-compose.yml`

Docker Compose runs:

- FastAPI API container
- PostgreSQL database container

Services:

- `image-matching-api`
- `image-matching-db`

The API is exposed on port `8000`.

PostgreSQL is exposed on port `5432`.

## 11. Database Persistence

Implemented PostgreSQL persistence for:

- Posts
- Images
- Image embeddings
- Suggestions
- AI usage records

The PostgreSQL database uses a persistent Docker volume.

Current verified image database state:

```text
Total images: 12
Images with embeddings: 12
Images without embeddings: 0
12. Automated Testing

Implemented automated tests using Pytest.

Test areas include:

API endpoints
Image analysis
Matching service
Cosine similarity
Embedding normalization
Confidence validation
Matching guards
Suggestion API
AI usage API

Verified result:

23 passed, 1 warning

Command used:

docker exec image-matching-api python -m pytest -q
13. Evaluation System

Created an evaluation dataset and evaluation script.

Files:

evaluation/dataset.json
evaluation/evaluate.py

The evaluation measures top-1 matching accuracy.

Verified result:

Total cases: 6
Correct top-1 predictions: 6
Top-1 precision: 100.00%

All six evaluation cases were classified correctly.

The evaluation includes both positive matching cases and negative/no-match cases.

14. API Documentation

FastAPI automatically provides interactive Swagger documentation.

Available at:

http://localhost:8000/docs

OpenAPI specification:

http://localhost:8000/openapi.json

The API documentation was verified to load successfully.

15. Integration Verification

The complete application was rebuilt using:

docker compose down
docker compose up --build -d

The containers started successfully.

Verified services:

image-matching-api
image-matching-db

The API successfully served:

/
/health
/posts
/docs
/openapi.json

The image upload workflow was also exercised against the running API.

16. Final Verification

Automated tests:

23 passed, 1 warning

Evaluation:

6 / 6 correct
100.00% top-1 precision

Database:

12 total images
12 images with embeddings
0 images without embeddings

AI usage:

Image analysis records: present
Embedding records: present

Docker:

API container: running
PostgreSQL container: running
17. Final Implementation

The completed implementation contains:

app/
├── api/
│   └── routes.py
├── database/
│   └── database.py
├── models/
│   ├── __init__.py
│   ├── image.py
│   ├── post.py
│   ├── suggestion.py
│   └── ai_usage.py
├── services/
│   ├── embedding_service.py
│   ├── matching_service.py
│   ├── vision_service.py
│   ├── batch_service.py
│   └── cost_service.py
└── main.py


evaluation/
├── dataset.json
└── evaluate.py


tests/
├── __init__.py
├── test_api.py
└── test_matching_service.py


Dockerfile
docker-compose.yml
requirements.txt
README.md
EVIDENCE.md
BUILDLOG.md
 18. Final Status

The backend capstone implementation is complete and has been verified through:

Docker Compose deployment
PostgreSQL persistence
FastAPI API verification
Google Gemini integration
Semantic embedding generation
Image-to-post matching
Matching validation
Human review workflow
Batch processing
AI usage tracking
Automated tests
Evaluation dataset
Evaluation script
Swagger documentation

Final verified status:

PROJECT STATUS: COMPLETED