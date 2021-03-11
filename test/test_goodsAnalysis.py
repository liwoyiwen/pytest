from test.myInit import MyInit
import requests


class TestGoodsAnalysis(MyInit):
    def test_goods_analysis(self):
        """商品分析概览"""
        url = self.baseUrl + "/api/analysis/goodsAnalysis/goodsAnalysis"
        params = {
            "startTime": "2021-02-17",
            "endTime": "2021-02-23",
            "shopId": ""
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_goods_sales_rank(self):
        """商品销量排行"""
        url = self.baseUrl + "/api/analysis/goodsAnalysis/goodsSalesRank"
        params = {
            "startTime": "2021-02-17",
            "endTime": "2021-02-23",
            "shopId": "",
            "sort": "desc"
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
