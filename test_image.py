from unittest.mock import patch
from app.services.vision_service import analyze_image


def test_image_analysis():
    with patch(
        "app.services.vision_service.client.models.generate_content"
    ) as mock_generate:

        mock_generate.return_value.text = "A dog sitting indoors."

        result = analyze_image("uploads/dogimage.webp")

        assert isinstance(result, str)
        assert len(result) > 0
        assert result == "A dog sitting indoors."