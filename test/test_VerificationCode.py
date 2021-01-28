from common.read_data import *
import pytest
import requests
import logging
from test.myInit import *

class TestVerificationCode(MyInit):




    datas=get_excel(filename='login_data.xls',sheetName="Verification_code",dtype={"mobile":str})

    @pytest.mark.parametrize("value",datas)
    def test_send(self,value):
        param={
            "mobile":value['mobile']
        }
        msg=value['msg']
        success=value['success']
        url=self.baseUrl+"/api/base/user/getVerification"
        res=requests.post(url=url,headers=self.headers,params=param)
        logging.error(res.json())
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
        if msg != '':
            assert res.json()['msg'] == msg




