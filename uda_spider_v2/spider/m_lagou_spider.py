
import requests
import pymysql
import random
import time
import json
import time

import uuid

# ========
import os
import sys
sys.path.append("..")

from util.file_reader import parse_job_xml
from util.file_reader import mkdir

# 将模块路径加到当前模块扫描的路径里
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from spider.jobdetail_spider import crawl_job_detail

import pandas as pd
from util import log
from config.config import *

try:
    # 导入parse模块并命名为parse
    from urllib import parse as parse
except:
    import urllib as parse

    sys.reload()
    sys.setdefaultencoding('utf-8')

# ======

# def get_uuid():
#     return str(uuid.uuid4())
# cookies = "JSESSIONID="+get_uuid()+"; _ga=GA1.2.586354285.1544933627; user_trace_token="+get_uuid()+"; LGUID="+get_uuid()+"; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22%24device_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gid=GA1.2.1275858251.1547435002; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; X_MIDDLE_TOKEN=0ce89912810bc00f0a3924888d329140; LGSID="+get_uuid()+"; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fm.lagou.com%2Futrack%2FtrackMid.html%3Ff%3Dhttps%253A%252F%252Fm.lagou.com%252Fsearch.html%26t%3D1547445758%26_ti%3D1; PRE_LAND=https%3A%2F%2Fm.lagou.com%2Fsearch.html; _gat=1; SEARCH_ID="+get_uuid() + "; LGRID="+get_uuid()

joblist_json = {
    "companyId": '公司ID',
    "workYear": '工作经验',
    "education": '教育程度',
    "jobNature": '工作性质',
    "positionName": '岗位名称',
    "positionId": '岗位ID',
    "createTime": '发布时间',
    "city": '城市',
    "companyLogo": '公司LOGO',
    "industryField": '工业领域',
    "positionAdvantage": '岗位优势',
    "salary": '薪资',
    "companySize": '公司规模',
    "companyShortName": '公司简称',
    "positionLables": '岗位标签',
    "financeStage": '融资阶段',
    "companyLabelList": '公司标签',
    "longitude": '经度',
    "latitude": '纬度',
    "companyFullName": '公司全称',
    "firstType": '一级分类',
    "secondType": '二级分类',
    "isSchoolJob": '是否实习',
    "thirdType": '三级分类',
    "skillLables": '技能标签'
}
# 请求网址及请求头参数
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "82",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "JSESSIONID=ABAAABAAADEAAFI89DEF8645D339BEF9BAB65BFC9A664B0; _ga=GA1.2.586354285.1544933627; user_trace_token=20181216121347-fbe4e12e-00e8-11e9-9315-525400f775ce; LGUID=20181216121347-fbe4e436-00e8-11e9-9315-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22%24device_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gid=GA1.2.1275858251.1547435002; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; X_MIDDLE_TOKEN=0ce89912810bc00f0a3924888d329140; LGSID=20190114145541-67f41543-17c9-11e9-b64c-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Futrack%2FtrackMid.html%3Ff%3Dhttps%253A%252F%252Fwww.lagou.com%252Fjobs%252Flist%255F%2525E5%252589%25258D%2525E7%2525AB%2525AF%2525E5%2525BC%252580%2525E5%25258F%252591%2525E5%2525B7%2525A5%2525E7%2525A8%25258B%2525E5%2525B8%252588%253FlabelWords%253D%2526fromSearch%253Dtrue%2526suginput%253D%26t%3D1547446205%26_ti%3D1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E5%2589%258D%25E7%25AB%25AF%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; SEARCH_ID=7960832a41da4dd4a024ab7cf5e42d94; LGRID=20190114150329-7ee35565-17ca-11e9-b64c-5254005c3644",
    "Host": "www.lagou.com",
    "Origin": "https://www.lagou.com",
    "Pragma": "no-cache",
    "Referer": "https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput=",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "X-Requested-With": "XMLHttpRequest"
}

