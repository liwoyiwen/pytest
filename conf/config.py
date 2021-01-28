import configparser
import os
import ast
configPath=os.path.join(os.path.dirname(__file__),"config.ini")




class Read_config:
    def __init__(self,env):
        self.config=configparser.ConfigParser()
        self.config.read(configPath)
        self.env=env

    def get_conf(self,param):
        value=self.config.get(self.env,param)
        return value



    def get_headers(self):
        value=self.config.get(self.env,"headers")
        return ast.literal_eval(value)

    def get_baseUrl(self):
        value=self.config.get(self.env,"url")
        return value


    def set_conf(self,param,value):
        self.config.set(self.env,param,value)
        with open(configPath,'w+') as f:
            return self.config.write(f)

if __name__=="__main__":
    read_config=Read_config("tecent")

    read_config.set_conf("name","woyanan1")
