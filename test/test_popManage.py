# -*- coding: UTF-8 -*-
import requests
import pytest
from test.myInit import MyInit
from datetime import datetime
import json

from common.es_connection import *
import time
from common.mysql_engine import get_peoplepackage_list


class TestPopManage(MyInit):
    peoplePackage_list_data = get_excel(filename='peoplePackage_data.xls', sheetName='peoplePackage_list',
                                        converters={
                                            "beginDate": lambda x: datetime.strftime(x,
                                                                                     "%Y-%m-%d") + " 00:00:00" if x != '' else '',
                                            "endDate": lambda x: datetime.strftime(x,
                                                                                   "%Y-%m-%d") + " 23:59:59" if x != '' else '',
                                            'sql': lambda x: x.strip().replace('%', '%%')
                                        })

    peoplePackage_portrait_data = get_excel(filename='peoplePackage_data.xls', sheetName='peoplepackage_portait')

    synchronous_data = get_excel(filename='peoplePackage_data.xls', sheetName='peoplepackage_portait',
                                 converters={"package": lambda x: get_sql(x, market)[0]['id']})

    dsp_put_data = get_excel(filename='peoplePackage_data.xls', sheetName='dsp_put')
    advert_pull_data = get_excel(filename='peoplePackage_data.xls', sheetName='advert_pull')

    @pytest.mark.parametrize('value', peoplePackage_list_data)
    def test_peoplePackage_list(self, value):
        """人群包列表"""

        print(json.dumps(value, indent=4))
        params = {
            "name": value['name'],
            "status": value['status'],
            "beginDate": value['beginDate'],
            "endDate": value['endDate'],
        }

        success = value['success']
        res = requests.post(url=self.baseUrl + "/api/market/peoplePackage/queryList", json=params, headers=self.headers)
        print(res.json())
        real_total_count = len(get_peoplepackage_list(user_id=self.user_id, params=params))
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_total_count

    @pytest.mark.parametrize('value', peoplePackage_portrait_data)
    def test_people_portrait(self, value):
        """人群包画像"""
        url = self.baseUrl + "/api/heart/crowdPackage/getCrowdPackagePortray"
        people_package = get_sql(value['package'], market)[0]
        params = {
            "crowdPackageId": people_package['id']
        }

        res = requests.get(url=url, params=params, headers=self.headers)
        success = value['success']
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert people_package['build_status'] == 0
        assert res.json()['data']['overview']['memberCount'] == people_package['data_count']

    def test_import_crowdPackage(self):
        """外部导入人群包"""
        url = self.baseUrl + "/api/market/peoplePackage/importCrowdPackage"
        old_name = "./files/" + "test.csv"
        new_name = "./files/" + "outImport_" + datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S") + ".csv"

        os.rename(old_name, new_name)

        with open(new_name, "rb") as f:
            files = {
                "file": f
            }
            header = {
                "token": self.headers['token']
            }

            res = requests.post(url=url, headers=header, files=files)
        os.rename(new_name, old_name)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        package_id = res.json()['data']

        time.sleep(10)
        assert_people_package_detail(package_id)

    @pytest.mark.parametrize("value", synchronous_data)
    def test_get_synchronous_status(self, value):
        """获取人群同步状态"""
        url = self.baseUrl + "/api/market/peoplePackage/selectPeoplePackageSynchronousStatus"

        params = {
            "id": value['package']
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", synchronous_data)
    def test_peoplePackage_synchronous(self, value):
        """人群同步"""
        url = self.baseUrl + "/api/market/peoplePackage/peoplePackageSynchronous"
        params = {
            "id": value['package']
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", synchronous_data)
    def test_disable(self, value):
        """禁用人群"""
        url = self.baseUrl + "/api/market/peoplePackage/disable/" + str(value['package'])
        res = requests.post(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", synchronous_data)
    def test_enable(self, value):
        """启用人群"""
        url = self.baseUrl + "/api/market/peoplePackage/enable/" + str(value['package'])
        res = requests.post(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_get_dsp_shop(self):
        """获取店铺dsp 授权列表"""
        url = self.baseUrl + "/api/base/shop/selectShopByUser"
        res = requests.post(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", advert_pull_data)
    def test_advert_pull(self, value):
        """获取可投放广告列表"""
        url = self.baseUrl + "/api/market/advertMerge/advertPull"
        params = {
            "shopId": value['shopId'],
            "putChannel": value['putChannel']
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", dsp_put_data, ids=[i['case_name'] for i in dsp_put_data])
    def test_dsp_put(self, value):
        """广告普通投放"""
        url = self.baseUrl + "/api/market/advertMerge/setPersonPackage"
        params = {
            "peoplePackageName": value['peoplePackageName'],
            "peoplePackageNumber": value['peoplePackageNumber'],
            "peoplePackageId": value['peoplePackageId'],
            "shopId": value['shopId'],
            "putChannel": value['putChannel'],
            "advertId": value['advertId'],
            "putState": value['putState']
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_path(self):
        print("*************")
        print(os.path.dirname(__file__))
        print("*************")
