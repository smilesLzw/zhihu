import scrapy

from zhihu_crawl.items import AnswerItem


class AnswerCrawler(scrapy.Spider):
    name = 'answer_crawler'

    def start_requests(self):
        url = 'https://www.zhihu.com/api/v4/questions/281447893/answers'
        for page in range(10):
            yield scrapy.FormRequest(
                url=url,
                method='GET',
                formdata={
                    'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
                    'limit': '5',
                    'offset': str(page * 5),
                    'platform': 'desktop',
                    'sort_by': 'default'
                },
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