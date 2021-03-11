from test.myInit import MyInit
import requests


class TestRealAnalysis(MyInit):
    def test_real_survey(self):
        """销售概况"""
        url = self.baseUrl + "/api/dataanalysis/orderRealAnalysis/realSurvey"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_real_trend(self):
        """今日走势"""
        url = self.baseUrl + "/api/dataanalysis/orderRealAnalysis/realTrend"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_real_top(self):
        """销售金额-销售件数-成交客户数-下单支付转化率"""
        url = self.baseUrl + "/api/dataanalysis/orderRealAnalysis/realTop"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True
