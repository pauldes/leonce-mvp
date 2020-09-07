import os
import sys
from typing import List
import random

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import box.box
from sqlalchemy.orm import Session

from src.scrapping import youtube_channel_scrapper
from src.model import youtube_video
from db import crud, models, schemas, database

config = box.Box.from_yaml(filename="config.yaml")
templates = Jinja2Templates(directory="frontend/templates")
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title=config.api.title,
    description="Léonce-MVP project.",
    version="0.1")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.post("/videos/", response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    db_video = crud.get_video_by_url(db, url=video.url)
    if db_video:
        raise HTTPException(status_code=400, detail="Video already registered")
    return crud.create_video(db=db, video=video)

@app.get("/videos/", response_model=List[schemas.Video])
def read_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=skip, limit=limit)
    return videos

@app.get("/videos/{video_id}", response_model=schemas.Video)
def read_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@app.get("/")
async def root():
    return {"message": "Leonce is the real MVP."}

@app.get("/upvote/{video_id}")
async def upvote_video(request: Request, video_id: str):
    ip = request.client.host
    raise NotImplementedError
    pass

@app.get("/home", response_class=HTMLResponse)
async def show_home(request: Request, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=0, limit=1000)
    youtube_videos = []
    for video in videos:
        conv_video = youtube_video.YoutubeVideo(video_url=video.url, video_title=video.title, thumbnail_url=video.thumbnail_url)
        youtube_videos.append(conv_video)
    random.shuffle(youtube_videos)
    return templates.TemplateResponse("home.html", {"request": request, "config": config.frontend, "videos": youtube_videos})

@app.get("/update-database")
async def update_database(request: Request, db: Session = Depends(get_db)):
    videos = get_videos()
    for video in videos:
        db_video = crud.get_video_by_url(db, url=video.video_url)
        if db_video:
            print("Video", video.video_url, "already registered")
        else:
            new_video = schemas.VideoCreate(url=video.video_url, title=video.video_title, thumbnail_url=video.thumbnail_url)
            created = crud.create_video(db=db, video=new_video)
    return {"message": "Database have been updated."}

def get_videos():
    channel = config.crawler.channel
    scrolls = config.crawler.scrolls
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    results = scrapper.get_channel_videos(scrolls=scrolls)
    return results

def get_videos_example():
    video_title = 'Playoffs NBA 2020 : débrief dans la Conférence Est !'
    video_url = 'https://www.youtube.com/watch?v=f4pRyHDYWEI'
    video_obj = youtube_video.YoutubeVideo(video_url=video_url, video_title=video_title)
    return [video_obj]*20

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')

