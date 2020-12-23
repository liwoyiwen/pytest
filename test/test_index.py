import pytest

class TestIndex:
    def test_info(self,info):
        res=info
        assert res.status_code==200
        assert res.json()['status']==0



    @pytest.mark.parametrize("message",{
            "pageNumber":1,
            "pageSize":20,
            "remainWay":"STRONG",
            "hasRead":"NO"
        })
    def test_message(self,message):
        res=message
        assert res.status_code == 200
        assert res.json()['status'] == 0





    def test_judgeAllHasRead(self,judgeAllHasRead):
        res=judgeAllHasRead
        assert res.status_code == 200
        assert res.json()['status'] == 0


    def test_shoplist(self,shoplist):
        res=shoplist
        assert res.status_code == 200
        assert res.json()['status'] == 0
