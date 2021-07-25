from helper import Helper 
from login import WebLogin
from time import sleep
import requests
import datetime
import config 
from log import Log
import importlib
import network
import json


class WebTask:

    def __init__(self):
        self.Req=None
        self.config = config.WebConfig()

    #执行get请求方式的任务
    def exec_get_tasks(self):


        arr = self.config.get_info("request_configs","web_cookie")
            
        for activity in arr:

            if activity["request_type"]=="get":

                ls = self.config.get_info("request_configs",activity["domain"]+"_activity")

                for item in ls:

                    Log.title(item["name"]+"      "+item["url"])
                    
                    if Helper.isEnd(item["end_time"])==False:

                        #设置请求数据
                        req =network.WebGet()

                        for option in item[activity["domain"]+"_operations"]:
                
                            if activity["domain"] == "qzone":
                                Log.info(option["name"]+":  "+req.get_request(activity["domain"],"",option["actid"],option["ruleid"],option["uin"],activity["file"],option["delayed"]))
                            if activity["domain"] == "guanjia":
                                Log.info(option["name"]+":  "+req.get_request(activity["domain"],option["giftId"],"","","",activity["file"],option["delayed"]))
        pass


    #执行post请求方式的任务
    def exec_post_tasks(self):

        arr = self.config.get_info("request_configs","web_cookie")
            
        for activity in arr:

            if activity["request_type"]=="post":

                ls = self.config.get_info("request_configs",activity["domain"]+"_activity")

                for item in ls:

                    Log.title(item["name"]+"      "+item["url"])

                    if Helper.isEnd(item["end_time"])==False:

                        #设置请求数据
                        req = network.WebPost(item["iActivityId"],item["iFlowId"],activity["file"],item["set_aree_host"])

                        f = open(activity["file"],"r")
                        cookieStr = f.read()
                        f.close()

                        role_info = network.Get(cookieStr).get_dnf_role_info()  #获取角色信息

                        if item["iFlowId"] != "":
                            #先绑定大区角色
                            k = network.Post(cookieStr,item["iActivityId"],item["iFlowId"],item["set_aree_host"]).set_role_area(role_info)
                            Log.node("绑定成功      "+ role_info["user_areaName"] +" " +role_info["user_roleName"])


                        for option in item[activity["domain"]+"_operations"]:

                            for i in range(option["count"]):

                                Log.info(option["name"]+":  "+req.post_request(activity["domain"],option["iFlowId"],option["delayed"]))
                

        pass


  
class AppTask:

    def __init__(self):
        self.Req=None
        self.config = config.AppConfig()
      


     #执行post请求方式的任务
    def exec_post_tasks(self,):
            
       

        ls = self.config.get_info("request_configs","activity")
        for domain_list in ls:
            if domain_list["run"] == True:

                arr_activity = self.config.get_info("request_configs",domain_list["domain"]+"_activity")
                for it in arr_activity:
                    Log.title(it["name"]+"      "+it["url"])
                    if   Helper.isEnd(it["end_time"])==False:
                    
                        role_info = network.Get(domain_list["app_cookie"]).get_dnf_role_info()  #获取角色信息
                        role_info.update({"uin":domain_list["uin"]})
                        role_info_items = role_info.items()
                        req = network.AppPost(domain_list["app_cookie"],domain_list["domain"],it["iActivityId"],it["iFlowId"],domain_list["user_id"],it["set_aree_host"])
                        if it["iFlowId"] != "":
                            #绑定大区角色
                            
                       
                            network.Post(domain_list["app_cookie"],it["iActivityId"],it["iFlowId"],it["set_aree_host"]).set_role_area(role_info)
                            Log.node("绑定成功      "+ role_info["user_areaName"] +" " +role_info["user_roleName"])
                        else:
                            Log.node("该活动不需要绑定大区，但需要助手绑定角色")    
                        #这里是每个活动下子请求
                        for option in it[domain_list["domain"]+"_operations"]:
                            para = {}
                            it_items = it.items()

                            if option["name"] == "领取每日登陆聚豆":
                                headers={
                                    "Cookie":domain_list["app_cookie"]
                                }
                                sv = requests.get("https://djcapp.game.qq.com/daoju/igw/main/?_service=app.message.imsdk.login",headers=headers)
                            
                            #道聚城任务 道聚许愿需要查询lol角色信息 这里做一下特殊判断 是这个任务就查询一下lol角色信息
                            if option["name"] == "道具许愿":
                                role_info = network.Get(domain_list["app_cookie"]).get_lol_role_info()  #获取角色信息
                                role_info_items = role_info.items()
                                #许愿任务需要的角色参数放进 para
                                if role_info_items != None:
                                    for key2,value2 in role_info_items:
                                        para[key2] = value2
                                option["iGoodsId"] = Helper.get_lol_info()[datetime.date.today().day]

                            if option["name"] == "兑换5个调整箱":
                                role_info = network.Get(domain_list["app_cookie"]).get_dnf_role_info()  #获取角色信息
                                for key1,value1 in role_info.items():
                                    for key2,value2 in option.items():
                                        if option[key2] == key1:
                                            para[key2] = value1


                            if option["request_type"] == "post":
                                #子项需要的公共数据筛选后放入 para
                                for key,value in it_items:
                                    if key != "name" and key !="url" and key != "iFlowId" and key != "end_time" and key != "set_aree_host" and key != domain_list["domain"]+"_operations":
                                        para[key]=value
                                        if role_info_items != None:
                                            for key2,value2 in role_info_items:
                                                if it[key] == key2:
                                                    para[key] = value2
                        
                            #子项数据筛选放入 para
                            option_items = option.items()
                            for key,value in option_items:
                                if key != "name" and key !="count" and key != "delayed" and key != "request_type" and key != "lRoleId" and key != "iZone": #后面两个条件专门为兑换调整箱加得
                                    para[key]=value

                            for i in range(option["count"]):
                                Log.info(option["name"]+":  "+req.request(para,domain_list["domain"],it["set_aree_host"],option["request_type"]))
                                sleep(option["delayed"])

        pass

  