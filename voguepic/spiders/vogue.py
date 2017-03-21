# -*- coding:utf-8 -*-
import scrapy
import re
import os
import urllib
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

class vogue_spider(scrapy.spiders.Spider):

    name = "voguepic"

    start_urls = ["http://shows.vogue.com.cn/"]

    def parse(self, response):
        hxs = Selector(response) #创建查询对象
        items = hxs.xpath('//div[@class="rank"]/ul/li')
        print "rank brand"
        print len(items)

        for i in range(len(items)):#遍历
            true_link = hxs.xpath('//div[@class="rank"]/ul/li[%d]/span/a/@href'%i).extract()
            if true_link:
                true_link = str(true_link)
                aa,true_link,bb = true_link.split("\'")
                print true_link
                yield Request(true_link, callback=self.pic_parse)

    def pic_parse(self, response):
        now_hxs = Selector(response)
        now_items = now_hxs.xpath('//*[@id="x1_picScrollX01"]/div[1]/div[4]/ul/li')

        for i in range(len(now_items)):#遍历
            true_pic = now_hxs.xpath('//*[@id="x1_picScrollX01"]/div[1]/div[4]/ul/li[%d]/img/@crs'%i).extract()
            brandname = now_hxs.xpath('//*[@id="x1_picScrollX01"]/div[1]/div[4]/ul/li[%d]/img/@alt'%i).extract()
            brandname = str(brandname)
            brandname = brandname[3:7]
            print true_pic,brandname
            if true_pic:
                file_name = "%s%d.jpg"%(brandname,i)
                file_path = os.path.join("G:\\pics2",file_name)
                true_pic = str(true_pic)
                aa,true_pic,bb = true_pic.split("\'")
                urllib.urlretrieve(true_pic,file_path)