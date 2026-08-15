from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    file_path = Column(String(500), nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"))

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post")