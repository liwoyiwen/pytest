# -*- coding: UTF-8 -*-
import requests


class TestPopPortraitCase:


    def test_memberOverview(self,getheaders):
        '''人群画像'''


        url="http://test.shulanchina.cn/api/heart/member/overview"
        params={
            "shopId":None,
            "labels":["性别：男性","性别：未知"],
            "rangeLabelReqs":[],
            "shopIds":[]
        }

        res = requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code==200
        assert res.json()["status"]==0

