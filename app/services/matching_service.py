import math
from typing import Any

from sqlalchemy.orm import Session

from app.models.image import Image
from app.models.post import Post


# Main semantic similarity threshold.
# The guard will only accept a recommendation when
# the similarity is high enough AND the image is compatible
# with the post.
SIMILARITY_THRESHOLD = 0.35

# Minimum vision confidence required for an automatic recommendation.
CONFIDENCE_THRESHOLD = 0.60
def _context_adjustment(
    image_description: str,
    post: Post,
) -> float:
    """
    Adjust semantic similarity using explicit contextual clues.
    """

    description = (image_description or "").lower()
    post_text = f"{post.title} {post.content}".lower()

    adjustment = 0.0

    # Office-specific posts should not win when the
    # description does not mention office/work context.
    office_terms = {
        "office",
        "workplace",
        "desk",
        "work",
    }

    if (
        any(term in post_text for term in office_terms)
        and not any(term in description for term in office_terms)
    ):
        adjustment -= 0.12

    # Give a small boost when the description explicitly
    # talks about pets/people and the post does too.
    pet_terms = {
        "pet",
        "pets",
        "people",
        "companionship",
    }

    if (
        any(term in description for term in pet_terms)
        and any(term in post_text for term in pet_terms)
    ):
        adjustment += 0.08

    return adjustment

