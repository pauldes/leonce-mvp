from typing import List, Optional

from pydantic import BaseModel

class VideoBase(BaseModel):
    url: str
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None

class VoteBase(BaseModel):
    ip: str
    video_id: int

class Vote(VoteBase):
    id: int

    class Config:
        orm_mode = True

class VoteCreate(VoteBase):
    pass

class Video(VideoBase):
    id: int
    is_active: bool
    votes: List[Vote] = []

    class Config:
        orm_mode = True

class VideoCreate(VideoBase):
    pass