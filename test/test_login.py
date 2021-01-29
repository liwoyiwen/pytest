from common.read_data import *
import pytest
import requests
from test.conftest import get_cipher
from test.myInit import MyInit


class TestLogin(MyInit):
    login_data = get_excel(filename="login_data.xls", sheetName="login_data", converters={"password": get_cipher},
                      dtype={"accountName": str})

    @pytest.mark.parametrize("value",login_data)
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
