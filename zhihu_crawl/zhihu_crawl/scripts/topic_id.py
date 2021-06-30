'''
抓取话题广场，解析页面顶部的话题，返回其 topic_id
'''

import logging

import requests
from bs4 import BeautifulSoup


TOPICS_URL = 'https://www.zhihu.com/topics'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def download():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    try:
        res = requests.get(url=TOPICS_URL, headers=headers)
        if res.status_code == 200:
            return res.text
        logging.error(f'get invalid status code {res.status_code}')
    except requests.RequestException:
        logging.error(f'error occurred while scraping {TOPICS_URL}')


def parse_topic_id():
    html = download()
    data_id_array = []
    selector = BeautifulSoup(html, 'lxml')
    li_elms = selector.select('li[class*="zm-topic-cat-item"]')
    for li_elm in li_elms:
        data_id = li_elm.attrs['data-id']
        if data_id not in data_id_array:
            data_id_array.append(data_id)

    return data_id_array