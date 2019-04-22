# -*- coding: utf-8 -*-

import scrapy

class ZhaopingItem(scrapy.Item):

    jobType = scrapy.Field()  # 工作种类（大类:互联网、金融……）
    jobName = scrapy.Field()  # 职位名称
    emplType = scrapy.Field()  # 工作类型(全职、兼职)
    eduLevel = scrapy.Field()  # 学历要求
    companyName = scrapy.Field()  # 公司名称
    salary = scrapy.Field()  # 工资
    welfare = scrapy.Field()  # 福利
    city = scrapy.Field()  # 城市
    workingExp = scrapy.Field()  # 要求
    infoComLink = scrapy.Field()  # 公司详情连接
    positionUrl=scrapy.Field() # 职位详情链接


class KeyWordItem(scrapy.Item):
    Industy_name = scrapy.Field()  # 所属行业
    Job_keywords = scrapy.Field()  # 工作关键词
