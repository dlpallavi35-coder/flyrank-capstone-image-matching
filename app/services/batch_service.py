import time
from typing import Callable

from sqlalchemy.orm import Session

from app.models.image import Image
from app.services.embedding_service import generate_embedding


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def _run_with_retry(
    operation: Callable,
    max_retries: int = MAX_RETRIES,
):
    last_error = None

    for attempt in range(max_retries):
        try:
            return operation()

        except Exception as error:
            last_error = error

            if attempt == max_retries - 1:
                raise

            time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))

    raise last_error


def process_image_embeddings(
    db: Session,
) -> dict:

    images = (
        db.query(Image)
        .filter(Image.embedding.is_(None))
        .all()
    )

    processed = 0
    failed = 0
    failures = []

    for image in images:
        try:
            text = image.ai_description or image.filename

            embedding = _run_with_retry(
                lambda: generate_embedding(
                    text,
                    db=db,
                )
            )

            image.embedding = embedding

            processed += 1

        except Exception as error:
            failed += 1

            failures.append(
                {
                    "image_id": image.id,
                    "filename": image.filename,
                    "error": str(error),
                }
            )

    db.commit()

    return {
        "total": len(images),
        "processed": processed,
        "failed": failed,
        "failures": failures,
    }