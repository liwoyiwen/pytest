# -*- coding: UTF-8 -*-
import requests
import pytest
from test.myInit import *
from common.es_connection import assert_people_package_detail
import ast
from common.utils import getName


class TestPopPortraitCase(MyInit):
    generateCrowdPackage_data = get_excel(filename='peoplePackage_data.xls', sheetName='generateCrowdPackage')

    @pytest.mark.parametrize('value', generateCrowdPackage_data)
    def test_member_overview(self, value):
        """人群画像"""
        url = self.baseUrl + "/api/heart/member/overview"
        params = {
            "shopId": value['shopId'],
            "labels": ast.literal_eval(value['labels']) if value['labels'] != '' else [],
            "rangeLabelReqs": ast.literal_eval(value['rangeLabelReqs']) if value['rangeLabelReqs'] != '' else [],
            "shopIds": []
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.parametrize('value', generateCrowdPackage_data)
    def test_generate_crowdPackage(self, value):
        """生成人群包"""
        url = self.baseUrl + "/api/heart/crowdPackage/generateCrowdPackage"

        params = {
            "shopId": value['shopId'],
            "name": getName(value['name']),
            "oriType": value['oriType'],
            "labels": ast.literal_eval(value['labels']) if value['labels'] != '' else [],
            "rangeLabelReqs": ast.literal_eval(value['rangeLabelReqs']) if value['rangeLabelReqs'] != '' else []
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        time.sleep(10)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        package_id = res.json()['data']
        assert_people_package_detail(package_id)

    @pytest.mark.parametrize('value', generateCrowdPackage_data)
    def test_member_list(self, value):
        """会员列表"""
        url = self.baseUrl + "/api/heart/member/list"
        params = {
            "shopId": value['shopId'],
            "labels": ast.literal_eval(value['labels']) if value['labels'] != '' else [],
            "rangeLabelReqs": ast.literal_eval(value['rangeLabelReqs']) if value['rangeLabelReqs'] != '' else [],
            "shopIds": [],
            "pageNumber": 1,
            "pageSize": 10
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']

    def test_member_portraits_list(self):
        """用户个像--标签列表"""
        url = self.baseUrl + "/api/heart/memberPortraits/list"
        params = {
            "id": "BA34B560FA0D3A223A0FBBA949FBFF60",
            "shopId": 0
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_member_portraits_rfm(self):
        """用户个像--rfm"""
        url = self.baseUrl + "/api/heart/memberPortraits/rfm"
        params = {
            "id": "BA34B560FA0D3A223A0FBBA949FBFF60",
            "shopId": 0
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_consumer_history(self):
        """用户个像--购买历史"""
        url = self.baseUrl + "/api/heart/consumerHistory/getConsumerHistory"
        params = {
            "memberId":"BA34B560FA0D3A223A0FBBA949FBFF60"
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True