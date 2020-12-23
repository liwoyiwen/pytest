import pytest
import requests

@pytest.fixture()
def index(request,getheaders):
    headers=getheaders
    params=request.param

    res=requests.get(url="http://test.shulanchina.cn/api/base/user/info",headers=headers)

    yield res

@pytest.fixture()
def info(getheaders):
    """ 获取用户信息"""
    res=requests.get(
        url="http://test.shulanchina.cn/api/base/user/info",
        headers=getheaders)

    yield res


@pytest.fixture()
def message(request, getheaders):

    """ 获取消息列表"""

    res=requests.post(url="http://test.shulanchina.cn/api/base/message/list",
        headers=getheaders,json=request.param)


    yield res


@pytest.fixture()
def judgeAllHasRead(getheaders):
    """ 首页小红点"""
    res = requests.get(
        url="http://test.shulanchina.cn/api/base/message/judgeAllHasRead",
        headers=getheaders)
    yield res



@pytest.fixture()
def shoplist(getheaders):
    """ 店铺列表"""
    res=requests.get(
        url="http://test.shulanchina.cn/api/base/shop/list",
        headers=getheaders)
    yield res

