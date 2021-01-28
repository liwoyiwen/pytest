# -*- coding: UTF-8 -*-

import pytest
import requests
from common.read_data import *
import time as t

from common.mysql_engine import *
from test.myInit import *

class TestTencent(MyInit):

    datas = get_excel(filename='dsp_data.xls', sheetName="ad_data", converters={"materialName": getName})
    search_advert_datas=get_excel(filename='dsp_data.xls', sheetName="search_advert",converters={
        "sql":lambda x: x.strip().replace('%', '%%')
    })

    search_adMaterial_datas=get_excel(filename='dsp_data.xls', sheetName="search_adMaterial",converters={
        "sql":lambda x: x.strip().replace('%', '%%')
    })

    search_popularizePage_datas=get_excel(filename="dsp_data.xls",sheetName="search_popularizePage",converters={
        "sql":lambda x: x.strip().replace('%', '%%'),
        "startDate": lambda x:datetime.strftime(x,"%Y-%m-%d %H:%M:%S") if x!='' else '',
        "endDate":lambda x:datetime.strftime(x,"%Y-%m-%d %H:%M:%S") if x!='' else ''

    })





    @pytest.mark.parametrize("value",datas)
    def test_addAd(self,value):
        print(value)
        advert_params={
            "shopId": TestTencent.shopId,
            "putMedia": value['putMedia'],
            "paymentType": value['paymentType'],
            "advertSpace": str(value['advertSpace']),
            "advertSpaceName": value['advertSpaceName'],
            "launchPeople": self.launchPeople,
            "peoplePackageName": self.peoplePackageNumber,
            "peoplePackageNumber": self.peoplePackageNumber,
            "launchMode": value['launchMode'],
            "launchStartTime": getDate1(3),
            "launchEndTime": None,
            "launchTimeInterval": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            "launchTimeInfo": "不限",
            "directUrl": None,
            "totalAdvertBudget": "500",
            "singlePrice": "50",
            "advertName": getName("ljf-2"),
            "optimizeTarget": value['optimizeTarget'],
            "skpiType": value['skpiType'],
            "popularizeId": value['popularizeId'],
            "fallUrl": value['fallUrl'],
            "miniId": value['miniId'],
            "miniLink": value['miniLink']
        }

        print(json.dumps(advert_params,indent=4))
        res = requests.post(url=self.baseUrl+"/api/market/advertMerge/saveAdvert",headers=self.headers, json=advert_params)
        print("**************************")
        print(res.json())

        print("**************************")
        advertGroupId = res.json()['data']['advertGroupId']
        advertId = res.json()['data']['advertId']
        assert res.json()['status'] == 0


        material_params = {
            "materialName": value['materialName'],
            "materialStyle": value['materialStyle'],
            "skipStyle": value['skpiType'],
            "wechatPopularizePageId": value['popularizeId'],
            "imageVideoUrl": value['imageVideoUrl'],
            "skipAdvertisingCopyName": value['skipAdvertisingCopyName'],
            "skipUrl": value['fallUrl'],
            "shareTitle": value['shareTitle'],
            "shareDescribe": value['shareDescribe'],
            "actionButton": value['actionButton'],
            "advertTitle": value['advertTitle'],
            "miniProgramAdvertisingCopyName": value['miniProgramAdvertisingCopyName'],
            "miniProgramId": value['miniId'],
            "miniProgramUrl": value['miniLink'],
            "brandName": "222",
            "brandUrl": "https://test-oss.shulanchina.cn/imageAndVideo/20201012/1602489174860_53.jpg",
            "pixel": value['pixel'],
            "advertGroupId": advertGroupId,
            "advertId": advertId,
            "shopId": self.shopId,
            "payType": value['payType'],
            "shopName": "微信广告投放专属店铺",
            "advertGroupName": None,
            "advertName": getName("ljf-2")

        }
        print(material_params)

        res1=requests.post(url=self.baseUrl+"/api/market/wechatAdverMaterial/addMaterial",headers=self.headers,json=material_params)
        assert res1.json()['status']==0
        print(res1.json())


        t.sleep(30)
        advert_id=int(str(advertId)[1:])
        sql = "select tencent_material_id from wechat_material where advert_id=%d" % advert_id
        print(get_sql(sql, market))
        tencent_material_id = get_sql(sql, market)[0]['tencent_material_id']

        assert tencent_material_id != None
        t.sleep(3)

    @pytest.mark.skip('skip')
    @pytest.mark.parametrize("value",search_advert_datas)
    def test_search_advert(self,value):
        print(json.dumps(value,indent=4))

        params={
            "shopId":value['shopId'],
            "putState":value['putState'],
            "putChannel":value['putChannel'],
            "advertName":value['advertName'],
            "ascRule":value['ascRule'],
            "sortField":value['sortField']

        }
        success=value['success']

        res=requests.post(url=self.baseUrl+"/api/market/advertMerge/advertList",
                          headers=self.headers,
                          json=params)

        print(json.dumps(res.json(),indent=4))

        real_totalCount=get_sql(value['sql'],market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount']==real_totalCount

    @pytest.mark.skip('skip')
    @pytest.mark.parametrize("value",search_adMaterial_datas)
    def test_search_material(self,value):
        print(json.dumps(value,indent=4))
        params={
            "shopId": value['shopId'],
            "shulanPutInStatus": value['shulanPutInStatus'],
            "putChannel": value['putChannel'],
            "materialName": value['materialName'],
            "advertName": value['advertName'],
            "pageNumber": 1,
            "pageSize": 10

        }
        print(json.dumps(params,indent=4))
        success=value['success']

        res=requests.post(url=self.baseUrl+"/api/market/advertMaterial/selectMaterial",
                          headers=self.headers,
                          json=params)

        print(json.dumps(res.json(),indent=4))

        real_totalCount=get_sql(value['sql'],market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount']==real_totalCount

    @pytest.mark.skip('skip')
    @pytest.mark.parametrize('value',search_popularizePage_datas)
    def test_search_popularizePage(self, value):
        print(json.dumps(value,indent=4))

        params = {
            "shopId": value['shopId'],
            "putChannel": value['putChannel'],
            "popularizeStatus": value['popularizeStatus'],
            "popularizeName": value['popularizeName'],
            "startDate": value['startDate'],
            "endDate": value['endDate'],
            "pageNumber": 1,
            "pageSize": 50

        }
        print(json.dumps(params, indent=4))
        success = value['success']

        res = requests.post(url=self.baseUrl+"/api/market/advertMerge/popularizePage",
                            headers=self.headers,
                            json=params)

        print(json.dumps(res.json(), indent=4))

        real_totalCount = get_sql(value['sql'], market)[0]['total']
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_totalCount