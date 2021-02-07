from test.myInit import MyInit
import requests
from decimal import Decimal
import pytest
from enums.myEnum import *
from datetime import timedelta, datetime
from common.mysql_engine import *


class TestShoppingMall(MyInit):
    def test_wallet_remaining(self):
        url = self.baseUrl + "/api/base/user/info"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        print(res.json()['data']['balance'])
        assert res.json()['data']['balance'] == get_user(self.user_id)['balance']

    def test_wallet_consumption(self):
        url = self.baseUrl + "/api/base/user/walletDetailList"

        params = {
            "pageSize": 10,
            "pageNum": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == len(get_wallet_consumption(self.user_id))

    def test_sms_remaining(self):
        url = self.baseUrl + "/api/base/tradeRecords/selectResidue"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'][0]['total'] == get_sms_remaining(self.user_id)

    def test_sms_consumption(self):
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

        assert small == get_portraitUpgrade_remaining(self.user_id, 200, 2000) + get_portraitUpgrade_remaining(self.user_id, 2000, 20000)
        assert middle == get_portraitUpgrade_remaining(self.user_id, 20000, 50000)
        assert big == get_portraitUpgrade_remaining(self.user_id, 50000, 100000)

    def test_portraitUpgrade_consumption(self):
        url = self.baseUrl + "/api/base/portraitUpgrade/calculateHistory?pageNumber=1&pageSize=10"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == len(get_portraitUpgrade_consumption(self.user_id))

    def test_app_remaining(self):
        url = self.baseUrl + "/api/base/appCircle/findNumber"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'] == get_app_remaining(self.user_id)

    def test_app_consumption(self):
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
        url = self.baseUrl + "/api/base/pay/flowPackageRemain"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'] ==get_flow_package_remaining(self.user_id)

    def test_flow_package_consumption(self):
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
        url = self.baseUrl + "/api/base/dsp/getAdvertiserFund"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_AdvertiserFund_consumption(self):
        url = self.baseUrl + "/api/base/dsp/capital/flow"
        params = {
            "pageSize": 20,
            "pageNumber": 1,
            "status": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    # @pytest.mark.parametrize("featureId", [None, 0, 2, 3, 4, 12])
    # @pytest.mark.parametrize("paymentChannel", [None, 0, 2, 4, 5, 6, 7, 8])
    @pytest.mark.skip('skip')
    @pytest.mark.parametrize("featureId", [None,
                                           Feature.portraitUpgrade.value,
                                           Feature.appCircle.value,
                                           Feature.balance.value,
                                           Feature.flowPackage.value,
                                           Feature.sms.value])
    @pytest.mark.parametrize("paymentChannel", [None,
                                                PaymentChannel.balance.value,
                                                PaymentChannel.yin_lian.value,
                                                PaymentChannel.ali_pay.value,
                                                PaymentChannel.office_gift.value,
                                                PaymentChannel.open_gift.value,
                                                PaymentChannel.person_charge.value,
                                                PaymentChannel.person_refund.value])
    @pytest.mark.parametrize("paymentStatus", [None, 'RECHARGE_SUCCESS', 'RECHARGE_FAILURE', 'RECHARGE_ING', 'REFUND'])
    @pytest.mark.parametrize("startDate",[None, datetime.strftime(datetime.now() - timedelta(days=30), '%Y-%m-%d %H:%M:%S')])
    @pytest.mark.parametrize("endDate", [None, datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')])
    def test_purchase_order(self, featureId, paymentChannel, paymentStatus, startDate, endDate):
        url = self.baseUrl + "/api/base/portraitUpgrade/purchaseQuantityHistory"
        params = {
            "startDate": startDate,
            "endDate": endDate,
            "paymentChannel": paymentChannel,
            "featureId": featureId,
            "paymentStatus": paymentStatus,
            "sort": None,
            "pageNumber": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, json=params)

        sql = f"select * from user_expenses_record where user_id={self.user_id}"
        if featureId is not None:
            sql += f" and feature_id={featureId}"
        if paymentChannel is not None:
            sql += f" and payment_channel={paymentChannel}"
        if paymentStatus is not None:
            sql += f" and payment_status='{paymentStatus}'"
        if startDate is not None:
            sql += f" and gmt_create >='{startDate}'"
        if endDate is not None:
            sql += f" and gmt_create <='{endDate}'"

        result = get_sql(sql, base)

        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == len(result)

    def test_smsPackage_list(self):
        url = self.baseUrl + "/api/base/pay/tenantSmsPackageList"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_purchase_sms(self):
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
