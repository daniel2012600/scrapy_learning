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
        ptt_id = 1
        page = 3
        while page >= 0:
            res_x = response.text
            origin_xpath = etree.HTML(res_x)
            title_url_list = origin_xpath.xpath('//*[@id="main-container"]/div[2]/div/div[2]/a/@href')



        yield from self.scrape(response)  #爬取網頁內容

    # def translation_date(x):#日期格式轉換的funtion
    #     date_dict = {"Jan":'01',"Feb":'02',"Mar":'03',"Apr":'04',"May":'05',"Jun":'06',"Jul":'07',"Aug":'08',"Sep":'09',"Oct":'10',"Nov":'11',"Dec":'12'}
    #     match = re.match('\w{3}\s\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s\d{4}',x[0])
    #     #把list內的索引值，透過正規式抓自己要的部分製作成新的日期格式
    #     if match:
    #         mon = re.search(r'\w{3}\s(\w{3})\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s\d{4}',x[0]).group(1)
    #         day = re.search(r'\w{3}\s\w{3}\s+(\d{1,2})\s\d{2}:\d{2}:\d{2}\s\d{4}',x[0]).group(1)
    #         if len(day) == 1:
    #             day = '0' + day
    #         year = re.search(r'\w{3}\s\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s(\d{4})',x[0]).group(1)
    #         newdate = '{}/{}/{}'.format(year,date_dict[mon],day)
    #         return newdate

    def scrape(self, response):
        ptt_id = 1
        page = 3
        while page >= 0:

            res_x = response.text
            origin_xpath = etree.HTML(res_x)
            title_url_list = origin_xpath.xpath('//*[@id="main-container"]/div[2]/div/div[2]/a/@href')

            for i in title_url_list:
                ptt_id = ptt_id
                try:
                    title_url = 'https://www.ptt.cc/' + i
                    print(111111111111111111)
                    print(title_url)
                    print(111111111111111111)
                    res_article = scrapy.Request(title_url, cookies={'over18': '1'})
                    print(111111111111111111)
                    print(res_article)
                    print(111111111111111111)
                    # one_xpath = etree.HTML(res_article)
                    # titlename = one_xpath.xpath('//*[@id="main-content"]/div[3]/span[2]/text()')
                    # titlename = titlename[0] #使爬下來的list轉為字串
                    # print(111111111111111111)
                    # print(titlename)
                    # print(111111111111111111)
                    # time = one_xpath.xpath('//*[@id="main-content"]/div[4]/span[2]/text()')
                    # time = translation_date(time)
                    # content = one_xpath.xpath('//*[@id="main-content"]/text()')
                    # content = [content[i].replace('\n', ' ') for i in range(len(content))]
                    # content =','.join(content).strip(' ,')
                    # comments = one_xpath.xpath('//*[@id="main-content"]/div/span/text()')
                    # new_comments = comments[8:]
                    # new_comments = [new_comments[i].replace('\n', ' ') for i in range(len(new_comments))]
                    # new_comments = ','.join(new_comments)

                    # sql = "insert into ptt_sql.ptt_movie(ID,Title,Date,Content,Comments) values(%s,%s,%s,%s,%s)"
                    # val = (ptt_id,titlename,time,content,new_comments)
                    # cursor.execute(sql,val)
                    # ptt_id += 1

                except SyntaxError as e:
                    print(e.args)
                # except pymysql.err.DataError as e:
                #     print(e.args)

            page -= 1
            last_page_url = origin_xpath.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href')
            new_url = 'https://www.ptt.cc' + last_page_url[0]
            url = new_url
            pass
            # for post_title in titlename_list:
            #     NewsScraperItem = {
            #         "post_title": post_title
            #     }
            
            # yield NewsScraperItem