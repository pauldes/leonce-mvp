import os
import sys

from src.scrapping import youtube_channel_scrapper

def main():
    channel = "TrashTalkProduction"
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    results = scrapper.scrap_channel(scrolls=10)

if __name__ == "__main__":
    sys.exit(main())


