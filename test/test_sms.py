# -*-coding:utf-8-*-
import pytest
from datetime import datetime
from datetime import timedelta
from common.utils import getName
import json
from test.myInit import *


class TestSms(MyInit):
    add_material_data = get_excel(filename='sms_data.xls', sheetName="add_material", converters={
        "name": lambda x: getName(x) if x != '' else ''})

    add_plan_data = get_excel(filename='sms_data.xls', sheetName="add_plan", converters={
        "name": lambda x: getName(x) if x != '' else '',
        'startTime': lambda x: datetime.strftime(datetime.now(), "%Y-%m-%d" if x != '' else ''),
        'putMoment': lambda x: datetime.strftime(datetime.now() + timedelta(hours=1), "%H:%M") if x != '' else '', })

    search_plan_data = get_excel(filename='sms_data.xls', sheetName='search_plan', converters={
        'startDate': lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != '' else '',
        'endDate': lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != '' else '',
        'sql': lambda x: x.replace('%', '%%')})

    search_material_data = get_excel(filename='sms_data.xls', sheetName='search_material', converters={
        "gmtStartDate": lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != '' else '',
        "gmtEndDate": lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != '' else '',
        'sql': lambda x: x.strip().replace('%', '%%')
    })

    search_operation_data = get_excel(filename='sms_data.xls', sheetName='search_operation', converters={
        "startDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else '',
        "endDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else '',
        'sql': lambda x: x.strip().replace('%', '%%')
    })

    @pytest.mark.parametrize("value", add_material_data)
    def test_add_material(self, value):
        print(json.dumps(value, indent=4))
        params = {
            "content": value['content'],
            "name": value['name'],
            "putScene": value['putScene'],
            "shopId": value['shopId'],
            "signature": value['signature'],
            "url": value['url']
        }

        msg = value['msg']
        success = value['success']
        url = self.baseUrl + '/api/market/material/add'
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
        if msg != '':
            assert res.json()['msg'] == msg

    @pytest.mark.parametrize("value", add_plan_data)
    def test_add_plan(self, value):
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
        msg = value['msg']
        success = value['success']
        print(json.dumps(params, indent=4))
        res = requests.post(url=self.baseUrl + "/api/market/plan/add", headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
        if msg != '':
            assert res.json()['msg'] == msg

        if success:
            plan_id = get_plan(params['name'])['id']
            self.assert_plan_detail(plan_id)

    def assert_plan_detail(self, plan_id):
        url = self.baseUrl + "/api/market/plan/detail" + "/" + str(plan_id)
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    @pytest.mark.parametrize('value', search_plan_data)
    def test_search_plan(self, value):
        print(json.dumps(value, indent=4))

        params = {
            "name": value['name'],
            "putScene": value['putScene'],
            "putStatus": value['putStatus'],
            "shopId": value['shopId'],
            "startDate": value['startDate'],
            "endDate": value['endDate']

        }
        success = value['success']

        res = requests.post(url=self.baseUrl + "/api/market/plan/list",
                            headers=self.headers,
                            json=params)

        print(res.json())

        total_count = get_sql(value['sql'], market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == total_count

    @pytest.mark.parametrize('value', search_material_data)
    def test_search_material(self, value):
        print(json.dumps(value, indent=4))
        params = {
            "shopId": value['shopId'],
            "name": value['name'],
            "auditStatus": value['auditStatus'],
            "gmtStartDate": value['gmtStartDate'],
            "gmtEndDate": value['gmtEndDate']
        }

        success = value['success']
        res = requests.post(url=self.baseUrl + "/api/market/material/list",
                            headers=self.headers,
                            json=params)

        print(res.json())

        total_count = get_sql(value['sql'], market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == total_count

    @pytest.mark.parametrize('value', search_operation_data)
    def test_search_operation(self, value):
        print(json.dumps(value, indent=4))
        params = {
            "shopId": value['shopId'],
            "planName": value['planName'],
            "startDate": value['startDate'],
            "endDate": value['endDate'],
            "timeRange": value['timeRange']

        }
        success = value['success']
        res = requests.post(url=self.baseUrl + "/api/market/smslog/list",
                            headers=self.headers,
                            json=params)

        print(res.json())

        total_count = get_sql(value['sql'], market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == total_count
