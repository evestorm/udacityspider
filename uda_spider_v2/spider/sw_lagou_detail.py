import pymysql
import json

import logging
import os
import sys
sys.path.append("..")
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import Counter
import xlsxwriter
import time
from config.config import TIME_SLEEP
import random

from util.excel_helper import mkdirs_if_not_exists
from util.file_reader import mkdir

# 连接数据库
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    port=8889,
    db='lagou_job',
    charset='utf8mb4')

# 添加数据到mysql
def add_Mysql(positionId, description):
    print('add_mysql')
    # 将数据写入数据库中
    try:
        cursor = db.cursor()
        sql = 'insert into job_detail (positionId, description) values ("%d", "%s")' % (positionId, description)
        print(sql)
        cursor.execute(sql)
        print(cursor.lastrowid)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

def query_Mysql(searchKeyWords):
    print('query_mysql')
    JOB_DETAIL_DATA = list()

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT positionId FROM job_list WHERE searchKeyWords LIKE '%" + \
        searchKeyWords + "%' AND positionId >= 5487969 ORDER BY positionId ASC"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            JOB_DETAIL_DATA.append(row[0])
            # 打印结果
            # print("positionId=%s" %
            #     (positionId))
    except Exception as e:
        print("Error: unable to fetch data")
        # print(e)
        db.rollback()
    return JOB_DETAIL_DATA


# 请求网址及请求头参数
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=ABAAABAAADEAAFI89DEF8645D339BEF9BAB65BFC9A664B0; _ga=GA1.2.586354285.1544933627; user_trace_token=20181216121347-fbe4e12e-00e8-11e9-9315-525400f775ce; LGUID=20181216121347-fbe4e436-00e8-11e9-9315-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22%24device_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; X_MIDDLE_TOKEN=0ce89912810bc00f0a3924888d329140; _gid=GA1.2.1005731183.1547813104; TG-TRACK-CODE=index_search; SEARCH_ID=bbe519a1274444edb92a5c765ad536c2; LGSID=20190119155323-4b9c2d9a-1bbf-11e9-bfab-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D58.222.50.99; _gat=1; LG_LOGIN_USER_ID=21f59ccc2d8a70469a4f62623e675b5479e12ca8d21d532b; _putrc=19ACEB5635CB4BA7; login=true; unick=%E6%9D%A8%E4%BA%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=5; index_location_city=%E4%B8%8A%E6%B5%B7; gate_login_token=6eb545f8fcad364eee634d661f6ec68660d456a3286c5594; LGRID=20190119155740-e4a1d54c-1bbf-11e9-bfac-525400f775ce",
    "Host": "www.lagou.com",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))


# 保存职位详细信息
if __name__ == '__main__':
    queryList = query_Mysql("无人驾驶工程师")
    for pid in queryList:
        # print(item)
        # 开始休眠
        print("Start : %s" % time.ctime())
        time.sleep(random.randint(1, 4))
        print("End : %s" % time.ctime())
        print('positionId：' + str(pid) + '开始')

        try:
            request_url = 'https://www.lagou.com/jobs/' + str(pid) + '.html'
            response = s.get(request_url, headers=headers, timeout=1000000)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html5lib')

                items = soup.find('div', class_='items')
                jd = soup.find_all('div', class_='job-detail')[0].get_text(
                ).strip().replace('\n', '').replace('&nbps;', '')  # jd
                # print(jd)
                add_Mysql(pid, jd)
                print('positionId：' + str(pid) + '结束')
            elif response.status_code == 403:
                logging.error('request is forbidden by the server...')
            else:
                logging.error(response.status_code)
        except requests.exceptions.RequestException as e:
            logging.error(response.status_code + "超时3次")

    print("该职位完成")
