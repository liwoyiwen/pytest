import pytest
import os
if __name__ == '__main__':
    # pytest.main(['--html=report/reportname.html','./test/test_01.py',"./test2/"])
    # pytest.main(['-s','-q','--alluredir','./report/xml', 'test_01.py'])

    # pytest.main(["-s",'./test/','./test2/'])
    # pytest.main(["--html=report/reportname.html", "--env=test",'./test/'])

    #pytest.main(["--html=report/reportname.html", './test/test_sceneAndGoods.py','-n=1'])
    os.environ['--env']='test'
    #pytest.main(["-s", './test/test_appCircle.py', '-n=1'])
    pytest.main(["--html=report/reportname.html", "--env=test", './test/test_appCircle.py'])