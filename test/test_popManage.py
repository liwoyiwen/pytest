# -*- coding: UTF-8 -*-
import requests
import pytest
from test.myInit import MyInit
from common.read_data import *


class TestPopManage(MyInit):
    search_peoplePackage_datas = get_excel(filename='peoplePackage_data.xls', sheetName='search_peoplePackage',
                                           converters={
                                               "beginDate": lambda x: datetime.strftime(x,
                                                                                        "%Y-%m-%d %H:%M:%S") if x != '' else '',
                                               "endDate": lambda x: datetime.strftime(x,
                                                                                      "%Y-%m-%d %H:%M:%S") if x != '' else '',
                                               'sql': lambda x: x.strip().replace('%', '%%')
                                           })

    peoplePackage_portait_datas = get_excel(filename='peoplePackage_data.xls', sheetName='peoplepackage_portait')

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

    @pytest.mark.parametrize('value', search_peoplePackage_datas)
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
        real_totalCount = get_sql(value['sql'], market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_totalCount

    @pytest.mark.parametrize('value', peoplePackage_portait_datas)
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
