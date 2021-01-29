import requests
from test.myInit import MyInit


class TestIndex(MyInit):

    def test_info(self):
        res = requests.get(
            url=self.baseUrl + "/api/base/user/info",
            headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_message(self):
        params = {
            "pageNumber": 1,
            "pageSize": 20,
            "remainWay": "STRONG",
            "hasRead": "NO"
        }
        res = requests.post(url=self.baseUrl + "/api/base/message/list",
                            headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_judgeAllHasRead(self):
        res = requests.get(
            url=self.baseUrl + "/api/base/message/judgeAllHasRead",
            headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_shopList(self):
        res = requests.get(
            url=self.baseUrl + "/api/base/shop/list",
            headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_01(self):
        print(self.headers)
