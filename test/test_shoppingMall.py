from test.myInit import MyInit
import requests
from decimal import Decimal
import pytest
from enums.myEnum import *
from datetime import timedelta, datetime
from common.mysql_engine import *


class TestShoppingMall(MyInit):
    purchase_order_data = get_excel(filename='shoppingMall_data.xls', sheetName='purchase_order',
                                    converters={
                                        "startDate": lambda x: datetime.strftime(x,
                                                                                 "%Y-%m-%d %H:%M:%S") if x != '' else '',
                                        "endDate": lambda x: datetime.strftime(x,
                                                                               "%Y-%m-%d %H:%M:%S") if x != '' else '',
                                        'sql': lambda x: x.strip().replace('%', '%%')
                                    })

    def test_wallet_remaining(self):
        """获取钱包余额"""
        url = self.baseUrl + "/api/base/user/info"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        print(res.json()['data']['balance'])
        assert res.json()['data']['balance'] == get_user(self.user_id)['balance']

    def test_wallet_consumption(self):
        """获取钱包消费记录"""
        url = self.baseUrl + "/api/base/user/walletDetailList"

        params = {
            "pageSize": 10,
            "pageNum": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == len(get_wallet_consumption(self.user_id))

    def test_sms_remaining(self):
        """获取剩余短信条数"""
        url = self.baseUrl + "/api/base/tradeRecords/selectResidue"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'][0]['total'] == get_sms_remaining(self.user_id)

    def test_sms_consumption(self):
        """获取短信消费记录"""
        url = self.baseUrl + "/api/base/fundLog/queryConsumptionRecords"

        params = {
            "pageSize": 10,
            "pageNum": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == len(get_sms_consumption(self.user_id))

    def test_portraitUpgrade_remaining(self):
        """获取画像升级剩余条数"""
        url = self.baseUrl + "/api/base/portraitUpgrade/userAccount"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        small = 0
        middle = 0
        big = 0
        for item in res.json()['data']:
            if item["start"] == 200 and item["end"] == 2000:
                small = + item["totalRemaining"]
            elif item["start"] == 2000 and item["end"] == 20000:
                small = + item["totalRemaining"]
            elif item["start"] == 20000 and item["end"] == 50000:
                middle = + item["totalRemaining"]
            elif item["start"] == 50000 and item["end"] == 100000:
                big = + item["totalRemaining"]

        assert small == get_portraitUpgrade_remaining(self.user_id, 200, 2000) + get_portraitUpgrade_remaining(
            self.user_id, 2000, 20000)
        assert middle == get_portraitUpgrade_remaining(self.user_id, 20000, 50000)
        assert big == get_portraitUpgrade_remaining(self.user_id, 50000, 100000)

    def test_portraitUpgrade_consumption(self):
        """获取画像升级消费记录"""
        url = self.baseUrl + "/api/base/portraitUpgrade/calculateHistory?pageNumber=1&pageSize=10"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == len(get_portraitUpgrade_consumption(self.user_id))

    def test_app_remaining(self):
        """获取app 圈人剩余条数"""
        url = self.baseUrl + "/api/base/appCircle/findNumber"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'] == get_app_remaining(self.user_id)

    def test_app_consumption(self):
        """获取app 圈人消费记录"""
        url = self.baseUrl + "/api/base/appCircle/findDetail"
        params = {
            "pageSize": 10,
            "pageNum": 1
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == len(get_app_consumption(self.user_id))

    def test_flow_package_remaining(self):
        """获取精准流量包剩余量"""
        url = self.baseUrl + "/api/base/pay/flowPackageRemain"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'] == get_flow_package_remaining(self.user_id)

    def test_flow_package_consumption(self):
        """精准流量包消费记录"""
        url = self.baseUrl + "/api/base/pay/flowPackageDetails"
        params = {
            "pageNumber": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == len(get_flow_package_consumption(self.user_id))

    def test_getAdvertiserFund(self):
        """获取广告余额"""
        url = self.baseUrl + "/api/base/dsp/getAdvertiserFund"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_AdvertiserFund_consumption(self):
        """获取广告余额消费记录"""
        url = self.baseUrl + "/api/base/dsp/capital/flow"
        params = {
            "pageSize": 20,
            "pageNumber": 1,
            "status": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", purchase_order_data, ids=[i['case_name'] for i in purchase_order_data])
    def test_purchase_order(self, value):

        """获取购买记录"""
        url = self.baseUrl + "/api/base/portraitUpgrade/purchaseQuantityHistory"
        params = {
            "startDate": value['startDate'],
            "endDate": value['endDate'],
            "paymentChannel": value['paymentChannel'],
            "featureId": value['featureId'],
            "paymentStatus": value['paymentStatus'],
            "sort": None,
            "pageNumber": 1,
            "pageSize": 10
        }
        print(params)
        res = requests.post(url=url, headers=self.headers, json=params)

        sql = f"select * from user_expenses_record where user_id={self.user_id}"
        if value['featureId'] != '':
            sql += f" and feature_id={value['featureId']}"
        if value['paymentChannel'] != '':
            sql += f" and payment_channel={value['paymentChannel']}"
        if value['paymentStatus'] != '':
            sql += f" and payment_status='{value['paymentStatus']}'"
        if value['startDate'] != '':
            sql += f" and gmt_create >='{value['startDate']}'"
        if value['endDate'] != '':
            sql += f" and gmt_create <='{value['endDate']}'"

        result = get_sql(sql, base)

        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == len(result)

    def test_purchase_sms(self):
        """购买短信包"""
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_user(self.user_id)['balance']
        sms_before = get_sms_remaining(self.user_id)
        params = {
            "button": True,
            "featureId": 3,
            "payType": 4,
            "payAmount": "0.01",
            "payRequest":
                {
                    "smsPackageId": 1,
                    "payPassword": "user11"
                }
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        balance_after = get_user(self.user_id)['balance']
        sms_after = get_sms_remaining(self.user_id)
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount']))


        assert sms_after - sms_before == 10000

    def test_purchase_portraitUpgrade(self):
        """购买画像升级包"""
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_user(self.user_id)['balance']

        params = {
            "button": True,
            "featureId": 0,
            "payType": 4,
            "payAmount": "0.01",
            "payRequest":
                {
                    "priceListId": 2,
                    "payPassword": "user11"
                }
        }
        package = get_price(params['payRequest']['priceListId'])

        total_remaining_before = get_portraitUpgrade_remaining(self.user_id, package['start'], package['end'])

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        balance_after = get_user(self.user_id)['balance']
        total_remaining_after = get_portraitUpgrade_remaining(self.user_id, package['start'], package['end'])

        assert total_remaining_after - total_remaining_before == 1, "画像升级包新增失败"
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount'])), "余额扣减失败"

    def test_purchase_appCirle(self):
        """购买app圈人包"""
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_user(self.user_id)['balance']
        params = {
            "button": True,
            "featureId": 2,
            "payType": 4,
            "payAmount": "0.01",
            "payRequest":
                {
                    "priceListId": 17,
                    "payPassword": "user11"
                }
        }

        package = get_price(params['payRequest']['priceListId'])
        total_remaining_before = get_app_remaining(self.user_id)

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

        balance_after = get_user(self.user_id)['balance']
        total_remaining_after = get_app_remaining(self.user_id)
        assert total_remaining_after - total_remaining_before == package['number'], "app新增失败"
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount'])), "余额扣减失败"

    def test_purchase_flowPackage(self):
        """购买精准流量包"""
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_user(self.user_id)['balance']
        params = {
            "button": True,
            "featureId": 12,
            "payType": 4,
            "payAmount": "0.01",
            "payRequest":
                {
                    "priceListId": 240,
                    "payPassword": "user11"
                }
        }

        package = get_price(params['payRequest']['priceListId'])
        total_remaining_before = get_flow_package_remaining(self.user_id)
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        balance_after = get_user(self.user_id)['balance']
        total_remaining_after = get_flow_package_remaining(self.user_id)
        assert total_remaining_after - total_remaining_before == package['number'], "精准流量包新增失败"
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount']))

    def test_sms_package(self):
        """获取短信包列表"""
        url = self.baseUrl + "/api/base/pay/tenantSmsPackageList"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_portraitUpgrade_package(self):
        """获取画像升级包列表"""
        url = self.baseUrl + "/api/base/portraitUpgrade/priceList"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_app_package(self):
        """获取app 圈人包列表"""
        url = self.baseUrl + "/api/base/appCircle/appPurchaseList"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_flow_package(self):
        """获取精装流量包列表"""
        url = self.baseUrl + "/api/base/pay/flowPackageList"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_dsp_package(self):
        """获取广告包列表"""
        url = self.baseUrl + "/api/base/user/getRechargeAmountList?featureId=5"
        res = requests.post(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_check_order_status(self):
        """获取订单支付状态"""
        url = self.baseUrl + "/api/base/portraitUpgrade/checkOrderPaymentStatus?orderNumber=SL80255714"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
