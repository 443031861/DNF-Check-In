import urllib3
import urllib
import re
from helper import Helper
from log import Log
from webVerification import *
from http import cookiejar
from selenium import webdriver
import requests
import json
from time import sleep
import config
import win32api,win32con


#网页
class WebGet:
  
  def __init__(self):
    timestamp = time.time()*1000
    self.get_url = "http://act.guanjia.qq.com/bin/act/comjoin_1121.php?giftId={giftId}&area_id=88&charac_no=22204588&charac_name=%E5%93%BA%E4%B9%B3%E7%9A%84%E5%99%A8%E5%AE%98&callback=jQuery172047199012987159716_"+ str(timestamp)[:13] +"&isopenid=1&_=1609531262835"
    self.get_url_no_giftId = "https://h5.qzone.qq.com/proxy/domain/activity.qzone.qq.com/fcg-bin/fcg_qzact_count?g_tk={g_tk}&r=0.6750271703604405&callback=mallv84_Callback&actid={actid}&ruleid={ruleid}&countid=&uin={uin}&callbackFun=mallv84&_=1610150207204"
    # self.get_url_no_giftId="https://h5.qzone.qq.com/proxy/domain/activity.qzone.qq.com/fcg-bin/fcg_qzact_count?g_tk=1502305648&r=0.06762843182522738&callback=mallv87_Callback&actid=4216&ruleid=29064&countid=&uin=443031861&callbackFun=mallv87&_=1609537007694"
    self.cookieStr=""
    self.headers = {
        "Host":"",
        "Referer":"",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }

  #get请求页面上奖品
  def get_request(self,domain,giftId,actid,ruleid,uin,cookie_file,delayed):

    if domain == "guanjia":
      self.setAllPostParm(domain,giftId,"","","",cookie_file)
      res = requests.get(url=self.get_url,headers=self.headers,timeout=5)
      sleep(delayed)

    if domain == "qzone":
      self.setAllPostParm(domain,"",actid,ruleid,uin,cookie_file)
      res = requests.get(url=self.get_url_no_giftId,headers=self.headers,timeout=5)
      sleep(delayed)

    return self.results(res)


  #设置请求需要的所有参数

  def setAllPostParm(self,domain,giftId,actid,ruleid,uin,cookie_file):

    if domain=="guanjia":
      f = open(cookie_file,"r")
      self.cookieStr = f.read()
      f.close()
      self.get_url = self.get_url.format(giftId=giftId)
      self.headers["Cookie"] = self.cookieStr.encode(encoding="utf-8")
      self.headers["Referer"] = "http://guanjia.qq.com"
    
    if domain == "qzone":
      f = open(cookie_file,"r")
      self.cookieStr = f.read()
      cookie = Helper.js_getcookie(self.cookieStr)  # js获取的cookie字符串 转json对象
      f.close()
      g_tk = Helper.getGtk(cookie['p_skey'])
      actid=actid
      ruleid=ruleid
      uin=uin
      self.get_url_no_giftId = self.get_url_no_giftId.format(g_tk=g_tk,actid=actid,ruleid=ruleid,uin=uin)
      self.headers["Cookie"] = self.cookieStr
      self.headers["Referer"] = "https://act.qzone.qq.com/vip/meteor/blockly/p/6489x47ffe"
      self.headers["Host"] = "h5.qzone.qq.com"
    

  def results(self, res):

    # res = res.text.encode(res.encoding).decode("GB2312")

    return res.text

