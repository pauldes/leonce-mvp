import os
import sys

from fastapi import FastAPI

from src.scrapping import youtube_channel_scrapper

app = FastAPI()

#api = FastAPI(title=config.API_PROJECT_NAME, openapi_url="/api/v1/openapi.json")
#api.mount("/static", StaticFiles(directory="static"))

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.get("/")
async def root():
    return {"message": "Leonce is the real MVP."}

def test():
    channel = "TrashTalkProduction"
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    #results = scrapper.get_channel_videos(scrolls=50)
    results = scrapper.get_channel_videos(scrolls=1)
    print(len(results))
    first = results[0]
    print(first)
    print(first.to_dict())
