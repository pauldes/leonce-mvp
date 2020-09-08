from sqlalchemy.orm import Session

from . import models, schemas

def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_video_by_url(db: Session, url: str):
    return db.query(models.Video).filter(models.Video.url == url).first()

def get_videos(db: Session, skip: int = 0, limit: int = 100, ordered_by_votes: bool = False):
    if ordered_by_votes:
        res = db.query(models.Video).offset(skip).limit(limit).all()
        res = sorted(res, key = lambda video: len(video.votes), reverse=True )
        #TODO SQL ordering instead of python
    else:
        res = db.query(models.Video).offset(skip).limit(limit).all()
    return res

def create_video(db: Session, video: schemas.VideoCreate):
    #db_video = models.Video(url=video.url, title=video.title, thumbnail_url=video.thumbnail_url)
    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_vote_by_ip_and_video_id(db: Session, ip: str, video_id: str):
    return db.query(models.Vote).filter(models.Vote.ip == ip).filter(models.Vote.video_id == video_id).first()

def create_vote(db: Session, vote: schemas.VoteCreate):
    db_vote = models.Vote(**vote.dict())
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote
