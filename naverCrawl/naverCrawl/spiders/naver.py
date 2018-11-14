

# -*- coding: utf-8 -*-

from naverCrawl.items import NavercrawlItem
import scrapy
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
from datetime import datetime

today = datetime.today().strftime("%Y%m%d")

targetUrl = "https://news.naver.com"
req = Request(targetUrl)
data = urlopen(req).read()
bs = BeautifulSoup(data,'html.parser')

temp = bs.find('div',{'class':'lnb_menu'}).find('ul').find_all('li')

categoryListTemp = []
categoryList = []

for cate in range(2,8,1):
    categoryNum = temp[cate].find('a',href=True)['href']
    categoryNum = categoryNum.split('=')[-1]
    categoryListTemp.append(categoryNum)

for side1 in categoryListTemp:
    time.sleep(2)
    req = Request("https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1={0}".format(side1))
    data = urlopen(req).read()
    bs = BeautifulSoup(data,'html.parser')
    category = bs.find('ul',{'class':'nav'}).find_all('li')
    for smallCategory in category:
        if '속보' in smallCategory.find('a').get_text():
            break
        side2 = smallCategory.find('a',  href=True)['href']
        side2 = side2.split('&')[-1]
        categoryList.append("https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&{0}&sid1={1}".format(side2,side1))


class DatabloggerSpider(scrapy.Spider):
    # The name of the spider
    name = "naverCrawler"
    allowed_domains = ["news.naver.com"]
    start_urls = categoryList
    def start_requests(self):
        for url in self.start_urls:
            try:
                for page in range(1,3):
                    time.sleep(3)
                    yield scrapy.Request(url+'&date={0}&page={1}'.format(today,page), self.parse_article)
            except:
                pass



    def parse_article(self,response):
        articles = response.xpath('//*[@id="main_content"]/div[2]/ul[1]/li/dl/dt/a/@href').extract()
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        for article in articles:
            try:
                time.sleep(2)

                yield scrapy.Request(article, self.parse_data)
            except:
                pass

    def parse_data(self,response):
        print('****************************************************')

        text = ""
        for i in  response.xpath('//*[@id="articleBodyContents"]/text()').extract():
            text = text + i
        text = text.rstrip().strip()
        item = NavercrawlItem()
        item['title'] = response.xpath('//*[@id="articleTitle"]/text()').extract_first()
        item['context'] = text
        item['reporter'] = response.xpath('/html/head/meta[6]/@content').extract_first()

        date = response.xpath('//*[@id="main_content"]/div[1]/div[3]/div/span/text()').extract()[-1]
        date = date.split()[0].replace('-','.')

        item['date'] = date
        item['link'] = response.url
        item['category'] = response.xpath('/html/head/meta[7]/@content').extract_first()
        if response.xpath('//*[@id="articleBodyContents"]/span[1]/img/@src').extract_first():
            item['img'] = response.xpath('//*[@id="articleBodyContents"]/span[1]/img/@src').extract_first()
        else :
            item['img'] = response.xpath('//*[@id="articleBodyContents"]/div[2]/div/span[1]/img/@src').extract_first()
        yield item


