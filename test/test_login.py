from common.read_data import get_excel
import pytest
import requests
from test.myInit import MyInit
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from conf.config import ReadConfig


class TestLogin(MyInit):
    login_data = get_excel(filename="login_data.xls", sheetName="login_data", dtype={"accountName": str})
    verification_code_data = get_excel(filename="login_data.xls", sheetName="verification_code", dtype={"mobile": str})

    @pytest.mark.parametrize("value", login_data)
    def test_login(self, value):
        """登录"""
        password, cookie = self.get_cipher(value['password'])

        url = self.baseUrl + '/api/base/user/login'
        params = {
            'accountName': value["accountName"],
            'password': password

        }
        headers = {
            'Content-Type': 'application/json',
            "Cookie": cookie
        }
        res = requests.post(url=url, headers=headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            assert res.json()['msg'] == value['msg']

    @staticmethod
    def get_cipher(password):
        read_config = ReadConfig()
        base_url = read_config.get_baseUrl()
        url = base_url + '/api/base/check/key'

        headers = {'Content-Type': 'application/json'}
        res = requests.get(url=url, headers=headers)
        cookie = 'SESSION=' + res.cookies['SESSION']
        public_key = f'''-----BEGIN PUBLIC KEY-----
                        {res.json()["data"]}
                    -----END PUBLIC KEY-----'''
        rsa_key = RSA.importKey(public_key)  # 传入公钥
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)  # 生成对象
        cipher_text1 = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))
        password = cipher_text1.decode('utf-8')

        return password, cookie

    @pytest.mark.parametrize("value", verification_code_data)
    def test_send_code(self, value):
        """发送验证码"""
        url = self.baseUrl + "/api/base/user/getVerification"
        param = {
            "mobile": value['mobile']
        }

        res = requests.post(url=url, headers=self.headers, params=param)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            assert res.json()['msg'] == value['msg']

    def test_get_key(self):
        """获取key码"""
        url = self.baseUrl + "/api/base/check/key"
        res = requests.get(url=url)
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_set_password(self):
        """设置密码"""
        url = self.baseUrl + "/api/base/user/setPassword"
        password, cookie = self.get_cipher("m3nk3333")
        headers = {
            'Content-Type': 'application/json',
            "Cookie": cookie
        }
        params = {
            "id": 426,
            "password": password

        }
        res = requests.post(url=url, headers=headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] is True

    def test_code_login(self):
        """验证码登录"""
        url = self.baseUrl + "/api/base/user/verificationCodeLogin"
        params = {
            "mobile": 18866666666,
            "code": 1120
        }
        res = requests.post(url=url, params=params)
        assert res.status_code == 200
        assert res.json()['success'] is True
