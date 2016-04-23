# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from meituan.items import MeituanItem
from bs4 import BeautifulSoup

class MovieSpider(scrapy.Spider):
    name = 'meituan_spider'
    allowed_domains=['meituan.com']
    start_urls=[
        'http://bj.meituan.com/dianying/'
    ]

    def parse(self, response):
        #soup=BeautifulSoup(response)
        #print soup.prettify()
        movies = response.xpath('//a[@class="reco-movieinfo__cover"]')
        titles =movies.xpath('@title').extract()
        rates=movies.xpath("string(strong)").extract()
        img_url1=movies.xpath('img/@src').extract()[0:5]
        img_url2=movies.xpath('img/@data-src').extract()
        img_urls = img_url1+img_url2

        count = 0
        for title,rate,img_url in zip(titles,rates,img_urls):
            item = MeituanItem()
            item['title']=title
            item['rate']=rate
            item['source']='meituan'
            item['img_url']=img_url
            #print item
            yield  item



