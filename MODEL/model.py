import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from MODEL.code import *
import os

url='https://www.omiai-jp.com/search'
os.environ["MY_LOGIN_ID"] = "YOURID"
os.environ["MY_LOGIN_PASSWORD"] = "YOURPASSWORD"


class strategy():
    def __init__(self,driver,pattern=0,words=None,execute=0):
        self.driver = driver
        self.words = words
        self.pattern = pattern
        self.execute = execute
        self.counter = 0
        self.favorite = 0
        self.reloadnum = 0
        self.attempts = 0
        self.notdelnum = 0
        

    def login(self):
        print("ログイン中")
        self.driver.get(url)
        time.sleep(5)       

        element = self.driver.find_element_by_id('om-button-fb-login')
        click(element)

        windowmv(self.driver)

        facebook = self.driver.find_elements_by_class_name('inputtext')

        login_id = os.environ.get("MY_LOGIN_ID")
        login_pass = os.environ.get("MY_LOGIN_PASSWORD")
        facebook[0].send_keys(login_id)
        facebook[1].send_keys(login_pass)

        element = self.driver.find_element_by_id('loginbutton')
        click(element,timer=5)

        try:
            element = self.driver.find_element_by_css_selector("#platformDialogForm > div._2_bh > div > table > tbody > tr > td._51m-.uiOverlayFooterButtons._51mw > button._42ft._4jy0.layerConfirm._51_n.autofocus._4jy5._4jy1.selected._51sy")
            click(element)
            exception(self.driver)
        except:
            pass

        windowmv(self.driver)

        self.driver.maximize_window()
        time.sleep(2)

        print('ログイン成功')
        # try:
        #     element = self.driver.find_elements_by_class_name("_2s5p")
        #     click(element)


    def randomsearch(self):
        if self.pattern == 0:
            scrolllowest(self.driver,timer=2)
        else:
            for _ in range(20):
                scrolllowest(self.driver,timer=1)
        people = self.driver.find_elements_by_class_name('col-xs-12')
        person = np.random.choice(people)
        locscroll(person)
        click(person)
        driverback(self.driver,refresh=self.pattern)
        self.counter += 1
        print("counter=%s" % self.counter)

            
    def wordsfavo(self):
        self.reloadnum,people = reloading(self.driver,self.reloadnum,self.attempts,'col-xs-12')
        # ifexit(self.driver,"お気に入り完了",people,self.counter)
        if len(people[self.counter:]) == 0:
            self.framework
        for person in people[self.counter:]:
            # scrolllowest(self.driver)
            if not elemattempt(self.driver,person):
                self.attempts = 1
                break
            self.attempts = 0 
            element = self.driver.find_element_by_css_selector("#om-modal-member-detail > nav > div > div > div.dropdown.right-area")
            specialclick(self.driver,element)
            #プロフィール読み込み
            text = self.driver.find_element_by_id("om-modal-member-detail-inrtoduction").text
            #ログイン状況
            logintime = self.driver.find_element_by_id("om-modal-member-detail-online-status").text
            if logintime == "24時間以内":
                for word in self.words:
                    if text.find(word)>=0:
                        try:
                            element = self.driver.find_element_by_css_selector("#om-member-detail-menu-favorite-add")#お気に入り登録
                            click(element)
                            self.favorite+=1
                            colorword("favorite=%s" % self.favorite, 'blue')
                            break
                        except:
                            break
            driverback(self.driver)
            self.counter += 1
            print("counter=%s" % self.counter)


    def favodelete(self):
        self.reloadnum,people = reloading(self.driver,self.reloadnum,self.attempts,'om-list-item-row')
        ifexit(self.driver,"削除完了",people,self.counter)
        # if len(people[self.counter:]) == 0:
        #     self.framework
        for person in people[self.counter:]:
            # scrolllowest(self.driver)
            self.counter += 1
            if not elemattempt(self.driver,person):
                self.attempts = 1
                self.counter = self.notdelnum
                # if self.pattern == 0:
                break
            self.attempts = 0
            deletenum = 1
            if self.pattern == 1:
                deletenum = eitherdelete(self.driver)
                                
            username = self.driver.find_element_by_id("om-modal-member-detail-basis-nickname").text
            print("username=%s"%username)
            if deletenum != 0:
                delete(self.driver)
            else:
                self.notdelnum += 1
            driverback(self.driver)


    def scraping(self):
        executefunction = ["randomsearch実行中","wordsfavo実行中","favodelete実行中"]
        print(executefunction[self.execute])
        print("pattern=%s" % self.pattern)
        
        if self.execute == 1:
            print(self.words)

        if self.execute == 2:
            favoopen(self.driver)
            
        self.framework()
        
    
    def framework(self):
        while True:
            try:
                if self.execute == 0:
                    self.randomsearch()
                if self.execute == 1:
                    self.wordsfavo()
                if self.execute == 2:
                    self.favodelete()
            
            except:
                exception(self.driver)
                freefavo(self.driver)
                self.driver.refresh()
                continue
