from google import genai
from google.genai import types
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
import os

from app.models.ai_usage import AIUsage

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class ImageMetadata(BaseModel):
    subject: str = Field(
        description="Main subject visible in the image"
    )

    category: str = Field(
        description="General category such as animal, vehicle, food, person, landscape"
    )

    attributes: List[str] = Field(
        description="Important visible attributes"
    )

    caption: str = Field(
        description="Accurate description of the image"
    )

    confidence: float = Field(
        description="Confidence from 0.0 to 1.0"
    )


def analyze_image(
    image_path: str,
    db: Session | None = None,
) -> ImageMetadata:

    extension = os.path.splitext(image_path)[1].lower()

    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }

    mime_type = mime_types.get(extension)

    if mime_type is None:
        raise ValueError(
            f"Unsupported image format: {extension}"
        )

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            image,
            """
            Analyze ONLY the supplied image.

            Do not use the filename.

            Return:
            - subject
            - category
            - important visible attributes
            - accurate caption
            - confidence between 0.0 and 1.0

            Do not invent objects or details that are not visible.
            """
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ImageMetadata,
        ),
    )

    if not response.parsed:
        raise ValueError(
            "Gemini returned invalid structured output"
        )

    metadata = response.parsed

    if not 0.0 <= metadata.confidence <= 1.0:
        raise ValueError(
            "Invalid confidence value"
        )

    if db is not None:
        usage = AIUsage(
            operation="image_analysis",
            model="gemini-3.6-flash",
            input_tokens=0,
            output_tokens=0,
            estimated_cost=0.0,
        )

        db.add(usage)

    return metadata