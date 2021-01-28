import time
import pytest
import random
import requests
import json
from conf.config import *

@pytest.fixture(scope='session')
def get_token():
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
    access_token=res.json()['data']['access_token']
    read_config=Read_config("tecent")

    read_config.set_conf("access_token",access_token)






@pytest.fixture()
def createPlan(get_token,request):
    common_params = {
        "timestamp": int(time.time()),
        "nonce": str(time.time()) + str(random.randint(0, 999999)),
        "access_token": get_token
    }

    '''
    parameters={
        "account_id": self.account_id,
        "campaign_name": getName("广告计划ljf"),
        "campaign_type": "CAMPAIGN_TYPE_NORMAL",
        "promoted_object_type": "PROMOTED_OBJECT_TYPE_ECOMMERCE",
        "daily_budget": 10000,
        "configured_status": "AD_STATUS_NORMAL",
        "speed_mode": "SPEED_MODE_STANDARD"
    }




    '''
    parameters=request.param
    print(parameters)
    for k in parameters:
        if type(parameters[k]) is not str:
            parameters[k] = json.dumps(parameters[k])
    res = requests.post(url="https://api.e.qq.com/v1.1//campaigns/add", params=common_params, data=parameters)
    print(res.json())
    return res.json()['data']['campaign_id']
