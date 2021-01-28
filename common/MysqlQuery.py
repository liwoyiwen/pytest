import pymysql.cursors
from configparser import ConfigParser

import re

connection=pymysql.connect(host="192.168.100.166",port=3326,user="lijunfang",password="REmq4ofAABMzRKp2",db="market")
cur=connection.cursor()

def get_mysqlConection(sql):
    connection = pymysql.connect(host="192.168.100.166", port=3326, user="lijunfang", password="REmq4ofAABMzRKp2",
                            db="market")
    cur = connection.cursor()

    #sql="select * from material where user_id=6 and name like '%%%%%s%%%%' and gmt_create <= '2020-11-19 23:59:59' and gmt_create >= '2020-10-19 23:59:59'"%("自动化")

    cur.execute(sql)

    result = cur.fetchall()
    return result




def getmembers(packId):
    sql = "select members from people_package_detail where people_package_id=%d"%(packId)
    cur.execute(sql)
    result = cur.fetchall()
    members = result[0][0]
    res = re.findall(r'"memberId":"([^"]+)"', members)
    set1=set(res)
    return set1

def get_category():
    connection = pymysql.connect(host="192.168.100.166", port=3326, user="lijunfang", password="REmq4ofAABMzRKp2",
                            db="flask")
    cur = connection.cursor()

    sql="select * from category"
    cur.execute(sql)
    results = cur.fetchall()
    print(cur.description)
    results=list(results)
    list1 = [dict(zip(result.keys(), result)) for result in results]

    return list1
if __name__=="__main__":
    get_category()