# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TopicItem(scrapy.Item):
    topic_id = scrapy.Field()
    title = scrapy.Field()
    follower = scrapy.Field()
    answer = scrapy.Field()


class QuestionItem(scrapy.Item):
    question = scrapy.Field()
    question_id = scrapy.Field()
    answer_id = scrapy.Field()
    created_id = scrapy.Field()


class AnswerItem(scrapy.Item):
    question = scrapy.Field()
    question_id = scrapy.Field()
    question_created_time = scrapy.Field()
    answer = scrapy.Field()
    answer_id = scrapy.Field()
    answer_created_time = scrapy.Field()
    voteup_count = scrapy.Field()
