import scrapy
import logging
from scrapy.http import FormRequest
from .items import PttItem
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('ptt.log', 'w', 'utf-8')],
                    level=logging.WARNING)

class PttGossipingSpider(scrapy.Spider):
    name = 'ptt_gossiping'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']

    page = 0
    max_page =  2

    def parse(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            logging.warning('回答已滿18歲')
            yield FormRequest.from_response(response, formdata={'yes': 'yes'}, callback=self.parse)
        else:
            self.page += 1
            for href in response.xpath("//div[@class='r-ent']//div[@class='title']//a/@href"):
                url = response.urljoin(href.extract())
                logging.warning('----清單網頁：{}'.format(url))
                yield scrapy.Request(url, callback=self.parse_page)
            if self.page < PttSpider.max_page:
                next_page = response.xpath(
                    '//div[@class="action-bar"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('----清單網頁：{}'.format(url))
                    yield scrapy.Request(url, self.parse)
            else:
                logging.warning('到達抓取網頁個數上限')

    def parse_page(self, response):
        logging.warning('----個別網頁：{}'.format(response.url))
        item = PttItem()
        item['title'] = response.xpath('//meta[@property="og:title"]/@content')[0].extract()
        item['author'] = response.xpath('//div[@id="main-content"]//span[@class="article-meta-value"]/text()')[0].extract().split()[0]
        datetime2 = response.xpath('//div[@id="main-content"]//span[@class="article-meta-value"]/text()')[-1].extract()
        item['date'] = datetime.strptime(datetime2, '%a %b %d %H:%M:%S %Y')  # Fri Apr  9 19:07:56 2021
        item['content'] = response.xpath('//div[@id="main-content"]/text()')[0].extract()
        comments = []
        total_score = 0
        for comment in response.xpath('//div[@class="push"]'):
            push_tag = comment.css('span.push-tag::text')[0].extract()
            push_user = comment.css('span.push-userid::text')[0].extract()
            push_content = comment.css('span.push-content::text')[0].extract()
            if '推' in push_tag:
                score = 1
            elif '噓' in push_tag:
                score = -1
            else:
                score = 0
            total_score += score
            comments.append({'user': push_user, 'content': push_content, 'score': score})
        item['comments'] = comments
        item['score'] = total_score
        item['url'] = response.url
        yield item