# FlyRank Capstone – Evidence

## Project Verification Evidence

**Project:** FlyRank Capstone – AI Image Matching Engine

**Track:** Backend

**Repository:**

https://github.com/dlpallavi35-coder/flyrank-capstone-image-matching

**Status:** Completed

---

## 1. Docker Verification

### Command

```bash
docker compose ps
```

### Verified Services

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

## 2. Automated Test Evidence

### Command

```bash
docker exec image-matching-api python -m pytest -q
```

### Verified Result

```text
23 passed, 1 warning
```

### Test Coverage

The automated tests cover:

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

## 3. Evaluation Evidence

### Command

```bash
docker exec image-matching-api python -m evaluation.evaluate
```

### Verified Result

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

### Evaluation Summary

| Metric | Result |
|---|---:|
| Total evaluation cases | 6 |
| Correct predictions | 6 |
| Top-1 precision | 100% |

The 100% result applies to the included six-case evaluation dataset.

---

## 4. Database and Embedding Evidence

### Command

```bash
docker exec image-matching-db psql -U postgres -d image_matching_db -c "SELECT COUNT(*) AS total_images, COUNT(embedding) AS images_with_embedding, COUNT(*) - COUNT(embedding) AS images_without_embedding FROM images;"
```

### Verified Result

```text
 total_images | images_with_embedding | images_without_embedding
--------------+-----------------------+--------------------------
           13 |                    13 |                        0
```

### Result

```text
Total images: 13
Images with embeddings: 13
Images without embeddings: 0
```

This confirms that all currently stored images have generated embeddings.

---

## 5. AI Usage Evidence

### Endpoint

```text
GET /ai-usage
```

### Verified Usage Summary

```json
{
  "total_operations": 14,
  "total_input_tokens": 0,
  "total_output_tokens": 0,
  "total_estimated_cost": 0
}
```

The usage records include:

```text
image_analysis
model: gemini-3.6-flash
```

and:

```text
embedding
model: gemini-embedding-001
```

The records confirm that the application has executed both image-analysis and embedding operations.

---

## 6. Gemini DNS Evidence

### Command

```bash
docker exec image-matching-api python -c "import socket; print(socket.gethostbyname('generativelanguage.googleapis.com'))"
```

### Verified Result

```text
172.217.116.4
```

This confirms that the API container can resolve:

```text
generativelanguage.googleapis.com
```

---

## 7. Gemini TCP Connectivity Evidence

### Command

```bash
docker exec image-matching-api python -c "import socket; s=socket.create_connection(('generativelanguage.googleapis.com',443),timeout=15); print('TCP 443 OK'); s.close()"
```

### Verified Result

```text
TCP 443 OK
```

This confirms TCP connectivity from the API container to HTTPS port 443.

---

## 8. Gemini TLS Evidence

### Command

```bash
docker exec image-matching-api python -c "import ssl,socket; s=socket.create_connection(('generativelanguage.googleapis.com',443),timeout=15); c=ssl.create_default_context().wrap_socket(s,server_hostname='generativelanguage.googleapis.com'); print('TLS OK:', c.version()); c.close()"
```

### Verified Result

```text
TLS OK: TLSv1.3
```

This confirms successful TLS negotiation from the API container.

---

## 9. OpenSSL Evidence

### Command

```bash
docker exec image-matching-api python -c "import ssl; print(ssl.OPENSSL_VERSION)"
```

### Verified Result

```text
OpenSSL 3.5.6 7 Apr 2026
```

---

## 10. API Documentation Evidence

FastAPI Swagger documentation is available at:

```text
http://localhost:8000/docs
```

OpenAPI documentation is available at:

```text
http://localhost:8000/openapi.json
```

---

## 11. Health Check Evidence

The application provides:

```text
GET /health
```

Expected healthy response:

```json
{
  "status": "healthy"
}
```

---

## 12. Image Processing Evidence

The implemented image-processing flow is:

```text
Image Upload
      |
      v
Image Validation
      |
      v
Gemini Image Analysis
      |
      v
Image Metadata
      |
      v
PostgreSQL Storage
      |
      v
Semantic Embedding
      |
      v
Post Embedding Comparison
      |
      v
Cosine Similarity
      |
      v
Validation Guards
      |
      v
Review Suggestion
```

---

## 13. Matching Evidence

The matching system uses semantic embeddings and cosine similarity.

Implemented validation includes:

- Similarity threshold validation
- Confidence validation
- Subject compatibility
- Category compatibility
- Invalid embedding handling
- Zero-vector protection
- Embedding dimension validation

The automated test suite verifies both successful matches and rejection cases.

---

## 14. Review Workflow Evidence

The application implements suggestion review actions:

```text
Pending
Approved
Rejected
```

Suggestion endpoints include:

```text
GET /suggestions
GET /suggestions/{suggestion_id}
POST /suggestions/{suggestion_id}/approve
POST /suggestions/{suggestion_id}/reject
```

Image review endpoints include:

```text
GET /images/{image_id}/review
POST /images/{image_id}/approve
POST /images/{image_id}/reject
```

---

## 15. Batch Processing Evidence

The application provides:

```text
POST /images/process-batch
```

The batch processing service handles images that do not have embeddings.

The current database verification shows:

```text
Total images: 13
Images with embeddings: 13
Images without embeddings: 0
```
### Verified Batch Endpoint Result

```text
HTTP/1.1 202 Accepted

{"status":"started","message":"Image embedding batch processing started in the background"}
```
---

## 16. Complete Verification Commands

The complete project verification can be reproduced using:

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

```bash
docker exec image-matching-api python -c "import socket; print(socket.gethostbyname('generativelanguage.googleapis.com'))"
```

```bash
docker exec image-matching-api python -c "import ssl; print(ssl.OPENSSL_VERSION)"
```

```bash
docker exec image-matching-api python -c "import socket; s=socket.create_connection(('generativelanguage.googleapis.com',443),timeout=15); print('TCP 443 OK'); s.close()"
```

```bash
docker exec image-matching-api python -c "import ssl,socket; s=socket.create_connection(('generativelanguage.googleapis.com',443),timeout=15); c=ssl.create_default_context().wrap_socket(s,server_hostname='generativelanguage.googleapis.com'); print('TLS OK:', c.version()); c.close()"
```

---

## 17. Final Evidence Summary

| Verification | Result |
|---|---|
| Docker API container | Working |
| PostgreSQL container | Working |
| FastAPI application | Working |
| Gemini DNS resolution | Working |
| Gemini TCP 443 | Working |
| Gemini TLS | TLS 1.3 |
| OpenSSL | 3.5.6 |
| Automated tests | 23 passed |
| Evaluation cases | 6 |
| Correct evaluation predictions | 6 |
| Evaluation precision | 100% |
| Stored images | 13 |
| Images with embeddings | 13 |
| Images without embeddings | 0 |
| Image analysis records | Present |
| Embedding records | Present |
| Image matching | Working |
| Review workflow | Implemented |
| Batch processing | Implemented |
| AI usage tracking | Implemented |
| Swagger documentation | Available |

---

## Final Status

The FlyRank Capstone backend has been verified through Docker, database, AI connectivity, automated tests, evaluation, embedding verification, and AI usage records.

**Project Status: Completed**

**Track: Backend**