
import requests
import json
from elasticsearch import Elasticsearch
def test_01():

    '''人群解密'''
    es = Elasticsearch(hosts="192.168.100.166", port=9200)
    body = {
        "query": {
            "match": {
                "peoplePackageId": 3428
            }
        }
    }

    res = es.search(index="people_package_content", body=body)
    num = len(res["hits"]["hits"])
    url = "http://hk-encry.shulanchina.cn/hkEncryption/decrypt"

    total = []
    for i in range(0, num):
        total.extend(res["hits"]["hits"][i]["_source"]['contents'])
    print(total)

    ll = [total[i:i + 200] for i in range(0, len(total), 100)]



    """
    
        for i in ll:
        params = {
            "dataJsonArray": json.dumps(i)
        }
        res = requests.post(url=url, params=params)
        print(res.json())
        assert res.json()['code'] == 200

    
    """
    for i in ll:
        params = {
            "dataJsonArray": json.dumps(i)
        }
        res = requests.post(url=url, params=params)
        print(res.json())
        assert res.json()['code'] == 200