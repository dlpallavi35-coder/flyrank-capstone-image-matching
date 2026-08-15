from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
import shutil
import os
from app.database.database import get_db
from app.models.post import Post
from app.schemas.post_schema import PostCreate

router = APIRouter()


@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        title=post.title,
        content=post.content,
        author=post.author
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
def upload_image(file: UploadFile = File(...)):
    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Image uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }