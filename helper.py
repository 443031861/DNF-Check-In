
import time,datetime
import os,sys
import binascii
from log import Log
import importlib
import re
import json
import jsonpath
from urllib import parse


class Helper:
    
    #url编码
    @staticmethod
    def decode_url(text,count):
        for i in range(count):
            text = parse.quote(text)
        return text


    @staticmethod
    def Alert(driver):
        try:
            dig_alert = driver.switch_to.alert
            dig_alert.text
            return dig_alert
        except Exception:
            return False
    #判断元素是否存在

    @staticmethod
    def ele_exists(ele):
        if len(ele) == 1:
            return True
        else:
            return False
    #格式化 js代码获取cookie字符串为JSON

    @staticmethod
    def js_getcookie(cookie):
        cookieArr = cookie.split(";")
        obj = {}
        for o in cookieArr:
            arr = o.split("=")
            key = str(arr[0]).replace(" ", "")
            obj[key] = arr[1]
        return obj

    #检查活动是否过期    
    @staticmethod
    def isEnd(end_time):

        if Helper.temporal_comparison(end_time)==True:
            Log.node("活动正在进行中...")
            return False
        else:
            Log.hint("活动已经过期")
            return True


    #读取请求需要的参数文本
    @staticmethod
    def get_request_para_text():

        f = open("data\\request_para.json",encoding="utf-8",errors='ignore')
        text = f.read()
        f.close()

        return text


    #读取大区数据 通过 区名 返回 大区id
    @staticmethod
    def get_areaid(area_name):
        f = open("reference_data\\DNF大区数据.json",encoding="utf-8",errors='ignore')
        area_json =  f.read()
        f.close()
        area_json = json.loads(area_json)
        result = jsonpath.jsonpath(area_json,'$..opt_data_array[?(@.t=="'+ area_name +'"])')
        user_areaName = result[0]["v"]

        return user_areaName
    #获取lol数据，返回许愿道聚的id 列表
    @staticmethod
    def get_lol_info():
        f = open("reference_data\\LOL许愿道聚数据.json",encoding="utf-8",errors='ignore')
        area_json =  f.read()
        f.close()
        area_json = json.loads(area_json)
        result = jsonpath.jsonpath(area_json,'$..propId')
        return result

    #比较时间
    @staticmethod
    def temporal_comparison(end_time):
        Log.node("判断活动是否过期")

        #当前时间
        Current_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Log.node('当前时间      ' + Current_Time)
        Current_Time_int = int(time.mktime(
            time.strptime(Current_Time, "%Y-%m-%d %H:%M:%S")))

        #活动结束时间
        Start_Time = end_time + ' 23:59:59'
        Log.node('活动结束时间  ' + Start_Time)
        Start_Time_int = int(time.mktime(
            time.strptime(Start_Time, "%Y-%m-%d %H:%M:%S")))

        #对比
        if Current_Time_int > Start_Time_int:
            Log.node("当前时间大于活动结束时间")
            #相差多少天
            Days = str((datetime.datetime.fromtimestamp(
                Current_Time_int)-datetime.datetime.fromtimestamp(Start_Time_int)).days)
            Log.node("当前时间-活动结束时间相差(天)  -" + Days)

            #相差多少秒
            Seconds1 = (datetime.datetime.fromtimestamp(
                Current_Time_int)-datetime.datetime.fromtimestamp(Start_Time_int)).seconds
            Seconds2 = int(Days)*24*3600
            Seconds = Seconds1 + Seconds2
            # Log.node("当前时间-活动结束时间相差(秒): " + str(Seconds))
            return False

        elif Current_Time_int == Start_Time_int:
            Log.node("当前时间等于活动结束时间")
            return False
        else:
            Log.node("当前时间小于活动结束时间")
            #相差多少天
            Days = str((datetime.datetime.fromtimestamp(Start_Time_int) -
                        datetime.datetime.fromtimestamp(Current_Time_int)).days)
            Log.node("当前时间-活动结束时间相差(天)  " + Days)
            #相差多少秒
            Seconds1 = (datetime.datetime.fromtimestamp(
                Start_Time_int)-datetime.datetime.fromtimestamp(Current_Time_int)).seconds
            Seconds2 = int(Days)*24*3600
            Seconds = Seconds1 + Seconds2
            # Log.node("当前时间-活动结束时间相差(秒): " + str(Seconds))
            return True
    

    #传入类 和 方法名，执行该方法
    @staticmethod
    def exec_function(file_name,class_name,fun_name,op_name,para):
        
        module = importlib.import_module(file_name)
        ob = getattr(module,class_name)()
        result = getattr(ob,fun_name)(op_name,para)

        return result


    #判断文件是否存在
    @staticmethod
    def file_exists(src):
        return os.path.exists(src)


    #判断Json对象中是否存在某属性Key
    @staticmethod
    def isKeyInJson(jsonObj,para):
        if para in jsonObj:
            return True
        else:
            return False

    #计算返回formdata中的g_gk
    @staticmethod
    def getGtk(sKey):

        hash = 5381
        for key in sKey:
            hash += (hash << 5) + ord(key)
            g_tk = hash & 2147483647

        return g_tk

    #get 回调str 转 json对象
    @staticmethod
    def callback2json(s):

        result = re.sub(r"\n|\t","",s)
        result = re.findall(r"[(](.*?)[)]",result)
        result= json.loads(result[0])
        
        return result




    # #16进制转字符串
    # @staticmethod
    # def hexToStr(data):
    #     result = binascii.unhexlify(data)
    #     return result
    
    # #字符串转16进制
    # @staticmethod
    # def strToHex(data):
    #     data = bytes(data,encoding='utf-8')
    #     return binascii.hexlify(data)
    # #
    # @staticmethod
    # def QQLoginEncrypt(p,u,c,md5=""):
    #     hexu = Helper.strToHex(u)
    #     md5p = md5(p)
    #     clen = "000"+len(c)
    #     binc= Helper.strToHex(c.upper())
    #     key = Helper.hexToStr(md5p+hexu).upper()
    #     data = md5p.upper()+hexu+clen+binc
    #     pass


