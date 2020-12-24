# -*- coding: UTF-8 -*-
import requests


class TestPopManage:


    def test_01_peoplePackageList(self,getheaders):
        '''人群画像'''
        url="http://test.shulanchina.cn/api/market/peoplePackage/queryList"
        params={
            "name":"app",
            "beginDate":"2020-11-02 00:00:00",
            "endDate":"2020-12-23 23:59:59",
            "type":None,
            "pageNum":1,
            "pageSize":10,
            "status":"ENABLE"
        }

        res = requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code==200
        assert res.json()["status"]==0