from sys import platform
import sys
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from traceback import print_exc

def GetUrlTime(now):
    return str(now.year % 100) + \
           (('0' + str(now.month)) if now.month < 10 else str(now.month)) + \
           (('0' + str(now.day)) if now.day < 10 else str(now.day))


def GetScriptTime(now):
    return str(now.year) + '-' + \
           (('0' + str(now.month)) if now.month < 10 else str(now.month)) + '-' + \
           (('0' + str(now.day)) if now.day < 10 else str(now.day))


def page_has_loaded(deiver):
    page_state = deiver.execute_script('return document.readyState')
    print('page_state: ' + page_state)
    return page_state == 'complete'


def WebsiteExecute(tag, count, now, gap, critical, fileWrite):
    isCritical = False

    for i in range(0, count):
        try:
            nowString = GetUrlTime(now)
            url = 'http://www.flycua.com/flight2014/' + tag + nowString + '_CNY.html'
            print('Start retrieving ' + tag + nowString)

            if platform == 'win32':
                driver = webdriver.PhantomJS(
                    'E:\Dropbox\Dropbox\Soft\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
                # driver = webdriver.Chrome('E:\Dropbox\Dropbox\Soft\chromedriver_win32\chromedriver.exe')
            elif platform == 'linux' or platform == 'linux2':
                pass
                driver = webdriver.PhantomJS('/root/phantomjs')
                # to implement
            else:
                print('Abort retrieving cause platform not exist: ' + platform)
                with open('LowPriceOutput.txt', 'a') as myfile:
                    myfile.write('Abort retrieving cause platform not exist: ' + platform + '\n')
                break

            driver.get(url)
            WebDriverWait(driver, 5).until(page_has_loaded)

            html = driver.execute_script('return document.getElementsByTagName("html")[0].innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            info = soup.find_all('li', class_='active', title=GetScriptTime(now))
            print(info)
            if str(info).__len__() >= 2:
                soup2 = BeautifulSoup(str(info)[1:-1], 'html.parser')
                info2 = soup2.find_all('b')
                print(info2)
                print('End retrieving ' + tag + nowString)
                if str(info2).__len__() >= 10:
                    price = int(str(info2)[5:-5].replace(',', ''))

                    if price <= critical:
                        print('Record low price ' + tag + nowString)
                        fileWrite += tag + nowString + ', Price: ' + str(price) + '\n'
                        isCritical = True

            driver.quit()

            now += datetime.timedelta(days=1)
            time.sleep(gap)
        except Exception as e:
            print ('type is:', e.__class__.__name__)
            print_exc()
            print('Error retrieving ' + tag + nowString + '\n')
            with open('LowPriceOutput.txt', 'a') as myfile:
                myfile.write('Error retrieving ' + tag + nowString)
            continue

    return isCritical


if __name__ == '__main__':
    realNow = datetime.datetime.now()
    while realNow.weekday() != 2:
        realNow += datetime.timedelta(days=1)

    for i in range(0, 26):
        fileWrite = ''

        now = realNow
        while now.weekday() != 2:
            now += datetime.timedelta(days=1)
        nowString = GetUrlTime(now)

        with open('LowPriceOutput.txt', 'a') as myfile:
            myfile.write(nowString + ' (CheckDate): \n')

        if WebsiteExecute('nay-hny-', 3, now, 60, 500, fileWrite):
            while now.weekday() != 0:
                now += datetime.timedelta(days=1)
            if WebsiteExecute('hny-nay-', 3, now, 60, 500, fileWrite):
                with open('LowPriceOutput.txt', 'a') as myfile:
                    myfile.write(fileWrite)

        realNow += datetime.timedelta(days=7)

    sys.exit(0)
