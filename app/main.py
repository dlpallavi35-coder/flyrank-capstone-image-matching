from fastapi import FastAPI

from app.database.database import Base, engine

app = FastAPI(
    title="AI Image Understanding & Content Matching Engine",
    version="1.0.0"
)
from app.models.post import Post
from app.models.image import Image
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "AI Image Matching Engine Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }