from sqlalchemy import create_engine
from common.read_data import *

market = create_engine('mysql+pymysql://lijunfang:REmq4ofAABMzRKp2@192.168.100.166/market?charset=utf8',
                       encoding='utf-8')
base = create_engine('mysql+pymysql://lijunfang:REmq4ofAABMzRKp2@192.168.100.166/base?charset=utf8', encoding='utf-8')
analysis = create_engine('mysql+pymysql://lijunfang:REmq4ofAABMzRKp2@192.168.100.166/analysis?charset=utf8',
                         encoding='utf-8')


def get_people_package(name=None):
    people_package = get_sql(f"select * from people_package where name='{name}'", market)[0]
    return people_package


def get_plan(name=None):
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
