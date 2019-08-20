from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
from MODEL import model


wordspack = [[]]


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless","-hl",type=int,default=0,help="headlessを設定")
    parser.add_argument("--pattern","-pa",type=int,default=1,help="ランダム0はrefreshなし、プロフ探索のwordを選ぶ、ファボ消し1でいいね済み、not24時間を削除")
    parser.add_argument("--execute","-ex",type=int,default=0,help="0はランダム探索,1はプロフ探索,2はファボ消し")

    args = parser.parse_args()
    
    headless = args.headless
    pattern = args.pattern
    execute = args.execute

    if headless == 1:
        options = Options()
        options.add_argument('--headless')
        if execute != 3:
            options.add_argument('--blink-settings=imagesEnabled=false')
        driver=webdriver.Chrome(options=options)

    else:
        driver=webdriver.Chrome()
    
    if execute == 1:
        words = wordspack[pattern]
    else:
        words = None
    strategy = model.strategy(driver,pattern,words,execute)
    strategy.login()
    strategy.scraping()




