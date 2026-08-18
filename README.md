# AI Image Understanding & Content Matching Engine

An AI-powered backend service that analyzes uploaded images, generates AI descriptions, stores image metadata in PostgreSQL, and matches images with relevant blog posts.

The project is built using **FastAPI, PostgreSQL, Docker, SQLAlchemy, and Google Gemini AI**.

---

## 1. Project Overview

The AI Image Understanding & Content Matching Engine is a backend service designed to automatically understand uploaded images and determine which blog post is most relevant to the image.

The system provides:

1. Image upload through a REST API.
2. AI-powered image analysis using Google Gemini.
3. Image metadata storage in PostgreSQL.
4. Blog post creation and retrieval.
5. Matching between image descriptions and blog posts.
6. Persistent storage using PostgreSQL.
7. Containerized execution using Docker Compose.

The project is designed as a backend-first service and does not require a frontend UI.

---

## 2. Problem Statement

Content platforms often contain many blog posts and images. Manually selecting the most appropriate image for each post can be slow and inconsistent.

This project explores an automated backend workflow:

```text
Uploaded Image
      |
      v
 Gemini Vision Analysis
      |
      v
 Image Description / Metadata
      |
      v
 PostgreSQL
      |
      v
 Matching Engine
      |
      v
 Relevant Blog Post