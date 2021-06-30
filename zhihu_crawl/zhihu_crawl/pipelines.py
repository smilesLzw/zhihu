# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import redis
from itemadapter import ItemAdapter


class ZhihuCrawlPipeline:
    def process_item(self, item, spider):
        return item


class TopicCrawlPipeline:
    def __init__(self):
        self.redis_con = redis.Redis(
            host='localhost',
            port=6379,
            db=11
        )

    def process_item(self, item, spider):
        redis_key = 'question_crawler:start_urls'
        return item


class QuestionCrawlPipeline:
    def process_item(self, item, spider):
        return item


class AnswerCrawlPipeline:
    def process_item(self, item, spider):
        return item