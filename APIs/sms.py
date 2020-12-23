import requests
import pytest
from common.utils import *

@pytest.fixture()
def getShortUrl(request,getheaders):
    res=requests.post(url="http://test.shulanchina.cn/api/market/plan/generateShortUrl",
                      headers=getheaders,json=request.param)
    yield res.json()["data"]

@pytest.fixture()
def getplanId(getheaders):

    params = {
        "name":None,
        "auditStatus":None,
        "startDate":None,
        "endDate":None,
        "type":None,
        "putStatus":None,
        "putScene":None,
        "shopId":0,
        "pageNumber":1,
        "pageSize":10
    }


    res = requests.post(url="http://test.shulanchina.cn/api/market/plan/list", headers=getheaders, json=params)
    yield res.json()["data"]["data"][0]['id']

@pytest.fixture()
def MaterialList(request,getheaders):
    res = requests.post(url="http://test.shulanchina.cn/api/market/plan/add",
                        headers=getheaders, json=request.param)

    yield res


@pytest.fixture()
def MaterialDetail(request,getheaders):
    res = requests.get(url="http://test.shulanchina.cn/api/market/material/queryDetail"+"/"+str(request.param),
                        headers=getheaders)

    yield res

@pytest.fixture()
def PlanList(request,getheaders):
    res = requests.post(url="http://test.shulanchina.cn//api/market/plan/list",
                       headers=getheaders,json=request.param)

    yield res

@pytest.fixture()
def PlanDetail(request,getheaders):
    res = requests.get(url="http://test.shulanchina.cn/api/market/plan/detail"+"/"+str(request.param),
                        headers=getheaders)

    yield res



@pytest.fixture()
def SmslogList(request,getheaders):
    res = requests.post(url="http://test.shulanchina.cn/api/market/smslog/list",
                        headers=getheaders, json=request.param)

    yield res



@pytest.fixture()
def SmslogDetail(request,getheaders):
    res = requests.get(url="http://test.shulanchina.cn/api/market/smslog/detail"+"/"+str(request.param),
                        headers=getheaders)

    yield res


@pytest.fixture()
def SmslogAnalysis(request,getheaders):
    res = requests.get(url="http://test.shulanchina.cn/api/market/smslog/analysis"+"/"+str(request.param),
                       headers=getheaders)

    yield res