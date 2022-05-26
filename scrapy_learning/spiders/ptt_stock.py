import scrapy
import requests
from lxml import etree
import re
import pandas as pd



class PttStockSpider(scrapy.Spider):
    name = 'ptt_stock'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Stock/index.html']

    def parse(self, response):
        pass
        # res_x = response.text
        # origin_xpath = etree.HTML(res_x)
        # title_url_list = origin_xpath.xpath('//*[@id="main-container"]/div[2]/div/div[2]/a/@href')
        # for i in title_url_list:

        #     title_url = 'https://www.ptt.cc/' + i

        #     # 進入文章內獲取內文資訊
        #     yield scrapy.Request(title_url, self.parse_content)
        #     pass

        # last_page_url = origin_xpath.xpath("//a[@class='btn wide'][contains(.,'上頁')]/@href")

        # new_url = 'https://www.ptt.cc' + last_page_url[0]
        # if new_url != "https://www.ptt.cc/bbs/Stock/index5113.html":
        #     yield scrapy.Request(new_url, callback = self.parse)

    def translation_date(self,date):#日期格式轉換的funtion
        date_dict = {"Jan":'01',"Feb":'02',"Mar":'03',"Apr":'04',"May":'05',"Jun":'06',"Jul":'07',"Aug":'08',"Sep":'09',"Oct":'10',"Nov":'11',"Dec":'12'}
        match = re.match('\w{3}\s\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s\d{4}',date[0])
        #把list內的索引值，透過正規式抓自己要的部分製作成新的日期格式
        if match:
            mon = re.search(r'\w{3}\s(\w{3})\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s\d{4}',date[0]).group(1)
            day = re.search(r'\w{3}\s\w{3}\s+(\d{1,2})\s\d{2}:\d{2}:\d{2}\s\d{4}',date[0]).group(1)
            if len(day) == 1:
                day = '0' + day
            year = re.search(r'\w{3}\s\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s(\d{4})',date[0]).group(1)
            newdate = '{}/{}/{}'.format(year,date_dict[mon],day)
            return newdate


    def parse_content(self, response):

        res = etree.HTML(response.text)
        titlename = res.xpath('//*[@id="main-content"]/div[3]/span[2]/text()')
        titlename = titlename[0] #使爬下來的list轉為字串
        time = res.xpath('//*[@id="main-content"]/div[4]/span[2]/text()')
        time = self.translation_date(time)
        content = res.xpath('//*[@id="main-content"]/text()')
        content = [content[i].replace('\n', ' ') for i in range(len(content))]
        content =','.join(content).strip(' ,')
        comments = res.xpath('//*[@id="main-content"]/div/span/text()')
        new_comments = comments[8:]
        new_comments = [new_comments[i].replace('\n', ' ') for i in range(len(new_comments))]
        new_comments = ','.join(new_comments)

            # sql = "insert into ptt_sql.ptt_movie(ID,Title,Date,Content,Comments) values(%s,%s,%s,%s,%s)"
            # val = (ptt_id,titlename,time,content,new_comments)
            # ptt_id += 1

        NewsScraperItem = {
            "post_title": titlename,
            "post_date": time,
            "post_content": content,
            "comments": new_comments
        }
        
        yield NewsScraperItem