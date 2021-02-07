# -*- coding: UTF-8 -*-
import requests
import pytest
from test.myInit import MyInit
from datetime import datetime
import json

from common.es_connection import *


class TestPopManage(MyInit):
    search_peoplePackage_data = get_excel(filename='peoplePackage_data.xls', sheetName='search_peoplePackage',
                                          converters={
                                              "beginDate": lambda x: datetime.strftime(x,
                                                                                       "%Y-%m-%d %H:%M:%S") if x != '' else '',
                                              "endDate": lambda x: datetime.strftime(x,
                                                                                     "%Y-%m-%d %H:%M:%S") if x != '' else '',
                                              'sql': lambda x: x.strip().replace('%', '%%')
                                          })

    peoplePackage_portait_data = get_excel(filename='peoplePackage_data.xls', sheetName='peoplepackage_portait')

    '''
    
        def test_searchPeople(self,):
        url=get_envs.get_baseUrl()+"/api/market/peoplePackage/queryList"
        res = requests.post(url=url, headers=TestPopManage.headers, json=param)
        sql = "select * from people_package where user_id=6 and ori_type!='AI_PACKAGE'"
        if param['beginDate']:
            sql = sql + " and gmt_create >= '%s'" % param['beginDate']

        if param['endDate']:
            sql = sql + " and gmt_create <= '%s'" % param['endDate']

        if param['name']:
            sql = sql + " and name like '%%%%%s%%%%'" % param['name']

        if param['status']:
            sql = sql + " and status='%s'" % param['status']

        print(sql)
        result = get_mysqlConection(sql)
        assert res.status_code==200
        assert res.json()["status"]==0
        assert res.json()["data"]["totalCount"]==len(result)
    
    
    
    '''

    @pytest.mark.parametrize('value', search_peoplePackage_data)
    def test_searchPeoplePackage(self, value):
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
        real_total_count = get_sql(value['sql'], market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_total_count

    @pytest.mark.parametrize('value', peoplePackage_portait_data)
    def test_peoplePortrait(self, value):
        url = self.baseUrl + "/api/heart/crowdPackage/getCrowdPackagePortray"
        sql = value['crowdPackageId']
        people_dict = get_sql(sql, market)[0]
        params = {
            "crowdPackageId": people_dict['id']
        }

        res = requests.get(url=url, params=params, headers=self.headers)
        success = value['success']
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert people_dict['build_status'] == 0
        assert res.json()['data']['overview']['memberCount'] == people_dict['data_count']

    def test_import_crowdPackage(self):
        url = self.baseUrl + "/api/market/peoplePackage/importCrowdPackage"
        new_name = "../files/" + "outImport_" + datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S") + ".csv"
        os.rename("../files/test.csv", new_name)

        with open(new_name, "rb") as f:
            files = {
                "file": f
            }
            header = {
                "token": self.headers['token']
            }

            res = requests.post(url=url, headers=header, files=files)
        os.rename(new_name, "../files/test.csv")
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0
        package_id = res.json()['data']
        time.sleep(10)
        detail_num, count, status = get_people_package_detail(package_id)
        assert detail_num >= 0, "验证es 人群详情"
        assert detail_num == count, "人群数量"
        assert status == 0, "人群状态"
