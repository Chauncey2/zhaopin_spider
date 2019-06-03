# -*- coding: utf-8 -*-
import scrapy
from ..items import KeyWordItem


class KeyWordSpiderSpider(scrapy.Spider):
    name = 'keywords_spider'
    allowed_domains = ['https://www.zhaopin.com/']
    start_urls = ['https://www.zhaopin.com/']

    def parse(self, response):

        for items in response.xpath('//*[@id="root"]/div[2]/div[2]/div[1]/ol/li'):
            item=KeyWordItem()
            item['Industy_name']=items.xpath('./div[1]/text()').extract_first()
            item['Job_keywords']=items.xpath('./div[2]/div/div[position()>1]/a/text()').extract()
            yield item


