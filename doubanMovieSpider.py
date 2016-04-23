# -*- coding: utf-8 -*-

import  requests
from bs4 import BeautifulSoup
import  os.path
import os
import pymongo

def makeDir():
    cur_path= os.getcwd()
    pic_path = os.path.join(cur_path,'pic')
    douban_path = os.path.join(pic_path,'douban')
    #print douban_path
    if os.path.exists(douban_path):
        return douban_path
    else:
        os.mkdir(douban_path)
        return douban_path
#img_url='https://img1.doubanio.com/view/movie_poster_cover/mpst/public/p2324130709.jpg'
#img_path='D:\python\code\movie\pic\douban\p2324130709.jpg'
def download_img(img_url,img_path):
    if os.path.isfile(img_path):
        return
    else:
        res = requests.get(img_url,stream=True)
        if res.status_code==200:
            with open(img_path,'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)

#download_img(img_url,img_path)


url='https://movie.douban.com/nowplaying/beijing/'
client =pymongo.MongoClient('localhost',27017)
db =client['crawler']
movie_table = db['movie']
base_dir = makeDir()


html = requests.get(url).text
soup = BeautifulSoup(html,'lxml')


movies =soup.select('#nowplaying > div.mod-bd > ul  > li.list-item')

if movies:
    for movie in movies:
        #print movie
        title= movie.get('data-title')
        rate=movie.get('data-score')
        img_url = movie.select('ul > li.poster > a > img')[0]['src']
        #print title+'\t'+rate+'\t'+img_url

        img_path = os.path.join(base_dir,img_url.split('/')[-1])
        #print img_path
        data={
            'title':title,
            'rate':rate,
            'source':'douban',
            'img_path':img_path,
            'img_url':img_url
        }
        movie_table.insert_one(data)
        download_img(img_url,img_path)