from test.myInit import MyInit
import requests


class TestGlobal(MyInit):
    def test_user_info(self):
        """获取用户详情"""
        url = self.baseUrl + "/api/base/user/info"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_message_list(self):
        """消息列表"""
        url = self.baseUrl + "/api/base/message/list"
        params = {
            "pageNumber": 1,
            "pageSize": 20,
            "remainWay": "STRONG",
            "hasRead": "NO"
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_message_judgeAllHasRead(self):
        """消息列表小红点"""
        url = self.baseUrl + "/api/base/message/judgeAllHasRead"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_shop_list(self):
        """店铺列表"""
        url = self.baseUrl + "/api/base/shop/list"
        res = requests.get(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_permission_userJurisdiction(self):
        """获取用户是否是自定义数量包用户"""
        url = self.baseUrl + "/api/base/permission/userJurisdiction"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_updateNoviceStatus(self):
        """更新新手导航状态"""
        url = self.baseUrl + "/api/base/user/updateNoviceStatus"
        res = requests.post(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_message_detail(self):
        """消息详情"""
        url = self.baseUrl + "/api/base/message/detail/2805"
        res = requests.get(url=url, headers=self.headers)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_logout(self):
        """退出登录"""
        url = self.baseUrl + "/api/base/user/logout"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True
