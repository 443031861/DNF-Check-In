# -*- coding:utf-8 -*-
import task
from login import WebLogin
from log import Log
import time
import requests
from urllib import parse
import json
from requests import request
from selenium import webdriver
from helper import Helper
import config  
import toml
import re
import requests
import jsonpath
import network
import login
import datetime


class main:

    if __name__=="__main__":

        # 登录
        login =login.WebLogin()
        login.Login()

        # 执行请求
        task_web = task.WebTask()
        task_web.exec_post_tasks()  #心悦相关活动

        # task_web.exec_get_tasks()  #空间相关活动

        # s = '{"ret":"600","msg":"非常抱歉，您的资格已经用尽！","flowRet":{"iRet":"600","sLogSerialNum":"AMS-DJ-0112213517-5gNjFW-11117-324410","iAlertSerial":"0","sMsg":"不好意思，每天只有一次获取聚豆的机会，明天再来吧"}}'
        # v = json.loads(s)
  

        # task_app = task.AppTask()
        # task_app.exec_post_tasks()

        Log.title("完成签到和奖励领取")

        # x = input()

        
    
    



