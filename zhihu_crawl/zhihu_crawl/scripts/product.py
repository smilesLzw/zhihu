import json
import re
from urllib.parse import urljoin
import logging

import redis
import requests


TOPIC_URL = 'https://www.zhihu.com/topic'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
redis_con = redis.Redis(
    host='localhost',
    port=6379,
    db=10,
)





def top_answer_task_producer(topic_data):
    redis_key = 'answer_crawler:start_urls'
    for data in topic_data:
        topic_url = re.findall('href=\"(.*?)\"', data)[0]
        top_answer_id = topic_url.split('/')[-1]
        answer_url = topic_url + '/top-answers'
        url = urljoin(TOPIC_URL, answer_url)
        task = {
            'topic_url': url,
            'method': 'GET'
        }
        redis_con.lpush(redis_key, json.dumps(task))


def topic_task_producer(topic_data):
    redis_key = 'topic_crawler:start_urls'
    for data in topic_data:
        topic_url = re.findall('href=\"(.*?)\"', data)[0]
        top_answer_id = topic_url.split('/')[-1]
        answer_url = topic_url + '/top-answers'
        url = urljoin(TOPIC_URL, answer_url)
        task = {
            'topic_url': url,
            'method': 'GET'
        }
        redis_con.lpush(redis_key, json.dumps(task))

def main():
    for topic_id in topic_id_array:
        offset = 0
        while True:
            topic_data = download(topic_id, offset*10)
            offset += 2
            if topic_data['msg']:
                topic_task_producer(topic_data['msg'])
                continue
            else:
                break


if __name__ == '__main__':
    main()