# -*- coding: UTF-8 -*-

import pytest
from common.read_data import *
import random
import requests
import json
from conf.config import *
import time
from common.utils import getName, getDate, getDate1


class TestTencent:
    datas = get_excel(filename="tencent_material.xls", sheetName="Sheet2", converters={
        "adcreative_name": lambda x: getName(x)
    })

    access_token = "1a93af5ca4e172bfcb8cf5a991878bf7"
    account_id = 11300272

    @property
    def get_common_params(self):
        common_params = {
            "timestamp": int(time.time()),
            "nonce": str(time.time()) + str(random.randint(0, 999999)),
            "access_token": TestTencent.access_token
        }
        return common_params

    def convert(self, params):
        for k in params:
            if type(params[k]) is not str:
                params[k] = json.dumps(params[k])

        return params

    def creatPlan(self, parameters):
        res = requests.post(url="https://api.e.qq.com/v1.1/campaigns/add", params=self.get_common_params,
                            data=self.convert(parameters))
        print(res.json())
        return res.json()['data']['campaign_id']

    def createGroup(self, parameters):
        if parameters['bid_mode'] == "BID_MODE_OCPC" or parameters['bid_mode'] == "BID_MODE_OCPM":
            parameters['optimization_goal'] = "OPTIMIZATIONGOAL_ECOMMERCE_ORDER"
            parameters['bid_strategy'] = "BID_STRATEGY_AVERAGE_COST"

        res = requests.post(url='https://api.e.qq.com/v1.1/adgroups/add', data=self.convert(parameters),
                            params=self.get_common_params)
        print(res.json())
        return res.json()['data']['adgroup_id']

    @pytest.mark.parametrize("value", datas)
    def test(self, value):
        print(value)

    @pytest.mark.parametrize("value", datas)
    def test_add(self, value):

        campaign_parameters = {
            "account_id": TestTencent.account_id,
            "campaign_name": getName("广告计划ljf"),
            "campaign_type": "CAMPAIGN_TYPE_NORMAL",
            "promoted_object_type": "PROMOTED_OBJECT_TYPE_ECOMMERCE",
            "daily_budget": 100000,
            "configured_status": "AD_STATUS_NORMAL",
            "speed_mode": "SPEED_MODE_STANDARD"
        }
        campaign_id = self.creatPlan(campaign_parameters)

        adgroup_parameters = {
            "account_id": TestTencent.account_id,
            "campaign_id": campaign_id,
            "adgroup_name": getName("广告组ljf"),
            "promoted_object_type": "PROMOTED_OBJECT_TYPE_ECOMMERCE",
            "begin_date": getDate(3),
            "end_date": getDate(10),
            "bid_mode": value['bid_mode'],
            "bid_amount": 10000,
            "time_series": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            "site_set": ast.literal_eval(value['site_set']),
            "daily_budget": 100000,
            "targeting_id": 263590112,
        }
        adgroup_id = self.createGroup(adgroup_parameters)

        del value['bid_mode']

        adcreative_parameters = {
            "adcreative_name": value['adcreative_name'],
            "adcreative_template_id": value['adcreative_template_id'],
            "adcreative_elements": ast.literal_eval(value['adcreative_elements']),
            "page_type": value['page_type'],
            "page_spec": ast.literal_eval(value['page_spec']),
            "promoted_object_type": value['promoted_object_type'],
            "site_set": ast.literal_eval(value['site_set'])

        }

        adcreative_parameters['campaign_id'] = campaign_id
        adcreative_parameters['account_id'] = TestTencent.account_id
        print(json.dumps(adcreative_parameters, indent=4))

        res = requests.post(url='https://api.e.qq.com/v1.1/adcreatives/add', params=self.get_common_params,
                            data=self.convert(adcreative_parameters))
        print(res.json())

        adcreative_id = res.json()['data']['adcreative_id']
        ad_parameters = {
            "account_id": TestTencent.account_id,
            "adgroup_id": adgroup_id,
            "adcreative_id": adcreative_id,
            "ad_name": value['adcreative_name']
        }
        print(json.dumps(ad_parameters, indent=4))
        res = requests.post(url="https://api.e.qq.com/v1.1/ads/add", params=self.get_common_params,
                            data=self.convert(ad_parameters))
        print(res.json())
        time.sleep(1)
