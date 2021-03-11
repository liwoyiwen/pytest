from sqlalchemy import create_engine
from common.read_data import *
from conf.config import ReadConfig

os.environ['--env'] = 'test'

read_config = ReadConfig()
username = read_config.get_conf("mysql-username")
password = read_config.get_conf("mysql-password")
url = read_config.get_conf("mysql-url")

market = create_engine(f'mysql+pymysql://{username}:{password}@{url}/market?charset=utf8', encoding='utf-8')
base = create_engine(f'mysql+pymysql://{username}:{password}@{url}/base?charset=utf8', encoding='utf-8')
analysis = create_engine(f'mysql+pymysql://{username}:{password}@{url}/analysis?charset=utf8', encoding='utf-8')
ads = create_engine(f'mysql+pymysql://{username}:{password}@{url}/ads?charset=utf8', encoding='utf-8')

def get_people_package(name=None):
    people_package = get_sql(f"select * from people_package where name='{name}'", market)[0]
    return people_package


def get_plan(name):
    plan = get_sql(f"select * from plan where name='{name}'", market)[0]
    return plan


def get_wechat_advert(advert_id=None):
    advert_id = int(str(advert_id)[1:])
    wechat_advert = get_sql(f"select * from wechat_advert where id={advert_id}", market)[0]
    return wechat_advert


def get_dsp_advert(advert_id=None):
    advert_id = int(str(advert_id)[1:])
    wechat_advert = get_sql(f"select * from dsp_advert where id={advert_id}", market)[0]
    return wechat_advert


def get_user(user_id):
    user_info = get_sql(f"select * from user where id={user_id}", base)[0]
    return user_info


def get_price(price_id):
    price = get_sql(f"select * from price_list where id={price_id}", base)[0]
    return price


def get_flow_package_remaining(user_id):
    remaining = get_sql(f"select * from flow_package_remaining where user_id={user_id}", base)[0]["total_remain"]
    return remaining


def get_app_remaining(user_id):
    remaining = get_sql(f"select * from app_sms_remaining where user_id={user_id}", base)[0]["total_remaining"]
    return remaining


def get_portraitUpgrade_remaining(user_id=None, start=None, end=None):
    remaining = \
        get_sql(f"select * from user_calculated_quantity where user_id={user_id} and start={start} and end={end}",
                base)[0][
            'total_remaining']
    return remaining


def get_sms_remaining(user_id):
    remaining = \
        get_sql(f"select sum(amount+gifts) as sms_remaining from user_sms_remaining where user_id={user_id}", base)[0][
            'sms_remaining']
    return remaining


def get_wallet_consumption(user_id):
    wallet_consumption = get_sql(f"select * from wallet_detail where user_id={user_id} ORDER BY create_time desc", base)
    return wallet_consumption


def get_sms_consumption(user_id):
    sms_consumption = get_sql(
        f"select * from (select consumption_id, operate_time, sum(pre_pay_sms_num) 预计消费, sum(sms_amount) 实际消费 from fund_consumption_log where user_id={user_id} GROUP BY consumption_id  ORDER BY operate_time desc) as a",
        base)
    return sms_consumption


def get_portraitUpgrade_consumption(user_id):
    portraitUpgrade_consumption = get_sql(
        f"select * from user_consumer_record where user_child_id={user_id} and feature_id=0", base)
    return portraitUpgrade_consumption


def get_app_consumption(user_id):
    app_consumption = get_sql(
        f"select *  from user_consumer_record where user_child_id={user_id} and feature_id=2", base)
    return app_consumption


def get_flow_package_consumption(user_id):
    flow_package_consumption = get_sql(
        f"select * from user_consumer_record where user_child_id={user_id} and feature_id in (8,9,11)", base)
    return flow_package_consumption


def get_app_demand(name):
    app_demand = get_sql(f"select * from app_crowd_pack_demand where name='{name}'", market)[0]
    return app_demand


def get_app_demand_detail(demand_bill_code):
    app_demand_detail = \
        get_sql(f"select middle_order_id from app_pull_middle_data where order_no='{demand_bill_code}'", market)[0]
    return app_demand_detail


