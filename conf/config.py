import configparser
import os
import ast

configPath = os.path.join(os.path.dirname(__file__), "config.ini")


class ReadConfig1:
    def __init__(self, env):
        self.config = configparser.ConfigParser()
        self.config.read(configPath)
        self.env = env

    def get_conf(self, param):
        value = self.config.get(self.env, param)
        return value

    def get_headers(self):
        value = self.config.get(self.env, "headers")
        return ast.literal_eval(value)

    def get_baseUrl(self):
        value = self.config.get(self.env, "url")
        return value

    def set_conf(self, param, value):
        self.config.set(self.env, param, value)
        with open(configPath, 'w+') as f:
            return self.config.write(f)


class ReadConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(configPath)
        # self.env = os.getenv('--env')
        #os.environ['--env'] = 'test'
        self.env = 'test'

    def get_conf(self, param):
        value = self.config.get(self.env, param)
        return value

    def get_headers(self):
        value = self.config.get(self.env, "headers")
        return ast.literal_eval(value)

    def get_baseUrl(self):
        value = self.config.get(self.env, "url")
        return value

    def set_conf(self, param, value):
        self.config.set(self.env, param, value)
        with open(configPath, 'w+') as f:
            return self.config.write(f)


if __name__ == "__main__":
    pass
