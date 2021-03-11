from test.myInit import MyInit
import requests


class TestPreSales(MyInit):
    def test_forecast_analysis(self):
        """当年销售额全年预测"""
        url = self.baseUrl + "/api/dataanalysis/annualSalesForecastAnalysis/queryYearAnnualSalesForecastAnalysis"
        params = {
            "shopId": 69,

        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_buy_frequency(self):
        """各购买频次对应销售贡献比 && 年度各购买频次对应销售贡献比"""
        url = self.baseUrl + "/api/dataanalysis/salesForecast/buyFrequencySalesRate"
        params = {
            "shopId": 69
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_buy_frequency(self):
        """新客各购买频次对应销售贡献比&&老客各购买频次对应销售贡献比"""
        url = self.baseUrl + "/api/dataanalysis/salesForecast/newOldCustomerBuyFrequencySalesRate"
        params = {
            "shopId": 69
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_frequency_analysis(self):
        """客户粘性分析"""
        url = self.baseUrl + "/api/dataanalysis/purchaseFrequencyAnalysis/queryPurchaseFrequencyAnalysis"
        params = {
            "shopId": 69
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_goods_rank(self):
        """全量商品排行榜"""
        url = self.baseUrl + "/api/dataanalysis/salesForecast/commodityList"
        params = {
            "shopId": 69,
            "startTime": None,
            "endTime": None,
            "sortField": "orderCustomer",
            "ascRule": 0,
            "pageSize": 10,
            "pageNumber": 1
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_new_and_old_customers(self):
        """新老客趋势图"""
        url = self.baseUrl + "/api/dataanalysis/newAndOldBuyerPersonNumTrend/queryNewAndOldBuyerPersonNumTrend"
        params = {
            "shopId": 69,

        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_new_and_old_price(self):
        """新老客客单价"""
        url = self.baseUrl + "/api/dataanalysis/newAndOldBuyerUnitPriceTrend/queryNewAndOldBuyerUnitPriceTrend"
        params = {
            "shopId": 69,

        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_frequency_analysis(self):
        """客户粘性分析"""
        url = self.baseUrl + "/api/dataanalysis/purchaseFrequencyAnalysis/queryPurchaseFrequencyAnalysis"
        params = {
            "shopId": 69,

        }

        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True
