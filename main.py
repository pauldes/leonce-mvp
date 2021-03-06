import os
import sys
from typing import List
import random
import hashlib

from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
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

def hash_file(file_path):
    """ Compute the hash of a file.

    Args:
        file_path (str): Path to the file

    Returns:
        int: hash of the file content
    """
    with open(file_path, "r") as file_reader:
        content = file_reader.read()
        return int(hash(content))

js_file_version = hash_file("./frontend/static/script.js")
css_file_version = hash_file("./frontend/static/custom-styles.css")

app = FastAPI(
    title=config.api.title,
    description="Léonce-MVP project.",
    version="0.1",
    docs_url=None,
    redoc_url=None)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.post("/api/videos/", response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    db_video = crud.get_video_by_url(db, url=video.url)
    if db_video:
        raise HTTPException(status_code=403, detail="Video already registered")
    return crud.create_video(db=db, video=video)

@app.get("/api/videos/", response_model=List[schemas.Video])
def read_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=skip, limit=limit)
    return videos

@app.get("/api/videos/{video_id}", response_model=schemas.Video)
def read_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@app.get("/")
async def root():
    return RedirectResponse(url='/ranked')

@app.post("/api/upvote/{video_id}")
async def upvote_video(request: Request, video_id: str, db: Session = Depends(get_db)):
    ip = request.client.host
    hashed_ip = hashlib.sha256(ip.encode('utf-8')).hexdigest()
    db_vote = crud.get_vote_by_ip_and_video_id(db, hashed_ip, video_id)
    if db_vote:
        raise HTTPException(status_code=403, detail="Vote already registered for this IP and video")
        # Choose if we allow multiple votes per IP..
    else:
        vote = schemas.VoteCreate(ip=hashed_ip, video_id=video_id)
        return crud.create_vote(db=db, vote=vote)

@app.get("/random", response_class=HTMLResponse)
async def show_random(request: Request, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=0, limit=1000)
    num_videos = min(config.api.num_random_videos, len(videos))
    videos = random.sample(videos, k=num_videos)
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "config": config.frontend, 
            "videos": videos, 
            "nav": "random",
            "css_version": css_file_version,
            "js_version": js_file_version
            })

@app.get("/ranked", response_class=HTMLResponse)
async def show_ranked(request: Request, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=0, limit=1000, ordered_by_votes=True)
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "config": config.frontend, 
            "videos": videos, 
            "nav": "ranked",
            "css_version": css_file_version,
            "js_version": js_file_version
            })

def update_database_effective(request: Request, db: Session = Depends(get_db)):
    videos = get_videos()
    for video in videos:
        db_video = crud.get_video_by_url(db, url=video.url)
        if db_video:
            print("Video", video.url, "already registered")
        else:
            new_video = schemas.VideoCreate(url=video.url, title=video.title, thumbnail_url=video.thumbnail_url)
            created = crud.create_video(db=db, video=new_video)
    print("Update done.")

@app.get("/api/update-database")
async def update_database(background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    #background_tasks.add_task(update_database_effective, request, db=db)
    # return {"message": "Database will be updated."}
    return {"message": "Database update is disabled."}

def get_videos():
    channel = config.crawler.channel
    scrolls = config.crawler.scrolls
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    results = scrapper.get_channel_videos(scrolls=scrolls)
    return results

def get_videos_example():
    video_title = 'Playoffs NBA 2020 : débrief dans la Conférence Est !'
    video_url = 'https://www.youtube.com/watch?v=f4pRyHDYWEI'
    video_obj = youtube_video.YoutubeVideo(url=video_url, title=video_title)
    return [video_obj]*20

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "--update-database" in sys.argv or "-u" in sys.argv:
            update_database_effective(request=None)
        else:
            print("Unknown args.")
    else:
        uvicorn.run(app, host='0.0.0.0')

