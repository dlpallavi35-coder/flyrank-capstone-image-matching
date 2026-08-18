from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def analyze_image(image_path: str):
    # Determine MIME type from the file extension
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
        raise ValueError(f"Unsupported image format: {extension}")

    # Read the actual image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            image,
            """
            Analyze ONLY the image provided.

            Do not use the filename to determine what is in the image.

            Return the following:

            1. Detailed Description
            Describe exactly what is visible in the image.

            2. Objects Present
            List the main objects visible in the image.

            3. Scene Type
            Identify the type of scene, such as indoor, outdoor,
            portrait, animal, food, landscape, vehicle, etc.

            4. Keywords
            Provide relevant keywords describing the image.

            Be visually accurate. Do not invent objects or scenes
            that are not visible in the image.
            """
        ],
    )

    return response.text