#网页
class WebPost:

  def __init__(self,iActivityId,iFlowId,cookie_file,host):
 
    f = open(cookie_file,"r")
    self.cookieStr = f.read()
    f.close()
   
    # self.cookie_url = "http://act.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=tgclub&iActivityId=166962&sServiceDepartment=xinyue&sSDID=26ebd6b381f853ff7ecc1def1a43de7a&sMiloTag=AMS-MILO-166962-513581-FDA8F2BD88B65A45B4E82C813C4186C5-1609298471232-0wW9Rk&isXhrPost=true"
    self.post_xinyue_url= "http://act.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=tgclub&iActivityId="+iActivityId+"&sServiceDepartment=xinyue&sSDID=26ebd6b381f853ff7ecc1def1a43de7a&sMiloTag=AMS-MILO-166962-673270-FDA8F2BD88B65A45B4E82C813C4186C5-1609451203156-28K1Is&isXhrPost=true"
    self.post_dnf_url= "https://x6m5.ams.game.qq.com/ams/ame/amesvr?ameVersion=0.3&sServiceType=dnf&iActivityId="+iActivityId+"&sServiceDepartment=group_3&sSDID=382e8e2f9051635a93bf7e27ea01455b&sMiloTag=AMS-MILO-347445-723165-o0443031861-1609451174137-blOy38&isXhrPost=true"
    self.sKey =""
    self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400",
                    'cookie': ""}
    self.post_frome = {
        "sServiceType": "dnf",
        "iActivityId": iActivityId,
        "iFlowId": "",
        "g_tk": ""
    }

  #设置请求需要的所有参数

  def setAllPostParm(self,iFlowId):


    cookie = Helper.js_getcookie(self.cookieStr)  # js获取的cookie字符串 转json对象
    self.sKey = cookie['skey']

    self.post_frome["g_tk"] = Helper.getGtk(self.sKey)
    self.post_frome["iFlowId"] = iFlowId
    self.headers["cookie"] = self.cookieStr
    
    pass

  #请求结果Unicode 转 字符串

  def results(self, res):
    
    res = res.text.encode(res.encoding).decode("utf-8")
    message = json.loads(res)
    result ="【 "+message['flowRet']["sMsg"]+"】"
    if Helper.isKeyInJson(message,"modRet"):
      result += "【 "+message["modRet"]["sMsg"]+"】"

    return result

  #post请求页面上奖品
  def post_request(self,domain,iFlowId,delayed):

    if domain == "dnf":
      self.setAllPostParm(iFlowId)
      res = requests.post(url=self.post_dnf_url, data=self.post_frome,
                          headers=self.headers)
      sleep(delayed)
      # print(res)

    if domain == "xinyue":
      self.setAllPostParm(iFlowId)
      res = requests.post(url=self.post_xinyue_url, data=self.post_frome,
                          headers=self.headers)
      sleep(delayed)
      # print(res)

    return self.results(res)


#下面是App 的 Get 和 Post  其中查询角色和设置到期貌似是通用的

#App
class AppGet:

  def __init__(self,cookie):
      user =config.WebConfig().get_user_info()
      self.user = user[0]
      self.cookie=cookie



class AppPost:

  # cate 参数文件中要读取的类目名称
  def __init__(self,cookie,cate,iActivityId,iFlowId,user_id,host):

      self.iActivityId=iActivityId
      self.iFlowId=iFlowId
      self.user_id=user_id



      #读取参数文件
      self.cookie=cookie
      
      self.config = config.AppConfig()
      # user = self.config.get_user_info()
      # self.user = user[0]
      self.ContentLength=""
      

  #请求页面上的操作
  # domain 参数文件中要读取的类目名称
  def request(self,para,domain,host,request_type):

        #读取助手请求需要的参数
      text = Helper.get_request_para_text()

      request_data=json.loads(text)[domain][request_type]

      #设置请求需要用到的参数
      data = request_data["data"]
      for key,value  in  para.items():
        data[key] = para[key]

      cookie = Helper.js_getcookie(self.cookie)  
      g_tk = Helper.getGtk(cookie['skey'])
 

      #删除没有用到的 value 为空的数据
      for k in list(data.keys()):
        if not data[k]:
          if k == "g_tk" or k == "p_tk":
            data[k] = g_tk
          else:
            del data[k]
        
      
      if request_type == "post":
        url = "https://" + host + "/ams/ame/amesvr?iActivityId=" + para["iActivityId"]
        data = urllib.parse.urlencode(data)
        headers = request_data["headers"]
        headers["Host"]=host
        headers["Content-Length"] = str(len(data))
        headers["Cookie"] = self.cookie
        res = requests.post(url=url,data=data,headers=headers)
        result = self.results(res)
      else:
        get_host=data["host"]
        del data["host"]
        url =  request_data["url"].format(host=get_host)+ urllib.parse.urlencode(data)
        headers = request_data["headers"]
        headers["Host"]=get_host
        headers["Cookie"] = self.cookie
        res = requests.get(url=url,headers=headers)
        result = self.results(res)
     

   

      return result
  
  #设置DNF助手请求需要的参数
  # activity 配置文件中 activity对象
  def setAllPostParm(self,activity):


    cookie = Helper.js_getcookie(self.cookie)  
    g_tk = Helper.getGtk(cookie['skey'])

  
    pass

  def results(self, res):
      res =res.text.encode("utf-8").decode("unicode_escape")
      p = re.compile(r"{(.*)}",re.S)
      res = re.search(p,res).group()
      try:
        message = json.loads(res)
        result ="【 "+message['msg']+" 】"
        if Helper.isKeyInJson(message,"flowRet"):
          result += "【 "+message["flowRet"]["sMsg"]+" 】"
      except:
        return res

      return result



#公共的不区分Web 和 Apps

