from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class AIUsage(Base):
    __tablename__ = "ai_usage"

    id = Column(Integer, primary_key=True, index=True)

    operation = Column(
        String(100),
        nullable=False,
    )

    model = Column(
        String(100),
        nullable=False,
    )

    input_tokens = Column(
        Integer,
        nullable=False,
        default=0,
    )

    output_tokens = Column(
        Integer,
        nullable=False,
        default=0,
    )

    estimated_cost = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )