import csv
from common.utils import *
import codecs
import ast
import os
import pandas as pd
from datetime import datetime
import json
from common.mysql_engine import *
def get_csv(filename,fields):
    datas = []

    data_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'data', filename)
    with codecs.open(data_path, 'r', encoding='gbk') as fp:
        keys = csv.reader(fp)
        for csv_key in keys:
            csv_reader = csv.DictReader(fp, csv_key)
            print(csv_key)
            for row in csv_reader:
                row.update((key, conversion(row[key])) for key, conversion in fields)
                datas.append(dict(row))



    return datas






def get_excel(filename="test_data.xls",sheetName=None,converters=None,dtype=None):
    data_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'data', filename)
    df=pd.read_excel(data_path,sheet_name=sheetName,converters=converters, dtype=dtype,keep_default_na=False)
    print(df.dtypes)
    test_data=df.to_dict(orient='records')

    return test_data



def get_sql(sql,con):
    df=pd.read_sql(sql,con=con)
    test_data = df.to_dict(orient='records')
    return test_data
    print(test_data[0]["tencent_material_id"])


if __name__=="__main__":
    datas = get_excel(filename="dsp_data.xls", sheetName="ad_data", converters={

    })
    print(datas)





