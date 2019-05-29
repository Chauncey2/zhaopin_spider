# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import QianchengItem


class QianchengSpider(scrapy.Spider):
    name = 'qiancheng_spider'

    baseUrl="https://search.51job.com/list/000000,000000,0000,00,9,99,{0},2,1.html"

    def start_requests(self):
        '''
        构造请求队列
        :return: 请求队列
        '''
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

        print(detail_url_list)
        if detail_url_list is None:
            init_url = response.meta['start_url']
            yield scrapy.Request(url=init_url, callback=self.detail_parse)


    def detail_parse(self,response):
        """
        详情页页面抓取函数
        :param response:
        :return:item数据
        """
        item=QianchengItem()    # 定义数据

        item["jobType"]=response.xpath("//div[@class='mt10']/p/a/text()").extract()
        item["jobName"]=response.xpath("//div[@class='cn']/h1/text()").extract()

        item["eduLevel"]=response.xpath("//p[@class='msg ltype']/text()").extract()     # 需要特殊处理

        item["companyName"] = response.xpath("").extract()
        item["salary"] = response.xpath("").extract()
        item["welfare"] = response.xpath("").extract()

        item["city"] = response.xpath("//p[@class='msg ltype']/text()").extract()       # 需要特殊处理
        item["workingExp"] = response.xpath("//p[@class='msg ltype']/text()").extract() # 需要特殊处理

        item["extractSkillTag"] = response.xpath("").extract()

        item["releaseTime"] = response.xpath("//p[@class='msg ltype']/text()").extract() # 需要特殊处理

