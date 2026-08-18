from unittest.mock import patch, MagicMock

from app.services.vision_service import analyze_image, ImageMetadata


def test_image_analysis():
    mock_response = MagicMock()

    mock_response.parsed = ImageMetadata(
        subject="dog",
        category="animal",
        attributes=["golden fur", "sitting"],
        caption="A dog sitting indoors.",
        confidence=0.95
    )

    with patch(
        "app.services.vision_service.client.models.generate_content",
        return_value=mock_response
    ):
        result = analyze_image("uploads/dogimage.webp")

    assert isinstance(result, ImageMetadata)
    assert result.subject == "dog"
    assert result.category == "animal"
    assert result.confidence == 0.95