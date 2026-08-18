from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.post import Post
from app.models.image import Image

from app.api.routes import router


app = FastAPI(
    title="AI Image Understanding & Content Matching Engine",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


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