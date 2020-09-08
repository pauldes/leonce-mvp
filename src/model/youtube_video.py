import requests
import urllib.parse

class YoutubeVideo:

    def __init__(self, url: str, title: str, thumbnail_url: str=None):
        self.url = url
        self.title = title
        self.thumbnail_url = thumbnail_url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, thumbnail_url: str):
        if thumbnail_url is None:
            thumbnail_url = self.get_thumbnail_url(self.url)
        self._thumbnail_url = thumbnail_url

    @staticmethod
    def get_thumbnail_url(url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        video_id = urllib.parse.parse_qs(parsed.query)['v'][0]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return thumbnail_url

    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "thumbnail_url": self.thumbnail_url
        }
