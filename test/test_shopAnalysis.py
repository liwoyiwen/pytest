from test.myInit import MyInit
import requests


class TestShopAnalysis(MyInit):
    def test_totalComparisonOfYears(self):
        """年份总对比"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/totalComparisonOfYears"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_MonthlySales(self):
        """月销售额同比"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/yoyMonthlySales"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_monthlyPaymentConversionRatio(self):
        """月新老客支付转化对比"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/monthlyPaymentConversionRatio"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_yearNewAndOld(self):
        """年新老客对比"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/yearNewOldCustSplitChart"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_monthNewAndOld(self):
        """月新老客对比"""
        url = self.baseUrl + "/api/dataanalysis/newAndOldCustomers/monthNewAndOldGuests"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_regionalTurnover(self):
        """各省份同比"""

        url = self.baseUrl + "/api/dataanalysis/newAndOldCustomers/regionalTurnover"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_repurchaseValueForProvince(self):
        """各省份复购价值指数"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/repurchaseValueForProvince"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_firstOrderAndRepurchaseRate(self):
        """新客首笔客单价"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/firstOrderAndRepurchaseRate"
        params = {
            "shopId": 70
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_paymentAmountRanking(self):
        """月高精准度排行榜--付款金额排行"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/paymentAmountRanking"
        params = {
            "shopId": 70,
            "statisticalDimension": "0",
            "payStartTime": "2021-01-29",
            "payEndTime": "2021-02-04",
            "excludeRefunds": "1",
            "interceptionPeopleCount": 5000,
            "pageNumber": 1,
            "pageSize": 10,
            "excludeOrderAmount": 0
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_numberOfPaymentsRanking(self):
        """月高精准度排行榜--付款件数排行"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/numberOfPaymentsRanking"
        params = {
            "shopId": 70,
            "statisticalDimension": "0",
            "payStartTime": "2021-01-29",
            "payEndTime": "2021-02-04",
            "excludeRefunds": "1",
            "interceptionPeopleCount": 5000,
            "pageNumber": 1,
            "pageSize": 10,
            "excludeOrderAmount": 0,
            "excludeOrderNumber": 0
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_topPaymentTimeRanking(self):
        """月高精准度排行榜--付款时间排行"""
        url = self.baseUrl + "/api/dataanalysis/shopAnalysis/topPaymentTimeRanking"
        params = {
            "shopId": 70,
            "productName": "",
            "payStartTime": "2021-01-29",
            "payEndTime": "2021-02-04",
            "excludeRefunds": "1",
            "interceptionPeopleCount": 5000,
            "pageNumber": 1,
            "pageSize": 10,
            "excludeOrderAmount": 0,
            "numberOfSingleOrdersNumberStart": None,
            "numberOfSingleOrdersNumberEnd": None
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] is True
