from test.myInit import MyInit
import requests
import pytest


class TestUserAnalysis(MyInit):
    def test_buy_ability(self):
        """购买力分析"""
        url = self.baseUrl + "/api/analysis/member/buyAbility"
        params = {
            "shopId": ""
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", [["consumptionRate", "consumptionPreference"],
                                       ["consumptionClass", "consumptionPeriod"],
                                       ["payAmount", "consumptionTime"],
                                       ["payLongTime", "consumptionTime"]],
                             ids=["购买成功次数/促销方式偏好", "购买商品数量/购物时间交叉分析", "实际支付金额 / 消费时段交叉分析", "支付耗时/消费时段交叉分析"])
    def test_cross_analysis(self, value):
        """购买力交叉分析图"""
        url = self.baseUrl + "/api/heart/member/crossAnalysis"
        params = {
            "shopId": None,
            "crossAnalysisLabels": value,
            "searchDays": 365,
            "labels": [],
            "rangeLabelReqs": [],
            "shopIds": []
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_life_cycle(self):
        """生命周期分析"""
        url = self.baseUrl + "/api/analysis/member/lifeCycle"
        params = {
            "shopId": ""
        }

        res = requests.get(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize('rfmType', ["4", "3", "1", "2"], ids=["RFM分析", "最后付款时间距今日", "购买频次分析F", "购买金额分析M"])
    def test_rfm_report(self, rfmType):
        """RFM分析"""
        url = self.baseUrl + "/api/analysis/RFM/findRFMReport"
        params = {
            "shopId": "",
            "rfmType": rfmType
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_repurchase_analysis(self):
        """回购分析"""
        url = self.baseUrl + "/api/dataanalysis/repurchaseDayAnalysis/queryRepurchaseDayAnalysis"
        params = {
            "shopId": 69
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_week_analysis(self):
        """购买星期分布"""
        url = self.baseUrl + "/api/dataanalysis/consumeTimeAnalysis/queryConsumeTimeByWeekAnalysis"
        params = {
            "shopId": 69
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_hour_analysis(self):
        """购买小时分布"""
        url = self.baseUrl + "/api/dataanalysis/consumeTimeAnalysis/queryConsumeTimeByHourAnalysis"
        params = {
            "shopId": 69
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_rate_analysis(self):
        """活动策略敏感度"""
        url = self.baseUrl + "/api/dataanalysis/placeOrderConvRateAnalysis/queryPlaceOrderConvRateAnalysis"
        params = {
            "shopId": 69,
            "startTime": "2021-02-17",
            "endTime": "2021-02-23",
            "goodsName": None,
            "sort": "convRate",
            "asc": 1,
            "pageSize": 10,
            "pageNumber": 1
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_down_load(self):
        """下载报表"""
        pass
