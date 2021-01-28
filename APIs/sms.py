import requests
import pytest
from common.utils import *

@pytest.fixture()
def getShortUrl(getMaterialId,get_envs):
    res=requests.post(url=get_envs.get_baseUrl()+"/api/market/plan/generateShortUrl",
                      headers=get_envs.get_headers(),json={"materialId":getMaterialId})
    yield res.json()["data"]

@pytest.fixture()
def getplanId(get_envs):

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


    res = requests.post(url=get_envs.get_baseUrl()+"/api/market/plan/list", headers=get_envs.get_headers(), json=params)
    yield res.json()["data"]["data"][0]['id']


@pytest.fixture()
def getMaterialId(get_envs):
    params = {
        "gmtStartDate": None,
        "gmtEndDate": None,
        "name": None,
        "auditStatus": "AUDIT_SUCCESS",
        "shopId": 0,
        "pageNum": 1,
        "pageSize": 10
    }

    res = requests.post(url=get_envs.get_baseUrl()+"/api/market/material/list", headers=get_envs.get_headers(), json=params)
    yield res.json()["data"]["data"][0]['id']