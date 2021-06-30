import scrapy

from zhihu_crawl.items import QuestionItem


class QuestionCrawler(scrapy.Spider):
    name = 'question_crawler'

    def start_requests(self):
        url = 'https://www.zhihu.com/api/v4/topics/19555513/feeds/essence'
        for page in range(10):
            yield scrapy.FormRequest(
                url=url,
                method='GET',
                formdata={
                    'include': 'data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,answer_type;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.paid_info;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;',
                    'limit': '10',
                    'offset': '3469640'
                },
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


