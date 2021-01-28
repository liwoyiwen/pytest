# -*-coding:utf-8-*-

from common.read_data import *
import pytest
import requests
from conf.config import *
from datetime import datetime
from datetime import timedelta
from common.mysql_engine import *
from test.myInit import *
class TestSmsMaterial(MyInit):



    add_material_datas = get_excel(filename='sms_data.xls',sheetName="add_material", converters={
        "name": lambda x:getName(x) if x!='' else ''})

    add_plan_datas=get_excel(filename='sms_data.xls',sheetName="add_plan", converters={
        "name": lambda x:getName(x) if x!='' else '',
        'startTime':lambda x:datetime.strftime(datetime.now(),"%Y-%m-%d" if x!='' else ''),
        'putMoment':lambda x:datetime.strftime(datetime.now()+timedelta(minutes=20),"%H:%M") if x!='' else '',})

    search_plan_datas=get_excel(filename='sms_data.xls',sheetName='search_plan',converters={
        'startDate':lambda x:datetime.strftime(x,"%Y-%m-%d %H:%M:%S") if x!='' else '',
        'endDate':lambda x:datetime.strftime(x,"%Y-%m-%d %H:%M:%S") if x!='' else '',
        'sql':lambda x:x.replace('%','%%')})


    search_material_datas=get_excel(filename='sms_data.xls',sheetName='search_material',converters={
        "gmtStartDate":lambda x:datetime.strftime(x,"%Y-%m-%d %H:%M:%S") if x!='' else '',
        "gmtEndDate":lambda x:datetime.strftime(x,"%Y-%m-%d %H:%M:%S") if x!='' else '',
        'sql': lambda x: x.strip().replace('%', '%%')
    })

    search_operation_datas=get_excel(filename='sms_data.xls',sheetName='search_operation',converters={
        "startDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else '',
        "endDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else '',
        'sql': lambda x: x.strip().replace('%', '%%')
    })



    @pytest.mark.parametrize("value", add_material_datas)
    def test_addMaterial(self, value):
        print(json.dumps(value,indent=4))
        params={
            "content":value['content'],
            "name":value['name'],
            "putScene":value['putScene'],
            "shopId":value['shopId'],
            "signature":value['signature'],
            "url":value['url']
        }

        msg=value['msg']
        success=value['success']
        url =self.baseUrl+'http://test.shulanchina.cn/api/market/material/add'
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code==200
        assert res.json()['success']==success
        if msg!='':
            assert res.json()['msg']==msg




    @pytest.mark.parametrize("value", add_plan_datas)
    def test_addPlan(self,value):
        shortUrl=''
        if value['materialId']!='':
            try:

                res1=requests.post(url=self.baseUrl+"/api/market/plan/generateShortUrl",
                                   json={'materialId':value['materialId']},
                                   headers=self.headers)

                shortUrl=res1.json()['data']
            except:
                print('shortURL')

        params={
            "materialId": value['materialId'],
            "name": value['name'],
            "peoplePackageId": ast.literal_eval(value['peoplePackageId']) if value['peoplePackageId']!='' else [],
            "putScene": value['putScene'],
            "shortUrl": shortUrl,
            "startTime": value['startTime'],
            "putMoment": value['putMoment']
        }
        msg = value['msg']
        success = value['success']
        print(json.dumps(params, indent=4))
        res=requests.post(url=self.baseUrl+"/api/market/plan/add",headers=self.headers,json=params)
        print(res.json())
        assert res.status_code==200
        assert res.json()['success']==success
        if msg!='':
            assert res.json()['msg']==msg




    @pytest.mark.parametrize('value',search_plan_datas)
    def test_searchPlan(self,value):
        print(json.dumps(value,indent=4))

        params={
            "name":value['name'],
            "putScene":value['putScene'],
            "putStatus":value['putStatus'],
            "shopId":value['shopId'],
            "startDate":value['startDate'],
            "endDate":value['endDate']

        }
        success=value['success']

        res=requests.post(url=self.baseUrl+"/api/market/plan/list",
                          headers=self.headers,
                          json=params)

        print(res.json())

        real_totalCount=get_sql(value['sql'],market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount']==real_totalCount




    @pytest.mark.parametrize('value',search_material_datas)
    def test_searchMaterial(self,value):
        print(json.dumps(value,indent=4))
        params={
            "shopId":value['shopId'],
            "name":value['name'],
            "auditStatus":value['auditStatus'],
            "gmtStartDate":value['gmtStartDate'],
            "gmtEndDate":value['gmtEndDate']
        }

        success = value['success']
        res=requests.post(url=self.baseUrl+"/api/market/material/list",
                          headers=self.headers,
                          json=params)


        print(res.json())

        real_totalCount=get_sql(value['sql'],market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount']==real_totalCount

    @pytest.mark.parametrize('value',search_operation_datas)
    def test_seatchOperation(self,value):
        print(json.dumps(value,indent=4))
        params={
            "shopId":value['shopId'],
            "planName": value['planName'],
            "startDate":value['startDate'],
            "endDate": value['endDate'],
            "timeRange": value['timeRange']

        }
        success = value['success']
        res=requests.post(url=self.baseUrl+"/api/market/smslog/list",
                          headers=self.headers,
                          json=params)


        print(res.json())

        real_totalCount=get_sql(value['sql'],market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount']==real_totalCount