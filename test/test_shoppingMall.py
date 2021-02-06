from test.myInit import MyInit
import requests
from common.read_data import *
from decimal import Decimal
import pytest
from enums.myEnum import *
from datetime import timedelta, datetime


class TestShoppingMall(MyInit):
    def test_wallet_remaining(self):
        url = self.baseUrl + "/api/base/user/info"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        print(res.json()['data']['balance'])
        assert res.json()['data']['balance'] == \
               get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]

    def test_wallet_consumption(self):
        url = self.baseUrl + "/api/base/user/walletDetailList"

        params = {
            "pageSize": 10,
            "pageNum": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == get_sql(
            f"select count(id) as total from wallet_detail where user_id={self.user_id} ORDER BY create_time desc", base)[0]['total']

    def test_sms_remaining(self):
        url = self.baseUrl + "/api/base/tradeRecords/selectResidue"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'][0]['total'] == get_sql(
            f"select sum(amount+gifts) as sms_remaining from user_sms_remaining where user_id={self.user_id}", base)[0]['sms_remaining']

    def test_sms_consumption(self):
        url = self.baseUrl + "/api/base/fundLog/queryConsumptionRecords"

        params = {
            "pageSize": 10,
            "pageNum": 1
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == get_sql(
            f"select count(consumption_id) as total from (select consumption_id, operate_time, sum(pre_pay_sms_num) 预计消费, sum(sms_amount) 实际消费 from fund_consumption_log where user_id={self.user_id} GROUP BY consumption_id  ORDER BY operate_time desc) as a", base)[0]['total']

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

        assert small == get_sql(
            f"select total_remaining from user_calculated_quantity where (start=2000 and end=20000)  and user_id={self.user_id}", base)[0]["total_remaining"]
        assert middle == get_sql(
            f"select total_remaining from user_calculated_quantity where start=20000 and end=50000 and user_id={self.user_id}", base)[0]["total_remaining"]

        assert big == get_sql(
            f"select total_remaining from user_calculated_quantity where start=50000 and end=100000 and user_id={self.user_id}", base)[0]["total_remaining"]

    def test_portraitUpgrade_consumption(self):
        url = self.baseUrl + "/api/base/portraitUpgrade/calculateHistory?pageNumber=1&pageSize=10"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == get_sql(
            f"select count(id) as total from user_consumer_record where user_child_id={self.user_id} and feature_id=0", base)[0]["total"]

    def test_app_remaining(self):
        url = self.baseUrl + "/api/base/appCircle/findNumber"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'] == \
               get_sql(f"select * from app_sms_remaining where user_id={self.user_id}", base)[0][
                   'total_remaining']

    def test_app_consumption(self):
        url = self.baseUrl + "/api/base/appCircle/findDetail"
        params = {
            "pageSize": 10,
            "pageNum": 1
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['total'] == get_sql(
            f"select count(id) as total from user_consumer_record where user_child_id={self.user_id} and feature_id=2", base)[0][
            'total']

    def test_flowPackage_remaining(self):
        url = self.baseUrl + "/api/base/pay/flowPackageRemain"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data'] == \
               get_sql(f"select * from flow_package_remaining where user_id={self.user_id}", base)[0][
                   'total_remain']

    def test_flowPack_consumption(self):
        url = self.baseUrl + "/api/base/pay/flowPackageDetails"
        params = {
            "pageNumber": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, params=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        assert res.json()['data']['totalCount'] == get_sql(
            f"select count(id) as total from user_consumer_record where user_child_id={self.user_id} and feature_id in (8,9,11)", base)[0]['total']

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
    @pytest.mark.parametrize("startDate",
                             [None, datetime.strftime(datetime.now() - timedelta(days=30), '%Y-%m-%d %H:%M:%S')])
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
        balance_before = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
        sms_before = get_sql(f"select sum(amount+gifts) as sms_remaining from user_sms_remaining where user_id={self.user_id}", base)[0]['sms_remaining']
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
        balance_after = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
        sms_after = get_sql(f"select sum(amount+gifts) as sms_remaining from user_sms_remaining where user_id={self.user_id}", base)[0]['sms_remaining']

        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount']))

        assert sms_after - sms_before == 10000

    def test_purchase_portraitUpgrade(self):
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]

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
        package = get_sql(f"select * from price_list where id={params['payRequest']['priceListId']}", base)[0]
        total_remaining_before = get_sql(
            f"select * from user_calculated_quantity where user_id={self.user_id} and start={package['start']} and end={package['end']}", base)[0]['total_remaining']

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        balance_after = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
        total_remaining_after = get_sql(
            f"select * from user_calculated_quantity where user_id={self.user_id} and start={package['start']} and end={package['end']}", base)[0]['total_remaining']

        assert total_remaining_after - total_remaining_before == 1, "画像升级包新增失败"
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount'])), "余额扣减失败"

    def test_purchase_appCirle(self):
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
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

        package = get_sql(f"select * from price_list where id={params['payRequest']['priceListId']}", base)[0]
        total_remaining_before = get_sql(f"select * from app_sms_remaining where user_id={self.user_id}", base)[0][
            "total_remaining"]

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        balance_after = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
        total_remaining_after = get_sql(f"select * from app_sms_remaining where user_id={self.user_id}", base)[0][
            "total_remaining"]
        assert total_remaining_after - total_remaining_before == package['number'], "app新增失败"
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount'])), "余额扣减失败"

    def test_purchase_flowPackage(self):
        url = self.baseUrl + "/api/base/basePay/total"
        balance_before = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
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

        package = get_sql(f"select * from price_list where id={params['payRequest']['priceListId']}", base)[0]
        total_remaining_before = get_sql(f"select * from flow_package_remaining where user_id={self.user_id}", base)[0][
            "total_remain"]

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0
        balance_after = get_sql(f"select balance from user where id={self.user_id}", base)[0]["balance"]
        total_remaining_after = get_sql(f"select * from flow_package_remaining where user_id={self.user_id}", base)[0][
            "total_remain"]
        assert total_remaining_after - total_remaining_before == package['number'], "精准流量包新增失败"
        assert Decimal(str(balance_before)) - Decimal(str(balance_after)) == Decimal(str(params['payAmount']))
