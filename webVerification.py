from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from log import Log
from PIL import Image
from six import BytesIO
from cv2 import cv2 as cv
from selenium.webdriver import ActionChains
import time
import numpy as np
import uuid


x_offset=31 #验证码滑块偏移量

class SlidingVerification:

    def __init__(self,driver):
        self.verifyer = None
        self.driver=driver
        self.count=1



    def get_url(self,url, user, password):
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.ID, 'dologin')))
        driver.find_element_by_id('dologin').click()
        time.sleep(2)
        driver.switch_to_frame(driver.find_element_by_id('login_frame'))
        driver.find_element_by_id("switcher_plogin").click()
        user_input = driver.find_element_by_id('u')
        pwd_input = driver.find_element_by_id('p')
        btn = driver.find_element_by_id('login_button')
        user_input.send_keys(user)
        pwd_input.send_keys(password)
        time.sleep(1)
        btn.click()
        time.sleep(0.5)
        return driver

    #获取滑动验证图片在浏览器的位置

    
    def get_position(self,verifyer):

        self.driver.switch_to_default_content()

        x,y=0,0

        for item in verifyer:

            ele = self.driver.find_element_by_id(item)  
            location = ele.location
            x = x + location['x']
            y = y + location['y']
            self.driver.switch_to_frame(self.driver.find_element_by_id(item))
        
        ele = self.driver.find_element_by_id('slideBg')  
        location = ele.location
        x = x + location['x']
        y = y + location['y']
        
        size = ele.size
        top, bottom, left, right = y, y + size['height'], x, x + size[
            'width']
        # print("验证图片在游览器中的位置:"+str(x)+','+str(y))
        # print("验证图片元素宽高:"+str(size['width'])+','+str(size['height']))

        self.driver.switch_to_default_content()

        return (left, top, right, bottom)

    #获取整个浏览器的截图。并从内存进行读取

    
    def get_screenshot(self):
        screenshot = self.driver.get_screenshot_as_png()
        f = BytesIO()
        f.write(screenshot)
        self.driver.get_screenshot_as_file(".\\screenshot\\test.png")
        return Image.open(f)

    #通过对比截图和浏览器宽高的大小，算出换算比例。
    #由于截图是有浏览器的边缘的拖拽条，所以有边缘的浏览器的宽度+10px

    
    def get_position_scale(self, screen_shot):
        height = self.driver.execute_script(
            'return document.documentElement.clientHeight')
        width = self.driver.execute_script(
            'return document.documentElement.clientWidth')
        # print("游览器的宽高:"+str(width)+","+str(height))
        # print("截取图片的宽高:"+str(screen_shot.size[0])+","+str(screen_shot.size[1]))
        x_scale = screen_shot.size[0] / (width)
        y_scale = screen_shot.size[1] / (height)
        # print("宽高比例:"+str(x_scale)+","+str(y_scale))
        return (x_scale, y_scale)

    #截取有缺口的滑动图片

  
    def get_slideimg_screenshot(self,screenshot,position,scale):
        x_scale,y_scale = scale
        position = [position[0] * x_scale, position[1] * y_scale, position[2] * x_scale, position[3] * y_scale]
        #position=[60,80,500,300]
        # print("截图验证图片的位置："+ str(position))
        img = screenshot.crop(position)
        img.save(".\\screenshot\\quyue.png")
        return img
  
  
  

    #计算出滑动的轨迹

    
    def get_track(self,distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正 2
                a = 4
            else:
                # 加速度为负 3
                a = -3
            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    #进行移动

 
    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

  

    def get_pos(self,image,verifyer):

        self.driver.switch_to_default_content()

        Log.node("正在进行第 "+ str(self.count) +" 次尝试")
        mgray = cv.cvtColor(image,cv.COLOR_BGR2GRAY) #彩色转灰度
        blurred = cv.GaussianBlur(mgray,(5, 5), 0)
        canny = cv.Canny(blurred, 50, 80)
        # cv.imshow('canny',canny)
        # cv.waitKey(0)
        
        contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #找轮廓
        cv.drawContours(image,contours,-1,(0,0,255),3)
        # cv.imshow('image',image)
        # cv.waitKey(0)
        for i, contour in enumerate(contours):
            # print("---------------------")
            M = cv.moments(contour)
            if M['m00'] == 0:
                cx = cy = 0
            else:
                cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            if 1000 < cv.contourArea(contour) < 1350 and 150 < cv.arcLength(contour, True) < 160:
                if cx < 210:
                    continue
                x, y, w, h = cv.boundingRect(contour) # 外接矩形
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 150, 255), 2)
                cv.imwrite("dst\\ccc.png",image)
                # cv.imshow('image', image)
                Log.node("成功找到缺口轮廓")
                return  x
        #没有找到缺口点击刷新 还张图片继续（递归）
        Log.node("没有找到缺口轮廓，点击刷新切换图片后再次尝试")

        for item in self.verifyer:
            self.driver.switch_to_frame(self.driver.find_element_by_id(item))

        self.driver.find_element_by_id('e_reload').click()
        time.sleep(2)
        self.cut()
        img0 = cv.imread("screenshot\\quyue.png")
        self.count = self.count+1

        self.driver.switch_to_default_content()

        return self.get_pos(img0,verifyer)

    
    def cut(self):
        self.driver.switch_to.default_content() #回到主页
        position = self.get_position(self.verifyer)  # 获取滑动验证图片的位置
        # print("验证图片的位置")
        # print(position)
        screenshot = self.get_screenshot()  # 截取整个浏览器图片
        
        position_scale = self.get_position_scale(screenshot)  # 获取截取图片宽高和浏览器宽高的比例
        # print("宽高比")
        # print(position_scale)
        self.get_slideimg_screenshot(screenshot, position, (1,1))  # 截取有缺口的滑动验证图片
        return

    #截取所有轮廓保存到本地，然后得到想要的轮廓的合适参数参数
    @staticmethod
    def get_pos_cs():
        image = cv.imread("screenshot\\quyue.png")
        # mgray = cv.cvtColor(image,cv.COLOR_BGR2GRAY) #彩色转灰度
        blurred = cv.GaussianBlur(image,(5, 5), 0)
        canny = cv.Canny(blurred, 20, 40)
        cv.imshow('canny',canny)
        cv.waitKey(0)
        
        contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #找轮廓
        cv.drawContours(image,contours,-1,(0,0,255),3)
        cv.imshow('image',image)
        cv.waitKey(0)
        for i, contour in enumerate(contours):
            image = cv.imread("screenshot\\quyue.png")
            print("---------------------")
            M = cv.moments(contour)
            if M['m00'] == 0:
                cx = cy = 0
            else:
                cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            print("cv.contourArea(contour):  "+str(cv.contourArea(contour))+"  ,  "+"cv.arcLength:  "+str(cv.arcLength(contour, True)))
            print("cx:  "+str(cx)+"  ,  "+"cy:  "+str(cy))
            x, y, w, h = cv.boundingRect(contour) # 外接矩形
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 150, 255), 2)
            cv.imwrite("dst\\"+ str(i) +"___"+str(cv.contourArea(contour))+"----"+str(cv.arcLength(contour, True))+".png",image)
            
        return 0

    #进行滑动验证
    def Verification(self,verifyer):

        self.driver.switch_to_default_content()

        self.verifyer=verifyer
        Log.node("开始进行滑动验证")


        #进入验证图片所在的iframe
        for item in self.verifyer:
            self.driver.switch_to_frame(self.driver.find_element_by_id(item))
        
        # 将小块隐藏
        self.driver.execute_script(
        "document.getElementsByClassName('tc-jpp-img')[0].style['display'] = 'none'")  
        self.cut()
        img0 = cv.imread("screenshot\\quyue.png")

       
        left = self.get_pos(img0,self.verifyer) #/ position_scale[0] # 将该位置还原为浏览器中的位置

         #进入验证图片所在的iframe
        for item in self.verifyer:
            self.driver.switch_to_frame(self.driver.find_element_by_id(item))

        self.driver.execute_script(
        "document.getElementsByClassName('tc-jpp-img')[0].style['display'] = 'block'")  # 将小块重新显示
        slide_btn = self.driver.find_element_by_id( 
        'tcaptcha_drag_thumb')  # 获取滑动按钮
        track = self.get_track(left-x_offset)  # 获取滑动的轨迹，此函数定义在第9点
        Log.node("开始滑动滑块到指定位置  滑动距离："+ str(left))
        self.move_to_gap(slide_btn, track)  # 进行滑动

        self.driver.switch_to_default_content()

        return

# success = driver.find_element_by_css_selector(
#     '.geetest_success_radar_tip')  # 获取显示结果的标签
# time.sleep(2)
# if success.text == "验证成功":
#     login_btn = driver.find_element_by_css_selector(
#         'button.j-login-btn')  # 如果验证成功，则点击登录按钮
#     login_btn.click()
# else:
#     print(success.text)
#     print('失败')