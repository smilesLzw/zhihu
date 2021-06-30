import json

import scrapy
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup

from zhihu_crawl.items import TopicItem


class TopicCrawler(RedisSpider):
    name = 'topic_crawler'
    redis_key = f"{name}:start_urls"

    def make_request_from_data(self, data):
        task = json.loads(data.decode('utf-8'))
        return scrapy.FormRequest(
            dont_filter=False,
            url=task['url'],
            method=task['method'],
            meta=task['meta'],
            callback=self.parse_topic_index
        )

    def parse_topic_index(self, response):
        print(response.body)
        html = response.body.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        try:
            topic_title = soup.select('div[class="TopicMetaCard-title"]')
            follower = soup.select('div[class*="NumberBoard"] button strong')
            answer = soup.select('div[class*="NumberBoard"] a strong')

            item = TopicItem()
            item['topic_id'] = response.meta['topic_id']
            item['title'] = topic_title[0].text if topic_title else ''
            item['follower'] = follower[0].attrs['title'] if follower else ''
            item['answer'] = answer[0].attrs['title'] if answer else ''

            yield item
        except Exception as e:
            print(e.args)
