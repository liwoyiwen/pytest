from test.myInit import MyInit
import requests
from common.utils import *
from common.mysql_engine import *
from common.es_connection import *
from datetime import datetime

class TestAppCircle(MyInit):

    def test_app_list(self):
        """获取app列表"""
        url = self.baseUrl + "/api/market/appCrowdPack/app/list"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_demand_list(self):
        """获取app 圈人工单列表"""
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
        """生成app圈人工单"""
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
        demand_bill_code = get_app_demand(params['name'])['demand_bill_code']
        middle_order_id = get_app_demand_detail(demand_bill_code)['middle_order_id']
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
            demand_after = get_app_demand(params['name'])
            assert demand_after['pull_num'] >= 0
            assert demand_after['demand_status'] == 2

            package_id = get_people_package(params['name'])['id']
            assert_people_package_detail(package_id)
