import scrapy
from bs4 import BeautifulSoup

from zhihu_crawl.items import TopicItem


class TopicCrawler(scrapy.Spider):
    name = 'topic_crawler'

    def start_requests(self):
        url = 'https://www.zhihu.com/topic/19555513/top-answers'
        yield scrapy.FormRequest(
            url=url,
            method='GET',
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
            item['title'] = topic_title[0].text if topic_title else ''
            item['follower'] = follower[0].attrs['title'] if follower else ''
            item['answer'] = answer[0].attrs['title'] if answer else ''

            yield item
        except Exception as e:
            print(e.args)