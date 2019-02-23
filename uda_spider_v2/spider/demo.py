#!/usr/bin/python3

import pymysql

# 打开数据库连接
# 连接数据库
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    port=8889,
    db='lagou_job',
    charset='utf8mb4')


def query_Mysql(searchKeyWords):
    print('query_mysql')
    JOB_DETAIL_DATA = list()

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT positionId FROM job_list WHERE searchKeyWords LIKE '%" + searchKeyWords + "%'"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            JOB_DETAIL_DATA.append([row[0]])
            # 打印结果
            # print("positionId=%s" % (positionId))
    except Exception as e:
        print("Error: unable to fetch data")
        # print(e)
        db.rollback()
    return JOB_DETAIL_DATA


print(query_Mysql("前端开发工程师"))