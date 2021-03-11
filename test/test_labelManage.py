# -*- coding: UTF-8 -*-
import requests
from test.myInit import MyInit
from common.read_data import get_excel, get_sql
import pytest
from common.utils import getName
import ast
import pandas as d
from common.mysql_engine import analysis


class TestLabelManage(MyInit):
    label_group_list_data = get_excel(filename='label_data.xls', sheetName='label_group_list')
    save_label_group_data = get_excel(filename='label_data.xls', sheetName='save_label_group')

    def test_label_list(self):
        """根据分类获取标签"""

        category_url = self.baseUrl + "/api/heart/memberLabel/getCategoryList"
        category_res = requests.get(url=category_url, headers=self.headers)
        assert category_res.status_code == 200
        assert category_res.json()["status"] == 0

        url = self.baseUrl + "/api/heart/memberLabel/list"
        params = {
            "categoryId": category_res.json()['data'][0]['id'],
            "pageNumber": 1,
            "pageSize": 10
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_label_collect(self):
        """收藏标签"""
        url = self.baseUrl + "/api/heart/memberLabel/favorite?id=5d5b5d07fbccb96a29581682"
        res = requests.post(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_collections_list(self):
        """获取收藏标签列表"""
        url = self.baseUrl + "/api/heart/memberLabel/favorites"
        params = {
            "pageNumber": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.parametrize("value", label_group_list_data)
    def test_label_group_list(self, value):
        """获取标签组列表"""
        url = self.baseUrl + "/api/analysis/label/labelGroupList"
        params = {
            "name": value['name'],
            "source": value['source'],
            "pageNumber": 1,
            "pageSize": 10
        }
        print(params)
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.parametrize("value", save_label_group_data)
    def test_save_labelGroup(self, value):
        """保存标签组"""
        url = self.baseUrl + "/api/analysis/label/saveLabelGroup"
        params = {
            "name": getName(value["name"]),
            "labels": ast.literal_eval(value['labels']) if value['labels'] != '' else [],
            "source": value["source"],
            "webShowBack": value["webShowBack"]
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())

        assert res.status_code == 200
        assert res.json()["status"] == 0
        global uuiId, webShowBack
        uuiId = res.json()['data']
        webShowBack = params['webShowBack']

    def test_save_config(self):
        """保存标签组反选信息"""
        url = self.baseUrl + "/api/base/frontEndConfig/saveConfig"
        params = {
            "source": "以场圈人（标签组）",
            "uniId": uuiId,
            "value": webShowBack
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_find_config(self):
        """获取标签组反选信息"""
        url = self.baseUrl + "/api/base/frontEndConfig/findConfig"
        params = {
            "source": "以场圈人（标签组）",
            "uniId": uuiId
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_searchLabelByCategory(self):
        """根据分类名称查找标签"""
        url = self.baseUrl + "/api/heart/memberLabel/searchLabelByCategory"
        params = {
            "categoryId": "5dcdfe1f3649f4a0f6f99b01"
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_favoritesBySearch(self):
        """搜索收藏标签"""
        url = self.baseUrl + "/api/heart/memberLabel/favoritesBySearch"
        res = requests.get(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_searchValueByLabel(self):
        """获取标签值"""
        url = self.baseUrl + "/api/heart/memberLabel/searchValueByLabel"
        params = {
            "id": "5d5b5d07fbccb96a29581682"
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_label_addUserSearches(self):
        """热门标签搜索次数加一"""
        url = self.baseUrl + "/api/analysis/label/addUserSearches"
        params = {
            "searchText": "休闲食品 - 1"
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_searchLevelLabel(self):
        """根据名称搜索标签品类"""
        url = self.baseUrl + "/api/analysis/label/searchLevelLabel"
        params = {
            "name": "饼干"
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def teardown_class(self):
        sql = f"delete from label_group where id={uuiId}"
        try:
            d.read_sql(sql, analysis)
        except Exception as e:
            print(e)
        finally:
            analysis.dispose()
