# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import pymysql
import pymongo
from . import settings
import logging
 
class MongoDBPipeline:

    collection = 'test1'

    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', settings.MONGODB_URI)
        db_name = spider.settings.get('MONGODB_DB_NAME', settings.MONGODB_DB)
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(item)
        return item

    def close_spider(self, spider):
        self.client.close()

# class PttPipeline:
#     def __init__(self):   #連線資料庫，資料庫相關設定值放在settings.py
#         self.connect = pymysql.connect(
#             host=settings.MYSQL_HOST,
#             db=settings.MYSQL_DB,
#             user=settings.MYSQL_USER,
#             passwd=settings.MYSQL_PASS,
#             charset='utf8',
#             use_unicode=True)
#         self.cursor = self.connect.cursor()

#     def process_item(self, item, spider):
#         if item.__class__ == PttItem:   #不同Item插入不同的資料表
#             try:
#                 self.cursor.execute("select * from page where date = '%s' and author = '%s'" %
#                                     (item['date'].strftime('%Y-%m-%d %H:%M:%S'), item['author'])) # 檢查是否已經在資料庫內
#                 ret = self.cursor.fetchone()
#                 if not ret:  # 如果沒有在資料庫內
#                     logging.warning("----插入資料到資料庫")
#                     self.cursor.execute("""insert into page value (%s, %s, %s, %s, %s, %s, %s)""",
#                                         (item['author'], item['date'].strftime('%Y-%m-%d %H:%M:%S'),
#                                          item['title'], item['content'], str(item['comments']),
#                                          item['score'], item['url']))  # 插入
#                     self.connect.commit()  # 資料庫有變更時，需要commint才會執行，select不需要commit
#                 else:
#                     logging.warning("----已存在資料庫中")
#             except Exception as error:
#                 self.connect.rollback()  #發生錯誤，則退回上一次資料庫狀態
#             return item


# class ScrapyLearningPipeline:
#     def process_item(self, item, spider):
#         return item
