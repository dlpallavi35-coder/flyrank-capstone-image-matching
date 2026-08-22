# FlyRank Capstone – Build Log

## Project

**Project Name:** FlyRank Capstone – AI Image Matching Engine

**Track:** Backend

**Status:** Completed

**Repository:**

https://github.com/dlpallavi35-coder/flyrank-capstone-image-matching

---

## 1. Project Setup

The project was implemented as a Dockerized FastAPI backend with PostgreSQL persistence and Google Gemini integration.

Main technologies:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Google Gemini
- Gemini Embeddings
- Docker
- Docker Compose
- Pytest

The application consists of two main Docker services:

- `image-matching-api`
- `image-matching-db`

---

## 2. Backend API

The FastAPI application provides endpoints for:

- Application information
- Health checking
- Post creation
- Post retrieval
- Image upload
- Image review
- Image approval
- Image rejection
- Image-to-post matching
- Suggestion management
- Batch embedding processing
- AI usage tracking

Swagger documentation is available at:

```text
http://localhost:8000/docs
```

OpenAPI documentation is available at:

```text
http://localhost:8000/openapi.json
```

---

## 3. Database

PostgreSQL is used as the persistent database.

The Docker Compose database service uses:

```text
Database: image_matching_db
User: postgres
Port: 5432
```

The database stores:

- Posts
- Images
- Image metadata
- Embeddings
- Suggestions
- Review decisions
- AI usage records

---

## 4. Google Gemini Integration

Google Gemini is used for AI image analysis.

The application also uses:

```text
gemini-embedding-001
```

for semantic embedding generation.

The image processing pipeline performs:

1. Image upload
2. Image validation
3. Gemini image analysis
4. Image metadata generation
5. Image persistence
6. Embedding generation
7. Similarity comparison
8. Matching validation
9. Suggestion creation

---

## 5. Network and TLS Verification

Connectivity from the API Docker container to the Google Gemini API infrastructure was verified.

DNS resolution was tested using:

```bash
docker exec image-matching-api python -c "import socket; print(socket.gethostbyname('generativelanguage.googleapis.com') )"
```

Verified DNS result:

```text
172.217.116.4
```

TCP connectivity to HTTPS port 443 was verified using:

```bash
docker exec image-matching-api python -c "import socket; s=socket.create_connection(('generativelanguage.googleapis.com',443),timeout=15); print('TCP 443 OK'); s.close()"
```

Verified result:

```text
TCP 443 OK
```

TLS connectivity was verified using:

```bash
docker exec image-matching-api python -c "import ssl,socket; s=socket.create_connection(('generativelanguage.googleapis.com',443),timeout=15); c=ssl.create_default_context().wrap_socket(s,server_hostname='generativelanguage.googleapis.com'); print('TLS OK:', c.version()); c.close()"
```

Verified result:

```text
TLS OK: TLSv1.3
```

The API container uses:

```text
OpenSSL 3.5.6 7 Apr 2026
```

This confirms that the API container can resolve the Gemini API host and establish TCP and TLS connections to HTTPS port 443.

---

## 6. AI Operations

The application records AI operations in the database.

Tracked operations include:

- Image analysis
- Embedding generation

Verified AI usage records include:

```text
image_analysis
gemini-3.6-flash
```

and:

```text
embedding
gemini-embedding-001
```

The latest verified usage response contained:

```text
total_operations: 14
```

The recorded operations include image analysis and embedding generation.

---

## 7. Image Embeddings

The database was verified using:

```bash
docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"
```

Verified result:

```text
total_images | images_with_embedding | images_without_embedding
-------------+-----------------------+--------------------------
13           | 13                    | 0
```

Therefore:

```text
Total images: 13
Images with embeddings: 13
Images without embeddings: 0
```

---

## 8. Matching Engine

The matching engine uses semantic embeddings and cosine similarity.

The matching process includes:

- Embedding comparison
- Cosine similarity
- Similarity threshold validation
- Confidence validation
- Subject compatibility
- Category compatibility
- Invalid embedding handling
- Zero-vector protection
- Embedding dimension validation

The system can reject unsuitable candidates rather than returning an invalid match.

---

## 9. Review Workflow

The system implements a review workflow for image-to-post suggestions.

Suggestion states/actions include:

- Pending
- Approved
- Rejected

Images can also be independently:

- Approved
- Rejected

This allows the system to separate automated matching from human review.

---

## 10. Batch Processing

A batch processing endpoint was implemented for images that do not have embeddings.

The batch service:

- Finds images without embeddings
- Generates missing embeddings
- Handles failed processing
- Uses retry handling
- Returns processing information

The database verification currently shows:

```text
13 images
13 embeddings
0 missing embeddings
```

---

## 11. Automated Testing

Automated tests were executed inside the API container using:

```bash
docker exec image-matching-api python -m pytest -q
```

Verified result:

```text
23 passed, 1 warning
```

The tests cover:

- Root endpoint
- Health endpoint
- Post APIs
- Suggestion APIs
- AI usage API
- Cosine similarity
- Embedding normalization
- Invalid embeddings
- Confidence validation
- Low-confidence rejection
- Low-similarity rejection
- Subject compatibility
- Category compatibility
- Valid image-to-post matching

---

## 12. Evaluation

The evaluation script was executed using:

```bash
docker exec image-matching-api python -m evaluation.evaluate
```

Verified result:

```text
===== EVALUATION RESULTS =====

Total cases: 6
Correct top-1 predictions: 6
Top-1 precision: 100.00%

Case 1: expected=1 predicted=1 correct=True
Case 2: expected=2 predicted=2 correct=True
Case 3: expected=3 predicted=3 correct=True
Case 4: expected=1 predicted=1 correct=True
Case 5: expected=None predicted=None correct=True
Case 6: expected=None predicted=None correct=True
```

Evaluation summary:

```text
Total cases: 6
Correct predictions: 6
Top-1 precision: 100%
```

The 100% precision result applies to the included six-case evaluation dataset.

---

## 13. Docker Verification

The Docker services were verified using:

```bash
docker compose ps
```

The project uses:

```text
image-matching-api
image-matching-db
```

The API is exposed on:

```text
http://localhost:8000
```

PostgreSQL is exposed on:

```text
localhost:5432
```

---

## 14. Final Verification

The complete verification workflow is:

```bash
docker compose up --build -d
```

```bash
docker compose ps
```

```bash
docker exec image-matching-api python -m pytest -q
```

```bash
docker exec image-matching-api python -m evaluation.evaluate
```

```bash
docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"
```

The project was verified with:

```text
23 automated tests passing
6/6 evaluation cases correct
100% top-1 precision on the included evaluation dataset
13 stored images
13 images with embeddings
0 images without embeddings
Gemini DNS resolution working
TCP 443 connectivity working
TLS 1.3 connectivity working
AI usage records present
Docker API service working
PostgreSQL service working
```

---

## 15. Final Status

The backend capstone implementation is complete.

Implemented components include:

- FastAPI backend
- PostgreSQL database
- SQLAlchemy persistence
- Google Gemini image analysis
- Gemini semantic embeddings
- Image upload
- Image metadata extraction
- Image-to-post matching
- Cosine similarity
- Matching validation guards
- Review suggestions
- Image approval and rejection
- Batch embedding processing
- AI usage tracking
- Docker
- Docker Compose
- Automated tests
- Evaluation dataset
- Evaluation script
- Swagger API documentation

**Final Status: Completed**