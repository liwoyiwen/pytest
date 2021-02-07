
import os
import pandas as pd

def get_excel(filename="test_data.xls", sheetName=None, converters=None, dtype=None):
    data_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'data', filename)
    df = pd.read_excel(data_path, sheet_name=sheetName, converters=converters, dtype=dtype, keep_default_na=False)
    print(df.dtypes)
    test_data = df.to_dict(orient='records')

    return test_data


def get_sql(sql, con):
    df = pd.read_sql(sql, con=con)
    test_data = df.to_dict(orient='records')
    return test_data


if __name__ == "__main__":
    data = get_excel(filename="dsp_data.xls", sheetName="ad_data", converters={

    })
    print(data)
