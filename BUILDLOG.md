\# Build Log



\## Project



\*\*FlyRank Backend Track Capstone — Image Matching Backend\*\*



\## Overview



Built a backend service that accepts image uploads, analyzes images using

Google Gemini, stores image metadata and AI descriptions in PostgreSQL, and

matches uploaded images with existing posts.



\## Technology Stack



\- Python

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Google Gemini API

\- Docker

\- Docker Compose

\- Pytest



\## Development Steps



\### 1. Backend Setup



Created a FastAPI backend with a modular application structure containing

API routes, database configuration, models, schemas, and services.



\### 2. PostgreSQL Integration



Configured PostgreSQL using Docker Compose and SQLAlchemy.



The database contains:



\- `posts`

\- `images`



The `images.post\_id` column is a foreign key referencing `posts.id`.



\### 3. Post APIs



Implemented endpoints for:



\- Creating posts

\- Listing posts

\- Retrieving an individual post



\### 4. Image Upload



Implemented `POST /images/upload`.



The endpoint:



1\. Accepts an image file.

2\. Saves the uploaded image.

3\. Sends the image to the Gemini vision model.

4\. Generates an AI description.

5\. Finds the best matching post.

6\. Stores the image metadata and matched post ID.

7\. Returns the matching information.



\### 5. AI Image Analysis



Integrated Google Gemini for image understanding.



The image is sent as image bytes with its MIME type so that the model

analyzes the actual image rather than relying on the filename.



The generated response contains:



\- Detailed description

\- Objects present

\- Scene type

\- Keywords



\### 6. Image-to-Post Matching



Implemented a matching service that compares the generated image description

with existing post title and content.



The post with the highest number of common words is selected as the best

match.



\### 7. Dockerization



Configured Docker and Docker Compose for the FastAPI application and

PostgreSQL database.



The application and database run as separate containers.



\### 8. Testing



Configured Pytest and verified the test suite.



The current test run completes successfully with no failed tests.



\## Verification



Verified:



\- FastAPI application starts successfully.

\- `/health` responds successfully.

\- `/docs` and `/openapi.json` are accessible.

\- PostgreSQL tables are created.

\- Posts can be stored and retrieved.

\- Images can be uploaded.

\- Gemini generates image descriptions.

\- Uploaded images are associated with matching posts.

\- Docker containers run successfully.

