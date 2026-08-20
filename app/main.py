from fastapi import FastAPI

from app.database.database import Base, engine

# Import every model so SQLAlchemy knows about all tables
from app.models.post import Post
from app.models.image import Image
from app.models.suggestion import Suggestion
from app.models.ai_usage import AIUsage

from app.api.routes import router


app = FastAPI(
    title="AI Image Understanding and Content Matching Engine",
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(router)