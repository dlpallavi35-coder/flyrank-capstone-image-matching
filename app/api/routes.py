from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
import shutil
import os
from app.models.image import Image
from app.database.database import get_db
from app.models.post import Post
from app.schemas.post_schema import PostCreate
from app.services.vision_service import analyze_image
from app.services.matching_service import find_best_matching_post
from app.services.embedding_service import generate_embedding

router = APIRouter()


@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_text = f"{post.title} {post.content}"

    embedding = generate_embedding(post_text)

    new_post = Post(
        title=post.title,
        content=post.content,
        author=post.author,
        embedding=embedding
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post
@router.post("/images/upload")
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    description = analyze_image(file_path)

    matched_post = find_best_matching_post(
    image_description=description,
    db=db
)

    image = Image(
    filename=file.filename,
    file_path=file_path,
    ai_description=description,
    post_id=matched_post.id if matched_post else None
)   

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
    "message": "Image uploaded successfully",
    "image_id": image.id,
    "filename": image.filename,
    "path": image.file_path,
    "ai_description": image.ai_description,
    "matched_post_id": matched_post.id if matched_post else None,
    "matched_post_title": matched_post.title if matched_post else None
}