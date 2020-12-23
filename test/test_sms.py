import pytest
import requests
import random
from common.utils import *

class TestSms:



    @pytest.mark.parametrize("getShortUrl",[{"materialId":465}],indirect=True)
    def test_getShortUrl(self,getShortUrl):
        pass



    def test_addPlan(self,getShortUrl,getheaders,getMaterialId):

        print(getShortUrl)
        params={
            "name":getName("测试计划"),
            "startTime":getDate(),
            "materialId":getMaterialId,
            "peoplePackageId":[1435],
            "putMoment":getTime2(17),
            "putScene":"PULL_NEW",
            "shortUrl":getShortUrl
        }
        print("****************")
        print(params)
        print("****************")

        res = requests.post(url="http://test.shulanchina.cn/api/market/plan/add",
                            headers=getheaders, json=params)
        print(res.json())

        assert res.status_code == 200
        assert res.json()['status'] == 0


    @pytest.mark.parametrize("gmtStartDate",[None, "2020-08-03 00:00:00"])
    @pytest.mark.parametrize("gmtEndDate",[None, "2021-08-03 00:00:00"])
    @pytest.mark.parametrize("name",[None, "自动化"])
    @pytest.mark.parametrize("auditStatus",[None, "AUDIT_ING", "AUDIT_SUCCESS", "AUDIT_FAILURE"])
    def test_MaterialList(self,getheaders,gmtStartDate,gmtEndDate,name,auditStatus):
        params = {
            "gmtStartDate": gmtStartDate,
            "gmtEndDate": gmtEndDate,
            "name": name,
            "auditStatus": auditStatus,
            "shopId": 0,
            "pageNum": 1,
            "pageSize": 10
        }

        res = requests.post(url="http://test.shulanchina.cn/api/market/material/list",
                            headers=getheaders,
                            json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0


    def test_04_MaterialDetail(self,getheaders,getMaterialId):
        '''短信--素材详情'''
        url="http://test.shulanchina.cn"+"/api/market/material/queryDetail"
        params=getMaterialId
        res = requests.get(url=url+"/"+str(params), headers=getheaders)
        assert res.status_code == 200
        assert res.json()['status'] == 0



    @pytest.mark.parametrize("startDate",[None, "2020-08-03 00:00:00"])
    @pytest.mark.parametrize("endDate",[None, "2021-08-03 00:00:00"])
    @pytest.mark.parametrize("name",[None, "自动化"])
    @pytest.mark.parametrize("putStatus",[None, "NOT_PUT", "RESCINDED", "DONE"])
    @pytest.mark.parametrize("putScene", ["PULL_NEW", "NEW", "RE_PURCHASE", "PROMOTION", "OTHER"])
    def test_PlanList(self, getheaders,startDate,endDate,name,putStatus,putScene):
        '''短信--计划列表'''
        url = "http://test.shulanchina.cn" + "/api/market/plan/list"


        params = {
            "name": name,
            "auditStatus": None,
            "startDate": startDate,
            "endDate": endDate,
            "type": None,
            "putStatus": putStatus,
            "putScene": putScene,
            "shopId": 0,
            "pageNumber": 1,
            "pageSize": 10
        }

        res = requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0


    def test_PlanDetail(self,getplanId,getheaders):
        '''短信--计划详情'''
        url="http://test.shulanchina.cn"+"/api/market/plan/detail"
        params=getplanId
        res = requests.get(url=url + "/" + str(params), headers=getheaders)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_SmslogList(self,getheaders):
        '''短信--运营报告列表'''
        url = "http://test.shulanchina.cn"+"/api/market/smslog/list"
        name = random.choice([None, "自动化"])
        timeRange=random.choice(["CUSTOM"])
        startDate = "2019-08-03" if timeRange=="CUSTOM" else None
        endDate = "2020-12-03" if timeRange=="CUSTOM" else None
        params = {
            "startDate":startDate,
            "endDate":endDate,
            "planName":name,
            "type":None,
            "shopId":0,
            "timeRange":timeRange,
            "pageSize":10,
            "pageNum":1
        }
        res = requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0