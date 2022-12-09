import requests
from fake_useragent import UserAgent
from urllib.parse import urlencode

import config

API_KEY = config.API_KEY
user_agent = UserAgent()
# headers = {'user-agent': user_agent.random}
HEADERS = {
    "User-Agent": user_agent.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


def get_request_proxy(url):
    res = requests.get(get_proxy_url(url), headers=HEADERS)
    return res.text


def get_request(url):
    res = requests.get(url, headers=HEADERS)
    return res.text
