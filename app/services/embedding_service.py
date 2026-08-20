from google import genai
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os

from app.models.ai_usage import AIUsage

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def generate_embedding(
    text: str,
    db: Session | None = None,
):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    embedding = response.embeddings[0].values

    if db is not None:
        usage = AIUsage(
            operation="embedding",
            model="gemini-embedding-001",
            input_tokens=0,
            output_tokens=0,
            estimated_cost=0.0,
        )
        db.add(usage)

    return embedding