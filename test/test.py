'''
  此文件是开发开发过程中的部分测试代码
'''
import re
import json


keywords_list=[]
with open('keywords.json','r') as f:
    keywords_list=json.load(f)

for item in keywords_list:
    print(item['Industy_name'])
    print('*'*51)
    for job_key in item['Job_keywords']:
        print(job_key)






