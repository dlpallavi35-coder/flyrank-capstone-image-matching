# FlyRank Capstone – AI Image Matching Engine

## Project Overview

FlyRank Capstone is a backend service that accepts uploaded images, analyzes them using Google Gemini, generates semantic embeddings, and automatically matches images with the most relevant posts.

The system stores posts, images, embeddings, suggestions, review decisions, and AI usage information in PostgreSQL.

The project is built with FastAPI, SQLAlchemy, PostgreSQL, Google Gemini, Docker, and Docker Compose.

---

## Features

- Image upload API
- AI image analysis using Google Gemini
- Automatic image description generation
- Image metadata extraction
- Semantic embedding generation
- Post creation and retrieval APIs
- Image-to-post semantic matching
- Cosine similarity matching
- Confidence validation
- Similarity threshold validation
- Subject and category compatibility guards
- Human review suggestion workflow
- Image approval and rejection workflow
- Batch processing for missing image embeddings
- AI usage and cost tracking
- PostgreSQL persistence
- Dockerized application
- Docker Compose orchestration
- Health check endpoint
- Automated API tests
- Matching service tests
- Evaluation dataset and evaluation script
- Interactive Swagger API documentation

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Google Gemini | AI image analysis |
| gemini-embedding-001 | Semantic embeddings |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Pytest | Automated testing |

---

# System Architecture

