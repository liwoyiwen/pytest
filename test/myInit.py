# -*-coding:utf-8-*-

from conf.config import *
import requests
from common.read_data import *


class MyInit:

    def setup_class(self):
        envs = os.environ.get("--env")
        print(envs)
        read_config = Read_config("test")
        self.shopId = read_config.get_conf('shopId')
        self.categoryId = read_config.get_conf("categoryId")
        self.launchPeople = read_config.get_conf('launchPeople')
        self.peoplePackageName = read_config.get_conf('peoplePackageName')
        self.peoplePackageNumber = read_config.get_conf('peoplePackageNumber')
        self.headers = read_config.get_headers()
        self.baseUrl = read_config.get_baseUrl()

    def get_shortUrl(self, materialId):
        read_config = Read_config("test")
        base_url = read_config.get_baseUrl()
        url = base_url + '/api/market/plan/generateShortUrl'
        headers = read_config.get_headers()
        params = {
            "materialId": materialId
        }
        res = requests.post(url=url, headers=headers, json=params)
        print(res.json()['data'])
        return res.json()['data']

    def teardown_class(self):
        read_config = Read_config("test")
        base_url = read_config.get_baseUrl()
        url = base_url+ "/api/market/plan/revokePlan"
        plan_list = get_sql("select id from plan where user_id=6 and put_status='NOT_PUT' and name like '%%一键投放测试计划%%'",market)
        for plan in plan_list:
            params = {
                "planId": plan["id"]
            }
            res = requests.post(url=url, headers=self.headers, params=params)
            print(res.json())
