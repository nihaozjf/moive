# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import  ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.conf import  settings
import  pymongo

class MyImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #for img_url in item['img_url']:
        #    print img_url
        img_url = item['img_url']
        #print img_url

        yield  Request(img_url)

    def item_completed(self, results, item, info):
        img_path = [x['path'] for ok ,x in results if ok]
        if not img_path:
            raise DropItem('Item contains no images')
        item['img_path']=img_path[0]
        return  item

    def file_path(self, request, response=None, info=None):
        filename = request.url.split('/')[-1]
        return 'meituan/%s' %(filename)

class MongoDBPipeline(object):

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

class MeituanPipeline(object):
    def process_item(self, item, spider):
        return item
