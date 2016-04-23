# -*- coding: utf-8 -*-
__author__ = 'zhangjufu'
#from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.linkextractors import LinkExtractor
from comments.items import  CommentsItem
'''
http://www.meituan.com/dianying/yingping/248896/page35
'''
class CommentsSpider(CrawlSpider):
	name="CommentsSpider"
	allowed_domains=['meituan.com']
	'''
	start_urls=['http://www.meituan.com/dianying/yingping/246152/page1']
	rules=[
		Rule(sle(allow=('/dianying/yingping/246152/page\d+'),
		         restrict_xpaths=('//li[@class="next"]/a')),
		     callback='parse_item',
		     follow=True)
	]
	'''
	def __init__(self,movie_id='1',*args,**kwargs):

		self.movie_id=movie_id
		self.start_urls=['http://www.meituan.com/dianying/yingping/{}/page1'.format(str(self.movie_id))]

		self.rules=[
			Rule(LinkExtractor(allow=('/dianying/yingping/{}/page\d+'.format(str(self.movie_id))),
					 restrict_xpaths=('//li[@class="next"]/a')),
				 callback='parse_item',
				 follow=True)
		]
		super(CommentsSpider,self).__init__(*args,**kwargs)
		print '********init end******'

	def parse_item(self, response):
		#print 'parse_item'
		item=CommentsItem()
		item['movie_id']=self.movie_id
		comment=response.xpath('//span[@class="comment__content"]/text()')
		for c in comment.extract():
			item['comment']=c.strip()
			#print item
			yield item