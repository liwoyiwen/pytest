# -*- coding: UTF-8 -*-

import pytest
import requests
from datetime import datetime, timedelta
import time as t
from test.myInit import *
from common.utils import getName
import json
from common.mysql_engine import get_advert
import pandas as f


class TestTencent(MyInit):
    ad_data = get_excel(filename='dsp_data.xls', sheetName="ad_data", converters={"materialName": getName})
    advert_list_data = get_excel(filename='dsp_data.xls', sheetName="advert_list")

    material_list_data = get_excel(filename='dsp_data.xls', sheetName="material_list", )

    page_list_data = get_excel(filename="dsp_data.xls", sheetName="page_list", converters={
        "sql": lambda x: x.strip().replace('%', '%%'),
        "startDate": lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != '' else '',
        "endDate": lambda x: datetime.strftime(x, "%Y-%m-%d %H:%M:%S") if x != '' else ''

    })
    report_chart_data = get_excel(filename='dsp_data.xls', sheetName="report_chart", converters={
        "startDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else None,
        "endDate": lambda x: datetime.strftime(x, "%Y-%m-%d") if x != '' else None

    })

    dsp_data = get_excel(filename='dsp_data.xls', sheetName="dsp_data", converters={"materialName": getName})

    def test_get_dsp_open_shop(self):
        """获取dsp店铺授权列表"""
        url = self.baseUrl + "/api/base/shop/getDspOpenShopList"
        res = requests.post(url=url, headers=self.headers)
        print(json.dumps(res.json(), indent=4))
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_alter_advert_state(self):
        """广告状态禁用或启用"""
        url = self.baseUrl + "/api/market/advertMerge/alterAdvertState"
        params = {
            "advertEnable": 0,
            "shopId": 544,
            "advertId": 11070,
            "putChannel": 1
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(json.dumps(res.json(), indent=4))
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", report_chart_data)
    def test_query_report(self, value):
        """投放数据"""
        url = self.baseUrl + "/api/market/peoplePackage/queryPutAdvReportChart"
        params = {
            "materialId": value['materialId'],
            "advertId": value['advertId'],
            "startDate": value['startDate'],
            "endDate": value['endDate'],
            "dateType": value['dateType'],
            "queryValType": value['queryValType']
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(json.dumps(res.json(), indent=4))
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", ad_data)
    def test_add_wechat_advert(self, value):
        """新增广告素材"""
        print(value)
        advert_params = {
            "shopId": self.shopId,
            "putMedia": value['putMedia'],
            "paymentType": value['paymentType'],
            "advertSpace": str(value['advertSpace']),
            "advertSpaceName": value['advertSpaceName'],
            "launchPeople": self.launchPeople,
            "peoplePackageName": self.peoplePackageNumber,
            "peoplePackageNumber": self.peoplePackageNumber,
            "launchMode": value['launchMode'],
            "launchStartTime": datetime.strftime(datetime.now() + timedelta(days=3), "%Y-%m-%d %H:%M:%S"),
            "launchEndTime": None,
            "launchTimeInterval": "11111111111111111111111111111111111111111111111111111111"
                                  "111111111111111111111111111111111111111111111111111111111"
                                  "1111111111111111111111111111111111111111111111111111111"
                                  "11111111111111111111111111111111111111111111111111111111111111"
                                  "111111111111111111111111111111111111111111111111111111111111111111"
                                  "1111111111111111111111111111111111111111",
            "launchTimeInfo": "不限",
            "directUrl": None,
            "totalAdvertBudget": "500",
            "singlePrice": "50",
            "advertName": getName("ljf-2"),
            "optimizeTarget": value['optimizeTarget'],
            "skipType": value['skipType'],
            "popularizeId": value['popularizeId'],
            "fallUrl": value['fallUrl'],
            "miniId": value['miniId'],
            "miniLink": value['miniLink']
        }

        print(json.dumps(advert_params, indent=4))
        res = requests.post(url=self.baseUrl + "/api/market/advertMerge/saveAdvert", headers=self.headers,
                            json=advert_params)
        print(res.json())
        group_id = res.json()['data']['advertGroupId']
        advert_id = res.json()['data']['advertId']
        assert res.json()['status'] == 0

        material_params = {
            "materialName": value['materialName'],
            "materialStyle": value['materialStyle'],
            "skipStyle": value['skipType'],
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
            "advertGroupId": group_id,
            "advertId": advert_id,
            "shopId": self.shopId,
            "payType": value['payType'],
            "shopName": "微信广告投放专属店铺",
            "advertGroupName": None,
            "advertName": getName("ljf-2"),
            "screenCaptureUrl": value['screenCaptureUrl'],
            "tencentCopy": value['tencentCopy'],
            "adDescribe": value['adDescribe']

        }

        print(material_params)

        res1 = requests.post(url=self.baseUrl + "/api/market/wechatAdverMaterial/addMaterial", headers=self.headers,
                             json=material_params)
        assert res1.json()['status'] == 0
        print(res1.json())

        t.sleep(30)
        advert_id = int(str(advert_id)[1:])
        sql = f"select tencent_material_id from wechat_material where advert_id={advert_id}"
        print(get_sql(sql, market))
        tencent_material_id = get_sql(sql, market)[0]['tencent_material_id']
        assert tencent_material_id is not None
        t.sleep(3)

    @pytest.mark.parametrize("value", advert_list_data)
    def test_advert_list(self, value):
        """广告列表"""
        print(json.dumps(value, indent=4))

        params = {
            "shopId": value['shopId'],
            "putState": value['putState'],
            "putChannel": value['putChannel'],
            "advertName": value['advertName'],
            "ascRule": value['ascRule'],
            "sortField": value['sortField'],
            "pageNumber": 1,
            "pageSize": 10

        }
        success = value['success']

        res = requests.post(url=self.baseUrl + "/api/market/advertMerge/advertList",
                            headers=self.headers,
                            json=params)
        print(res.json()['data']['totalCount'])

        real_total_count = len(
            get_advert(user_id=self.user_id, shop_id=params['shopId'], channel=params['putChannel'],
                       put_state=params['putState'], advert_name=params['advertName']))

        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_total_count

    @pytest.mark.parametrize("value", material_list_data)
    def test_material_list(self, value):
        """素材列表"""
        print(json.dumps(value, indent=4))
        params = {
            "shopId": value['shopId'],
            "shulanPutInStatus": value['shulanPutInStatus'],
            "putChannel": value['putChannel'],
            "materialName": value['materialName'],
            "advertName": value['advertName'],
            "pageNumber": 1,
            "pageSize": 10

        }
        print(json.dumps(params, indent=4))
        success = value['success']

        res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/selectMaterial",
                            headers=self.headers,
                            json=params)

        real_total_count = len(
            get_advert_material(user_id=self.user_id, shop_id=params['shopId'], channel=params['putChannel'],
                                put_in_status=params['shulanPutInStatus'], advert_name=params['advertName'],
                                material_name=params['materialName']))
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_total_count

    @pytest.mark.parametrize("status", [1, 0], ids=["禁用", "启用"])
    def test_update_material_status(self, status):
        """启用或禁用素材"""
        url = self.baseUrl + "/api/market/wechatAdverMaterial/updateMaterialStatus"

        res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/selectMaterial",
                            headers=self.headers,
                            json={
                                "pageNumber": 1,
                                "pageSize": 10,
                                "shulanPutInStatus": 1,
                            }).json()['data']['data'][0]

        params = {
            "status": status,
            "materialId": res['materialId'],
            "shopId": res['shopId']
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize('value', page_list_data)
    def test_page_list(self, value):
        """推广页列表"""

        params = {
            "shopId": value['shopId'],
            "putChannel": value['putChannel'],
            "popularizeStatus": value['popularizeStatus'],
            "popularizeName": value['popularizeName'],
            "startDate": value['startDate'],
            "endDate": value['endDate'],
            "pageNumber": 1,
            "pageSize": 10

        }
        print(params)
        success = value['success']

        res = requests.post(url=self.baseUrl + "/api/market/advertMerge/popularizePage",
                            headers=self.headers,
                            json=params)

        print(res.json())

        real_total_count = len(
            get_page(user_id=self.user_id, shop_id=params['shopId'], channel=params['putChannel'],
                     status=params['popularizeStatus'], name=params['popularizeName'], startTime=params['startDate'],
                     endTime=params['endDate']))

        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['totalCount'] == real_total_count

    def test_delete_material(self):
        """删除素材"""
        url = self.baseUrl + "/api/market/wechatAdverMaterial/deleteMaterial"
        res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/selectMaterial",
                            headers=self.headers,
                            json={
                                "pageNumber": 1,
                                "pageSize": 10,
                                "shulanPutInStatus": 1,
                            }).json()['data']['data'][0]

        params = {
            "advertGroupId": res['advertGroupId'],
            "advertId": res['advertId'],
            "shopId": res['shopId'],
            "materialId": res['materialId']
        }

        res1 = requests.post(url=url, headers=self.headers, json=params)
        print(res1.json())
        assert res1.status_code == 200
        assert res1.json()['status'] == 0

    def test_wechat_preview_url(self):
        """微信推广页二维码"""
        url = self.baseUrl + "/api/market/wechatPopularize/findPreviewUrl"
        page_id = requests.post(url=self.baseUrl + "/api/market/advertMerge/popularizePage",
                                headers=self.headers,
                                json={
                                    "pageNumber": 1,
                                    "pageSize": 10,
                                    "putChannel": 1
                                }).json()['data']['data'][0]['id']

        params = {
            "popularizePageId": page_id
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_wechat_popularize_detail(self):
        """微信推广页详情"""
        url = self.baseUrl + "/api/market/wechatPopularize/getPopularizeDetail"
        page_id = requests.post(url=self.baseUrl + "/api/market/advertMerge/popularizePage",
                                headers=self.headers,
                                json={
                                    "pageNumber": 1,
                                    "pageSize": 10,
                                    "putChannel": 1
                                }).json()['data']['data'][0]['id']
        params = {
            "id": page_id
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_dsp_preview_url(self):
        """巨量推广页二维码"""
        url = self.baseUrl + "/api/market/dspPopularize/findPreviewUrl"
        page_id = requests.post(url=self.baseUrl + "/api/market/advertMerge/popularizePage",
                                headers=self.headers,
                                json={
                                    "pageNumber": 1,
                                    "pageSize": 10,
                                    "putChannel": 2
                                }).json()['data']['data'][0]['id']

        params = {
            "popularizePageId": page_id
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    def test_dsp_popularize_detail(self):
        """巨量推广页详情"""
        url = self.baseUrl + "/api/market/dspPopularize/PopularizeDetail"
        page_id = requests.post(url=self.baseUrl + "/api/market/advertMerge/popularizePage",
                                headers=self.headers,
                                json={
                                    "pageNumber": 1,
                                    "pageSize": 10,
                                    "putChannel": 2
                                }).json()['data']['data'][0]['id']
        params = {
            "id": page_id
        }

        res = requests.post(url=url, headers=self.headers, params=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['status'] == 0

    @pytest.mark.parametrize("value", dsp_data)
    def test_add_dsp_advert(self, value):

        advert_params = {
            "shopId": value['shopId'],
            "putMedia": value['putMedia'],
            "paymentType": value['paymentType'],
            "advertSpace": value['advertSpace'],
            "advertSpaceName": value['advertSpaceName'],
            "launchPeople": self.launchPeople,
            "peoplePackageName": self.peoplePackageNumber,
            "peoplePackageNumber": self.peoplePackageNumber,
            "launchStartTime": "2021-03-08 08:00:00",
            "launchTimeInterval": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            "launchTimeInfo": "不限",
            "launchMode": value['launchMode'],
            "directUrl": None,
            "totalAdvertBudget": "10000",
            "singlePrice": "1000",
            "advertName": value['materialName'],
            "optimizeTarget": value['optimizeTarget'],
            "skpiType": value['skipType'],
            "popularizeId": value['popularizeId'],
            "fallUrl": value['fallUrl'],

        }

        res = requests.post(url=self.baseUrl + "/api/market/advertMerge/saveAdvert", json=advert_params,
                            headers=self.headers)
        print(res.json())
        res.status_code == 200
        res.json()['status'] == 0
        advert_group_id = res.json()['data']['advertGroupId']
        advert_id = res.json()['data']['advertId']

        identifications = self.upload(value['materialStyle'], value['advertSpaceName'], value['type'])
        brand_name, brand_url = self.get_brand(shop_id=value['shopId'])
        material_params = {
            "imageOrVideoMaterialReq":
                [
                    {
                        "identifications": identifications,
                        "materialNameLong": value['materialName']
                    }
                ],
            "type": value['type'],
            "materialName": value['materialName'],
            "materialLabel": "素材标签",
            "materialClassify": "[\"医疗\",\"医疗周边服务\",\"赴外医疗\"]",
            "materialClassifyId": 19050604,
            "advertGroupId": advert_group_id,
            "advertId": advert_id,
            "shopId": value["shopId"],
            "brandName": brand_name,
            "brandUrl": brand_url
        }

        res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/addMaterial", json=material_params,
                            headers=self.headers)
        print(res.json())
        res.status_code == 200
        res.json()['status'] == 0
        time.sleep(60)

        sql = f"select id from dsp_advert where advert_name='{value['materialName']}'"
        advert_id = get_sql(sql, market)[0]['id']
        sql1 = f"update read_dmp_data_dispatcher set data_source_id='cadaecdd5b0e46f897c5e1cec5aca45a', dispatcher_status='PUSH' where advert_id={advert_id}"
        try:
            f.read_sql_query(sql1, ads)
        except Exception as e:
            print(e)
        finally:
            analysis.dispose()


    def upload(self, materialStyle, advertPositionName, advertPositionType):
        if materialStyle == 1:
            image_url = "../images/竖版大图.jpg"
        if materialStyle == 0:
            image_url = "../images/横版大图.jpg"

        if materialStyle == 3:
            image_url = "../images/横版大图.jpg"
            video_url = "../images/横版视频.mp4"
        if materialStyle == 4:
            image_url = "../images/竖版大图.jpg"
            video_url = "../images/竖版视频.mp4"

        if materialStyle == 2:
            # 横版大图
            pass

        header = {
            "token": self.headers['token']
        }

        params_image = {
            "materialStyle": materialStyle,
            "advertPositionName": advertPositionName,
            "identification": "",
            "advertPositionType": advertPositionType,
            "materialType": materialStyle,
            "imageOrVideoType": 0
        }
        params_video = {
            "materialStyle": materialStyle,
            "advertPositionName": advertPositionName,
            "identification": "",
            "advertPositionType": advertPositionType,
            "materialType": materialStyle,
            "imageOrVideoType": materialStyle
        }

        if materialStyle == 1 or materialStyle == 0:
            with open(image_url, "rb") as f:
                files = {"file": f}
                res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/upload", headers=header, files=files,
                                    data=params_image)
                identification = res.json()['data'].get("identification")

        if materialStyle == 3 or materialStyle == 4:
            with open(image_url, "rb") as f:
                files = {"file": f}
                res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/upload", headers=header, files=files,
                                    data=params_image)
                identification = res.json()['data'].get("identification")
                params_video['identification'] = identification

            with open(video_url, "rb") as f:
                files = {"file": f}
                res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/upload", headers=header, files=files,
                                    data=params_video)
                res.status_code == 200
                res.json()['status'] == 0

        return identification

    def get_brand(self, shop_id):
        params = {
            "shopId": shop_id,
            "brandIdentifications": None
        }
        res = requests.post(url=self.baseUrl + "/api/market/advertMaterial/getBrand", json=params, headers=self.headers)
        return res.json()['data']['brandName'], res.json()['data']['brandUrl']
