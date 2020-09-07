from sqlalchemy.orm import Session

from . import models, schemas

def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_video_by_url(db: Session, url: str):
    return db.query(models.Video).filter(models.Video.url == url).first()

def get_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Video).offset(skip).limit(limit).all()

def create_video(db: Session, video: schemas.VideoCreate):
    #db_video = models.Video(url=video.url, title=video.title, thumbnail_url=video.thumbnail_url)
    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
