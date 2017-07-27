import re
import sys
import datetime
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def GetTimeStr(time):
    return str(now.year % 100) + (('0' + str(now.month)) if now.month < 10 else str(now.month)) + str(now.day)


def GetTimeStr2(time):
    return str(now.year) + '-' + (('0' + str(now.month)) if now.month < 10 else str(now.month)) + '-' + str(now.day)


if __name__ == "__main__":
    now = datetime.datetime.now()
    nowString = GetTimeStr(now)

    with open("LowPriceOutput.txt", "a") as myfile:
        myfile.write(nowString + " (CheckDate): \n")

    for i in range(0, 180):
        nowString = GetTimeStr(now)
        print('Start retrieving ' + nowString)
        page = requests.get('http://www.flycua.com/flight2014/nay-hny-' + nowString + '_CNY.html')
        url = 'http://www.flycua.com/flight2014/nay-hny-' + nowString + '_CNY.html'

        driver = webdriver.PhantomJS(
            "E:\Dropbox\Dropbox\Soft\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\\bin\phantomjs.exe", 0)
        driver.get(url)

        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        info = soup.find_all('li', class_='active', title=GetTimeStr2(now))
        print(info)
        if str(info).__len__() >= 2:
            soup2 = BeautifulSoup(str(info)[1:-1], 'html.parser')
            info2 = soup2.find_all('b')
            print(info2)
            print('End retrieving ' + nowString)
            if str(info2).__len__() >= 10:
                price = int(str(info2)[5:-5].replace(',', ''))

                if price <= 500:
                    with open("LowPriceOutput.txt", "a") as myfile:
                        myfile.write("nay-hny-" + nowString + ", Price: " + price + "\n")

        driver.quit()

        now += datetime.timedelta(days=1)
        time.sleep(60)

    sys.exit(0)
