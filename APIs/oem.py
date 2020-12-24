import pytest
import requests
from common.utils import *


def addGroup(getheaders):
    '''巨量--创建广告组'''
    url = "http://test.shulanchina.cn/api/market/advertGroup/addAdvertGroup"
    params = {
        "budget": "5000",
        "shopId": 7,
        "advertGroupName": getName("ljf广告组")
    }

    res = requests.post(url=url, headers=getheaders, json=params)
    advertGroupId = res.json()["data"]["advertGroupId"]
    yield advertGroupId



def addAdvert(getheaders,addGroup):
    '''巨量--创建广告'''
    url="http://test.shulanchina.cn/api/market/advert/saveAdvert"
    params={
        "advertGroupId":"487",
        "shopId":7,
        "paymentType":1,
        "advertSpace":"1",
        "advertSpaceName":"今日头条",
        "launchPeople":"2730",
        "peoplePackageName":"20201221-3",
        "peoplePackageNumber":9999,
        "launchMode":0,
        "launchStartTime":"2020-12-31 08:00:00",
        "launchEndTime":None,
        "launchTimeInterval":"000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "launchTimeInfo":"[{\"week\":\"星期一\",\"times\":[\"05:30-06:00\"]}]",
        "directUrl":None,
        "totalAdvertBudget":10000,
        "singlePrice":"1000",
        "advertName":getName("ljf广告"),
        "transit":"",
        "transitState":"1",
        "fallUrl":None,
        "popularizeId":181}
    res=requests.post(url=url,headers=getheaders,json=params)
    print(res.json())

    advertId=res.json()["data"]["advertId"]
    yield advertId




