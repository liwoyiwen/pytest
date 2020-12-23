import pytest
import requests
class TestIndex:
    def test_info(self,getheaders):
        res = requests.get(
            url="http://test.shulanchina.cn/api/base/user/info",
            headers=getheaders)
        assert res.status_code==200
        assert res.json()['status']==0



    @pytest.mark.parametrize("params",[
        {
            "pageNumber":1,
            "pageSize":20,
            "remainWay":"STRONG",
            "hasRead":"NO"
        }
    ])
    def test_message(self,getheaders,params):
        res = requests.post(url="http://test.shulanchina.cn/api/base/message/list",
                            headers=getheaders, json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0





    def test_judgeAllHasRead(self,getheaders):
        res = requests.get(
            url="http://test.shulanchina.cn/api/base/message/judgeAllHasRead",
            headers=getheaders)
        assert res.status_code == 200
        assert res.json()['status'] == 0


    def test_shoplist(self,getheaders):
        res = requests.get(
            url="http://test.shulanchina.cn/api/base/shop/list",
            headers=getheaders)
        assert res.status_code == 200
        assert res.json()['status'] == 0
