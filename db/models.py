from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Video(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    thumbnail_url = Column(String)
    is_active = Column(Boolean, default=True)

    votes = relationship("Vote", back_populates="video")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    video_id = Column(Integer, ForeignKey("videos.id"))
    
    video = relationship("Video", back_populates="votes")