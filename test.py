'''
  此文件是开发开发过程中的部分测试代码
'''
import re

if __name__ == '__main__':
    '''
    从惊悚文件中读取关键词的测试
    '''
    # keywords_list=[]
    # with open('keywords.json','r') as f:
    #     keywords_list=json.load(f)
    #
    # for item in keywords_list:
    #     # print(item['Industy_name'])
    #     # print('*'*51)
    #     for job_key in item['Job_keywords']:
    #         print(job_key)
    #     print("================华丽的分割线=======================")

    '''
    测试正则匹配，改变url中的偏移量start后的值，读取全部的数据
    '''
    testUrl = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=489&workExperience=-1' \
              '&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=Android&kt=3'
    pattern = 'start=(.*?)&'
    offset = 100
    str_offset = str(offset)
    replace_str = 'start=' + str_offset + '&'
    url = re.sub(pattern=pattern, repl=replace_str, string=testUrl)
    print(url)
