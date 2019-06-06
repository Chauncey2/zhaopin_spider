# -*- coding: utf-8 -*-
from pymongo import MongoClient
from scrapy.conf import settings
from .items import ZhaopingItem,QianchengItem
import re
import numpy as np
import json

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

        # 处理智联招聘爬虫提交的数据
        if isinstance(item,ZhaopingItem):
            data=dict(item)
            data=ZhaopingPipeline.clear_data(data)
            self.post.insert(data)

        # 处理前程无忧爬虫提交的数据
        if isinstance(item,QianchengItem):
            data=dict(item)
            data=ZhaopingPipeline.clear_data_for_qiancheng(data)
            if data is not None:
                self.post.insert(data)

        return item

    @classmethod
    def clear_data(cls, data):
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

            # 处理工资字段
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
            # 处理工作经验字段
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

            # 处理职位所在城市字段
            city_str = data['city']

            if '-' in city_str:
                city_str = city_str.split('-')[0]
                print(city_str)
            result['city'] = city_str

            # 处理jobType字段
            jobType_str = data['jobType']
            jobType_str = jobType_str.split(',')[0]
            result['jobType'] = jobType_str

            # 处理发布时间字段
            release_time = data['releaseTime']
            release_time = release_time.split(' ')[0]
            result['releaseTime'] = release_time

            # 处理工作技能字段
            extractSkillTag = result["extractSkillTag"]
            if extractSkillTag is None:
                extractSkillTag = result["jobType"]
                result["extractSkillTag"] = extractSkillTag

            skilTag=json.loads(extractSkillTag)['skillLabel']
            if skilTag is None:
                temp=result["jobType"]
                skilTag.append(temp)

            result["extractSkillTag"]=skilTag

        except Exception as e:
            print(e.args)

            # 处理工作地址字段
            if '-' in result['city']:
                result['city'] = result['city'].split('-')[0]
            # 处理jobType字段
            jobType_str = data['jobType']
            jobType_str = jobType_str.split(',')[0]
            result['jobType'] = jobType_str

            # 处理发布时间字段
            release_time = data['releaseTime']
            release_time = release_time.split(' ')[0]
            result['releaseTime'] = release_time

            # 处理工作技能标签字段
            extractSkillTag = result["extractSkillTag"]
            if extractSkillTag is None:
                extractSkillTag = result["jobType"]
                result["extractSkillTag"] = extractSkillTag
            skilTag = json.loads(extractSkillTag)['skillLabel']

            if skilTag is None:
                skilTag.append(jobType_str)
            result["extractSkillTag"] = skilTag
            if skilTag is None:
                temp=result["jobType"]
                skilTag.append(temp)
            result["extractSkillTag"]=skilTag

        finally:
            return result

    @classmethod
    def clear_data_for_qiancheng(cls, data):
        result = data

        try:
            # 处理城市字段
            city = result['city'][0]
            city = city.split('\xa0\xa0|\xa0\xa0')[0]
            city=city.split('-')
            result['city'] = city[0]

            # companyName字段
            companyName = result['companyName'][0]
            companyName = companyName.replace("\t", "").replace("\n", "").replace("\r", "")
            result['companyName'] = companyName.split('\xa0\xa0|\xa0\xa0')[0]

            # 处理学历字段
            eduLevel = result["eduLevel"][0].split('\xa0\xa0|\xa0\xa0')
            eduLevel = eduLevel[2]
            eduLevel=ZhaopingPipeline.judeg_edu(eduLevel) # 判断学历字段是否合法
            result['eduLevel'] = eduLevel

            # 处理jobName字段
            jobName = result["jobName"][0]
            jobName = jobName.replace("\r", "").replace("\n", "").replace("\t", "")
            result["jobName"] = jobName

            # 处理jobType字段
            jobType = result['jobType'][0]
            jobType = jobType.replace("\r", "").replace("\n", "").replace("\t", "")
            result["jobType"] = jobType


            # 处理releaseTime字段
            releaseTime = result["releaseTime"][0]
            releaseTime = releaseTime.split('\xa0\xa0|\xa0\xa0')[-1:][0]
            releaseTime=releaseTime.replace("发布","")
            releaseTime="2019-"+releaseTime
            result['releaseTime'] = releaseTime

            # 处理薪资字段
            salary = result["salary"][0]
            if '万/月' in salary:
                salary = salary.replace('万/月', '')
                salary = salary.split('-')
                temp_salary = []
                for item in salary:
                    item = eval(item)
                    item = item * 10000
                    temp_salary.append(int(item))
                result['salary'] = temp_salary
            elif '千/月' in salary:
                salary = salary.replace('千/月', '')
                salary = salary.split('-')
                temp_salary = []
                for item in salary:
                    item = eval(item)
                    item = item * 1000
                    temp_salary.append(int(item))
                result['salary'] = temp_salary
            elif '万/年' in salary:
                salary = salary.replace('万/年', '')
                salary = salary.split('-')
                temp_salary_list = []
                for item in salary:
                    temp_salary = int((eval(item) / 12) * 10000)
                    temp_salary_list.append(temp_salary)
                result["salary"] = temp_salary_list
            else:
                result["salary"] = ["薪资面议"]

            # 处理 工作经验字段
            workingExp = result['workingExp'][0]
            workingExp = workingExp.split('\xa0\xa0|\xa0\xa0')[1]
            if "年经验" in workingExp and "以下" not in workingExp:
                workingExp = workingExp.replace("年", "").replace("经验", "")
                workingExp = workingExp.split('-')
                # 对工工作经验进行计算平均值
                avg_ex = []
                for item in workingExp:
                    item = eval(item)
                    avg_ex.append(item)

                avg = np.mean(avg_ex)  # 求平均工作经验值
                avg = int(np.ceil(avg))  # 向上取整
                exp_list = ZhaopingPipeline.choice_exp(avg)
                # print(exp_list)
                result["workingExp"] = exp_list
            elif "1年以下" in workingExp:
                workingExp = workingExp.replace("经验", "")
                result["workingExp"] = workingExp
            elif "无经验" in workingExp:
                workingExp = '无经验'
                result["workingExp"] = workingExp
            elif "不限" in workingExp:
                workingExp = '无经验'
                result["workingExp"] = workingExp
            elif "年以上" in workingExp:
                workingExp = workingExp.replace("经验", "")
                result['workingExp'] = workingExp
            else:
                workingExp = "不限"
                result["workingExp"] = workingExp

            # 处理extractSkillTag字段
            extractSkillTag = result["extractSkillTag"]
            if extractSkillTag is None:
                extractSkillTag = result["jobType"]
                result["extractSkillTag"] = extractSkillTag

            return result

        except Exception as e:
            print(e.args)
            return None

    @classmethod
    def choice_exp(cls,avg):
        if avg < 1:
            result = '1年以下'
        elif avg >= 1 and avg <= 3:
            result = [1, 3]
        elif avg > 3 and avg <= 5:
            result = [3, 5]
        elif avg > 5 and avg <= 10:
            result = [5, 10]
        else:
            result = '10年以上'
        return result

    @classmethod
    def judeg_edu(cls,eduLevel):

        if "中技" in eduLevel:
            eduLevel="中技"
        elif "中专" in eduLevel:
            eduLevel="中专"
        elif "高中" in eduLevel:
            eduLevel="高中"
        elif "大专" in eduLevel:
            eduLevel="大专"
        elif "本科" in eduLevel:
            eduLevel="本科"
        elif "硕士" in eduLevel:
            eduLevel="硕士"
        elif "博士" in eduLevel:
            eduLevel = "博士"
        else:
            eduLevel="不限"

        return eduLevel


    def close_spider(self,spider):
        """
        关闭数据库连接
        :param spider:
        :return:
        """
        self.client.close()  # 爬虫关闭，关闭数据库连接

