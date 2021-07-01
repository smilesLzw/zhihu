import json

import scrapy
from scrapy_redis.spiders import RedisSpider

from zhihu_crawl.items import AnswerItem


class AnswerCrawler(RedisSpider):
    name = 'answer_crawler'
    redis_key = f"{name}:start_urls"

    def make_request_from_data(self, data):
        task = json.loads(data.decode('utf-8'))
        return scrapy.FormRequest(
            url=task['url'],
            method=task['method'],
            formdata=task['body'],
            callback=self.parse_answer
        )

    def parse_answer(self, response):
        json_data = response.json()
        for data in json_data['data']:
            question = data['question'].get('title')
            question_id = data['question'].get('id')
            answer = data.get('content')
            answer_id = data.get('id')
            question_created_time = data['question'].get('created')
            answer_created_time = data.get('created_time')
            voteup_count = data.get('voteup_count')

            item = AnswerItem()
            item['question'] = question
            item['question_id'] = question_id
            item['answer'] = answer
            item['answer_id'] = answer_id
            item['question_created_time'] = question_created_time
            item['answer_created_time'] = answer_created_time
            item['voteup_count'] = voteup_count

            yield item