import re

data={
    'jobType': '软件/互联网开发/系统集成,软件工程师',
    'jobName': '互联网分析师-智能数据',
    'emplType': '全职',
    'eduLevel': '本科',
    'companyName': '北京神州泰岳软件股份有限公司',
    'salary': '4K-6K',
    'welfare': ['五险一金', '绩效奖金', '带薪年假', '节日福利', '员工旅游'],
    'city': '哈尔滨',
    'workingExp': '5-10年',
    'infoComLink': 'https://company.zhaopin.com/CZ120116920.htm',
    'positionUrl': 'https://jobs.zhaopin.com/CC120116927J00133857009.htm',
    'extractSkillTag': ['团队合作精神', '脚本', '使用sql', 'shell脚本编写',
                        '抓包分析工具', '团队合作', 'sql', '责任心', 'java',
                        'shell脚本', 'shell', '团队领导', '良好的团队合作精神',
                        '简单的shell脚本', 'pl/sql', '抓包']}

data2={'jobType': '销售业务,客户代表',
       'jobName': '日语办公室数据分析师双休稳定',
       'emplType': '全职',
       'eduLevel': '大专',
       'companyName': '上海万间信息技术有限公司',
       'salary': '4.5K-6K',
       'welfare': ['五险一金', '绩效奖金', '全勤奖', '节日福利', '弹性工作'],
       'city': '济南-高新区',
       'workingExp': '无经验',
       'infoComLink': 'https://company.zhaopin.com/CZ241308880.htm',
       'positionUrl': 'https://jobs.zhaopin.com/CZ241308880J00271368001.htm',
       'extractSkillTag': ['css', '数据分析', '日语', '韩语', '人力资源管理',
                           'html', '数据库', '人力资源', '财务'],
       'releaseTime':'2019-05-06 10:55:29'
       }

def clear_data(data):
    result=data
    try:
        # 处理薪资字段
        salary_pattern = "(.?)K-(.*?)K"
        salary_regex = re.compile(salary_pattern)
        salary_str = data['salary']
        if salary_str is not None :
            salary = []
            if salary_str == "薪资面议":
                salary.append(salary_str)
            else:
                r = salary_regex.findall(salary_str)
                min_sal = float(r[0][0]) * 1000
                max_sal = float(r[0][1]) * 1000
                salary.append(int(min_sal))
                salary.append(int(max_sal))

            result['salary']=salary

        # 处理工作经验字段
        exp_pattern = "(.*?)-(.*)年"
        exp_regex = re.compile(exp_pattern)
        exp_str = data["workingExp"]
        if exp_str is not None and exp_str != "不限" and exp_str != "无经验":
            exp = []
            if exp_str == "不限" or exp_str =="无经验":
                exp.append(exp_str)
            else:
                r2 = exp_regex.findall(exp_str)
                min_exp=int(r2[0][0])
                max_exp=int(r2[0][1])
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
        jobType_str=data['jobType']
        jobType_str=jobType_str.split(',')[0]
        result['jobType']=jobType_str

        # 处理发布时间字段
        release_time=data['releaseTime']
        release_time=release_time.split(' ')[0]
        result['releaseTime']=release_time
    except Exception as e:
        print(e.args)
    finally:
        return result


if __name__  ==  '__main__':
    print(type(clear_data(data2)["workingExp"]))
    print(clear_data(data2)["workingExp"])

    print(type(clear_data(data2)['salary']))
    print(clear_data(data2)['salary'])
    print(clear_data(data2)['city'])
    print(clear_data(data2)['jobType'])
    print(clear_data(data2)['releaseTime'])

