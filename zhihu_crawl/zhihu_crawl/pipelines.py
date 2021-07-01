# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

import redis
from itemadapter import ItemAdapter


class ZhihuCrawlPipeline:
    def process_item(self, item, spider):
        return item

class TopicCrawlPipeline:
    def process_item(self, item, spider):
        return item


class QuestionCrawlPipeline:
    def __init__(self):
        self.redis_con = redis.Redis(
            host='localhost',
            port=6379,
            db=11
        )
        self.redis_key = 'answer:start_urls'

    def process_item(self, item, spider):
        question_id = item['question']
        answer_url = f'https://www.zhihu.com/api/v4/questions/{question_id}/answers'
        for offset in range(10):
            task = {
                'url': answer_url,
                'method': 'GET',
                'body': {
                    'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
                    'limit': '10',
                    'offset': str(offset * 10),
                    'platform': 'desktop',
                    'sort_by': 'default'
                }
            }
            self.redis_con.lpush(self.redis_key, json.dumps(task))
        return item


class AnswerCrawlPipeline:
    def process_item(self, item, spider):
        return item