def get_advert(user_id=None, shop_id=None, put_state=None, channel=None, advert_name=None):
    sql1 = f"select * from wechat_advert where user_id={user_id}"
    sql2 = f"select * from dsp_advert where user_id={user_id}"
    if shop_id is not None and shop_id != '':
        sql1 += f" and shop_id={shop_id}"
        sql2 += f" and shop_id={shop_id}"

    if put_state == 1:
        sql1 += " and put_state in ('AD_STATUS_NO_MATERIAL')"
        sql2 += " and put_state in ('AD_STATUS_NO_MATERIAL')"
    elif put_state == 2:
        sql1 += " and put_state in ('AD_STATUS_CROWD_SYNCHRONOUS')"
        sql2 += " and put_state in ('AD_STATUS_CROWD_SYNCHRONOUS')"
    elif put_state == 3:
        sql1 += " and put_state in ('STATUS_POPULARIZE')"
        sql2 += " and put_state in ('STATUS_POPULARIZE')"
    elif put_state == 4:
        sql1 += " and put_state in ('STATUS_ACTIVE','STATUS_PART_ACTIVE')"
        sql2 += " and put_state in ('AD_STATUS_DELIVERY_OK')"
    elif put_state == 5:
        sql1 += " and put_state in ('STATUS_READY','STATUS_PREPARE','STATUS_PART_READY')"
        sql2 += " and put_state in ('AD_STATUS_NOT_START','AD_STATUS_NO_SCHEDULE')"
    elif put_state == 6:
        sql1 += " and put_state in ('STATUS_PENDING','STATUS_UNKNOWN')"
        sql2 += " and put_state in ('AD_STATUS_AUDIT','AD_STATUS_REAUDIT','AD_STATUS_CREATE')"
    elif put_state == 7:
        sql1 += " and put_state in ('STATUS_DENIED')"
        sql2 += " and put_state in ('AD_STATUS_AUDIT_DENY')"
    elif put_state == 8:
        sql1 += " and put_state in ('STATUS_FROZEN','STATUS_SUSPEND','STATUS_ACTIVE_CAMPAIGN_SUSPEND')"
        sql2 += " and put_state in ('AD_STATUS_DISABLE','AD_STATUS_CAMPAIGN_DISABLE')"
    elif put_state == 9:
        sql1 += " and put_state in ('STATUS_ACTIVE_ACCOUNT_LIMIT','STATUS_ACTIVE_CAMPAIGN_LIMIT','STATUS_ACTIVE_AD_LIMIT')"
        sql2 += " and put_state in ('AD_STATUS_CAMPAIGN_EXCEED','AD_STATUS_BUDGET_EXCEED')"
    elif put_state == 10:
        sql1 += " and put_state in ('STATUS_ACTIVE_ACCOUNT_FROZEN','STATUS_ACTIVE_ACCOUNT_EMPTY')"
        sql2 += " and put_state in ('AD_STATUS_BALANCE_EXCEED')"
    elif put_state == 11:
        sql1 += " and put_state in ('STATUS_STOP','STATUS_DELETED')"
        sql2 += " and put_state in ('AD_STATUS_DONE','AD_STATUS_DELETE')"

    if advert_name is not None and advert_name != '':
        sql1 += f" and advert_name like '%%{advert_name}%%'"
        sql2 += f" and advert_name like '%%{advert_name}%%'"

    wechat_adverts = get_sql(sql1, market)
    l1 = [int('1' + str(item['id'])) for item in wechat_adverts]

    dsp_adverts = get_sql(sql2, market)
    l2 = [int('2' + str(item['id'])) for item in dsp_adverts]
    if channel == 1:
        print(sql1)
        return l1

    if channel == 2:
        print(sql2)
        return l2
        print(sql2)
    if channel is None or channel == '':
        return l1 + l2


