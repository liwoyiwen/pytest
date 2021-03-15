import requests
from test.myInit import MyInit
import json

class TestIndex(MyInit):
    """首页"""


    def test_advert_list(self):
        """广告投放列表"""
        url=self.baseUrl+"/api/market/advertMerge/advert"
        res=requests.post(url=url,headers=self.headers)
        print(json.dumps(res.json(),indent=4))
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_smslog_list(self):
        """短信投放列表"""
        url=self.baseUrl+"/api/market/smslog/list"
        params={
            "startDate":None,
            "endDate":None,
            "planName":None,
            "type":None,
            "shopId":0,
            "timeRange":"RECENTLY_THIRTY_DAY",
            "pageSize":5,
            "pageNum":1
        }
        res = requests.post(url=url, headers=self.headers,json=params)
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_front_list(self):
        """店铺动态"""
        url=self.baseUrl+"/api/analysis/front/list"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['status'] == 0




    def test_send_message(self):
        url="https://oapi.dingtalk.com/robot/send?access_token=90e7b9510b2e05789c8ae9f6464b30c3babd22fba0fb53b55848b98e0ea066b2"
        headers={
            "Content-Type":"application/json;charset=utf-8"

        }

        message={
            "msgtype":"text",
            "text":{
                "content":"test"+":hello"
            },
            "at":{
                "atMobiles":[
                    "18616753564"
                ],
                "isAtAll":0

            }
        }

        res=requests.post(url=url,data=json.dumps(message),headers=headers)
        print(res.json())



    def test_send_link(self):
        url = "https://oapi.dingtalk.com/robot/send?access_token=90e7b9510b2e05789c8ae9f6464b30c3babd22fba0fb53b55848b98e0ea066b2"
        headers = {
            "Content-Type": "application/json;charset=utf-8"

        }

        message = {
            "msgtype": "link",
            "link": {
                "text": "test",
                "title":"title",
                "picurl":"http://www.baidu.cn",
                "messageUrl":"http://www.baidu.cn"
            },
            "at": {
                "atMobiles": [
                    "18616753564"
                ],
                "isAtAll": 0

            }
        }

        res = requests.post(url=url, data=json.dumps(message), headers=headers)
        print(res.json())

if __name__=='__main__':
  ytest.main(['-s','test_index.py'])