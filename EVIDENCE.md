# FlyRank Capstone – Evidence

## Project

- Name: flyrank-capstone-image-matching
- Track: Backend
- Status: Completed
- Base URL: http://localhost:8000

## 1. Application Health

Command:

```powershell
docker compose ps
Verified services:

image-matching-api — running
image-matching-db — running
API exposed on port 8000
PostgreSQL exposed on port 5432

Health endpoint:

GET http://localhost:8000/health

Verified response:

{
  "status": "healthy"
}
2. Automated Tests

Command:

docker exec image-matching-api python -m pytest -q

Verified result:

.......................                                                  [100%]


23 passed, 1 warning

The test suite covers:

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
3. Evaluation

Command:

docker exec image-matching-api python -m evaluation.evaluate

Verified result:

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
Total cases	6
Correct predictions	6
Top-1 precision	100.00%

The 100% precision result applies specifically to the included six-case evaluation dataset.

4. Database Verification

Command:

docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"

Verified result:

 total_images | images_with_embedding | images_without_embedding
--------------+-----------------------+--------------------------
           12 |                    12 |                        0
(1 row)

This confirms that all 12 currently stored images have embeddings.

5. Posts Verification

Command:

docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT id, title FROM posts ORDER BY id;"

Verified posts:

 id |            title
----+-----------------------------
  1 | A Happy Dog at the Office
  2 | The Benefits of Having Pets
  3 | Vintage Tram Transportation
(3 rows)
6. AI Usage Verification

Command:

docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT operation, model, COUNT(*) FROM ai_usage GROUP BY operation, model ORDER BY operation;"

Verified result:

   operation    |        model         | count
----------------+----------------------+-------
 embedding      | gemini-embedding-001 |     7
 image_analysis | gemini-3.6-flash     |     4
(2 rows)

The application therefore records both image-analysis and embedding operations.

The API also exposes:

GET /ai-usage

The verified API response contains 14 total AI operation records.

7. API Documentation

Swagger documentation is available at:

http://localhost:8000/docs

OpenAPI specification is available at:

http://localhost:8000/openapi.json

The API was verified to load successfully.

8. Image Processing

The verified image processing flow is:

Image Upload
     |
     v
Image Validation
     |
     v
Google Gemini Image Analysis
     |
     v
Image Metadata
     |
     v
PostgreSQL Storage
     |
     v
Semantic Embedding Generation
     |
     v
Post Matching
     |
     v
Validation Guards
     |
     v
Review Suggestion

The upload endpoint is:

POST /images/upload

Supported formats:

JPEG
PNG
WEBP
GIF
9. Matching Verification

The matching service uses semantic embeddings and cosine similarity.

Implemented validation includes:

Confidence validation
Similarity threshold validation
Subject compatibility
Category compatibility
Invalid embedding handling
Zero-vector protection
Embedding dimension validation

The automated matching tests passed successfully.

The evaluation script also produced 6 correct predictions out of 6 cases.

10. Review Workflow

The application provides suggestion review endpoints:

GET  /suggestions
GET  /suggestions/{suggestion_id}
POST /suggestions/{suggestion_id}/approve
POST /suggestions/{suggestion_id}/reject

Image review endpoints:

POST /images/{image_id}/approve
POST /images/{image_id}/reject
GET  /images/{image_id}/review

This provides a human review workflow for AI-generated matching suggestions.

11. Batch Processing

The application provides:

POST /images/process-batch

The batch service:

Finds images without embeddings
Generates missing embeddings
Retries failed embedding operations
Records failures
Returns a processing summary

Current database verification shows:

Total images: 12
Images with embeddings: 12
Images without embeddings: 0
12. Docker Verification

Command:

docker compose ps

Verified services:

image-matching-api
image-matching-db

The API is exposed at:

http://localhost:8000

PostgreSQL is exposed at:

localhost:5432

The application successfully rebuilt and started with:

docker compose up --build -d
13. Final Verification Commands

The following commands can be used to reproduce the main verification checks:

docker compose up --build -d


docker compose ps


docker exec image-matching-api python -m pytest -q


docker exec image-matching-api python -m evaluation.evaluate


docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"


docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT operation, model, COUNT(*) FROM ai_usage GROUP BY operation, model ORDER BY operation;"
14. Final Verified Results
Verification	Result
Docker API container	Running
PostgreSQL container	Running
API health	Healthy
Automated tests	23 passed
Evaluation cases	6
Correct predictions	6
Evaluation top-1 precision	100.00%
Stored images	12
Images with embeddings	12
Images without embeddings	0
AI image analysis	Working
Embedding generation	Working
Image-to-post matching	Working
Review workflow	Implemented
Batch processing	Implemented
AI usage tracking	Implemented
PostgreSQL persistence	Working
Docker Compose deployment	Working
Swagger documentation	Available
15. Evidence Scope

The evidence above records the verification results obtained during development.

The 100% evaluation precision is based on the included six-case evaluation dataset and should not be interpreted as a guarantee of 100% accuracy on arbitrary real-world images.

The database counts and AI usage counts represent the state of the local development database at the time of verification.

16. Final Status

Project: flyrank-capstone-image-matching

Track: backend

Status: completed