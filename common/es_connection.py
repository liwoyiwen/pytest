from elasticsearch import Elasticsearch
from common.read_data import *

es = Elasticsearch(hosts="192.168.100.166", port=9200)


def get_people_package_detail(package_id):
    body = {
        "size": 1000,
        "query": {
            "match": {
                "peoplePackageId": package_id
            }
        }
    }
    res = es.search(index="people_package_content", body=body)
    package_detail = []
    for item in res["hits"]["hits"]:
        package_detail.extend(item['_source']['contents'])

    people_package = get_sql(f"select * from people_package where id={package_id}", market)[0]
    detail_num = len(package_detail)
    count = people_package['data_count']
    status = people_package['build_status']

    return detail_num, count, status




if __name__ == "__main__":
    num, data_count, build_status = get_people_package_detail(3420)
    print(num)
    print(data_count)
    print(build_status)
