# -*-coding:utf-8-*-

import requests
from common.mysql_engine import *
import time
import random


class MyInit:

    def setup_class(self):

        read_config = ReadConfig()
        self.shopId = read_config.get_conf('shopId')
        self.categoryId = read_config.get_conf("categoryId")
        self.launchPeople = read_config.get_conf('launchPeople')
        self.peoplePackageName = read_config.get_conf('peoplePackageName')
        self.peoplePackageNumber = read_config.get_conf('peoplePackageNumber')
        self.user_id = read_config.get_conf('user_id')
        self.headers = read_config.get_headers()
        self.baseUrl = read_config.get_baseUrl()
        self.access_token = read_config.get_conf('access_token')

    def teardown_class(self):
        print("开始撤销计划")
        self.revoke_plan(self)

    def teardown_method(self):
        print("开始删除人群包")
        self.delete_custom_audiences()

    def revoke_plan(self):
        url = self.baseUrl + "/api/market/plan/revokePlan"
        plan_list = get_sql("select id from plan where user_id=6 and put_status='NOT_PUT' and name like '%%一键投放测试计划%%'",
                            market)
        for plan in plan_list:
            params = {
                "planId": plan["id"]
            }
            res = requests.post(url=url, headers=self.headers, params=params)
            print(res.json())

    def delete_custom_audiences(self):
        url = "https://api.e.qq.com/v1.1/custom_audiences/get"
        params = {
            "access_token": self.access_token,
            "timestamp": time.time(),
            "nonce": time.time(),
            "account_id": 11300272,
            "page": 1,
            "page_size": 50
        }
        res = requests.get(url=url, params=params)
        print(res.json())

        l = []
        for r in res.json()["data"]["list"]:
            l.append(r["audience_id"])
        print(l)

        for i in l:
            params2 = {
                "access_token": self.access_token,
                "timestamp": time.time(),
                "nonce": time.time(),

            }
            data = {
                "account_id": 11300272,
                "audience_id": i
            }
            res2 = requests.post(url="https://api.e.qq.com/v1.1/custom_audiences/delete",
                                 params=params2, data=data)
            print(res2.json())

    def get_shortUrl(self, material_id):
        url = self.baseUrl + '/api/market/plan/generateShortUrl'
        headers = read_config.get_headers()
        params = {
            "materialId": material_id
        }
        res = requests.post(url=url, headers=headers, json=params)
        print(res.json()['data'])
        return res.json()['data']
