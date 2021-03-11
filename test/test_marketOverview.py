from test.myInit import MyInit
import requests


class TestMarketOverview(MyInit):
    def test_select_chanel(self):
        """根据店铺获取授权渠道"""
        url = self.baseUrl + "/api/base/shop/selectAdvertChannelByShop"
        params = {
            "shopId": 660
        }
        res = requests.post(url=url, params=params, headers=self.headers)

        assert res.status_code == 200
        assert res.json()['status'] == 0
