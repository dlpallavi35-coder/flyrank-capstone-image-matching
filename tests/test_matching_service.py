from types import SimpleNamespace

from app.services.matching_service import (
    _cosine_similarity,
    _normalise_embedding,
    _safe_confidence,
    _guard_image,
)


def test_cosine_similarity_identical_vectors():
    result = _cosine_similarity(
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    )

    assert result == 1.0


def test_cosine_similarity_orthogonal_vectors():
    result = _cosine_similarity(
        [1.0, 0.0],
        [0.0, 1.0],
    )

    assert result == 0.0


def test_cosine_similarity_zero_vector():
    result = _cosine_similarity(
        [0.0, 0.0],
        [1.0, 2.0],
    )

    assert result == 0.0


def test_cosine_similarity_different_dimensions():
    result = _cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0, 0.0],
    )

    assert result == 0.0


def test_normalise_embedding_valid_list():
    result = _normalise_embedding(
        [1, 2, 3.5]
    )

    assert result == [1.0, 2.0, 3.5]


def test_normalise_embedding_none():
    result = _normalise_embedding(None)

    assert result is None


def test_normalise_embedding_invalid_type():
    result = _normalise_embedding(
        "not-an-embedding"
    )

    assert result is None


def test_normalise_embedding_invalid_value():
    result = _normalise_embedding(
        [1, "invalid", 3]
    )

    assert result is None


def test_safe_confidence_valid_value():
    assert _safe_confidence(0.85) == 0.85


def test_safe_confidence_clamps_high_value():
    assert _safe_confidence(1.5) == 1.0


def test_safe_confidence_clamps_low_value():
    assert _safe_confidence(-0.5) == 0.0


def test_safe_confidence_invalid_value():
    assert _safe_confidence("invalid") == 0.0
def test_guard_rejects_low_confidence_image():
    image = SimpleNamespace(
        confidence={
            "subject": "dog",
            "category": "animal",
            "attributes": ["indoors"],
            "caption": "A dog indoors.",
            "confidence": 0.40,
        }
    )

    post = SimpleNamespace(
        title="A Happy Dog at the Office",
        content="A friendly dog sitting indoors in an office.",
    )

    accepted, reason = _guard_image(
        image=image,
        post=post,
        similarity=0.90,
    )

    assert accepted is False
    assert "confidence" in reason.lower()


def test_guard_rejects_low_similarity():
    image = SimpleNamespace(
        confidence={
            "subject": "dog",
            "category": "animal",
            "attributes": ["indoors"],
            "caption": "A happy dog indoors.",
            "confidence": 0.98,
        }
    )

    post = SimpleNamespace(
        title="A Happy Dog at the Office",
        content="A friendly dog sitting indoors in an office.",
    )

    accepted, reason = _guard_image(
        image=image,
        post=post,
        similarity=0.20,
    )

    assert accepted is False
    assert "similarity" in reason.lower()


def test_guard_rejects_wolf_for_dog_post():
    image = SimpleNamespace(
        confidence={
            "subject": "wolf",
            "category": "animal",
            "attributes": ["forest"],
            "caption": "A wolf walking through a forest.",
            "confidence": 0.98,
        }
    )

    post = SimpleNamespace(
        title="A Happy Dog at the Office",
        content=(
            "Dogs can bring happiness and positive energy "
            "to the workplace. A friendly Golden Retriever "
            "sitting indoors can make an office environment "
            "feel warm and welcoming."
        ),
    )

    accepted, reason = _guard_image(
        image=image,
        post=post,
        similarity=0.90,
    )

    assert accepted is False
    assert "wolf" in reason.lower()
    assert "dog" in reason.lower()


def test_guard_accepts_dog_for_dog_post():
    image = SimpleNamespace(
        confidence={
            "subject": "dog",
            "category": "animal",
            "attributes": ["indoors"],
            "caption": "A happy dog sitting inside an office.",
            "confidence": 0.98,
        }
    )

    post = SimpleNamespace(
        title="A Happy Dog at the Office",
        content=(
            "Dogs can bring happiness and positive energy "
            "to the workplace. A friendly Golden Retriever "
            "sitting indoors can make an office environment "
            "feel warm and welcoming."
        ),
    )

    accepted, reason = _guard_image(
        image=image,
        post=post,
        similarity=0.90,
    )

    assert accepted is True
    assert "passed" in reason.lower()


def test_guard_rejects_vehicle_for_dog_post():
    image = SimpleNamespace(
        confidence={
            "subject": "tram",
            "category": "vehicle",
            "attributes": ["city"],
            "caption": "A vintage tram traveling through a city.",
            "confidence": 0.98,
        }
    )

    post = SimpleNamespace(
        title="A Happy Dog at the Office",
        content=(
            "Dogs can bring happiness and positive energy "
            "to the workplace. A friendly Golden Retriever "
            "sitting indoors can make an office environment "
            "feel warm and welcoming."
        ),
    )

    accepted, reason = _guard_image(
        image=image,
        post=post,
        similarity=0.90,
    )

    assert accepted is False
    assert "category" in reason.lower()