def get_advert_material(user_id=None, shop_id=None, put_in_status=None, channel=None, material_name=None,
                        advert_name=None):
    sql1 = f"select wechat_material.id from wechat_material inner join wechat_advert on " \
        f"wechat_advert.id=wechat_material.advert_id where wechat_material.user_id={user_id}"

    sql2 = f"select dsp_material.id from dsp_material inner join dsp_advert on " \
        f"dsp_advert.id=dsp_material.advert_id where dsp_material.user_id={user_id}"

    if shop_id is not None and shop_id != '':
        sql1 += f" and wechat_material.shop_id={shop_id}"
        sql2 += f" and dsp_material.shop_id={shop_id}"

    if put_in_status is not None and put_in_status != '':
        sql1 += f" and wechat_material.shulan_put_in_status={put_in_status}"
        sql2 += f" and dsp_material.shulan_put_in_status={put_in_status}"
    """
        if put_in_status == 0:
        sql1 += " and wechat_material.put_in_status in ('AD_STATUS_PARTIALLY_NORMAL','AD_STATUS_NORMAL')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_DELIVERY_OK')"
    if put_in_status == 1:
        sql1 += " and wechat_material.put_in_status in ('AD_STATUS_PENDING','AD_STATUS_PARTIALLY_PENDING','AD_STATUS_PREPARE')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_AUDIT','CREATIVE_STATUS_REAUDIT','CREATIVE_STATUS_AD_AUDIT','CREATIVE_STATUS_AD_REAUDIT')"
    elif put_in_status == 2:
        sql1 += " and wechat_material.put_in_status in ('AD_STATUS_DENIED')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_AUDIT_DENY','CREATIVE_STATUS_DATA_ERROR','CREATIVE_STATUS_AD_AUDIT_DENY')"
    elif put_in_status == 3:
        sql1 += " and wechat_material.put_in_status in ('AD_STATUS_INVALID')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_NOT_START','CREATIVE_STATUS_NO_SCHEDULE','CREATIVE_STATUS_CAMPAIGN_DISABLE','CREATIVE_STATUS_DISABLE','CREATIVE_STATUS_AD_DISABLE','CREATIVE_STATUS_PRE_ONLINE')"
    elif put_in_status == 4:
        sql1 += " and wechat_material.put_in_status in ('')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_CAMPAIGN_EXCEED','CREATIVE_STATUS_BUDGET_EXCEED','CREATIVE_STATUS_ADVERTISER_BUDGET_EXCEED')"
    elif put_in_status == 5:
        sql1 += " and wechat_material.put_in_status in ('')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_BALANCE_EXCEED')"
    elif put_in_status == 6:
        sql1 += " and wechat_material.put_in_status in ('AD_STATUS_DELETED')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_DELETE')"
    elif put_in_status == 7:
        sql1 += " and wechat_material.put_in_status in ('')"
        sql2 += " and dsp_material.put_in_status in ('CREATIVE_STATUS_DONE')"
    
    """

    if advert_name is not None and advert_name != '':
        sql1 += f" and wechat_advert.advert_name like '%%{advert_name}%%'"
        sql2 += f" and dsp_advert.advert_name like '%%{advert_name}%%'"

    if material_name is not None and material_name != '':
        sql1 += f" and wechat_material.material_name like '%%{material_name}%%'"
        sql2 += f" and dsp_material.material_name like '%%{material_name}%%'"

    wechat_adverts = get_sql(sql1, market)
    l1 = [item['id'] for item in wechat_adverts]

    dsp_adverts = get_sql(sql2, market)
    l2 = [item['id'] for item in dsp_adverts]
    if channel == 1:
        print(sql1)
        return l1

    if channel == 2:
        print(sql2)
        return l2
        print(sql2)
    if channel is None or channel == '':
        return l1 + l2


def get_page(user_id=None, shop_id=None, channel=None, status=None, name=None, startTime=None, endTime=None):
    sql1 = f"select id from wechat_popularize_page where user_id={user_id} and is_delete=0"
    sql2 = f"select id from dsp_popularize_page where user_id={user_id} and remove=0"
    if shop_id is not None and shop_id != '':
        sql1 += f" and shop_id={shop_id}"
        sql2 += f" and shop_id={shop_id}"

    if status == 'enable':
        sql1 += f" and administrator_id is not NULL"
        sql2 += f" and popularize_status in ('enable','auditAccepted')"

    if status == 'auditRejected':
        sql1 += f" and administrator_id='auditRejected'"
        sql2 += f" and popularize_status not in ('enable', 'auditAccepted','auditDoing','edit')"

    if status == 'auditDoing':
        sql1 += f" and administrator_id is NULL"
        sql2 += f" and popularize_status in ('auditDoing')"

    if status == 'edit':
        pass

    if name is not None and name != '':
        sql1 += f" and popularize_name like '%%{name}%%'"
        sql2 += f" and popularize_name like '%%{name}%%'"

    if startTime is not None and startTime != '':
        sql1 += f" and create_time>='{startTime}'"
        sql2 += f" and create_time>='{startTime}'"

    if endTime is not None and endTime != '':
        sql1 += f" and create_time<='{endTime}'"
        sql2 += f" and create_time>='{startTime}'"

    wechat_page = get_sql(sql1, market)
    l1 = [item['id'] for item in wechat_page]

    dsp_page = get_sql(sql2, market)
    l2 = [item['id'] for item in dsp_page]
    if channel == 1:
        print(sql1)
        print(l1)
        return l1

    if channel == 2:
        print(l1)
        print(sql2)
        return l2
        print(sql2)
    if channel is None or channel == '':
        print(l1)
        print(l2)
        return l1 + l2


