\# Evidence



\## 1. Application Health



The FastAPI application exposes a health endpoint:



`GET /health`



The endpoint was successfully tested while the Docker container was running.



\## 2. API Documentation



FastAPI documentation is available through:



`GET /docs`



The OpenAPI specification was also verified successfully through:



`GET /openapi.json`



\## 3. PostgreSQL Database



The PostgreSQL database is running in the Docker container:



`image-matching-db`



Database name:



`image\_matching\_db`



The database contains the following application tables:



\- `posts`

\- `images`



\## 4. Posts



The database was verified to contain posts including:



\- A Happy Dog at the Office

\- The Benefits of Having Pets

\- Vintage Tram Transportation



\## 5. Image Storage



The `images` table contains:



\- Image ID

\- Filename

\- File path

\- AI description

\- Upload timestamp

\- Matched post ID



\## 6. AI Image Analysis



Uploaded images are analyzed using Google Gemini.



The generated description includes information about the visible image,

objects, scene type, and relevant keywords.



\## 7. Image-to-Post Matching



The image matching workflow was verified in PostgreSQL.



Example verified result:



\- Image ID: `5`

\- Filename: `Dog\_picture.webp`

\- Matched Post ID: `1`

\- Matched Post: `A Happy Dog at the Office`



The relationship was verified using a SQL JOIN between the `images` and

`posts` tables.



\## 8. Docker



The application was successfully run using Docker Compose.



Running containers include:



\- `image-matching-api`

\- `image-matching-db`



The API is exposed on port `8000`.



\## 9. Automated Tests



Pytest was installed and executed using:



`python -m pytest -q`



The test run completed without test failures.



A dependency deprecation warning was displayed by the Google GenAI package,

but it did not cause the test run to fail.

