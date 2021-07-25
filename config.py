from configparser import ConfigParser
import toml
import os

class WebConfig:

    def __init__(self):

        file = open("web_config.toml",mode="rb")
        content = file.read()
        if content.startswith(b'\xef\xbb\xbf'):
            content=content[3:]
        self.config = toml.loads(content.decode("utf-8"))
  

    #得到配置文件信息  
    def get_info(self,tier_1="",tier_2="",tier_3=""):

        if tier_2 == "" and tier_3 == "":
            return self.config[tier_1]
        if tier_3 == "":
            return self.config[tier_1][tier_2]
        if tier_1 != "" and  tier_2 != "" and tier_3 !="":
            return self.config[tier_1][tier_2][tier_3]

        pass

    #获取用户信息
    def get_user_info(self):

        user = self.config["account_configs"]["user_info"]

        return user

    #获取相关活动
    def get_activity(self,name):

        activity = self.config["request_configs"][name+"_activity"]

        return activity
    
    #获取活动对应的perations
    def get_operations(self,name,activity):

        operations = activity[name+"_operations"]
        
        return  operations

   

    #获取cookie相关
    def get_web_cookie(self):

        results = self.config["request_configs"]["web_cookie"]

        return  results

    def get_sections(self,section):

        results = self.config["request_configs"][section]

        return results
    def get_request_configs(self):

        results = self.config["request_configs"]

        return results

        
class AppConfig:

    def __init__(self):

        file = open("app_config.toml",mode="rb")
        content = file.read()
        if content.startswith(b'\xef\xbb\xbf'):
            content=content[3:]
        self.config = toml.loads(content.decode("utf-8"))
  

    #得到配置文件信息  
    def get_info(self,tier_1="",tier_2="",tier_3=""):

        if tier_2 == "" and tier_3 == "":
            return self.config[tier_1]
        if tier_3 == "":
            return self.config[tier_1][tier_2]
        if tier_1 != "" and  tier_2 != "" and tier_3 !="":
            return self.config[tier_1][tier_2][tier_3]

        pass

    #获取用户信息
    def get_user_info(self):

        user = self.config["account_configs"]["user_info"]

        return user

    #获取相关活动
    def get_activity(self,name):

        activity = self.config["request_configs"][name+"_activity"]

        return activity
    
    #获取活动对应的perations
    def get_operations(self,name,activity):

        operations = activity[name+"_operations"]
        
        return  operations

   

    #获取cookie相关
    def get_web_cookie(self):

        results = self.config["request_configs"]["web_cookie"]

        return  results

    def get_sections(self,section):

        results = self.config["request_configs"][section]

        return results
    def get_request_configs(self):

        results = self.config["request_configs"]

        return results
