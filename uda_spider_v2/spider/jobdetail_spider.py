import logging
import os
import sys
sys.path.append("..")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import Counter
import xlsxwriter
import time
from config.config import TIME_SLEEP

from util.excel_helper import mkdirs_if_not_exists
from util.file_reader import mkdir

JOB_DETAIL_DIR = './data/list/'
COMBINE_DIR = './data/combine/'

logging.basicConfig(format="%(asctime)s-%(name)s-%(levelname)s-%(message)s\t", level=logging.DEBUG)

# 爬取工作详细信息
def crawl_job_detail(positionId, positionName):
    request_url = 'https://m.lagou.com/jobs/' + str(positionId) + '.html'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7',
        'Host': 'm.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': '_ga=GA1.2.586354285.1544933627; user_trace_token=20181216121347-fbe4e12e-00e8-11e9-9315-525400f775ce; LGUID=20181216121347-fbe4e436-00e8-11e9-9315-525400f775ce; index_location_city=%E6%AD%A6%E6%B1%89; JSESSIONID=ABAAABAAAGCABCC817290F2D10A4884A1DAD59FDEBD46B3; _ga=GA1.3.586354285.1544933627; _gid=GA1.2.344950455.1547198201; LGSID=20190111171640-9b25a991-1581-11e9-99b6-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fm.lagou.com%2Fjobs%2F4737590.html; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22%24device_id%22%3A%221683c33831386-06bab1a7389288-10326653-2073600-1683c338314768%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LGRID=20190111173959-dce0412e-1584-11e9-9aa2-525400f775ce',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    # https://m.lagou.com/jobs/4737590.html

    response = requests.get(request_url, headers=headers, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')

        items = soup.find('div', class_='items')
        jobnature = items.find('span', class_='item jobnature').span.text.strip()
        workyear = items.find('span', class_='item workyear').span.text.strip()
        education = items.find('span', class_='item education').span.text.strip()
        jd = soup.find_all('div', class_='content')[0].get_text().strip().replace('\n', '').replace('&nbps;', '')  # jd

        
        #　休眠２s
        time.sleep(TIME_SLEEP)
    elif response.status_code == 403:
        logging.error('request is forbidden by the server...')
    else:
        logging.error(response.status_code)

    return [positionId, positionName, jobnature, workyear, education, jd]

#过滤关键词：目前筛选的方式只是选取英文关键词
def search_skill(result):
    print(result)
    rule = re.compile(r'[a-zA-z]+')
    skil_list = rule.findall(result)
    print(skil_list)
    return skil_list

# 对出现的关键词计数，并排序，选取Top80的关键词作为数据的样本
def count_skill(skill_list):
    for i in range(len(skill_list)):
        skill_list[i] = skill_list[i].lower()
    count_dict = Counter(skill_list).most_common(80)
    return count_dict

# 对结果进行存储并生成Area图
def save_excel(count_dict, file_name):
    # /Users/macbook/Documents/new-udacity/uda_spider_v2/spider/data/combine/
    book = xlsxwriter.Workbook(r'%s%s.xls' % (COMBINE_DIR, file_name))
    tmp = book.add_worksheet()
    row_num = len(count_dict)
    for i in range(1, row_num):
        if i == 1:
            tag_pos = 'A%s' % i
            tmp.write_row(tag_pos, ['关键词', '频次'])
        else:
            con_pos = 'A%s' % i
            k_v = list(count_dict[i-2])
            tmp.write_row(con_pos, k_v)
    chart1 = book.add_chart({'type': 'area'})
    chart1.add_series({
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$80',
        'values': '=Sheet1!$B$2:$B$80'
    })
    chart1.set_title({'name': '关键词排名'})
    chart1.set_x_axis({'name': '关键词'})
    chart1.set_y_axis({'name': '频次(/次)'})
    tmp.insert_chart('C2', chart1, {'x_offset': 15, 'y_offset': 10})
    book.close()

# 保存职位详细信息
if __name__ == '__main__':
    for excel_file in os.listdir(JOB_DETAIL_DIR):
        df = pd.read_excel(os.path.join(JOB_DETAIL_DIR, excel_file), index_col=False)

        fin_skill_list = [] # 关键词总表

        jd_item_list = list()
        for _ in range(len(df)):
            positionId = df['职位编码'].tolist()[_]
            positionName = excel_file.replace('.xlsx', '')
            try:
                jd_item = crawl_job_detail(positionId, positionName)
                # print(jd_item)

                skill_list = search_skill(jd_item[5]) # 获取JD详情，直接是内容，不需要删除html标记
                fin_skill_list.extend(skill_list)

                jd_item_list.append(jd_item)
            except:
                pass

        print('***********************开始统计关键词出现频率***********************')
        count_dict = count_skill(fin_skill_list)
        print(count_dict)
        save_excel(count_dict, positionName)
        print('***********************正在保存到 combine***********************')

        # 列名
        col = [
            u'职位编码',
            u'职位类型',
            u'工作性质',
            u'工作经验',
            u'教育程度',
            u'详情描述']

        df = pd.DataFrame(jd_item_list, columns=col)
        # 保存路径和文件名
        path = "./data/detail/"
        mkdir(path)
        df.to_excel(path + positionName + "-JD.xlsx", sheet_name=positionName, index=False, encoding='UTF-8')
        print('%s has been written successfully... ————detail' % positionName)


