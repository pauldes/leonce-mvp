import os
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from src.scrapping import youtube_channel_scrapper

templates = Jinja2Templates(directory="frontend")

app = FastAPI(title="Leonce MVP")
#api = FastAPI(title=config.API_PROJECT_NAME, openapi_url="/api/v1/openapi.json")

#app.mount("/static", StaticFiles(directory="static"), name="static")

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

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')

def test():
    channel = "TrashTalkProduction"
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    #results = scrapper.get_channel_videos(scrolls=50)
    results = scrapper.get_channel_videos(scrolls=1)
    print(len(results))
    first = results[0]
    print(first)
    print(first.to_dict())