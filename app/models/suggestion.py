from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from app.database.database import Base


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)

    image_id = Column(
        Integer,
        ForeignKey("images.id"),
        nullable=False,
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=True,
    )

    similarity = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    status = Column(
        String(30),
        nullable=False,
        default="pending",
    )

    reason = Column(
        Text,
        nullable=True,
    )

    reviewed_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )