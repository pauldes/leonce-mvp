import requests
import urllib.parse

class YoutubeVideo:

    def __init__(self, video_url: str, video_title: str, thumbnail_url: str=None):
        self.video_url = video_url
        self.video_title = video_title
        self.thumbnail_url = thumbnail_url

    @property
    def video_url(self):
        return self._video_url

    @video_url.setter
    def video_url(self, video_url: str):
        self._video_url = video_url

    @property
    def video_title(self):
        return self._video_title

    @video_title.setter
    def video_title(self, video_title: str):
        self._video_title = video_title

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, thumbnail_url: str):
        if thumbnail_url is None:
            thumbnail_url = self.get_thumbnail_url(self.video_url)
        self._thumbnail_url = thumbnail_url

    @staticmethod
    def get_thumbnail_url(video_url: str) -> str:
        parsed = urllib.parse.urlparse(video_url)
        video_id = urllib.parse.parse_qs(parsed.query)['v'][0]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return thumbnail_url

    def to_dict(self):
        return {
            "video_url": self.video_url,
            "video_title": self.video_title,
            "thumbnail_url": self.thumbnail_url
        }
