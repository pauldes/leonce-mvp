from typing import List, Optional

from pydantic import BaseModel

class VideoBase(BaseModel):
    url: str
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None

class Video(VideoBase):
    id: int
    url: str
    title: str
    thumbnail_url: str
    is_active: bool
    items: List[Vote] = []

    class Config:
        orm_mode = True

class VideoCreate(VideoBase):
    pass