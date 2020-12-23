import pytest






if __name__=='__main__':
    #pytest.main(['--html=report/reportname.html','./test/test_01.py',"./test2/"])
    #pytest.main(['-s','-q','--alluredir','./report/xml', 'test_01.py'])

    #pytest.main(["-s",'./test/','./test2/'])
    pytest.main(["--html=report/reportname.html", './test/'])

    #pytest.main(["-s", './test/'])





