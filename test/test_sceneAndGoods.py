# -*- coding: UTF-8 -*-
import pytest
import requests
from common.read_data import *
from test.myInit import *
from datetime import datetime, timedelta


class TestScenePeopleTest(MyInit):
    generateSceneAndTradePeoplePack_data = get_excel(filename='sceneAndGoods_data.xls',
                                                     sheetName="generateSceneAndTradePeople",
                                                     converters={
                                                         "name": lambda x: x + datetime.strftime(datetime.now(),
                                                                                                 "%Y-%m-%d_%H-%M-%S")
                                                     })

    platformOverview_data = get_excel(filename="sceneAndGoods_data.xls", sheetName="platformOverview")
    oneKeyPut_data = get_excel(filename="sceneAndGoods_data.xls", sheetName="oneKeyPut-sms", converters={
        "name": lambda x: getName(x),
        "planName": lambda x: getName(x),
        "startTime": lambda x: datetime.strftime(datetime.now() + timedelta(days=20), "%Y-%m-%d"),
        "putMoment": lambda x: datetime.strftime(datetime.now(), "%H:%M"),

    })
    oneKeyPut_ad = get_excel(filename="sceneAndGoods_data.xls", sheetName="oneKeyPut-ad", converters={
        "name": lambda x: getName(x),

    })

    @pytest.mark.skip("skip")
    def test_getScene(self):
        url = self.baseUrl + "/api/analysis/label/getSceneCrowd"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.skip("skip")
    def test_overviewByGoods(self):
        url = self.baseUrl + "/api/heart/member/overviewByGoods"
        res = requests.post(url=url, headers=self.headers, json=[])
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    def test_getEstimateNumber(self):
        url = self.baseUrl + "/api/analysis/peoplePackage/getEstimateNumber"
        params = {
            "repeated": 0,
            "type": "SCENE_SELECT_PEOPLE",
            "scenePeopleLabel": ["主流时尚", "家庭主妇", "平价实惠", "美丽教主"],
            "categoryLabel": [],
            "peopleLabel": ["sex：男性", "sex：女性", "sex：未知"]
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.skip("skip")
    @pytest.mark.parametrize("value", platformOverview_data)
    def test_platformOverview(self, value):
        print(value)
        url = self.baseUrl + "/api/heart/member/platformOverview"
        params = {
            "query_labels": {
                "query_labels": ast.literal_eval(value['query_labels']),
                "condition_labels_region": "merge"
            },
            "aggr_charts": {
                "main_label": [
                    {"label_key": "is_have_baby", "value": []},
                    {"label_key": "payment_time_speed", "value": []},
                    {"label_key": "shopping_time", "value": []},
                    {"label_key": "payment_time_speed", "value": []},
                    {"label_key": "consumption_cap", "value": []},
                    {"label_key": "is_have_baby", "value": []},
                    {"label_key": "payment_time_speed", "value": []},
                    {"label_key": "shopping_time", "value": []},
                    {"label_key": "payment_time_speed", "value": []},
                    {"label_key": "consumption_cap", "value": []},
                    {"label_key": "city_level", "value": []}],
                "sub_labels": [
                    {"label_key": "payment_time_speed", "value": []},
                    {"label_key": "sex", "value": []},
                    {"label_key": "days_mean_buy", "value": []},
                    {"label_key": "preference_of_promotion", "value": []},
                    {"label_key": "is_have_pet", "value": []},
                    {"label_key": "payment_time_speed", "value": []},
                    {"label_key": "sex", "value": []}, {"label_key": "days_mean_buy", "value": []},
                    {"label_key": "preference_of_promotion", "value": []},
                    {"label_key": "is_have_pet", "value": []},
                    {"label_key": "is_have_pet", "value": []}
                ],
                "charts_type": "cross"
            },
            "repeated": 0
        }
        print(json.dumps(params, indent=4))
        success = value['success']
        res = requests.post(url=url, headers=TestScenePeopleTest.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success

    @pytest.mark.skip("skip")
    def test_flowPackageRemain(self):
        url = self.baseUrl + "/api/base/pay/flowPackageRemain"
        res = requests.post(url=url, headers=self.headers)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.skip("skip")
    @pytest.mark.parametrize('value', generateSceneAndTradePeoplePack_data)
    def test_generateSceneAndTradePeoplePackage(self, value):
        url = self.baseUrl + "/api/analysis/peoplePackage/getEstimateNumber"
        params = {
            "repeated": 0,
            "type": "SCENE_SELECT_PEOPLE",
            "scenePeopleLabel": ast.literal_eval(value['scenePeopleLabel']),
            "categoryLabel": ast.literal_eval(value['categoryLabel']),
            "peopleLabel": ast.literal_eval(value['peopleLabel'])
        }
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0
        estimateNumber = res.json()["data"]["number"]

        if estimateNumber >= value["dataCount"]:
            data_count = value["dataCount"]
        else:
            data_count = estimateNumber

        url = self.baseUrl + "/api/market/peoplePackage/generateSceneAndTradePeoplePackage"
        params = {
            "repeated": value['repeated'],
            "type": value['type'],
            "scenePeopleLabel": ast.literal_eval(value['scenePeopleLabel']),
            "categoryLabel": ast.literal_eval(value['categoryLabel']),
            "peopleLabel": ast.literal_eval(value['peopleLabel']),
            "estimateNumber": estimateNumber,
            "name": value['name'],
            "dataCount": data_count,
            "requestParam": value['requestParam']

        }
        print(json.dumps(params, indent=4))
        success = value['success']
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        print(res.json()['data'])
        assert res.status_code == 200
        assert res.json()['success'] == success
        assert res.json()['data']['id'] is not None
        peopackage_id = res.json()['data']['id']

        time.sleep(200)
        result = get_sql("select data_count, build_status from people_package where id=%d" % (peopackage_id), market)
        assert result[0]['data_count'] == data_count
        assert result[0]['build_status'] == 0

        url_packagePortray = self.baseUrl + "/api/heart/crowdPackage/getCrowdPackagePortray"
        params_packagePortray = {
            "crowdPackageId": peopackage_id
        }

        res = requests.get(url=url_packagePortray, params=params_packagePortray, headers=self.headers)
        assert res.status_code == 200
        assert res.json()['success'] == True
        assert res.json()['data']['overview']['memberCount'] == data_count

    @pytest.mark.skip("skip")
    def test_estimateCostByCount(self):
        url = self.baseUrl + "/api/market/plan/estimateCostByCount"
        params = {
            "materialId": 384,
            "dataCount": 10000
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        assert res.status_code == 200
        assert res.json()["status"] == 0

    @pytest.mark.parametrize("value", oneKeyPut_data)
    def test_oneKeyPut(self, value):
        url = self.baseUrl + "/api/market/advertMerge/oneKeyPut"
        print(json.dumps(value, indent=4))
        params = {
            "repeated": value["repeated"],
            "type": value["type"],
            "scenePeopleLabel": ast.literal_eval(value["scenePeopleLabel"]),
            "categoryLabel": ast.literal_eval(value["categoryLabel"]),
            "peopleLabel": ast.literal_eval(value["peopleLabel"]),
            "estimateNumber": value["estimateNumber"],
            "name": value["name"],
            "dataCount": value["dataCount"],
            "requestParam": value["requestParam"],
            "planName": value["planName"],
            "startTime": value["startTime"],
            "materialId": value["materialId"],
            "putMoment": value["putMoment"],
            "putScene": value["putScene"],
            "shortUrl": self.get_shortUrl(value["materialId"]),
            "putMode": value["putMode"]
        }
        print(json.dumps(params, indent=4))
        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0
        time.sleep(180)

        plan = get_sql("select * from plan where name='%s'" % value["planName"], market)[0]
        print(plan)
        assert plan is not None

        peoplePackage = get_sql("select * from people_package where name='%s'" % value["name"], market)[0]
        assert peoplePackage['id'] is not None
        assert peoplePackage['build_status'] == 0

    @pytest.mark.parametrize("value", oneKeyPut_ad)
    def test_oneKeyPut1(self, value):
        url = self.baseUrl + "/api/market/advertMerge/oneKeyPut"
        params = {
            "repeated": value["repeated"],
            "type": value["type"],
            "scenePeopleLabel": ast.literal_eval(value["scenePeopleLabel"]),
            "categoryLabel": ast.literal_eval(value["categoryLabel"]),
            "peopleLabel": ast.literal_eval(value["peopleLabel"]),
            "estimateNumber": value["estimateNumber"],
            "name": value["name"],
            "dataCount": value["dataCount"],
            "requestParam": value["requestParam"],
            "shopId": value["shopId"],
            "putChannel": value["putChannel"],
            "advertId": value["advertId"],
            "putState": str(value["putState"]),
            "putMode": value["putMode"]
        }

        res = requests.post(url=url, headers=self.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["status"] == 0
        time.sleep(180)

        peoplePackage = get_sql("select * from people_package where name='%s'" % value["name"], market)[0]
        assert peoplePackage['id'] is not None
        assert peoplePackage['build_status'] == 0

        if value["putChannel"] == 1:
            advert = get_sql("select * from wechat_advert where id=%d" % int(str(value["advertId"])[1:]), market)[0]

        elif value["putChannel"] == 2:
            advert = get_sql("select * from dsp_advert where id='%d'" % int(str(value["advertId"])[1:]), market)[0]

        if value['putState'] == 0:
            assert advert['launch_people'] == str(peoplePackage['id'])


        elif value['putState'] == 1:
            assert str(peoplePackage['id']) in advert['launch_people']
