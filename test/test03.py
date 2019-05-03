import re

data={
    'jobType': '软件/互联网开发/系统集成,软件工程师',
    'jobName': '互联网分析师-智能数据',
    'emplType': '全职',
    'eduLevel': '本科',
    'companyName': '北京神州泰岳软件股份有限公司',
    'salary': '4K-6K',
    'welfare': ['五险一金', '绩效奖金', '带薪年假', '节日福利', '员工旅游'],
    'city': '哈尔滨-南岗区',
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
       'city': '杭州-上城区',
       'workingExp': '无经验',
       'infoComLink': 'https://company.zhaopin.com/CZ241308880.htm',
       'positionUrl': 'https://jobs.zhaopin.com/CZ241308880J00271368001.htm',
       'extractSkillTag': ['css', '数据分析', '日语', '韩语', '人力资源管理',
                           'html', '数据库', '人力资源', '财务']}

def clear_data(data):
    result=data
    try:
        salary_pattern = "(.?)K-(.*?)K"
        salary_regex = re.compile(salary_pattern)

        exp_pattern="(.*?)-(.*)年"
        exp_regex=re.compile(exp_pattern)

        salary_str = data['salary']
        exp_str = data["workingExp"]

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
    except Exception as e:
        print(e.args)
    finally:
        return result

if __name__  ==  '__main__':
    print(type(clear_data(data)["workingExp"]))
    print(clear_data(data)["workingExp"])

    print(type(clear_data(data)['salary']))
    print(clear_data(data)['salary'])


