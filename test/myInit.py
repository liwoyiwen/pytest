from conf.config import *
import os

class MyInit:
    def setup_class(self):
        envs=os.environ.get("--env")
        print(envs)
        read_config=Read_config("test")
        self.shopId = read_config.get_conf('shopId')
        self.categoryId=read_config.get_conf("categoryId")
        self.launchPeople = read_config.get_conf('launchPeople')
        self.peoplePackageName = read_config.get_conf('peoplePackageName')
        self.peoplePackageNumber = read_config.get_conf('peoplePackageNumber')
        self.headers = read_config.get_headers()
        self.baseUrl=read_config.get_baseUrl()

    def teardown_class(self):
        pass