import pytest
import requests
import random
from common.utils import *

class TestSms:



    @pytest.mark.parametrize("getShortUrl",[{"materialId":465}],indirect=True)
    def test_getShortUrl(self,getShortUrl):
        pass


    @pytest.mark.parametrize("getShortUrl", [{"materialId": 465}], indirect=True)
    def test_addPlan(self,getShortUrl,getheaders):

        print(getShortUrl)
        params={
            "name":getName("测试计划"),
            "startTime":getDate(),
            "materialId":465,
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



    def test_MaterialList(self,getheaders):
        gmtStartDate = [None, "2020-08-03 00:00:00"]
        gmtEndDate = [None, "2021-08-03 00:00:00"]
        name = [None, "自动化"]
        auditStatus = [None, "AUDIT_ING", "AUDIT_SUCCESS", "AUDIT_FAILURE"]
        params = {
            "gmtStartDate": random.choice(gmtStartDate),
            "gmtEndDate": random.choice(gmtEndDate),
            "name": random.choice(name),
            "auditStatus": random.choice(auditStatus),
            "shopId": 0,
            "pageNum": 1,
            "pageSize": 10
        }

        res = requests.post(url="http://test.shulanchina.cn/api/market/material/list",
                            headers=getheaders,
                            json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0


    def test_04_MaterialDetail(self,getheaders):
        '''短信--素材详情'''
        url="http://test.shulanchina.cn"+"/api/market/material/queryDetail"
        params=465
        res = requests.get(url=url+"/"+str(params), headers=getheaders)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_05_PlanList(self, getheaders):
        '''短信--计划列表'''
        url = "http://test.shulanchina.cn" + "/api/market/plan/list"
        startDate = [None, "2020-08-03 00:00:00"]
        endDate = [None, "2021-08-03 00:00:00"]
        name = [None, "自动化"]
        putStatus = [None, "NOT_PUT", "RESCINDED", "DONE"]
        putScene = ["PULL_NEW", "NEW", "RE_PURCHASE", "PROMOTION", "OTHER"]

        params = {
            "name": random.choice(name),
            "auditStatus": None,
            "startDate": random.choice(startDate),
            "endDate": random.choice(endDate),
            "type": None,
            "putStatus": random.choice(putStatus),
            "putScene": random.choice(putScene),
            "shopId": 0,
            "pageNumber": 1,
            "pageSize": 10
        }

        res = requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0


    def test_06_PlanDetail(self,getplanId,getheaders):
        '''短信--计划详情'''
        url="http://test.shulanchina.cn"+"/api/market/plan/detail"
        params=getplanId
        res = requests.get(url=url + "/" + str(params), headers=getheaders)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_07_SmslogList(self,getheaders):
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