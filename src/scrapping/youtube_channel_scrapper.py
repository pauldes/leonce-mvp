import time

import requests
import urllib.parse
import selenium.webdriver

from src.model import youtube_video

class YoutubeChannelScrapper:

    def __init__(self, channel_name: str, web_driver: selenium.webdriver=None):
        self.channel_name = channel_name
        self.web_driver = web_driver

    @property
    def web_driver(self):
        # Lazy loading
        if self._web_driver is None:
            self._web_driver = self.create_web_driver()
        return self._web_driver

    @property
    def channel_name(self):
        return self._channel_name

    @channel_name.setter
    def channel_name(self, channel_name: str):
        self._channel_name = channel_name

    @web_driver.setter
    def web_driver(self, web_driver: selenium.webdriver):
        self._web_driver = web_driver

    @property
    def channel_url(self) -> str:
        return f"https://www.youtube.com/c/{self._channel_name}/videos"

    @staticmethod
    def save_image(image_url: str, save_to_path: str):
        img_url = build_img_url(href)
        img_blob = requests.get(image_url, timeout=5).content
        file_name = "".join(x for x in title if x.isalnum())
        with open("./data/" + file_name + ".jpg" , 'wb') as img_file:
            img_file.write(img_blob)

    def get_channel_videos(self, scrolls: int=0) -> list:
        """[summary]

        Args:
            scrolls (int, optional): Number of scrolls down that should be made to load the channel videos. 
            Depending on the context, a rule of thumb is 5 scrolls for 100 videos.
            A 1-second pause will be made after each scroll. Defaults to 0.

        Returns:
            list: A list of YoutubeVideo objects
        """
        print("Scrapping", self.channel_url)
        self.web_driver.get(self.channel_url)
        time.sleep(1)
        for _ in range(scrolls):
            time.sleep(1)
            self.web_driver.execute_script("scroll(0, 100000);")
        time.sleep(1)
        results = self.web_driver.find_elements_by_class_name("style-scope ytd-grid-video-renderer")
        errors_count = 0
        videos_found = []
        for element in results:
            try:
                video_url = element.find_element_by_id("thumbnail").get_attribute('href')
                video_title = element.find_element_by_id("video-title").get_attribute('title')
                if video_url is None or video_title is None:
                    raise Exception("Could not find video url or title")
                video_obj = youtube_video.YoutubeVideo(url=video_url, title=video_title)
                videos_found.append(video_obj)
            except Exception as e:
                print(e)
                errors_count += 1
        print("Errors count:", errors_count, "/", len(results))
        self.web_driver.quit()
        return videos_found

    @staticmethod
    def create_web_driver(firefox_exe_path: str="C:\Program Files\Mozilla Firefox\\firefox.exe", headless: bool=True):
        options = selenium.webdriver.firefox.options.Options()
        options.binary = firefox_exe_path
        options.headless = headless
        cap = selenium.webdriver.common.desired_capabilities.DesiredCapabilities().FIREFOX
        driver = selenium.webdriver.Firefox(options=options, capabilities=cap)
        return driver

