import numpy as np


data={'city': ['长沙\xa0\xa0|\xa0\xa0无工作经验\xa0\xa0|\xa0\xa0招1人\xa0\xa0|\xa0\xa0'
          '05-30发布'],
      'companyName': ['\r\n\t\t\t\t\t汉雅星空文化科技有限公司湖南分公司\t\t\t\t\t', '\r\n\t\t\t\t'],
      'eduLevel': ['长沙\xa0\xa0|\xa0\xa0无工作经验\xa0\xa0|\xa0\xa0招1人\xa0\xa0|\xa0\xa0'
              '05-30发布'],
      'extractSkillTag': [],
      'jobName': ['\r\n\t\t\t\tWeb前端开发工程师\t\t\t\t\t\t\t\t', '\r\n\t\t\t\t\t\t\t'],
      'jobType': ['\r\n\t\t\t\t\t\t\t\t\t\t软件工程师\t\t\t\t\t\t\t\t\t'],
      'releaseTime': ['长沙\xa0\xa0|\xa0\xa0无工作经验\xa0\xa0|\xa0\xa0招1人\xa0\xa0|\xa0\xa0'
                 '05-30发布'],
      'salary': ['20-50万/年'],
      'workingExp': ['长沙\xa0\xa0|\xa0\xa0无工作经验\xa0\xa0|\xa0\xa0招1人\xa0\xa0|\xa0\xa0'
                '05-30发布']}

data2={'city': ['北京-通州区\xa0\xa0|\xa0\xa03-4年经验\xa0\xa0|\xa0\xa0本科\xa0\xa0|\xa0\xa0'
          '招1人\xa0\xa0|\xa0\xa005-30发布'],
 'companyName': ['\r\n\t\t\t\t\t盈东科技（北京）有限公司\t\t\t\t\t', '\r\n\t\t\t\t'],
 'eduLevel': ['北京-通州区\xa0\xa0|\xa0\xa03-4年经验\xa0\xa0|\xa0\xa0本科\xa0\xa0'
              '|\xa0\xa0招1人\xa0\xa0|\xa0\xa005-30发布'],
 'extractSkillTag': [],
 'jobName': ['\r\n\t\t\t\tAndroid开发工程师\t\t\t\t\t\t\t\t', '\r\n\t\t\t\t\t\t\t'],
 'jobType': ['\r\n\t\t\t\t\t\t\t\t\t\t手机应用开发工程师\t\t\t\t\t\t\t\t\t',
             '\r\n\t\t\t\t\t\t\t\t\t\t软件工程师\t\t\t\t\t\t\t\t\t',
             'Android',
             'UI',
             'java'],
 'releaseTime': ['北京-通州区\xa0\xa0|\xa0\xa03-4年经验\xa0\xa0|\xa0\xa0本科\xa0\xa0'
                 '|\xa0\xa0招1人\xa0\xa0|\xa0\xa005-30发布'],
 'salary': ['1.3-1.8万/月'],
 'workingExp': ['北京-通州区\xa0\xa0|\xa0\xa03-4年经验\xa0\xa0|\xa0\xa0本科\xa0\xa0'
                '|\xa0\xa0招1人\xa0\xa0|\xa0\xa005-30发布']}

def clear_data_for_qiancheng(data):
    result=data
    print(result)

    # 处理城市字段
    city=result['city'][0]
    city=city.split('\xa0\xa0|\xa0\xa0')[0]
    print("城市：",city)
    result['city']=city

    # companyName字段
    companyName=result['companyName'][0]
    companyName=companyName.replace("\t","").replace("\n","").replace("\r","")
    print("公司名：",companyName)
    result['companyName']=companyName.split('\xa0\xa0|\xa0\xa0')[0]
    # print(result)

    # 处理学历字段
    eduLevel=result["eduLevel"][0].split('\xa0\xa0|\xa0\xa0')
    eduLevel=eduLevel[2]
    print("教育背景：",eduLevel)
    result['eduLevel']=eduLevel
    # print(eduLevel)

    # 处理jobName字段
    jobName=result["jobName"][0]
    jobName=jobName.replace("\r","").replace("\n","").replace("\t","")
    print("工作名称",jobName)
    result["jobName"]=jobName

    # 处理jobType字段
    jobType=result['jobType'][0]
    jobType=jobType.replace("\r","").replace("\n","").replace("\t","")
    print("工作类别",jobType)
    result["jobType"]=jobType
    # print(jobType)

    # 处理releaseTime字段
    releaseTime=result["releaseTime"][0]
    releaseTime=releaseTime.split('\xa0\xa0|\xa0\xa0')[-1:][0]
    print("发布日期：",releaseTime)
    result['releaseTime']=releaseTime
    # print(releaseTime)


    # 处理薪资字段
    salary=result["salary"][0]
    if '万/月' in salary:
        salary=salary.replace('万/月','')
        salary=salary.split('-')
        temp_salary=[]
        for item in salary:
            item=eval(item)
            item=item*10000
            temp_salary.append(int(item))

        result['salary']=temp_salary
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
        temp_salary_list=[]
        for item in salary:
            temp_salary=int((eval(item)/12)*10000)
            temp_salary_list.append(temp_salary)
        result["salary"]=temp_salary_list
    else:
        salary="薪资面议"
        result["salary"]=salary

    # 处理工作年限字段

    workingExp = result['workingExp'][0]
    workingExp=workingExp.split('\xa0\xa0|\xa0\xa0')[1]
    if "年经验" in workingExp and "以下" not in workingExp:
        workingExp = workingExp.replace("年", "").replace("经验", "")
        workingExp = workingExp.split('-')
        # 对工工作经验进行计算平均值
        avg_ex=[]
        for item in workingExp:
            item=eval(item)
            avg_ex.append(item)

        avg=np.mean(avg_ex)         # 求平均工作经验值
        avg=int(np.ceil(avg))       # 向上取整
        exp_list=choice_exp(avg)
        # print(exp_list)
        result["workingExp"]=exp_list
    elif "1年以下" in workingExp:
        workingExp = workingExp.replace("经验", "")
        result["workingExp"]=workingExp
    elif "无经验" in workingExp:
        workingExp='无经验'
        result["workingExp"] = workingExp
    elif "不限" in workingExp:
        workingExp = '无经验'
        result["workingExp"] = workingExp
    elif "年以上" in workingExp:
        workingExp=workingExp.replace("经验","")
        result['workingExp']=workingExp
    else:
        workingExp="不限"
        result["workingExp"]=workingExp

    # print(workingExp)
    # 处理extractSkillTag字段
    extractSkillTag=result["extractSkillTag"]
    temp_tag=result["jobType"]
    # print("***", result["jobType"])
    if extractSkillTag is None:
        # extractSkillTag=
        # print(result["jobType"])
        result["extractSkillTag"]=temp_tag
    # print("***",result["jobType"])
    print("***",result["extractSkillTag"])

def choice_exp(avg):
    if avg<1:
        result='1年以下'
    elif avg>=1 and avg<=3:
        result=[1,3]
    elif avg>3 and avg<=5:
        result=[3,5]
    elif avg>5 and avg<=10:
        result=[5,10]
    else:
        result='10年以上'
    return result


if __name__ == '__main__':
    clear_data_for_qiancheng(data2)