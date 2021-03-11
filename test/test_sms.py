# -*-coding:utf-8-*-
import pytest
from datetime import datetime
from datetime import timedelta
from common.utils import getName
import json
from test.myInit import *
import ast
from common.mysql_engine import get_sms_operation, get_sms_material, get_sms_plan


class TestSms(MyInit):
    add_material_data = get_excel(filename='sms_data.xls', sheetName="add_material", converters={
        "name": lambda x: getName(x) if x != '' else ''})

    add_plan_data = get_excel(filename='sms_data.xls', sheetName="add_plan", converters={
        "name": lambda x: getName(x) if x != '' else '',
        'startTime': lambda x: datetime.strftime(datetime.now(), "%Y-%m-%d" if x != '' else ''),
        'putMoment': lambda x: datetime.strftime(datetime.now() + timedelta(hours=1), "%H:%M") if x != '' else '', })

    plan_list_data = get_excel(filename='sms_data.xls', sheetName='plan_list', converters={
        'startDate': lambda x: datetime.strftime(x, "%Y-%m-%d") + " 00:00:00" if x != '' else '',
        'endDate': lambda x: datetime.strftime(x, "%Y-%m-%d") + " 23:59:59" if x != '' else ''})

    material_list_data = get_excel(filename='sms_data.xls', sheetName='material_list', converters={
        "gmtStartDate": lambda x: datetime.strftime(x, "%Y-%m-%d") + " 00:00:00" if x != '' else '',
        "gmtEndDate": lambda x: datetime.strftime(x, "%Y-%m-%d") + " 23:59:59" if x != '' else ''})

    operation_list_data = get_excel(filename='sms_data.xls', sheetName='operation_list', converters={
        "startDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else '',
        "endDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else '',
        'sql': lambda x: x.strip().replace('%', '%%')
    })

    @pytest.mark.parametrize("value", add_material_data, ids=[i['case_name'] for i in add_material_data])
    def test_add_material(self, value):
        """新增素材"""
        print(json.dumps(value, indent=4))
        params = {
            "content": value['content'],
            "name": value['name'],
            "putScene": value['putScene'],
            "shopId": value['shopId'],
            "signature": value['signature'],
            "url": value['url']
        }
        url = self.baseUrl + '/api/market/material/add'
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            assert res.json()['msg'] == value['msg']

    @pytest.mark.parametrize("value", add_plan_data, ids=[i['case_name'] for i in add_plan_data])
    def test_add_plan(self, value):
        """新增计划"""
        short_url = ''
        if value['materialId'] != '':
            res1 = requests.post(url=self.baseUrl + "/api/market/plan/generateShortUrl",
                                 json={'materialId': value['materialId']},
                                 headers=self.headers)

            short_url = res1.json()['data']

        params = {
            "materialId": value['materialId'],
            "name": value['name'],
            "peoplePackageId": ast.literal_eval(value['peoplePackageId']) if value['peoplePackageId'] != '' else [],
            "putScene": value['putScene'],
            "shortUrl": short_url,
            "startTime": value['startTime'],
            "putMoment": value['putMoment']
        }

        print(json.dumps(params, indent=4))
        res = requests.post(url=self.baseUrl + "/api/market/plan/add", headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            assert res.json()['msg'] == value['msg']

        if value['success']:
            plan_id = get_plan(params['name'])['id']
            self.assert_plan_detail(plan_id)

    def assert_plan_detail(self, plan_id):
        url = self.baseUrl + "/api/market/plan/detail" + "/" + str(plan_id)
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    @pytest.mark.parametrize('value', plan_list_data, ids=[i['case_name'] for i in plan_list_data])
    def test_plan_list(self, value):
        """计划列表"""
        print(json.dumps(value, indent=4))

        params = {
            "name": value['name'],
            "putScene": value['putScene'],
            "putStatus": value['putStatus'],
            "shopId": value['shopId'],
            "startDate": value['startDate'],
            "endDate": value['endDate']

        }

        res = requests.post(url=self.baseUrl + "/api/market/plan/list",
                            headers=self.headers,
                            json=params)

        print(res.json())

        real_total_count = len(get_sms_plan(user_id=self.user_id, params=params))

        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        assert res.json()['data']['totalCount'] == real_total_count

    def test_operation_analysis(self):
        """计划报告详情"""
        url = self.baseUrl + "/api/market/smslog/analysis/"
        smslog_id = requests.post(url=self.baseUrl + "/api/market/smslog/list",
                                  headers=self.headers,
                                  json={
                                      "pageNum": 1,
                                      "pageSize": 10,
                                      "shopId": 0,
                                      "timeRange": "RECENTLY_THIRTY_DAY"
                                  }).json()['data']['data'][0]['planId']
        res = requests.get(url=url + str(smslog_id), headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    @pytest.mark.parametrize('value', material_list_data, ids=[i['case_name'] for i in material_list_data])
    def test_material_list(self, value):
        """素材列表"""
        print(json.dumps(value, indent=4))
        params = {
            "shopId": value['shopId'],
            "name": value['name'],
            "auditStatus": value['auditStatus'],
            "gmtStartDate": value['gmtStartDate'],
            "gmtEndDate": value['gmtEndDate'],
            "pageNum": 1,
            "pageSize": 10
        }

        res = requests.post(url=self.baseUrl + "/api/market/material/list",
                            headers=self.headers,
                            json=params)

        print(res.json())

        real_total_count = len(get_sms_material(user_id=self.user_id, params=params))
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        assert res.json()['data']['totalCount'] == real_total_count

    def test_material_detail(self):
        """查看素材"""
        url = self.baseUrl + "/api/market/material/queryDetail"

        material_id = requests.post(url=self.baseUrl + "/api/market/material/list",
                                    headers=self.headers,
                                    json={
                                        "pageNum": 1,
                                        "pageSize": 10
                                    }).json()['data']['data'][0]['id']

        res = requests.get(url=url + '/' + str(material_id), headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_material_delete(self):
        """删除素材"""
        url = self.baseUrl + "/api/market/material/delete"

        material_id = requests.post(url=self.baseUrl + "/api/market/material/list",
                                    headers=self.headers,
                                    json={
                                        "pageNum": 1,
                                        "pageSize": 10
                                    }).json()['data']['data'][0]['id']

        res = requests.delete(url=url + '/' + str(material_id), headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    @pytest.mark.parametrize('value', operation_list_data, ids=[i['case_name'] for i in operation_list_data])
    def test_operation_list(self, value):
        """运营报告列表"""
        print(json.dumps(value, indent=4))
        params = {
            "shopId": value['shopId'],
            "planName": value['planName'],
            "startDate": value['startDate'],
            "endDate": value['endDate'],
            "timeRange": value['timeRange'],
            "pageNum": 1,
            "pageSize": 10,

        }
        success = value['success']
        res = requests.post(url=self.baseUrl + "/api/market/smslog/list",
                            headers=self.headers,
                            json=params)

        print(res.json())

        real_total_count = len(get_sms_operation(self.user_id, params=params))
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_total_count

    def test_operation_detail(self):
        """运营报告转化漏斗或详情"""
        url = self.baseUrl + "/api/market/smslog/detail/"

        smslog_id = requests.post(url=self.baseUrl + "/api/market/smslog/list",
                                  headers=self.headers,
                                  json={
                                      "pageNum": 1,
                                      "pageSize": 10,
                                      "shopId": 0,
                                      "timeRange": "RECENTLY_THIRTY_DAY"
                                  }).json()['data']['data'][0]['planId']

        res = requests.get(url=url + str(smslog_id), headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True
