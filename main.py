import os
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import box.box

from src.scrapping import youtube_channel_scrapper
from src.model import youtube_video

config = box.Box.from_yaml(filename="config.yaml")
templates = Jinja2Templates(directory="frontend/templates")

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

@app.get("/")
async def root():
    return {"message": "Leonce is the real MVP."}

@app.get("/upvote/{video_id}")
async def read_item(request: Request, video_id: str):
    ip = request.client.host
    raise NotImplementedError
    pass

@app.get("/home", response_class=HTMLResponse)
async def read_item(request: Request):
    videos = get_videos()
    return templates.TemplateResponse("home.html", {"request": request, "config": config.frontend, "videos": videos})

def init_database():
    channel = config.crawler.channel
    scrolls = config.crawler.scrolls
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    results = scrapper.get_channel_videos(scrolls=scrolls)
    print("Got", len(results), "videos")

def get_videos():
    video_title = 'Playoffs NBA 2020 : débrief dans la Conférence Est !'
    video_url = 'https://www.youtube.com/watch?v=f4pRyHDYWEI'
    video_obj = youtube_video.YoutubeVideo(video_url=video_url, video_title=video_title)
    return [video_obj, video_obj, video_obj, video_obj]

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')

