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

if __name__=='__main__':
    pytest.main(['-s','test_index.py'])