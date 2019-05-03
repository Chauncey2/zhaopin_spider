# -*- coding: utf-8 -*-
from pymongo import MongoClient
from scrapy.conf import settings
import re

class ZhaopingPipeline(object):

    def __init__(self):
        """
        初始换数据库
        """
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        self.client = MongoClient(host=host, port=port)
        mdb = self.client[dbname]
        self.post = mdb[settings['MONGODB_DOCNAME']]

    def process_item(self,item,spider):
        '''
        对爬虫返回的数据进行数据清洗
        :param item:页面数据
        :param spider:
        :return:处理后的数据
        '''

        data=dict(item)
        data=ZhaopingPipeline.clear_data(data)

        self.post.insert(data)
        return item

    def close_spider(self,spider):
        """
        关闭数据库连接
        :param spider:
        :return:
        """
        self.client.close()  # 爬虫关闭，关闭数据库连接

    @classmethod
    def clear_data(cls,data):
        """
        处理爬虫返回的数据
        :param data: 职位信息字典
        :return: 处理后的信息字典
        """
        result = data
        try:
            salary_pattern = "(.?)K-(.*?)K"
            salary_regex = re.compile(salary_pattern)

            exp_pattern = "(.*?)-(.*)年"
            exp_regex = re.compile(exp_pattern)

            salary_str = data['salary']
            exp_str = data["workingExp"]

            if salary_str is not None:
                salary = []
                if salary_str == "薪资面议":
                    salary.append(salary_str)
                else:
                    r = salary_regex.findall(salary_str)
                    min_sal = float(r[0][0]) * 1000
                    max_sal = float(r[0][1]) * 1000
                    salary.append(int(min_sal))
                    salary.append(int(max_sal))

                result['salary'] = salary

            if exp_str is not None and exp_str != "不限" and exp_str != "无经验":
                exp = []
                if exp_str == "不限" or exp_str == "无经验":
                    exp.append(exp_str)
                else:
                    r2 = exp_regex.findall(exp_str)
                    min_exp = int(r2[0][0])
                    max_exp = int(r2[0][1])
                    exp.append(min_exp)
                    exp.append(max_exp)

                result['workingExp'] = exp
        except Exception as e:
            print(e.args)
        finally:
            return result
