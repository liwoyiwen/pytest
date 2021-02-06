from test.myInit import MyInit
import requests
from common.kafka_connection import *
from kafka.errors import kafka_errors
from common.read_data import *
from common.es_connection import *
import pytest


class TestSmartCrowdPackage(MyInit):
    def test_getSmartCrowdPackage(self):
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
        package_id = get_sql("select * from people_package where name='%s'" % (params['peoplePackageName']), market)[0][
            'id']
        assert package_id is not None

        try:
            dict3 = {
                "package_id": package_id,
                "member_id": ["e0991e03e8e8627d5db7b0e9a6e9eb73", "f3b68100491caf5952254753b05e1b47"],
                "error_type": "",
                "over": "false"
            }

            producer.send("crowd_expand_result", json.dumps(dict3).encode())

            dict3 = {
                "package_id": package_id,
                "member_id": ["e0992e03e8e8627d5db7b0e9a6e9eb73", "d3b68100491caf5952254753b05e1b47"],
                "error_type": "",
                "over": "true"
            }

            producer.send("crowd_expand_result", json.dumps(dict3).encode())

        except kafka_errors as e:
            print(e)

        time.sleep(40)

        detail_num, count, status = get_people_package_detail(package_id)
        assert detail_num > 0, "验证es 人群详情"
        assert detail_num == count, "人群数量"
        assert status == 0, "人群状态"

    @pytest.mark.parametrize("value", [0, 1])
    def test_getShopOrPeoplePackage(self, value):
        url = self.baseUrl + "/api/analysis/smartPeople/getShopOrPeoplePackage"
        params = {
            "type": value
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_customerAcquisitionHistory(self):
        url = self.baseUrl + "/api/analysis/smartPeople/customerAcquisitionHistory"
        params = {
            "pageNumber": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['list'] is not None