def get_sms_plan(user_id=None, params=None):
    sql = f"select * from plan inner join material on plan.material_id=material.id where plan.user_id={user_id}"

    if params['shopId'] is not None and params['shopId'] != "" and params['shopId'] != 0:
        sql += f" and material.shop_id={params['shopId']}"

    if params['name'] is not None and params['name'] != "":
        sql += f" and  plan.name like '%%{params['name']}%%'"

    if params['putScene'] is not None and params['putScene'] != "":
        sql += f" and plan.put_scene='{params['putScene']}'"

    if params['putStatus'] is not None and params['putStatus'] != "":
        sql += f" and plan.put_status='{params['putStatus']}'"

    if params['startDate'] is not None and params['startDate'] != "":
        sql += f" and plan.gmt_create>='{params['startDate']}'"

    if params['endDate'] is not None and params['endDate'] != "":
        sql += f" and plan.gmt_create<='{params['endDate']}'"

    print(sql)
    plan_list = get_sql(sql, market)
    return plan_list


def get_sms_material(user_id=None, params=None):
    sql = f"select * from material where user_id={user_id} and is_delete='NOT_DELETE'"
    if params['shopId'] is not None and params['shopId'] != "" and params['shopId'] != 0:
        sql += f" and shop_id={params['shopId']}"

    if params['name'] is not None and params['name'] != "":
        sql += f" and name like '%%{params['name']}%%'"

    if params['auditStatus'] is not None and params['auditStatus'] != "":
        sql += f" and audit_status='{params['auditStatus']}'"

    if params['gmtStartDate'] is not None and params['gmtStartDate'] != "":
        sql += f" and gmt_create>='{params['gmtStartDate']}'"

    if params['gmtEndDate'] is not None and params['gmtEndDate'] != "":
        sql += f" and gmt_create<='{params['gmtEndDate']}'"

    material_list = get_sql(sql, market)
    return material_list


def get_sms_operation(user_id=None, params=None):
    sql = f"select plan.* from operation_report inner join plan on operation_report.plan_id=plan.id inner join material on plan.material_id=material.id where plan.user_id={user_id} and plan.put_status='DONE'"
    if params['shopId'] is not None and params['shopId'] != "" and params['shopId'] != 0:
        sql += f" and material.shop_id={params['shopId']}"

    if params['planName'] is not None and params['planName'] != "":
        sql += f" and  plan.name like '%%{params['planName']}%%'"

    if params['timeRange'] == "RECENTLY_SEVEN_DAY":
        sql += f" and datediff(plan.gmt_create,now())>=-7"

    if params['timeRange'] == "YESTERDAY":
        sql += f" and datediff(plan.gmt_create,now())=-1"

    if params['timeRange'] == "RECENTLY_THIRTY_DAY":
        sql += f" and datediff(plan.gmt_create,now())>=-30"

    if params['startDate'] is not None and params['startDate'] != "":
        sql += f" and plan.gmt_create>='{params['startDate']}'"

    if params['endDate'] is not None and params['endDate'] != "":
        sql += f" and plan.gmt_create<='{params['endDate']}'"

    operation_list = get_sql(sql, market)
    return operation_list


def get_peoplepackage_list(user_id=None, params=None):
    sql = f"select * from people_package where user_id=6 and ori_type!='AI_PACKAGE'"
    if params['status'] is not None and params['status'] != "":
        sql += f" and status='{params['status']}'"

    if params['name'] is not None and params['name'] != "":
        sql += f" and name like '%%{params['name']}%%'"

    if params['beginDate'] is not None and params['beginDate'] != "":
        sql += f" and gmt_create>='{params['beginDate']}'"

    if params['endDate'] is not None and params['endDate'] != "":
        sql += f" and gmt_create<='{params['endDate']}'"

    package_list = get_sql(sql, market)
    return package_list


if __name__ == "__main__":
    l = get_page(user_id=6, startTime='2021-01-31 17:55:26', endTime='2021-03-02 17:55:26')
    print(l)
    print(len(l))
