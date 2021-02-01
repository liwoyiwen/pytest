from sqlalchemy import create_engine

market=create_engine('mysql+pymysql://lijunfang:REmq4ofAABMzRKp2@192.168.100.166/market?charset=utf8',encoding='utf-8')
base=create_engine('mysql+pymysql://lijunfang:REmq4ofAABMzRKp2@192.168.100.166/base?charset=utf8',encoding='utf-8')
analysis=create_engine('mysql+pymysql://lijunfang:REmq4ofAABMzRKp2@192.168.100.166/analysis?charset=utf8',encoding='utf-8')
