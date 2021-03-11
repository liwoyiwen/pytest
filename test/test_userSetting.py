from common.read_data import get_excel
import pytest
import requests
from test.myInit import MyInit
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from conf.config import ReadConfig


class TestUserSetting(MyInit):
    password_update_data = get_excel(filename="login_data.xls", sheetName="password_update")
    base_update_data = get_excel(filename="login_data.xls", sheetName="base_update")
    pay_password_update_data = get_excel(filename="login_data.xls", sheetName="pay_password_update")

    @pytest.mark.parametrize('value', base_update_data)
    def test_base_update(self, value):
        """基础信息修改"""
        url = self.baseUrl + '/api/base/user/update'
        params = {
            "name": value['name'],
            "companyName": value['companyName'],
            "phoneNumber": value['phoneNumber']
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            res.json()['msg'] == value['msg']

    @pytest.mark.parametrize('value', pay_password_update_data)
    def test_pay_password_update(self, value):
        """支付密码修改"""
        url = self.baseUrl + '/api/base/user/updatePayPassword'
        params = {
            "type": value['type'],
            "password": value['password'],
            "newPassword": value['newPassword']
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            res.json()['msg'] == value['msg']

    @pytest.mark.parametrize("value", password_update_data)
    def test_password_update(self, value):
        """密码修改"""
        url = self.baseUrl + "/api/base/user/updatePassword"
        old_password, new_password, confirm_password, cookie = self.get_cipher1(value['oldPassword'],
                                                                                value['newPassword'],
                                                                                value['updatePasswordReq'])
        params = {
            "oldPassword": old_password,
            "newPassword": new_password,
            "updatePasswordReq": confirm_password
        }
        headers = self.headers
        headers.update({"cookie": cookie})
        print(headers)
        res = requests.post(url=url, headers=headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == value['success']
        if value['msg'] != '':
            assert res.json()['msg'] == value['msg']

    def test_isExistPayPassword(self):
        """判断是否存在支付密码"""
        url = self.baseUrl + "/api/base/user/isExistPayPassword"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] is True

    @staticmethod
    def get_cipher1(old_password, new_password, confirm_password):
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
        cipher_text1 = base64.b64encode(cipher.encrypt(old_password.encode(encoding="utf-8")))
        cipher_text2 = base64.b64encode(cipher.encrypt(new_password.encode(encoding="utf-8")))
        cipher_text3 = base64.b64encode(cipher.encrypt(confirm_password.encode(encoding="utf-8")))

        old = cipher_text1.decode('utf-8')
        new = cipher_text2.decode('utf-8')
        confirm = cipher_text3.decode('utf-8')
        return old, new, confirm, cookie
