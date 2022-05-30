# -*- coding: utf-8 -*-
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://root:root@cluster0.kkxyl1t.mongodb.net/test")
mydb = myclient["test_scrapy"]
mycol = mydb["test1"]
 
for x in mycol.find():
  print(x)