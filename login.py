from time import sleep
from selenium import webdriver
from webVerification import SlidingVerification
from selenium.webdriver.support.ui import WebDriverWait
from helper import Helper
from log import Log
import requests
import config as cf
import re


class WebLogin:
    def __init__(self):

        #用于进cookie验证的url
        self.check_coookie_guanjia = 'https://graph.qq.com/user/get_user_info?oauth_consumer_key=101478239&access_token={access_token}&openid={openid}&format=json'
        self.check_coookie_qzone = 'https://user.qzone.qq.com/{account}'

        config = cf.WebConfig()

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.binary_location="chromium\\chrome.exe"
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])  # 禁用系统日志
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(10)  # 全局查找元素5秒隐式等待
        self.driver.maximize_window()
        self.config = config
        user = config.get_user_info()
        self.user = user
        self.account = user[0]["account"]
        self.password = user[0]["password"]

        self.web_cookie = config.get_info("request_configs","web_cookie")

    #判断cookie是否过期

    def is_late_cookie(self,item):
        
        Log.node("验证 "+ item["url"] +" cookie是否过期")

        f = open(item["file"])
        cookieStr = f.read()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400",
            "Cookie": cookieStr
        }

        if item["domain"] == "guanjia":

            p = re.compile(r"TC_MK=(.*?);",re.S)
            access_token = re.search(p,cookieStr).group(1)
            p = re.compile(r"__qc__openid=(.*?);",re.S)
            openid = re.search(p,cookieStr).group(1)
            url = self.check_coookie_guanjia.format(access_token=access_token,openid=openid)

            res = requests.get(
                url, headers=headers)
            code = res.text.find(self.user[0]["name"])

            if code == -1:
                return True     #过期
            else:
                return False    #没过期

        if item["domain"] == "qzone":

            p =re.compile(r"ptui_loginuin=(.*?);",re.S)
            cookie_account = re.search(p,cookieStr).group(1)
            url = self.check_coookie_qzone.format(account=cookie_account)
            res = requests.get(
                url, headers=headers)
 
            code = res.text.find(self.user[0]["name"])
            if code == -1:
                return True     #过期
            else:
                return False    #没过期

    def Login(self):

        Log.title("用户信息")
        Log.info("用户名         "+self.user[0]["name"])
        Log.info("账号         "+self.user[0]["account"])
       

        Log.title("cookie检查")
        Log.node("检查是否需要重新登录获取cookie")

        #检查是否存在cookie文件
        isLogin = False
        for item in self.web_cookie:
            if Helper.file_exists(item["file"]) == False:
                isLogin = True
                break
            
        if isLogin:
            
            for item in self.web_cookie:
                
                if item["is_get_cookie"] == True:
                    self.Login_Web(item)
                    #保存使用同一cookie的其他网站cookie
                    for it in self.web_cookie:
                        if it["is_get_cookie"] == False and it["cookie_type"] == item["cookie_type"] :
                            self.driver.get(it["url"])
                            Log.node("保存 " + it["url"] + " cookie 到本地")
                            
                            sleep(5)

                            cookieStr = self.driver.execute_script("return  document.cookie")
                            f = open(it["file"], "w")
                            f.write(cookieStr)
                            f.close()
                            Log.node("保存完毕")
        else:

            for item in self.web_cookie:
                if item["is_get_cookie"] == True:
                    if self.is_late_cookie(item):
                        self.Login_Web(item)
                        #保存使用同一cookie的其他网站cookie
                        for it in self.web_cookie:
                            if it["is_get_cookie"] == False and it["cookie_type"] == item["cookie_type"] :
                                self.driver.get(it["url"])
                                Log.node("保存 " + it["url"] + " cookie 到本地")

                                sleep(5)

                                cookieStr = self.driver.execute_script("return  document.cookie")
                                f = open(it["file"], "w")
                                f.write(cookieStr)
                                f.close()
                                Log.node("保存完毕")
           

        self.driver.quit()
        pass

    #登录QQ空间获取cookie并保存到本地

    def Login_Web(self,web_cookie):

        self.driver.switch_to_default_content()

        Log.title("登录   "+web_cookie["url"])
        Log.node("正在跳转到登录页面")

        self.driver.get(web_cookie["url"])
        #是否需要点击登陆按钮
        if web_cookie["login_btn"] !="":
            self.driver.find_element_by_id(web_cookie["login_btn"]).click()


        #跳转进入账号密码登录按钮所在iframe
        for item in web_cookie["loginer"]:
            self.driver.switch_to_frame(item)

        #点击账号密码登录
        self.driver.find_element_by_id("switcher_plogin").click()

        Log.node("输入账号名和密码")
        u = self.driver.find_element_by_id('u')
        p = self.driver.find_element_by_id('p')
        u.clear()
        u.send_keys(self.account)
        p.clear()
        p.send_keys(self.password)
        sleep(1)

        self.driver.find_element_by_id('login_button').click()
        Log.node("开始登录等待页面加载...")
        sleep(2)

        Log.node("判断是否需要进行滑动验证")

        varif = SlidingVerification(self.driver)  # 滑动验证对象

        ele_id = web_cookie["verifyer"][len(web_cookie["verifyer"])-1]
        
        # ele = self.driver.find_element_by_id(ele_id)

        if self.ele_exists(ele_id) == True:
            
            varif.Verification(web_cookie["verifyer"])
            sleep(2)

        self.driver.switch_to.default_content()


        Log.node("判断是否需要短信验证")

        if self.ele_exists("login_frame") == True:

            self.driver.switch_to_frame(
                self.driver.find_element_by_id('login_frame'))
            el = self.driver.find_elements_by_id("verify")

            if Helper.ele_exists(el) == True:

                self.driver.switch_to_frame(el[0])
                self.driver.find_elements_by_class_name("get-sms")[0].click()
                Log.node("已点击发送验证码请注意查收...")
                Log.node("输入收到的短信验证码")
                x = input()

                self.driver.find_elements_by_tag_name(
                    "input")[0].send_keys(str(x))

                self.driver.find_elements_by_class_name("submit")[0].click()



        Log.node("完成登录操作")

        
   
        Log.node("保存 " + web_cookie["url"] + " cookie 到本地")
        sleep(5)
        cookieStr = self.driver.execute_script("return  document.cookie")
        f = open(web_cookie["file"], "w")
        f.write(cookieStr)
        f.close()

        self.driver.switch_to_default_content()

        pass

  
    def ele_exists(self,ele_id):

        try:
            self.driver.find_element_by_id(ele_id)
            return True
        except:
            return False
