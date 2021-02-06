from test.myInit import MyInit
import requests


class TestRealAnalysis(MyInit):
    def test_real_survey(self):
        url = self.baseUrl + "/api/dataanalysis/orderRealAnalysis/realSurvey"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_real_trend(self):
        url = self.baseUrl + "/api/dataanalysis/orderRealAnalysis/realTrend"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_real_top(self):
        url = self.baseUrl + "/api/dataanalysis/orderRealAnalysis/realTop"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True
