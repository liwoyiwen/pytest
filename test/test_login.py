from common.read_data import *
import pytest
import requests
from test.conftest import getCipher
from test.myInit import MyInit


class TestLogin(MyInit):
    datas = get_excel(filename="login_data.xls", sheetName="login_data", converters={"password": getCipher},
                      dtype={"accountName": str})

    @pytest.mark.parametrize("value", datas)
    def test_login(self, value):

        Expectation = value['Expectation']

        url = self.baseUrl + '/api/base/user/login'
        params = {
            'accountName': value["accountName"],
            'password': value["password"][0]

        }
        headers = {
            'Content-Type': 'application/json',
            "Cookie": value["password"][1]
        }
        res = requests.post(url=url, headers=headers, json=params)
        print(res.json())
        if Expectation != '':
            assert res.json()['msg'] == Expectation
        else:
            res.json()['success'] == True
