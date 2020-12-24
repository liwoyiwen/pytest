# -*- coding: UTF-8 -*-
import requests
import pytest


class TestLabelManage:

    CategoryIdList=['5d5b499afbccb96a2958160b',
                    '5d5b499afbccb96a2958160d',
                    '5d5b499afbccb96a29581610',
                    '5d5b499afbccb96a29581611',
                    '5d5b499afbccb96a2958160c',
                    '5d5b499afbccb96a2958160e',
                    '5dcdfe1f3649f4a0f6f99b01']





    def test_01_getCategoryList(self,getheaders):
        url = "http://test.shulanchina.cn/api/heart/memberLabel/getCategoryList"
        res = requests.get(url=url, headers=getheaders)
        assert res.status_code == 200
        assert res.json()["status"] == 0






    @pytest.mark.parametrize("categoryId",CategoryIdList)
    def test_02_labelList(self,getheaders,categoryId):

        url="http://test.shulanchina.cn/api/heart/memberLabel/list"
        params={
            "categoryId":categoryId,
            "pageNumber":1,
            "pageSize":10
        }

        res = requests.post(url=url, headers=getheaders, json=params)
        assert res.status_code==200
        assert res.json()["status"]==0