class Get:

  def __init__(self,cookie):
      user =config.WebConfig().get_user_info()
      self.user = user[0]
      self.cookie=cookie
      try:
        skey = Helper.js_getcookie(cookie)['skey']
      except:
        ##提醒OK消息框
        win32api.MessageBox(0, "app_config.toml 文件中没有配置cookie,程序终止", "提醒",win32con.MB_OK)
        input()
      
      self.g_tk = Helper.getGtk(skey)

  #获取dnf的角色信息
  def get_dnf_role_info(self):

    #这里加载一下查询dnf数据需要的请求参数
    Log.node("查询DNF角色相关信息")
    text =Helper.get_request_para_text()
    request_data=json.loads(text)["role_info"]["dnf"]

    #通过配置文件的area_name 在json文件中查找对应的大区id
    area_id = Helper.get_areaid(self.user["area_name"])

    #配置一下请求url 和 请求头
    url = request_data["url"].format(area_id=area_id)
    request_data["headers"]["Cookie"] = self.cookie
    headers= request_data["headers"]
    res =urllib.parse.unquote(requests.get(url=url, headers=headers).text)

    #这里把返回的角色信息进行正则处理，组装出角色信息对象
    user_md5str = re.search(re.compile(r"md5str:'(.*?)',",re.S),res).group(1)          
    checkparam = re.search(re.compile(r"dnf(.*?)'",re.S),res).group(1)
    user_role_list = re.search(re.compile(r"msg=(.*?)&",re.S),res).group(1).split("|") 

    #这里从返回的角色信息对象中，获取到角色的id
    for item in user_role_list:
      if item.find(self.user["role_name"]) !=-1:
        it = item.split(" ")
        user_roleId = it[0]
        break
    
    #完事可以返回角色数据了
    Log.node("设置绑定大区需要的参数并返回obj")
    obj={
        "user_area":area_id,                                                 #大区id
        "user_md5str":user_md5str,                                           #md5校验码
        "user_roleId":user_roleId,                                           #角色id
        "user_areaName":self.user["area_name"],                              #大区名  
        "user_roleName":self.user["role_name"],
        "user_checkparam":checkparam,                                        #验证串
        "g_tk":self.g_tk
    }    
    return  obj

  #获取lol的角色信息
  def get_lol_role_info(self):

    #这里加载一下查询lol数据需要的请求参数
    Log.node("查询DNF角色相关信息")
    text =Helper.get_request_para_text()
    request_data=json.loads(text)["role_info"]["lol"]

    #暂时没有拿到lol大区数据，这里直接查一区了
    # area_id = "1"   
    cookie = Helper.js_getcookie(self.cookie)  
    p_tk = Helper.getGtk(cookie['skey'])
    url = request_data["url"].format(p_tk=p_tk)

    request_data["headers"]["Cookie"] = self.cookie
    headers= request_data["headers"]
    res =urllib.parse.unquote(requests.get(url=url, headers=headers).text)


    # user_md5str = re.search(re.compile(r'md5str":"(.*?)",',re.S),res).group(1)          
    # checkparam = re.search(re.compile(r'lol(.*?)"',re.S),res).group(1)
    user_role_id =  re.search(re.compile(r"accountId=(.*?)&",re.S),res).group(1)

    obj = {
      "sRoleId" : user_role_id,
      "p_tk":self.g_tk
    }

    return obj



#公共的不区分Web 和 Apps

class Post:

  # cate 参数文件中要读取的类目名称
  def __init__(self,cookie,iActivityId,iFlowId,host):
      self.cookie=cookie
      self.iActivityId=iActivityId
      self.iFlowId=iFlowId
      self.host = host
      
  #设置DNF角色大区
  #obj 查询角色信息返回的对象 还 添加了配置文件中的一些信息
  #cate  参数json中 set_area 下的 子对象名称
  def set_role_area(self,obj):

      # 这里对user_checkparam这个参数进行 urlcode转码，中文要转3次 这里先转2次
      user_checkparam=""
      string ="|*0123456789"
      for i in obj["user_checkparam"]:
          if i in string:
              user_checkparam += Helper.decode_url(i,1)
          else:
              user_checkparam += Helper.decode_url(i,2)


      #读取参数 json文件
      text = Helper.get_request_para_text()
      data = self.request_data=json.loads(text)["set_area"]["post"]["data"]
      headers = self.request_data=json.loads(text)["set_area"]["post"]["headers"]

      #把必要的参数放到 post请求的body里
      dic = ["dnf",obj["user_area"],obj["user_roleId"],"dnf"+user_checkparam,obj["user_md5str"],self.iActivityId,self.iFlowId,obj["g_tk"]]
      items = data.items()
      i=0
      for key,value in items:
        data[key]=dic[i]
        i+=1
      
      #这里转最后一次码，顺便把 json 转成 urlcode 字符串
      data = urllib.parse.urlencode(data)

      #设置请求头的参数
      self.ContentLength =str(len(data))
      headers["Host"] = self.host
      headers["Cookie"] = self.cookie
      headers["Content-Length"] = self.ContentLength
    
      url = "https://"+self.host+"/ams/ame/amesvr?iActivityId="+self.iActivityId
      pos = requests.post(url=url,data=data,headers=headers).text

      return pos

  #格式化一下返回数据用于显示
  def results(self, res):

      res = res.text.encode(res.encoding).decode("utf-8")

      return res
 
