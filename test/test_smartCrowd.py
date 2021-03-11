from test.myInit import MyInit
import requests
from common.kafka_connection import *
from kafka.errors import kafka_errors
from common.utils import *
from common.es_connection import *
import pytest
import json


class TestSmartCrowdPackage(MyInit):
    def test_getSmartCrowdPackage(self):
        """发起智能圈人包"""
        url = self.baseUrl + "/api/market/smartPeople/getSmartCrowdPackage"
        params = {
            "referenceSource": 1,
            "referenceSourceIds": [3437],
            "numberOfExpansionsRequired": 10000,
            "deleteNewAndOldCustomers": 0,
            "peoplePackageName": getName("智能圈人"),
            "reference": "人群画像一键投放"
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        time.sleep(5)
        package_id = get_people_package(params['peoplePackageName'])['id']

        try:
            dict1 = {
                "package_id": package_id,
                "member_id": ["e0991e03e8e8627d5db7b0e9a6e9eb73", "f3b68100491caf5952254753b05e1b47"],
                "error_type": "",
                "over": "false"
            }

            producer.send("crowd_expand_result", json.dumps(dict1).encode())

            dict2 = {
                "package_id": package_id,
                "member_id": ["e0992e03e8e8627d5db7b0e9a6e9eb73", "d3b68100491caf5952254753b05e1b47"],
                "error_type": "",
                "over": "true"
            }

            producer.send("crowd_expand_result", json.dumps(dict2).encode())

        except kafka_errors as e:
            print(e)

        time.sleep(40)

        assert_people_package_detail(package_id)

    @pytest.mark.parametrize("value", [0, 1])
    def test_getShopOrPeoplePackage(self, value):
        """获取智能圈人包店铺列表和人群包列表"""
        url = self.baseUrl + "/api/analysis/smartPeople/getShopOrPeoplePackage"
        params = {
            "type": value
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_customerAcquisitionHistory(self):
        """获取智能圈人历史记录"""
        url = self.baseUrl + "/api/analysis/smartPeople/customerAcquisitionHistory"
        params = {
            "pageNumber": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['list'] is not None
