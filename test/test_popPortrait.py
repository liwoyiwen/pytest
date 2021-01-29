# -*- coding: UTF-8 -*-
import requests
import pytest
from test.myInit import *
import json


class TestPopPortraitCase(MyInit):
    generateCrowdPackage_data = []

    def test_memberOverview(self):
        url = self.baseUrl + "/api/heart/member/overview"
        params = {
            "shopId": None,
            "labels": ["性别：男性", "性别：未知"],
            "rangeLabelReqs": [],
            "shopIds": []
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.parametrize('value', generateCrowdPackage_data)
    def test_generateCrowdPackage(self, value):
        url = self.baseUrl + "/api/heart/crowdPackage/generateCrowdPackage"

        params = {
            "shopId": value['shopId'],
            "name": value['name'],
            "oriType": value['oriType'],
            "labels": ast.literal_eval(value['labels']) if value['labels'] != '' else [],
            "rangeLabelReqs": ast.literal_eval(value['rangeLabelReqs']) if value['rangeLabelReqs'] != '' else []
        }

        print(json.dumps(params, indent=4))
        success = value['success']
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json()['data'])
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
