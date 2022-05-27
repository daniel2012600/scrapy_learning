# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsScraperItem(scrapy.Item):
    post_title = scrapy.Field()
    post_date = scrapy.Field()
    post_content = scrapy.Field()
    comments = scrapy.Field()

class PttItem(scrapy.Item):
    author = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    comments = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()


class ScrapyLearningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

