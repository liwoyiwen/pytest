from common.read_data import *
import pytest
import requests
import logging
from test.myInit import *


class TestVerificationCode(MyInit):
    code_data = get_excel(filename='login_data.xls', sheetName="Verification_code", dtype={"mobile": str})

    @pytest.mark.parametrize("value", code_data)
    def test_send(self, value):
        url = self.baseUrl + "/api/base/user/getVerification"
        param = {
            "mobile": value['mobile']
        }
        msg = value['msg']
        success = value['success']
        res = requests.post(url=url, headers=self.headers, params=param)
        logging.error(res.json())
        print(res.json())
        assert res.status_code == 200
        assert res.json()['success'] == success
        if msg != '':
            assert res.json()['msg'] == msg
