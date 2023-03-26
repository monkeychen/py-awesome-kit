import sys
import os
import requests


class TwitterBee(object):

    def __init__(self):
        self.name = "twitter-bee"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400'
        }
        self.proxies = {"https_proxy": "http://127.0.0.1:8118", "http_proxy": "http://127.0.0.1:8118"}

    def extract_twitter_video_urls(self, post_url) -> list:
        jumper_url = "https://www.getfvid.com/zh/twitter"
        resp = requests.post(url=jumper_url, data={"url", post_url}, verify=False)
        # resp = requests.get(url=post_url, verify=False)
        content = resp.text
        print(content)
        return []


if __name__ == "__main__":
    post_url = "https://twitter.com/pachoogo/status/1604060974381613056?s=20&t=M9tDP4m4gyf4aMq09ejljg"
    twitter = TwitterBee().extract_twitter_video_urls(post_url)
