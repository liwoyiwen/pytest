import pytest
import requests

@pytest.fixture()
def index(request,getheaders):
    headers=getheaders
    params=request.param

    res=requests.get(url="http://test.shulanchina.cn/api/base/user/info",headers=headers)

    yield res