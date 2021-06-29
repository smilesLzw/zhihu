import re
import json
import logging
from urllib.parse import urljoin

import redis
import requests

from topic_id import parse_topic_id


TOPIC_URL = 'https://www.zhihu.com/topic'
redis_con = redis.Redis(
    host='localhost',
    port=6379,
    db=10,
)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def download(topic_id, offset):
    topic_api_url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    data = {
        'method': 'next',
        'params': f'{{"topic_id": {topic_id},"offset": {offset},"hash_id":""}}'
    }
    try:
        res = requests.post(topic_api_url, headers=headers, data=data)
        if res.status_code == 200:
            return res.json()
        logging.error(f'get invalid status code {res.status_code} while offset is {offset}')
    except requests.RequestException:
        logging.error(f'error occurred while offset is {offset}')


def topic_task_producer(topic_data):
    redis_key = 'topic_crawler:start_urls'
    for data in topic_data:
        topic_url = re.findall('href=\"(.*?)\"', data)[0]
        answer_url = topic_url + '/top-answers'
        url = urljoin(TOPIC_URL, answer_url)
        task = {
            'topic_url': url,
            'method': 'GET'
        }
        redis_con.lpush(redis_key, json.dumps(task))


def main():
    topic_id_array = parse_topic_id()
    for topic_id in topic_id_array:
        offset = 0
        while True:
            topic_data = download(topic_id, offset * 10)
            offset += 2
            if topic_data['msg']:
                topic_task_producer(topic_data['msg'])
                continue
            else:
                break


if __name__ == '__main__':
    main()