```text
Client
   |
   v
FastAPI API
   |
   +--------------------+
   |                    |
   v                    v
Google Gemini       PostgreSQL
Image Analysis      Database
   |                    |
   v                    |
Image Metadata          |
   |                    |
   v                    |
Embedding Service ------+
   |
   v
Matching Engine
   |
   v
Validation Guards
   |
   v
Review Suggestion
flyrank-capstone-image-matching/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── image.py
│   │   ├── post.py
│   │   ├── suggestion.py
│   │   └── ai_usage.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── matching_service.py
│   │   ├── vision_service.py
│   │   ├── batch_service.py
│   │   └── cost_service.py
│   │
│   └── main.py
│
├── evaluation/
│   ├── dataset.json
│   └── evaluate.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_matching_service.py
│
├── uploads/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

Prerequisites

Before running the project, make sure you have:

Docker Desktop
Docker Compose
Git
A Google Gemini API key
Environment Variables

Create a .env file in the project root directory:

GEMINI_API_KEY=your_google_gemini_api_key

Do not commit your real API key to GitHub.

Running the Project

Clone the repository:

git clone https://github.com/dlpallavi35-coder/flyrank-capstone-image-matching.git

Move into the project directory:

cd flyrank-capstone-image-matching

Create the .env file and add your Google Gemini API key.

Start the application:

docker compose up --build -d

Check that the containers are running:

docker compose ps

The application will run at:

http://localhost:8000
API Documentation

FastAPI provides interactive Swagger API documentation.

Open:

http://localhost:8000/docs

OpenAPI documentation is available at:

http://localhost:8000/openapi.json
Available API Endpoints
Application
Method	Endpoint	Description
GET	/	Returns application information
GET	/health	Returns API health status

Example health response:

{
  "status": "healthy"
}
Posts
Method	Endpoint	Description
POST	/posts	Creates a new post
GET	/posts	Returns all posts
GET	/posts/{post_id}	Returns a specific post
GET	/posts/{post_id}/images	Returns the best matching image for a post

When a post is created, the system attempts to generate a semantic embedding using the post title and content.

Images
Method	Endpoint	Description
POST	/images/upload	Uploads and processes an image
POST	/images/{image_id}/approve	Approves an image
POST	/images/{image_id}/reject	Rejects an image
GET	/images/{image_id}/review	Returns image review information
POST	/images/process-batch	Processes missing image embeddings

Supported image formats:

JPEG
PNG
WEBP
GIF
Suggestions
Method	Endpoint	Description
GET	/suggestions	Returns all suggestions
GET	/suggestions/{suggestion_id}	Returns a specific suggestion
POST	/suggestions/{suggestion_id}/approve	Approves a suggestion
POST	/suggestions/{suggestion_id}/reject	Rejects a suggestion
AI Usage
Method	Endpoint	Description
GET	/ai-usage	Returns AI operation and usage records
Image Processing Workflow

When an image is uploaded, the following process is performed:

Image Upload
      |
      v
Validate Image Format
      |
      v
Google Gemini Image Analysis
      |
      v
Generate Image Metadata
      |
      v
Store Image in PostgreSQL
      |
      v
Generate Semantic Embedding
      |
      v
Compare With Post Embeddings
      |
      v
Cosine Similarity Matching
      |
      v
Validation Guards
      |
      v
Create Review Suggestion
      |
      v
Return Matching Result

The image metadata includes information such as:

Subject
Category
Attributes
Caption
Confidence
Matching and Validation

The matching service compares image embeddings with post embeddings using cosine similarity.

Additional validation guards are used to reduce incorrect matches.

These checks include:

Low-confidence image rejection
Low-similarity match rejection
Subject compatibility validation
Category compatibility validation
Invalid embedding handling
Zero-vector protection
Embedding dimension validation

The system can reject a candidate match when the semantic similarity or image metadata indicates that the image is not compatible with the post.

Review Workflow

After image matching, a suggestion is created.

A suggestion can have the following review actions:

Pending
Approved
Rejected

The reviewer can approve or reject a suggested image-to-post match using the API.

Images can also be independently approved or rejected.

Batch Processing

The batch processing endpoint processes images that do not yet have embeddings.

The batch service:

Finds images with missing embeddings.
Generates embeddings.
Uses retry handling for failed operations.
Records failed image processing information.
Returns a processing summary.

Example response:

{
  "total": 10,
  "processed": 10,
  "failed": 0,
  "failures": []
}
AI Usage Tracking

The system records AI operations performed by the application.

Tracked operations include:

Image analysis
Embedding generation

The /ai-usage endpoint returns:

Total operations
Input tokens
Output tokens
Estimated cost
Individual AI usage records

Example response structure:

{
  "total_operations": 14,
  "total_input_tokens": 0,
  "total_output_tokens": 0,
  "total_estimated_cost": 0
}
Running Tests

Run all automated tests:

docker exec image-matching-api python -m pytest -v

Or use:

docker exec image-matching-api python -m pytest -q

Current verified result:

23 passed, 1 warning

The automated tests cover:

Root endpoint
Health endpoint
Post APIs
Suggestion APIs
AI usage API
Cosine similarity
Embedding normalization
Invalid embeddings
Confidence validation
Low-confidence rejection
Low-similarity rejection
Subject compatibility
Category compatibility
Valid image-to-post matching
Evaluation

The project includes an evaluation dataset and evaluation script.

Run the evaluation using:

docker exec image-matching-api python -m evaluation.evaluate

Current verified evaluation result:

===== EVALUATION RESULTS =====


Total cases: 6
Correct top-1 predictions: 6
Top-1 precision: 100.00%


Case results:


Case 1: expected=1 predicted=1 correct=True
Case 2: expected=2 predicted=2 correct=True
Case 3: expected=3 predicted=3 correct=True
Case 4: expected=1 predicted=1 correct=True
Case 5: expected=None predicted=None correct=True
Case 6: expected=None predicted=None correct=True

Evaluation summary:

Metric	Result
Total evaluation cases	6
Correct predictions	6
Top-1 precision	100%

The 100% result applies to the included 6-case evaluation dataset.

Database Verification

The PostgreSQL database stores uploaded images and their generated embeddings.

Run:

docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"

Current verified result:

 total_images | images_with_embedding | images_without_embedding
--------------+-----------------------+--------------------------
           12 |                    12 |                        0

This confirms that all 12 stored images currently have embeddings.

Docker Verification

Check the running services:

docker compose ps

The project uses:

image-matching-api
image-matching-db

The API runs on:

http://localhost:8000

The PostgreSQL database is available through:

localhost:5432
Complete Verification Workflow

Start or rebuild the application:

docker compose up --build -d

Check the containers:

docker compose ps

Run automated tests:

docker exec image-matching-api python -m pytest -q

Run the evaluation:

docker exec image-matching-api python -m evaluation.evaluate

Verify image embeddings:

docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"

Check AI usage:

curl http://localhost:8000/ai-usage

Open the API documentation:

http://localhost:8000/docs
Current Project Results

The project has been verified with the following results:

Verification	Result
Automated tests	23 passed
Evaluation cases	6 / 6 correct
Top-1 precision on evaluation dataset	100%
Stored images	12
Images with embeddings	12
Images without embeddings	0
Docker API container	Running
PostgreSQL container	Running
AI image analysis	Working
Embedding generation	Working
Image-to-post matching	Working
Review workflow	Implemented
Batch embedding processing	Implemented
AI usage tracking	Implemented
Evidence

The project was verified using the following commands.

Container verification:

docker compose ps

Automated tests:

docker exec image-matching-api python -m pytest -q

Verified result:

23 passed, 1 warning

Evaluation:

docker exec image-matching-api python -m evaluation.evaluate

Verified result:

Total cases: 6
Correct top-1 predictions: 6
Top-1 precision: 100.00%

Database verification:

docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"

Verified result:

TOTAL IMAGES: 12
WITH EMBEDDING: 12
WITHOUT EMBEDDING: 0

AI usage records confirm that both image analysis and embedding generation operations have been recorded by the application.

Project Status
Status: Completed
Track: Backend

The project includes:

AI-powered image analysis
Semantic embedding generation
Image-to-post matching
Matching validation guards
Review suggestions
Image approval and rejection
Batch embedding processing
AI usage tracking
PostgreSQL persistence
Docker deployment
Docker Compose orchestration
Automated tests
Evaluation dataset and evaluation script
Interactive API documentation