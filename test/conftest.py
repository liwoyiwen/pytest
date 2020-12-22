import pytest
import requests
import uuid
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from APIs.market import *


@pytest.fixture(scope="session",autouse=True)
def getheaders(login):
    headers={
        "Content-Type": "application/json",
        "token": login
    }
    yield headers


def getCipher(password):
    url='http://test2.shulanchina.cn/api/base/check/key'
    headers = {'Content-Type': 'application/json'}
    res=requests.get(url=url,headers=headers)
    try:

        cookie = 'SESSION=' + res.cookies['SESSION']

    except Exception:
        print("出异常了")

    print(res.json())
    publicKey=res.json()["data"]
    public_key = f'''-----BEGIN PUBLIC KEY-----
                {publicKey}
            -----END PUBLIC KEY-----'''
    rsa_key = RSA.importKey(public_key)  #传入公钥
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)  #生成对象
    cipher_text = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))

    password=cipher_text.decode('utf-8')

    return password,cookie




@pytest.fixture(scope="session",autouse=True)
def login(request):
    username="woyanan"
    password="m3nk3333"
    url = 'http://test2.shulanchina.cn/api/base/user/login'
    rsa_password, rsa_cookie = getCipher(password)
    headers = {'Content-Type': 'application/json', "Cookie": rsa_cookie}
    #headers = {'Content-Type': 'application/json'}
    params = {'accountName': username, 'password': rsa_password}
    res = requests.post(url=url, headers=headers, json=params)
    print(res.json())
    token = res.json()['data']['token']
    yield token



@pytest.fixture()
def max(request,metadata):
    print(metadata['url'])
    return request.param - 1


@pytest.fixture()
def min(request,metadata):
    print(metadata['username'])
    return request.param + 1