import json

import scrapy
from scrapy_redis.spiders import RedisSpider

from zhihu_crawl.items import QuestionItem


class QuestionCrawler(RedisSpider):
    name = 'question_crawler'
    redis_key = f'{name}:start_urls'

    def make_request_from_data(self, data):
        task = json.loads(data.decode('utf-8'))
        return scrapy.FormRequest(
            url=task['url'],
            method=task['method'],
            formdata=task['body'],
            callback=self.parse_question
        )

    def parse_question(self, response):
        json_data = response.json()
        for data in json_data['data']:
            question = data['target']['question'].get('title')
            question_id = data['target']['question'].get('id')
            answer_id = data['target'].get('id')
            created_time = data['target'].get('created_time')

            item = QuestionItem()
            item['question'] = question
            item['question_id'] = question_id
            item['answer_id'] = answer_id
            item['created_time'] = created_time

            yield item