def _cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    Calculate cosine similarity between two embedding vectors.
    """

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        return 0.0

    dot_product = sum(
        float(a) * float(b)
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(float(value) ** 2 for value in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(float(value) ** 2 for value in vector_b)
    )

    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0

    similarity = dot_product / (
        magnitude_a * magnitude_b
    )

    return max(-1.0, min(1.0, similarity))


def _normalise_embedding(
    embedding: Any,
) -> list[float] | None:
    """
    Convert a database JSON embedding into a list of floats.
    """

    if embedding is None:
        return None

    if not isinstance(embedding, list):
        return None

    try:
        return [float(value) for value in embedding]
    except (TypeError, ValueError):
        return None


def _extract_image_metadata(image: Image) -> dict:
    """
    Safely extract the structured vision metadata stored
    in the confidence JSON field.
    """

    metadata = image.confidence

    if not isinstance(metadata, dict):
        metadata = {}

    attributes = metadata.get("attributes", [])

    if not isinstance(attributes, list):
        attributes = []

    return {
        "subject": str(
            metadata.get("subject", "")
        ).strip().lower(),

        "category": str(
            metadata.get("category", "")
        ).strip().lower(),

        "attributes": [
            str(attribute).strip().lower()
            for attribute in attributes
            if attribute
        ],

        "caption": str(
            metadata.get("caption", "")
        ).strip(),

        "confidence": _safe_confidence(
            metadata.get("confidence")
        ),
    }


def _safe_confidence(value: Any) -> float:
    """
    Convert confidence to a safe value between 0 and 1.
    """

    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0

    return max(
        0.0,
        min(1.0, confidence),
    )


def _guard_image(
    image: Image,
    post: Post,
    similarity: float,
) -> tuple[bool, str]:
    """
    Mismatch guard.

    The recommendation is accepted only when:
    1. The semantic similarity clears the threshold.
    2. Vision confidence is high enough.
    3. Explicit subject/category mismatches are not detected.
    """

    metadata = _extract_image_metadata(image)

    confidence = metadata["confidence"]
    subject = metadata["subject"]
    category = metadata["category"]

    post_text = (
        f"{post.title} {post.content}"
    ).lower()

    # ---------------------------------------------------------
    # Confidence guard
    # ---------------------------------------------------------

    if confidence < CONFIDENCE_THRESHOLD:
        return (
            False,
            (
                "Rejected because image understanding "
                f"confidence is too low ({confidence:.2f})"
            ),
        )

    # ---------------------------------------------------------
    # Similarity guard
    # ---------------------------------------------------------

    if similarity < SIMILARITY_THRESHOLD:
        return (
            False,
            (
                "Rejected because semantic similarity "
                f"({similarity:.4f}) is below the required "
                f"threshold ({SIMILARITY_THRESHOLD:.2f})"
            ),
        )

    # ---------------------------------------------------------
    # Explicit subject mismatch guard
    # ---------------------------------------------------------

    animal_subjects = {
        "fox",
        "wolf",
        "dog",
        "cat",
        "bear",
        "deer",
        "horse",
        "bird",
        "rabbit",
    }

    post_subject = None

    for animal in animal_subjects:
        if animal in post_text:
            post_subject = animal
            break

    if (
        post_subject
        and subject
        and post_subject != subject
        and subject in animal_subjects
    ):
        return (
            False,
            (
                "Rejected by mismatch guard: "
                f"image subject is '{subject}' but the "
                f"post is about '{post_subject}'"
            ),
        )

    # ---------------------------------------------------------
    # Category mismatch guard
    # ---------------------------------------------------------

    if category:
        category_keywords = {
            "animal": {
                "animal",
                "fox",
                "wolf",
                "dog",
                "cat",
                "bear",
                "deer",
                "horse",
                "bird",
                "rabbit",
            },
            "vehicle": {
                "vehicle",
                "car",
                "truck",
                "bus",
                "tram",
                "train",
                "bicycle",
                "motorcycle",
            },
            "food": {
                "food",
                "meal",
                "dish",
                "fruit",
                "vegetable",
            },
            "person": {
                "person",
                "people",
                "human",
                "man",
                "woman",
                "child",
            },
            "landscape": {
                "landscape",
                "mountain",
                "forest",
                "beach",
                "lake",
                "river",
            },
        }

        for group_name, keywords in category_keywords.items():

            if category not in keywords:
                continue

            post_mentions_group = any(
                keyword in post_text
                for keyword in keywords
            )

            if (
                not post_mentions_group
                and group_name in {
                    "vehicle",
                    "food",
                    "person",
                    "landscape",
                }
            ):
                return (
                    False,
                    (
                        "Rejected by mismatch guard: "
                        f"image category '{category}' does not "
                        "match the post content"
                    ),
                )

            break

    return (
        True,
        "Passed semantic similarity, confidence, and mismatch guards",
    )
def _description_subject_mismatch(
    image_description: str,
    post: Post,
) -> bool:
    """
    Reject clearly incompatible animal subjects.
    """

    description = (image_description or "").lower()
    post_text = f"{post.title} {post.content}".lower()

    animal_subjects = {
        "fox",
        "wolf",
        "dog",
        "cat",
        "bear",
        "deer",
        "horse",
        "bird",
        "rabbit",
    }

    detected_subject = None

    for animal in animal_subjects:
        if animal in description:
            detected_subject = animal
            break

    if detected_subject is None:
        return False

    # If the image explicitly identifies an animal,
    # don't match it to a post explicitly about a different animal.
    for animal in animal_subjects:
        if animal in post_text and animal != detected_subject:
            return True

    return False
def _description_category_mismatch(
    image_description: str,
    post: Post,
) -> bool:
    """
    Reject clearly incompatible high-level categories.
    """

    description = (image_description or "").lower()
    post_text = f"{post.title} {post.content}".lower()

    animal_words = {
        "dog", "cat", "fox", "wolf", "bear",
        "deer", "horse", "bird", "rabbit",
    }

    vehicle_words = {
        "tram", "train", "bus", "car", "truck",
        "vehicle", "railway", "streetcar",
        "transportation",
    }

    image_is_animal = any(
        word in description
        for word in animal_words
    )

    image_is_vehicle = any(
        word in description
        for word in vehicle_words
    )

    post_is_animal = any(
        word in post_text
        for word in animal_words
    )

    post_is_vehicle = any(
        word in post_text
        for word in vehicle_words
    )

    if image_is_animal and post_is_vehicle:
        return True

    if image_is_vehicle and post_is_animal:
        return True

    return False
def find_best_matching_post(
    image_description: str,
    db: Session,
    image_metadata=None,
):
    """
    Match a text/image description to the best post using
    semantic embeddings.

    This function is used by the evaluation workflow and
    remains compatible with the upload workflow.
    """

    posts = db.query(Post).all()

    if not posts:
        return {
            "status": "rejected",
            "similarity": 0.0,
            "reason": "No posts are available for matching",
            "post": None,
        }

    # Import here to avoid unnecessary circular imports.
    from app.services.embedding_service import generate_embedding

    try:
        query_embedding = generate_embedding(
            image_description or "",
            db=db,
        )
    except Exception as exc:
        return {
            "status": "rejected",
            "similarity": 0.0,
            "reason": f"Embedding generation failed: {exc}",
            "post": None,
        }

    query_embedding = _normalise_embedding(
        query_embedding
    )

    if query_embedding is None:
        return {
            "status": "rejected",
            "similarity": 0.0,
            "reason": "Query embedding could not be generated",
            "post": None,
        }

    candidates = []

    for post in posts:

        if _description_subject_mismatch(
            image_description,
            post,
    ):
            continue

        if _description_category_mismatch(
            image_description,
            post,
    ):
            continue

        post_embedding = _normalise_embedding(
            post.embedding
    )

        if post_embedding is None:
            continue

        similarity = _cosine_similarity(
        query_embedding,
        post_embedding,
)

        adjusted_similarity = similarity + _context_adjustment(
        image_description,
        post,
)

        candidates.append(
    {
        "post": post,
        "similarity": adjusted_similarity,
        "embedding_similarity": similarity,
    }
)

    if not candidates:
        return {
            "status": "rejected",
            "similarity": 0.0,
            "reason": (
                "No posts with valid embeddings are available"
            ),
            "post": None,
        }

    candidates.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    best_candidate = candidates[0]

    return {
        "status": "matched",
        "similarity": round(
            best_candidate["similarity"],
            4,
        ),
        "reason": "Best semantic match was found",
        "post": best_candidate["post"],
    }
def find_best_image_for_post(
    post_id: int,
    db: Session,
):
    """
    Rank stored image embeddings against a post embedding.

    Every candidate passes through the mismatch guard before
    it can become the final recommendation.
    """

    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        return {
            "post_id": post_id,
            "match": None,
            "status": "rejected",
            "similarity": 0.0,
            "reason": "Post not found",
        }

    post_embedding = _normalise_embedding(
        post.embedding
    )

    if post_embedding is None:
        return {
            "post_id": post_id,
            "match": None,
            "status": "rejected",
            "similarity": 0.0,
            "reason": (
                "Post embedding is missing. "
                "Run the post embedding process first."
            ),
        }

    images = (
        db.query(Image)
        .filter(Image.embedding.isnot(None))
        .all()
    )

    if not images:
        return {
            "post_id": post_id,
            "match": None,
            "status": "rejected",
            "similarity": 0.0,
            "reason": "No embedded images are available",
        }

    candidates = []

    for image in images:
        image_embedding = _normalise_embedding(
            image.embedding
        )

        if image_embedding is None:
            continue

        similarity = _cosine_similarity(
            post_embedding,
            image_embedding,
        )

        guard_passed, guard_reason = _guard_image(
            image=image,
            post=post,
            similarity=similarity,
        )

        candidates.append(
            {
                "image": image,
                "similarity": similarity,
                "guard_passed": guard_passed,
                "reason": guard_reason,
            }
        )

    if not candidates:
        return {
            "post_id": post_id,
            "match": None,
            "status": "rejected",
            "similarity": 0.0,
            "reason": (
                "No valid embedded image candidates "
                "are available"
            ),
        }

    candidates.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    accepted_candidates = [
        candidate
        for candidate in candidates
        if candidate["guard_passed"]
    ]

    if not accepted_candidates:
        best_candidate = candidates[0]

        return {
            "post_id": post_id,
            "match": None,
            "status": "rejected",
            "similarity": round(
                best_candidate["similarity"],
                4,
            ),
            "reason": (
                "No confident match: "
                + best_candidate["reason"]
            ),
            "rejected_candidates": len(candidates),
        }

    best_candidate = accepted_candidates[0]
    best_image = best_candidate["image"]

    return {
        "post_id": post_id,
        "match": {
            "image_id": best_image.id,
            "filename": best_image.filename,
        },
        "status": "matched",
        "similarity": round(
            best_candidate["similarity"],
            4,
        ),
        "reason": best_candidate["reason"],
        "candidate_count": len(candidates),
    }