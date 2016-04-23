# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import  codecs
import pymongo
from scrapy.conf import  settings
from scrapy.exceptions import DropItem

class MongoPipeline(object):

    def __init__(self):
        connection =pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db= connection[settings['MONGODB_DB']]
        self.collection =db[settings['MONGODB_COLLECTION']]

    def process_item(self,item,spider):
        valid = True

        for data in item:
            if not data:
                valid=False
                raise  DropItem("Missing %s of item "%(data))
        if valid:

            self.collection.insert(dict(item))


class CommentsPipeline(object):

    def open_spider(self,spider):
        filename=spider.movie_id+'.json'
        self.file=codecs.open(filename,'wb',encoding='utf-8')

    #def __init__(self):
    #    self.file=codecs.open("248997.json",'wb',encoding='utf-8')

    def process_item(self, item, spider):
        #print 'pipeline process...'
        self.file.write(item['comment'])