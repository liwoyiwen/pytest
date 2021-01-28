# -*- coding: UTF-8 -*-
import requests
from test.myInit import MyInit


class TestLabelManage(MyInit):

    def test_getCategoryList(self):
        url =self.baseUrl+"/api/heart/memberLabel/getCategoryList"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()["status"] == 0



    def test_labelList(self):

        url=self.baseUrl+"/api/heart/memberLabel/list"
        params={
            "categoryId":self.categoryId,
            "pageNumber":1,
            "pageSize":10
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0





