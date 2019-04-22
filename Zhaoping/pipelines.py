# -*- coding: utf-8 -*-
from pymongo import MongoClient
from scrapy.conf import settings


class ZhaopingPipeline(object):
    # 初始化数据库
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        self.client = MongoClient(host=host, port=port)  # 创建数据库连接
        mdb = self.client[dbname]  # 指向指定数据库
        self.post = mdb[settings['MONGODB_DOCNAME']]  # 获取数据库中的表

    def process_item(self,item,spider):
        '''

        :param item:页面数据
        :param spider:
        :return:处理后的数据
        '''
        # print(item)
        data=dict(item)
        self.post.insert(data)  # 向数据表中添加数据

        return item

    def close_spider(self,spider):

        self.client.close()  # 爬虫关闭，关闭数据库连接


class KeywordsPipline(object):
    def __int__(self):
        pass

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider):
        pass
