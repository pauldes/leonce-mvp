import os
import sys

from src.scrapping import youtube_channel_scrapper

def main():
    channel = "TrashTalkProduction"
    scrapper = youtube_channel_scrapper.YoutubeChannelScrapper(channel)
    #results = scrapper.get_channel_videos(scrolls=50)
    results = scrapper.get_channel_videos(scrolls=1)
    print(len(results))
    first = results[0]
    print(first)
    print(first.to_dict())

if __name__ == "__main__":
    sys.exit(main())


