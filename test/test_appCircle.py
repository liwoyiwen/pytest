from test.myInit import MyInit
import requests
from common.utils import *
from common.read_data import *
import os
from common.es_connection import *


class TestAppCircle(MyInit):
    def test_app_list(self):
        url = self.baseUrl + "/api/market/appCrowdPack/app/list"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_demand_list(self):
        url = self.baseUrl + "/api/market/appCrowdPack/queryDemandList"
        params = {
            "startTime": None,
            "endTime": None,
            "accountName": None,
            "companyName": None,
            "userId": None,
            "pageNum": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_add_demand(self):
        url = self.baseUrl + "/api/market/appCrowdPack/addDemand"
        params = {
            "appName": "中外云仓",
            "name": "app" + datetime.strftime(datetime.now(), "%y-%m-%d_%H-%M-%S"),
            "num": 10000
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0
        demand = get_sql("select * from app_crowd_pack_demand where name='%s'" % params['name'], market)[0]
        demand_bill_code = demand['demand_bill_code']
        middle_order_id = \
            get_sql("select middle_order_id from app_pull_middle_data where order_no='%s'" % demand_bill_code, market)[
                0]["middle_order_id"]
        assert middle_order_id is not None

        if os.environ.get("--env") == "test":
            pull_order_params = {
                "workOrderNo": middle_order_id,
                "workOrderBatchNo": "100808571",
                "pageNum": 2,
                "total": 10000
            }

            res = requests.post(url="http://test2.shulanchina.cn/api/market/peoplePackage/pullOrder",
                                json=pull_order_params)
            assert res.status_code == 200
            assert res.json()['code'] == 0
            time.sleep(60)
            demand_after = get_sql("select * from app_crowd_pack_demand where name='%s'" % params['name'], market)[0]
            assert demand_after['pull_num'] >= 0
            assert demand_after['demand_status'] == 2
            package_id = get_sql("select * from people_package where name='%s'" % params['name'], market)[0]['id']

            detail_num, count, status = get_people_package_detail(package_id)
            assert detail_num > 0, "验证es 人群详情"
            assert detail_num == count, "人群数量"
            assert status == 0, "人群状态"
