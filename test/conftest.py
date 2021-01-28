
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from APIs.sms import *
from conf.config import Read_config
import os

def pytest_addoption(parser):
    parser.addoption("--env",action="store",
                     default="test",
                     help="test")

@pytest.fixture(scope="session",autouse=False)
def get_envs(request):
    env=request.config.getoption("--env")
    return env



def getCipher(password):
    url='http://test2.shulanchina.cn/api/base/check/key'
    headers = {'Content-Type': 'application/json'}
    res=requests.get(url=url,headers=headers)
    try:

        cookie = 'SESSION=' + res.cookies['SESSION']

    except Exception:
        print("出异常了")

    publicKey=res.json()["data"]
    public_key = f'''-----BEGIN PUBLIC KEY-----
                {publicKey}
            -----END PUBLIC KEY-----'''
    rsa_key = RSA.importKey(public_key)  #传入公钥
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)  #生成对象
    cipher_text = base64.b64encode(cipher.encrypt(password.encode(encoding="utf-8")))

    password=cipher_text.decode('utf-8')
    return password,cookie



@pytest.fixture(scope="session",autouse=False)
def login(get_envs):
    os.environ['--env']=get_envs
    read_config = Read_config(get_envs)
    username = read_config.get_conf("username")
    password = read_config.get_conf("password")
    baseUrl=read_config.get_baseUrl()
    url = baseUrl+'/api/base/user/login'
    rsa_password, rsa_cookie = getCipher(password)
    headers = {'Content-Type': 'application/json', "Cookie": rsa_cookie}
    params = {'accountName': username, 'password': rsa_password}
    res = requests.post(url=url, headers=headers, json=params)
    token = res.json()['data']['token']
    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    read_config.set_conf("headers", str(headers))




