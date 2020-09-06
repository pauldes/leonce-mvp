import os
import sys
import requests
import time
import urllib.parse as urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#sys.path.append('geckodriver.exe')

def remove_parameters(url):
    return url.split("?")[0]

def max_res_url(url):
    url = url.replace("hqdefault.jpg", "maxresdefault.jpg")
    return url

def build_img_url(video_url):
    parsed = urlparse.urlparse(video_url)
    video_id = parse_qs(parsed.query)['v'][0]
    img_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    return img_url

def main():

    url = "https://www.youtube.com/c/TrashTalkProduction/videos"

    binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options = Options()
    options.binary = binary
    #options.headless = True
    cap = DesiredCapabilities().FIREFOX
    driver = webdriver.Firefox(options=options, capabilities=cap, executable_path="geckodriver.exe")


    driver.get(url)

    # for item in driver.find_elements_by_id("img"):
    #     img_src = item.get_attribute('src')
    #     print(img_src)
    #

    for _ in range(50):
        time.sleep(0.5)
        driver.execute_script("scroll(0, 100000);")
    time.sleep(10)

    print("="*20)
    bug_counter = 0

    results = driver.find_elements_by_class_name("style-scope ytd-grid-video-renderer")
    for element in results:

        thumbnail = element.find_element_by_id("thumbnail")
        video_title = element.find_element_by_id("video-title")

        href = thumbnail.get_attribute('href')
        title = video_title.get_attribute('title')

        if href is None:
            bug_counter  = bug_counter + 1
        else:
            print(href, ">", title)
            img_url = build_img_url(href)
            img_blob = requests.get(img_url, timeout=5).content
            file_name = "".join(x for x in title if x.isalnum())
            with open("./data/" + file_name + ".jpg" , 'wb') as img_file:
                img_file.write(img_blob)

    driver.quit()
    print(bug_counter, "/", len(results))


if __name__ == "__main__":
    sys.exit(main())


