import pytest



@pytest.mark.usefixtures("getheaders")
class TestDemo:
    #@pytest.mark.parametrize("login",[ i for i in range(0,5)],indirect=True)

    def test_one(self,getheaders):
        getheaders['name']="lijunfang"
        assert 34<3

    @pytest.mark.parametrize("index", [i for i in range(0, 10)],indirect=True)
    def test_index(self,index,getheaders):
        print(getheaders['name'])
        print(index.json())

        assert index.status_code==200
        assert index.json()['status']==0





if __name__=='__main__':
    pytest.main(['-s','test_01.py','test_02.py'])

