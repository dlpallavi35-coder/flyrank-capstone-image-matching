import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.image import Image
from app.models.post import Post
from app.models.suggestion import Suggestion
from app.services.embedding_service import generate_embedding
from app.services.matching_service import find_best_matching_post
from app.services.matching_service import find_best_image_for_post
from app.services.batch_service import process_image_embeddings
from app.services.vision_service import analyze_image


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root():
    return {
        "message": "AI Image Understanding and Content Matching Engine"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post("/posts")
def create_post(
    title: str,
    content: str,
    author: str,
    db: Session = Depends(get_db),
):
    post = Post(
        title=title,
        content=content,
        author=author,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    # Generate the semantic embedding for the post.
    try:
        post.embedding = generate_embedding(
    f"{post.title} {post.content}",
    db,
)
        db.commit()
        db.refresh(post)
    except Exception:
        # The post is still created if embedding generation fails.
        pass

    return post


@router.get("/posts")
def get_posts(
    db: Session = Depends(get_db),
):
    return db.query(Post).all()


@router.get("/posts/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post


@router.get("/posts/{post_id}/images")
def get_post_image_matches(
    post_id: int,
    db: Session = Depends(get_db),
):
    return find_best_image_for_post(
        post_id=post_id,
        db=db,
    )


@router.post("/images/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format",
        )

    upload_directory = "uploads"
    os.makedirs(upload_directory, exist_ok=True)

    filename = file.filename or "uploaded_image"

    file_path = os.path.join(
        upload_directory,
        filename,
    )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty",
        )

    with open(file_path, "wb") as image_file:
        image_file.write(image_bytes)

    # ---------------------------------------------------------
    # 1. Vision analysis
    # ---------------------------------------------------------

    try:
        metadata = analyze_image(file_path, db)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Image analysis failed: {error}",
        )

    metadata_dict = {
        "subject": metadata.subject,
        "category": metadata.category,
        "attributes": metadata.attributes,
        "caption": metadata.caption,
        "confidence": metadata.confidence,
    }

    # ---------------------------------------------------------
    # 2. Store image metadata
    # ---------------------------------------------------------

    image = Image(
        filename=filename,
        file_path=file_path,
        ai_description=metadata.caption,
        confidence=metadata_dict,
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    # ---------------------------------------------------------
    # 3. Generate image embedding
    # ---------------------------------------------------------

    try:
        image.embedding = generate_embedding(
    metadata.caption,
    db,
)

        db.commit()
        db.refresh(image)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Image embedding generation failed: {error}",
        )

    # ---------------------------------------------------------
    # 4. Find candidate post
    # ---------------------------------------------------------

    match_result = find_best_matching_post(
        image_description=metadata.caption,
        db=db,
        image_metadata=metadata_dict,
    )

    matched_post = match_result.get("post")

    if (
        match_result["status"] == "matched"
        and matched_post is not None
    ):
        image.post_id = matched_post.id

        db.commit()
        db.refresh(image)

    # ---------------------------------------------------------
    # 5. Create review suggestion
    # ---------------------------------------------------------

    suggestion = Suggestion(
        image_id=image.id,
        post_id=(
            matched_post.id
            if matched_post is not None
            else None
        ),
        similarity=match_result["similarity"],
        status="pending",
        reason=match_result["reason"],
    )

    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)

    # ---------------------------------------------------------
    # 6. Return complete result
    # ---------------------------------------------------------

    return {
        "image_id": image.id,
        "filename": image.filename,

        "metadata": metadata_dict,

        "embedding": {
            "generated": image.embedding is not None,
            "dimensions": (
                len(image.embedding)
                if image.embedding
                else 0
            ),
        },

        "matching": {
            "status": match_result["status"],
            "similarity": match_result["similarity"],
            "reason": match_result["reason"],
            "post_id": (
                matched_post.id
                if matched_post is not None
                else None
            ),
            "post_title": (
                matched_post.title
                if matched_post is not None
                else None
            ),
            "suggestion_id": suggestion.id,
        },
    }


# -------------------------------------------------------------
# Suggestions / review workflow
# -------------------------------------------------------------


@router.get("/suggestions")
def get_suggestions(
    db: Session = Depends(get_db),
):
    return (
        db.query(Suggestion)
        .order_by(
            Suggestion.created_at.desc()
        )
        .all()
    )


