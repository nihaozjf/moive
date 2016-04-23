# -*- coding: utf-8 -*-
import codecs
import os
import jieba
import pandas
import numpy
import os.path
from wordcloud import WordCloud
import matplotlib.pyplot as plt


corpos = pandas.DataFrame(columns=['filePath','content'])

for root,dirs,files in os.walk('D:\\python\\code\\scrapy\\comment\\word'):
    for name in files:
        filePath=root+'\\'+name
        f=codecs.open(filePath,'r',encoding='utf-8')
        content=f.read()
        f.close()
        corpos.loc[len(corpos)+1] =[filePath,content.strip()]

#corpos.to_csv('df.csv',encoding='utf-8')
segments = pandas.DataFrame(columns=['filePath','segment'])
for content in corpos['content']:
    segs= jieba.cut(content)
    for seg in segs:
        segments.loc[len(segments)+1]=[corpos['filePath'],seg]

segments.to_csv('segments.csv',encoding='utf-8')
print 'save segments to segments.csv....'
#segments=pandas.read_csv('D:\\python\\code\\movie\\comments\\segments.csv')
segStat=segments.groupby(
    by="segment")['segment'].agg({
    'count':numpy.size}).reset_index().sort(
    columns=['count'],
    ascending=False
)

segStat.to_csv('segStat.csv',encoding='utf-8')
print 'save segStat to segStat.csv...'
#segStat=pandas.read_csv('D:\\python\\code\\movie\\comments\\segStat.csv')
stopwords= pandas.read_csv(
    'D:\\python\\code\\movie\\comments\\stop.txt',
    error_bad_lines=False,
)

fSegStat=segStat[~segStat.segment.isin(stopwords.stopword)]

fSegStat.to_csv('fSegStat.csv',encoding='utf-8')
print 'save fSegStat to fSegStat.csv...'
#fSegStat=pandas.read_csv('D:\\python\\code\\movie\\comments\\fSegStat.csv',encoding='utf-8')
wordcloud=WordCloud(
    font_path='D:\\python\\simhei.ttf',
    background_color='black'
)
#fSegStat_file=pandas.read_csv('D:\\python\\code\\movie\\comments\\fSegStat.csv')

wordcloud=wordcloud.fit_words(fSegStat.itertuples(index=False))
plt.imshow(wordcloud)
plt.show()
plt.close()

