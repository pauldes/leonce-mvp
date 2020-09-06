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

config = box.Box.from_yaml(filename="config.yaml")
templates = Jinja2Templates(directory="frontend/templates")

app = FastAPI(title=config.api.title)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
#app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="frontend/static")
#app.mount("/frontend/templates", StaticFiles(directory="frontend/templates"), name="frontend/templates")

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.get("/")
async def root():
    return {"message": "Leonce is the real MVP."}

@app.get("/hello/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    ip = request.client.host
    return templates.TemplateResponse("index.html", {"request": request, "name": name, "ip": ip})

@app.get("/random", response_class=HTMLResponse)
async def read_item(request: Request):
    img_url = 'https://img.youtube.com/vi/f4pRyHDYWEI/maxresdefault.jpg'
    return templates.TemplateResponse("random.html", {"request": request, "img_url": img_url})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')

def test():
    channel = config.crawler.channel
    scrolls = config.crawler.scrolls
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    results = scrapper.get_channel_videos(scrolls=scrolls)
    print(len(results))
    first = results[0]
    print(first)
    print(first.to_dict())