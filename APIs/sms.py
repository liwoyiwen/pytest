import requests
import pytest
from common.utils import *

@pytest.fixture()
def getShortUrl(getMaterialId,getheaders):
    res=requests.post(url="http://test.shulanchina.cn/api/market/plan/generateShortUrl",
                      headers=getheaders,json={"materialId":getMaterialId})
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
def getMaterialId(getheaders):
    params = {
        "gmtStartDate": None,
        "gmtEndDate": None,
        "name": None,
        "auditStatus": "AUDIT_SUCCESS",
        "shopId": 0,
        "pageNum": 1,
        "pageSize": 10
    }

    res = requests.post(url="http://test.shulanchina.cn/api/market/material/list", headers=getheaders, json=params)
    yield res.json()["data"]["data"][0]['id']