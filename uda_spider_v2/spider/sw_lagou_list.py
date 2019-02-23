"""
a web spider for lagou
"""
# -*- coding: utf-8 -*-
# !/usr/bin/env python

import pymysql
import json

# 导入第三方库
import os
import sys
sys.path.append("..")
import time
import random

import requests
from requests.adapters import HTTPAdapter

from util.file_reader import parse_job_xml
from util.file_reader import mkdir

# 将模块路径加到当前模块扫描的路径里
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir)))
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

# 连接数据库
db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=8889,
        db='lagou_job',
        charset='utf8mb4')

# 添加数据到mysql
def add_Mysql(companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables, searchKeyWords):
    print('add_mysql')
    # 将数据写入数据库中
    try:
        cursor = db.cursor()
        sql = 'insert into job_list (companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables, searchKeyWords) values ("%d",      "%s",     "%s",      "%s",      "%s",         "%d",       "%s",       "%s", "%s",        "%s",          "%s",              "%s",   "%s",        "%s",             "%s",           "%s",         "%s",             "%s",      "%s",     "%s",            "%s",      "%s",       "%d",        "%s",      "%s",         "%s")' % (
            companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables, searchKeyWords)
        print(sql)
        cursor.execute(sql)
        print(cursor.lastrowid)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

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
    "Cookie": "JSESSIONID=ABAAABAAADEAAFI89DEF8645D339BEF9BAB65BFC9A664B0; _ga=GA1.2.586354285.1544933627; user_trace_token=20181216121347-fbe4e12e-00e8-11e9-9315-525400f775ce; LGUID=20181216121347-fbe4e436-00e8-11e9-9315-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22%24device_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; X_MIDDLE_TOKEN=0ce89912810bc00f0a3924888d329140; _gid=GA1.2.1005731183.1547813104; TG-TRACK-CODE=index_search; SEARCH_ID=bbe519a1274444edb92a5c765ad536c2; LGSID=20190119155323-4b9c2d9a-1bbf-11e9-bfab-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D58.222.50.99; _gat=1; LG_LOGIN_USER_ID=21f59ccc2d8a70469a4f62623e675b5479e12ca8d21d532b; _putrc=19ACEB5635CB4BA7; login=true; unick=%E6%9D%A8%E4%BA%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=5; index_location_city=%E4%B8%8A%E6%B5%B7; gate_login_token=6eb545f8fcad364eee634d661f6ec68660d456a3286c5594; LGRID=20190119155740-e4a1d54c-1bbf-11e9-bfac-525400f775ce",
    "Host": "www.lagou.com",
    "Origin": "https://www.lagou.com",
    "Pragma": "no-cache",
    "Referer": "https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput=",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "X-Requested-With": "XMLHttpRequest"
}

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

# 从拉勾网爬取职位信息【列表页】
def crawl_jobs(sw_positionName):
    JOB_DATA = list()
    # 创建max_page_number对象，返回最大页数
    max_page_number = get_max_pageNo(sw_positionName)
    # 循环获取每页数据
    for i in range(1, max_page_number + 1):
        print('第' + str(i) + '页，总共' + str(max_page_number) + '页')
        # 开始休眠
        print("Start : %s" % time.ctime())
        time.sleep(random.randint(1, 5))
        print("End : %s" % time.ctime())
        data = {
            'first': 'false',
            'pn': i,
            'kd': sw_positionName
        }

        try:
            # 发送请求
            response = s.post(
                url=url, data=data, headers=headers, timeout=10000)
            # print(response.json())
            result = json.loads(response.text)
            # 返回判断
            if response.status_code == 200 and len(result['content']) > 0:
                job_messages = result['content']['positionResult']['result']
                # 循环数据库中需要的字段并且存入数据库和excel文件
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
                    # 在拉钩中搜索的职位关键词
                    searchKeyWords = sw_positionName
                    print(searchKeyWords)
                    # 写入数据库
                    add_Mysql(companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize, companyShortName,
                            positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables, searchKeyWords)
                    JOB_DATA.append([companyId, workYear, education, jobNature, positionName, positionId, createTime, city, companyLogo, industryField, positionAdvantage, salary, companySize,
                                    companyShortName, positionLables, financeStage, companyLabelList, longitude, latitude, companyFullName, firstType, secondType, isSchoolJob, thirdType, skillLables, searchKeyWords])

                print('crawling page %d done...' % i)

            elif response.status_code == 403:
                print(response.json())
                log.error('request is forbidden by the server...')
            else:
                print(response.json())
                log.error(response.status_code)
        except requests.exceptions.RequestException as e:
            log.error(response.status_code + "超时3次")

    return JOB_DATA


# 返回某个工作的最大页数
def get_max_pageNo(positionName):
    data = {
        'first': 'true',
        'pn': 1,
        'kd': positionName
    }

    try:
        # 发送请求
        response = s.post(
        url=url, data=data, headers=headers, timeout=10000)
        print(response.json())
        result = json.loads(response.text)
        # 返回判断
        if response.status_code == 200 and len(result['content']) > 0:
            max_page_no = int(
                int(result['content']['positionResult']['totalCount']) / 15 + 1)
            if max_page_no > 30:
                max_page_no = 30
            if max_page_no > MAX_PAGE:
                return MAX_PAGE
            return max_page_no
        elif response.status_code == 403:
            log.error('request is forbidden by the server...')
            return 0
        else:
            log.error(response.status_code)
            return 0
    except requests.exceptions.RequestException as e:
        log.error(response.status_code + "超时3次")
    return 0

    


# 爬取职位信息，将内容保存在当前目录的data文件夹下
if __name__ == '__main__':
    craw_job_list = parse_job_xml('../config/job.xml')
    for _ in craw_job_list:
        # 创建joblist对象
        joblist = crawl_jobs(_)
        col = [
            u'公司ID',
            u'工作经验',
            u'教育程度',
            u'工作性质',
            u'岗位名称',
            u'岗位ID',
            u'发布时间',
            u'城市',
            u'公司LOGO',
            u'工业领域',
            u'岗位优势',
            u'薪资',
            u'公司规模',
            u'公司简称',
            u'岗位标签',
            u'融资阶段',
            u'公司标签',
            u'经度',
            u'纬度',
            u'公司全称',
            u'一级分类',
            u'二级分类',
            u'是否实习',
            u'三级分类',
            u'技能标签',
            u'搜索关键词']
        # 创建DataFrame对象，列名为col数组
        df = pd.DataFrame(joblist, columns=col)
        path = "./data/list/"
        mkdir(path)
        # 文件保存路径
        df.to_excel(path + _ + ".xlsx", sheet_name=_, index=False)
        print('%s has been written successfully... ————list' % _)
