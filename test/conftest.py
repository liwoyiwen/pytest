import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import requests
import pytest
from conf.config import ReadConfig
from py._xmlgen import html
import time
import random

def pytest_addoption(parser):
    parser.addoption("--env", action="store",
                     default="test",
                     help="test")


@pytest.fixture(scope="session", autouse=False)
def get_envs(request):
    env = request.config.getoption("--env")
    return env


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
    cipher_text = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))
    password = cipher_text.decode('utf-8')
    return password, cookie


@pytest.fixture(scope="session", autouse=True)
def login():
    read_config = ReadConfig()
    username = read_config.get_conf("username")
    password = read_config.get_conf("password")
    base_url = read_config.get_baseUrl()
    url = base_url + '/api/base/user/login'
    rsa_password, rsa_cookie = get_cipher(password)
    headers = {'Content-Type': 'application/json', "Cookie": rsa_cookie}
    params = {'accountName': username, 'password': rsa_password}
    res = requests.post(url=url, headers=headers, json=params)
    token = res.json()['data']['token']
    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    read_config.set_conf("headers", str(headers))


@pytest.fixture()
def get_shortUrl():
    read_config = ReadConfig()
    base_url = read_config.get_baseUrl()
    url = base_url + '/api/market/plan/generateShortUrl'
    headers = read_config.get_headers()
    material_id = read_config.get_conf("materialId")
    params = {
        "materialId": material_id
    }
    res = requests.post(url=url, headers=headers, json=params)
    return res.json()['data']


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.insert(1, html.th('module'))
    cells.pop(-1)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    module_name = report.nodeid.encode('utf-8').decode("unicode_escape").split("::")[0]
    cells.insert(1, html.td(module_name))

@pytest.fixture(scope="session", autouse=True)
def get_tencent_token():
    params = {
        "timestamp": int(time.time()),
        "nonce": str(time.time()) + str(random.randint(0, 999999)),
        "client_id": 1110527770,
        "client_secret": "gjiPGP05WstMqsEB",
        "grant_type": "refresh_token",
        "authorization_code": "db0c73eeccb2bad7dd4c1aaf1c28f319",
        "redirect_uri": "https://shulanchina.cn",
        "refresh_token": "d76440d06cf38c4cec85bf67c7bbdd4a",
    }
    res = requests.get(params=params, url="https://api.e.qq.com/oauth/token")
    print(res.json())
    access_token = res.json()['data']['access_token']
    read_config = ReadConfig()

    read_config.set_conf("access_token", access_token)
