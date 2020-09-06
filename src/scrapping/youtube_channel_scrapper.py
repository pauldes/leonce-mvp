import time

import requests
import urllib.parse
import selenium.webdriver

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

    def scrap_channel(self, scrolls: int=0):
        print("Scrapping", self.channel_url)
        for _ in range(scrolls):
            time.sleep(0.5)
            self.web_driver.execute_script("scroll(0, 100000);")
        time.sleep(1)
        self.web_driver.get(self.channel_url)
        results = self.web_driver.find_elements_by_class_name("style-scope ytd-grid-video-renderer")
        bug_counter = 0
        videos_found = {}
        for element in results:
            try:
                video_url = element.find_element_by_id("thumbnail").get_attribute('href')
                video_title = element.find_element_by_id("video-title").get_attribute('title')
                if video_url is None or video_title is None:
                    raise Exception("Could not find video url or title")
                videos_found[video_title] = video_url
            except Exception as e:
                print(e)
                bug_counter  = bug_counter + 1
        print("Errors count:", bug_counter, "/", len(results))
        self.web_driver.quit()

    @staticmethod
    def get_thumbnail_url(video_url: str) -> str:
        parsed = urllib.parse.urlparse(video_url)
        video_id = urllib.parse.parse_qs(parsed.query)['v'][0]
        img_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return img_url

    @staticmethod
    def create_web_driver(firefox_exe_path: str="C:\Program Files\Mozilla Firefox\\firefox.exe", headless: bool=True):
        options = selenium.webdriver.firefox.options.Options()
        options.binary = firefox_exe_path
        options.headless = headless
        cap = selenium.webdriver.common.desired_capabilities.DesiredCapabilities().FIREFOX
        driver = selenium.webdriver.Firefox(options=options, capabilities=cap)
        return driver

