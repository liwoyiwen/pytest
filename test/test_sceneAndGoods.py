# -*- coding: UTF-8 -*-
import pytest
import requests
from common.read_data import *
from test.myInit import *
class TestScenePeopleTest(MyInit):




    generateSceneAndTradePeoplePack_datas = get_excel(filename='sceneAndGoods_data.xls',
                                                      sheetName="generateSceneAndTradePeople",
                                                      converters={
                                                          "name": lambda x: x + datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")
        })
    
    



    platformOverview_datas=get_excel(filename="sceneAndGoods_data.xls",sheetName="platformOverview")


    def test_getScene(self):
        url=self.baseUrl+"/api/analysis/label/getSceneCrowd"
        res=requests.post(url=url,headers=self.headers)
        assert res.status_code == 200
        assert res.json()["status"] == 0





    @pytest.mark.parametrize("value",platformOverview_datas)
    def test_platformOverview(self,value):
        print(value)
        url=self.baseUrl+"/api/heart/member/platformOverview"
        params={
            "query_labels":{
                "query_labels":ast.literal_eval(value['query_labels']),
                "condition_labels_region":"merge"
            },
            "aggr_charts":{
                "main_label":[
                    {"label_key":"is_have_baby","value":[]},
                    {"label_key":"payment_time_speed","value":[]},
                    {"label_key":"shopping_time","value":[]},
                    {"label_key":"payment_time_speed","value":[]},
                    {"label_key":"consumption_cap","value":[]},
                    {"label_key":"is_have_baby","value":[]},
                    {"label_key":"payment_time_speed","value":[]},
                    {"label_key":"shopping_time","value":[]},
                    {"label_key":"payment_time_speed","value":[]},
                    {"label_key":"consumption_cap","value":[]},
                    {"label_key":"city_level","value":[]}],
                "sub_labels":[
                    {"label_key":"payment_time_speed","value":[]},
                    {"label_key":"sex","value":[]},
                    {"label_key":"days_mean_buy","value":[]},
                    {"label_key":"preference_of_promotion","value":[]},
                    {"label_key":"is_have_pet","value":[]},
                    {"label_key":"payment_time_speed","value":[]},
                    {"label_key":"sex","value":[]},{"label_key":"days_mean_buy","value":[]},
                    {"label_key":"preference_of_promotion","value":[]},
                    {"label_key":"is_have_pet","value":[]},
                    {"label_key":"is_have_pet","value":[]}
                ],
                "charts_type":"cross"
            },
            "repeated":0
        }
        print(json.dumps(params,indent=4))
        success = value['success']
        res = requests.post(url=url, headers=TestScenePeopleTest.headers, json=params)
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success


    @pytest.mark.parametrize('value', generateSceneAndTradePeoplePack_datas)
    def test_generateSceneAndTradePeoplePackage(self, value):
        url = self.baseUrl+"/api/market/peoplePackage/generateSceneAndTradePeoplePackage"
        params = {
            "repeated": value['repeated'],
            "type": value['type'],
            "scenePeopleLabel": ast.literal_eval(value['scenePeopleLabel']),
            "categoryLabel": ast.literal_eval(value['categoryLabel']),
            "peopleLabel": ast.literal_eval(value['peopleLabel']),
            "estimateNumber": value['estimateNumber'],
            "name": value['name'],
            "dataCount": value['dataCount'],
            "requestParam": value['requestParam']

        }
        print(json.dumps(params, indent=4))
        success = value['success']
        res = requests.post(url=url, headers=TestScenePeopleTest.headers, json=params)
        print(res.json())
        print(res.json()['data'])
        assert res.status_code == 200
        assert res.json()['success'] == success

    def test_02(self):
        print(ast.literal_eval('[{"name":"场景人群","values":["(主流时尚)","(平价实惠)"]},{"name":"城市级别","values":["(一线城市)"]}]'))