# 连接数据库
db = pymysql.connect(
        host='127.0.0.1', 
        user='root', 
        password='root', 
        port=8889, 
        db='lagou_job', 
        charset='utf8mb4')


def add_Mysql(companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables):
    print('add_mysql')
    # 将数据写入数据库中
    try:
        cursor = db.cursor()
        sql = 'insert into job_list (companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables) values ("%d",      "%s",     "%s",      "%s",      "%s",         "%d",       "%s",       "%s", "%s",        "%s",          "%s",              "%s",   "%s",        "%s",             "%s",           "%s",         "%s",             "%s",      "%s",     "%s",            "%s",      "%s",       "%d",        "%s",      "%s")' % (companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables)
        print(sql)
        cursor.execute(sql)
        print(cursor.lastrowid)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def get_message(positionName):
    print(positionName)
    max_page_no = 31
    if max_page_no > MAX_PAGE + 1:
        max_page_no = MAX_PAGE
    for i in range(1, max_page_no):
        print('第' + str(i) + '页')
        print("Start : %s" % time.ctime())
        time.sleep(random.randint(1, 5))
        print("End : %s" % time.ctime())
        data = {
            'first': 'false',
            'pn': i,
            'kd': positionName
        }
        print(data)
        response = requests.post(
            url=url, data=data, headers=headers, timeout=10000)
        print(response)
        result = json.loads(response.text)
        print(response.json())
        job_messages = result['content']['positionResult']['result']
        for job in job_messages:
            # 公司ID
            companyId = job['companyId']
            print(companyId)
            # 工作经验
            workYear = job['workYear']
            print(workYear)
            # 教育程度
            education = job['education']
            print(education)
            # 工作性质
            jobNature = job['jobNature']
            print(jobNature)
            # 岗位名称
            positionName = job['positionName']
            print(positionName)
            # 岗位ID
            positionId = job['positionId']
            print(positionId)
            # 发布时间
            createTime = job['createTime']
            print(createTime)
            # 城市
            city = job['city']
            print(city)
            # 公司LOGO
            companyLogo = job['companyLogo']
            print(companyLogo)
            # 工业领域
            industryField = job['industryField']
            print(industryField)
            # 工作福利
            positionAdvantage = job['positionAdvantage']
            print(positionAdvantage)
            # 薪资
            salary = job['salary']
            print(salary)
            # 公司规模
            companySize = job['companySize']
            print(companySize)
            # 公司名称
            companyShortName = job['companyShortName']
            print(companyShortName)
            # 岗位标签
            if len(job['positionLables']) > 0:
                positionLables = ','.join(job['positionLables'])
            else:
                positionLables = 'None'
            print(positionLables)
            # 融资阶段
            financeStage = job['financeStage']
            print(financeStage)
            # 公司标签
            if len(job['companyLabelList']) > 0:
                companyLabelList = ','.join(job['companyLabelList'])
            else:
                companyLabelList = 'None'
            print(companyLabelList)
            # 经度
            longitude = job['longitude']
            print(longitude)
            # 纬度
            latitude = job['latitude']
            print(latitude)
            # 公司全称
            companyFullName = job['companyFullName']
            print(companyFullName)
            # 一级分类
            firstType = job['firstType']
            print(firstType)
            # 二级分类
            secondType = job['secondType']
            print(secondType)
            # 是否为实习
            isSchoolJob = job['isSchoolJob']
            print(isSchoolJob)
            # 三级分类
            thirdType = job['thirdType']
            print(thirdType)
            # 技能标签
            if len(job['skillLables']) > 0:
                skillLables = ','.join(job['skillLables'])
            else:
                skillLables = 'None'
            print(skillLables)
            # 写入数据库
            add_Mysql(companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables)


if __name__ == '__main__':
    # craw_job_list = parse_job_xml('../config/job.xml')
    # for _ in craw_job_list:
    get_message("前端开发工程师")
