# -*- coding: utf-8 -*-
import scrapy

from scrapy import signals
from scrapy.xlib.pydispatch import  dispatcher
from scrapy.selector import Selector
from nuomi.items import NuomiItem
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import  BeautifulSoup
import  time


class MovieSpider(scrapy.Spider):
    name = 'nuomi_spider'
    allowed_domains=['nuomi.com']
    #url = 'http://bj.nuomi.com/movie#showing-movies'
    start_urls=[
        'http://bj.nuomi.com/movie#showing-movies'
    ]
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.brower =webdriver.PhantomJS('D:\\phantomjs\\bin\\phantomjs.exe')
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    def spider_closed(self,spider):
        self.brower.close()

    def parse(self, response):

        self.brower.get('http://bj.nuomi.com/movie#showing-movies')
        time.sleep(5)
        soup= BeautifulSoup(self.brower.page_source)


        #print soup.prettify()

        titles = soup.select('#showing-movies-j > div > div.item-box > div.item-list.j-slider-box > ul > li > a')
        scores =soup.select('ul > li > a > div.fi-star.clearfix > div.star-cc ')
        imgs = soup.select('#showing-movies-j > div > div.item-box > div.item-list.j-slider-box > ul > li > a > img')

        item=NuomiItem()
        for title,score,img in zip(titles,scores,imgs):
            name=title.get('title')
            img_url=img.get('src')
            s = score.getText().replace('\n','')
            rate='0.0'
            #print s
            if s:
                rate=s
            #print rate
            item['title']=name
            item['rate']=rate
            item['source']='nuomi'
            item['img_url']=img_url

            #print item
            yield  item