# -*- coding: UTF-8 -*-
import pytest
import requests
import random
from common.utils import *

class TestScenePeopleTest:


    scenePeopleLabel = ['都市精英', '主流时尚', '平价实惠', '白富美', '家庭主妇', '美丽教主', '数码达人', '吃货']
    categoryLabel = []
    peopleLabel = [
        "sex：男性",
        "sex：女性",
        "sex：未知",
        "cityLevel：一线城市",
        "cityLevel：二线城市",
        "cityLevel：三线城市",
        "cityLevel：三线以下城市",
        "isHaveBaby：无宝宝",
        "isHaveBaby：有宝宝",
        "isHavePet：无宠物",
        "isHavePet：有宠物",

    ]


    def test_getScene(self,getheaders):
        url="http://test.shulanchina.cn/api/analysis/label/getSceneCrowd"
        res=requests.post(url=url,headers=getheaders)
        assert res.status_code == 200
        assert res.json()["status"] == 0



    def test_getEstimateNumber(self,getheaders):
        url="http://test.shulanchina.cn/api/analysis/peoplePackage/getEstimateNumber"
        params={
            "repeated":0,
            "type":"SCENE_SELECT_PEOPLE",
            "scenePeopleLabel":random.choices(self.scenePeopleLabel),
            "categoryLabel":[],
            "peopleLabel": random.choices(self.peopleLabel)

        }


        res=requests.post(url=url,json=params,headers=getheaders)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_generateSceneAndTradePeoplePackage(self,getheaders):
        url='http://test.shulanchina.cn/api/market/peoplePackage/generateSceneAndTradePeoplePackage'
        params={
            "repeated":0,
            "type":"SCENE_SELECT_PEOPLE",
            "scenePeopleLabel":random.choices(self.scenePeopleLabel),
            "categoryLabel":[],
            "peopleLabel": random.choices(self.peopleLabel),
            "estimateNumber":500000,
            "name":getName("以场圈人"),
            "dataCount":10000,
            "requestParam":
                "{\"crossAnalysisLabels\":[\"性别：男性\",\"性别：女性\",\"性别：未知\",\"城市级别：一线城市\",\"有无宝宝：无宝宝\",\"有无宠物：无宠物\"],\"rangeLabelReqs\":[],\"query_labels\":[{\"name\":\"场景人群\",\"values\":[\"(家庭主妇)\",\"(美丽教主)\"]},{\"name\":\"性别\",\"values\":[\"(男性)\",\"(女性)\",\"(未知)\"]},{\"name\":\"城市级别\",\"values\":[\"(一线城市)\"]},{\"name\":\"有无宝宝\",\"values\":[\"(无宝宝)\"]},{\"name\":\"有无宠物\",\"values\":[\"(无宠物)\"]}],\"repeated\":0}"
        }
        res=requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0