@router.get("/suggestions/{suggestion_id}")
def get_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    suggestion = (
        db.query(Suggestion)
        .filter(
            Suggestion.id == suggestion_id
        )
        .first()
    )

    if not suggestion:
        raise HTTPException(
            status_code=404,
            detail="Suggestion not found",
        )

    return suggestion


@router.post("/suggestions/{suggestion_id}/approve")
def approve_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    suggestion = (
        db.query(Suggestion)
        .filter(
            Suggestion.id == suggestion_id
        )
        .first()
    )

    if not suggestion:
        raise HTTPException(
            status_code=404,
            detail="Suggestion not found",
        )

    if suggestion.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Suggestion has already been reviewed",
        )

    suggestion.status = "approved"
    suggestion.reviewed_at = datetime.utcnow()

    if suggestion.post_id is not None:
        image = (
            db.query(Image)
            .filter(
                Image.id == suggestion.image_id
            )
            .first()
        )

        if image:
            image.post_id = suggestion.post_id

    db.commit()
    db.refresh(suggestion)

    return {
        "message": "Suggestion approved",
        "suggestion": suggestion,
    }


@router.post("/suggestions/{suggestion_id}/reject")
def reject_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    suggestion = (
        db.query(Suggestion)
        .filter(
            Suggestion.id == suggestion_id
        )
        .first()
    )

    if not suggestion:
        raise HTTPException(
            status_code=404,
            detail="Suggestion not found",
        )

    if suggestion.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Suggestion has already been reviewed",
        )

    suggestion.status = "rejected"
    suggestion.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(suggestion)

    return {
        "message": "Suggestion rejected",
        "suggestion": suggestion,
    }


# -------------------------------------------------------------
# Image review workflow
# -------------------------------------------------------------


@router.post("/images/{image_id}/approve")
def approve_image(
    image_id: int,
    db: Session = Depends(get_db),
):
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    image.review_status = "approved"
    image.review_reason = "Approved by reviewer"

    db.commit()
    db.refresh(image)

    return {
        "image_id": image.id,
        "review_status": image.review_status,
        "review_reason": image.review_reason,
    }


@router.post("/images/{image_id}/reject")
def reject_image(
    image_id: int,
    db: Session = Depends(get_db),
):
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    image.review_status = "rejected"
    image.review_reason = "Rejected by reviewer"

    db.commit()
    db.refresh(image)

    return {
        "image_id": image.id,
        "review_status": image.review_status,
        "review_reason": image.review_reason,
    }


@router.get("/images/{image_id}/review")
def inspect_image_review(
    image_id: int,
    db: Session = Depends(get_db),
):
    image = (
        db.query(Image)
        .filter(Image.id == image_id)
        .first()
    )

    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )

    return {
        "image_id": image.id,
        "filename": image.filename,
        "review_status": image.review_status,
        "review_reason": image.review_reason,
        "confidence": image.confidence,
    }


# -------------------------------------------------------------
# Batch processing
# -------------------------------------------------------------


@router.post("/images/process-batch")
def process_images_batch(
    db: Session = Depends(get_db),
):
    return process_image_embeddings(db)


# -------------------------------------------------------------
# AI usage / cost tracking
# -------------------------------------------------------------


@router.get("/ai-usage")
def get_ai_usage(
    db: Session = Depends(get_db),
):
    from app.models.ai_usage import AIUsage

    usage = (
        db.query(AIUsage)
        .order_by(
            AIUsage.created_at.desc()
        )
        .all()
    )

    total_cost = sum(
        item.estimated_cost
        for item in usage
    )

    return {
        "total_operations": len(usage),

        "total_input_tokens": sum(
            item.input_tokens
            for item in usage
        ),

        "total_output_tokens": sum(
            item.output_tokens
            for item in usage
        ),

        "total_estimated_cost": round(
            total_cost,
            8,
        ),

        "records": [
            {
                "id": item.id,
                "operation": item.operation,
                "model": item.model,
                "input_tokens": item.input_tokens,
                "output_tokens": item.output_tokens,
                "estimated_cost": item.estimated_cost,
                "created_at": item.created_at,
            }
            for item in usage
        ],
    }