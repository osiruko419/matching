import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import termcolor
import sys
from datetime import datetime
import os
import hashlib
from glob import glob
from bs4 import BeautifulSoup
import cv2
import csv

timer = 2


def specialclick(driver,element,x=0,y=0,timer=timer):
    action = ActionChains(driver)
    action.move_to_element_with_offset(element,x,y)
    action.click()
    action.perform()
    time.sleep(timer)


def elemattempt(driver,element):
    try:
        locscroll(element)
        click(element)
        return True
    except:
        exception(driver)
        return False


def colorword(word,color):
    word = termcolor.colored(word,color)
    print(word)
    

def driverback(driver, refresh=0, timer=timer):
    driver.back()
    time.sleep(timer)
    if refresh != 0:
        driver.refresh()
        time.sleep(timer)
    

def click(element,timer=timer):
    element.click()
    time.sleep(timer)


def windowmv(driver,timer=timer,window=-1):
    handle_array = driver.window_handles
    driver.switch_to.window(handle_array[window])
    time.sleep(timer)       


def locscroll(element,timer=timer):
    element.location_once_scrolled_into_view
    time.sleep(timer)


def scrolllowest(driver,timer=timer):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")        
    time.sleep(timer)


def ifexit(driver,word,people,counter):
    if len(people[counter:]) == 0:
        now=datetime.now().strftime("%Y%m%d-%H:%M:%S")
        driver.save_screenshot(word+'%s.png' % now)
        print(word)            
        driver.close()
        sys.exit()


def exception(driver):
    colorword("exception", 'red')
    now = datetime.now().strftime("%Y%m%d-%H:%M:%S")
    driver.save_screenshot('exception_{}.png'.format(now))


def pagesoup(driver):
    source = driver.page_source
    soup = BeautifulSoup(source)
    return soup


def personpath(soup,counter):
    personsource = soup.select("#om-search-index-content > div.clearfix.search-list > div:nth-child(%s)" % counter)
    personid = str(personsource[0])[58:65]
    personpath = "%s" % personid
    return personpath


def shottrimming(driver,photonum,path):
    w = driver.execute_script('return document.body.scrollWidth')
    h = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(w,h)
    shotpath = '%s/screenshot%s.png' % (path,photonum)
    driver.save_screenshot(shotpath)
    img = cv2.imread(shotpath)
    img = img[70:460,152:542] #[y,x]
    cv2.imwrite(shotpath, img)


def photoremove(path):
    photopaths = []
    hashs = []
    removes = []

    photopaths.extend(glob('%s/*.png' % path))

    for photopath in photopaths:
        with open(photopath,'rb') as photo:
            photodata = photo.read()
            hashdata = hashlib.md5(photodata) #ハッシュ値を持ってくる
            hashs.append(hashdata.hexdigest()) #16進数にしてる

    for i in range(len(photopaths)):
        if photopaths[i] in removes:
            continue
        for j in range(i+1, len(photopaths)):
            if photopaths[j] in removes:
                continue
            if hashs[i] == hashs[j] and not photopaths[j] in removes:
                removes.append(photopaths[j])

    for photo in removes:
        os.remove(photo)


def delete(driver):
    element = driver.find_element_by_css_selector("#om-modal-member-detail > nav > div > div > div.dropdown.right-area")
    specialclick(driver,element)
    element = driver.find_element_by_id("om-member-detail-menu-favorite-delete")
    try:
        click(element)
        colorword("delete!", 'blue')
    except:
        pass


def reloading(driver,reloadnum,attempts,classname):
    colorword("reload%s" % reloadnum, 'red')
    reloadnum += 1
    if attempts == 1:
        driver.refresh()
        for _ in range(reloadnum):
            scrolllowest(driver,timer=0.5)
    people = driver.find_elements_by_class_name(classname)
    return reloadnum,people


def favoopen(driver):
    try:
        element = driver.find_element_by_id("om-global-menu-column-other")
        click(element)
        element = driver.find_element_by_css_selector("#om-other-menu > div > div.other-menu-list.row > div.menu-item.menu-item-favorite.col-xs-8")
        click(element)
    except:
        driver.refresh()
        print("open　favorite try again")
        favoopen(driver)


def eitherdelete(driver):
    deletenum = 0
    try:
        element = driver.find_element_by_css_selector("#om-member-detail-footer-button > div > div.om-button-yellow-M.om-button-profile-action-single.om-button-appeal.om-button-interest-action.om-button-interest-style")
        click(element)
        element = driver.find_element_by_css_selector("#om-dialog-appeal > div > div > div.modal-header.om-modal-header > button")
        click(element)
        # counter -= 1
        deletenum += 1
        

    except:
        pass

    try:
        logintime = driver.find_element_by_id("om-modal-member-detail-online-status").text
        if logintime != "24時間以内":
            deletenum += 1
    except:
        pass

    return deletenum


def freefavo(driver):
    while True:
        try:
            element = driver.find_element_by_id('om-pickup-index-button-interest')
            click(element)
            colorword("無料いいね発生","blue")
        except:
            break


# def writecsv():
#     stock = [["Apple", 24], ["Banana", 14], ["Orange", 8]] # 二重のリスト
#     with open("stock.csv", "w", encoding="Shift_jis") as file: # 文字コードをShift_JISに指定
#     writer = csv.writer(file, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
#     writer.writerows(stock) # csvファイルに書き込み


