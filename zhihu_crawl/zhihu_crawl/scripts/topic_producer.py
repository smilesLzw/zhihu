'''
抓取话题广场下的所有大话题类目下的小话题链接。

小话题由 API 请求返回。 
'''
import random
import re
import json
import logging

import redis
import requests

from topic_id import parse_topic_id
from get_proxy import get_proxy_from_api


TOPIC_URL = 'https://www.zhihu.com/topic'
redis_con = redis.Redis(
    host='localhost',
    port=6379,
    db=10,
)

PROXY_ARRAY = get_proxy_from_api()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def download(topic_id, offset):
    topic_api_url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    ip = random.choice(PROXY_ARRAY)
    proxy = {
        'https': f'http://{ip["ip"]}:{ip["port"]}'
    }
    data = {
        'method': 'next',
        'params': f'{{"topic_id": {topic_id},"offset": {offset},"hash_id":""}}'
    }
    try:
        res = requests.post(topic_api_url, headers=headers, data=data, proxies=proxy)
        if res.status_code == 200:
            return res.json()
        logging.error(f'get invalid status code {res.status_code} while offset is {offset}')
    except requests.RequestException:
        logging.error(f'error occurred while offset is {offset}')


def topic_task_producer(topic_data):
    redis_key = 'topic_crawler:start_urls'
    for data in topic_data:
        topic_id = re.findall('href=\"/topic/(.*?)\"', data)[0]
        url = 'https://www.zhihu.com/topic/{}/top-answers'.format(topic_id)
        task = {
            'url': url,
            'method': 'GET',
            'meta': {
                'topic_id': topic_id
            }
        }
        logging.info(f'Task production is successful!')
        redis_con.lpush(redis_key, json.dumps(task))


def question_task_producer(topic_data):
    redis_key = 'question_crawler:start_urls'
    for data in topic_data:
        topic_id = re.findall('href=\"/topic/(.*?)\"', data)[0]
        url = 'https://www.zhihu.com/api/v4/topics/{}/feeds/essence'.format(topic_id)
        for offset in range(10):
            task = {
                'url': url,
                'method': 'GET',
                'body': {
                    'include': 'data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,answer_type;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.paid_info;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;',
                    'limit': '10',
                    'offset': str(offset * 10)
                }
            }
            logging.info(f'Question task production is successful!')
            redis_con.lpush(redis_key, json.dumps(task))


# 生产话题具体的 URL，当前为单线程，后续可优化为多线程/进程生产
def main():
    topic_id_array = parse_topic_id()
    count = 1
    for topic_id in topic_id_array:
        offset = 0
        # 因无法得知话题的总数目，因此通过 while True 方式生产任务，可通过判断请求返回后的 msg 是否为空来终止任务生产
        while True:
            logging.info(f'Current task count: {count}')
            count += 1
            topic_data = download(topic_id, offset * 10)
            offset += 2
            if topic_data['msg']:
                topic_task_producer(topic_data['msg'])
                question_task_producer(topic_data['msg'])
                continue
            else:
                break


if __name__ == '__main__':
    main()