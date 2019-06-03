# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import QianchengItem


class QianchengSpider(scrapy.Spider):
    name = 'qiancheng_spider'

    baseUrl="https://search.51job.com/list/000000,000000,0000,00,9,99,{0},2,1.html"

    def start_requests(self):
        with open('keywords.json', 'r') as f:
            keywords_list = json.load(f)

        start_urls = []
        for item in keywords_list:
            for job_key in item['Job_keywords']:
                start_urls.append(self.baseUrl.format(job_key))

        if start_urls is not None:
            for url in start_urls:
                print("start_url:", url)
                yield scrapy.Request(url=url, callback=self.parse, meta={'start_url': url})

    def parse(self, response):
        content=response.xpath("//div[@class='dw_table']")
        detail_url_list=content.xpath("div[@class='el']/p/span/a/@href").extract()
        for url_item in detail_url_list:
            print(url_item)
        print(len(detail_url_list))
        num_list=len(detail_url_list)
        for i in range(num_list):
            url=detail_url_list.pop()
            print(url)
            print("剩余地址数：",len(detail_url_list))
            yield scrapy.Request(url=url, callback=self.detail_parse)

        next_url=response.xpath("//li[@class='bk']/a[contains(text(),'下一页')]/@href").extract()[0]
        print("next_url",next_url)
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)
        elif detail_url_list is not None:
            init_url = response.meta['start_url']
            yield scrapy.Request(url=init_url, callback=self.detail_parse)


    def detail_parse(self,response):

        item=QianchengItem()
        item["jobType"]=response.xpath("//div[@class='mt10']/p/a/text()").extract()
        item["jobName"]=response.xpath("//div[@class='cn']/h1/text()").extract()
        item["eduLevel"]=response.xpath("//p[@class='msg ltype']/@title").extract()
        item["companyName"] = response.xpath("//p[@class='cname']/a[1]/text()").extract()
        item["salary"] = response.xpath("//div[@class='cn']/strong/text()").extract()
        item["city"] = response.xpath("//p[@class='msg ltype']/@title").extract()
        item["workingExp"] = response.xpath("//p[@class='msg ltype']/@title").extract()
        item["extractSkillTag"] = response.xpath("//div[@class='mt10']/p[2]/a/text()").extract()
        item["releaseTime"] = response.xpath("//p[@class='msg ltype']/@title").extract()

        yield item
