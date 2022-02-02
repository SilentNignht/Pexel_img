from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import requests
import os
import time


driver = Chrome(executable_path='./chromedriver')                   # 根據柏辰提供的https://segmentfault.com/a/1190000040450510
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {   # 所記載的隱藏Selenium 黑科技寫法，讓Pexel防Selenium可以被破解
    "source": """
       Object.defineProperty(navigator, 'webdriver', {
         get: () => undefined
       })
     """
})


url = "https://www.pexels.com/zh-tw/search/%E5%8F%A3%E7%BD%A9/?page=1"       # 要爬的網站
url_start = "https://www.pexels.com/zh-tw/search/%E5%8F%A3%E7%BD%A9/?page="  # 換頁機制


def pic_catch(soup):                             # 爬蟲的函數，基本上參考爬蟲老師的圖片下載寫法
    for a in soup.select("a.js-photo-link"):
        imageSrc = a.img["src"]
        image = requests.get(imageSrc)
        imageContent = image.content
        i = str(a["href"]).split("/")[3]         # 取名採用網站的圖片編碼，之後要加避免重複的時候可以用到
        path = f"{dir}/{i}.jpg"
        file = open(path, "wb")                  # 這邊是用開關資料夾的方式寫，改用with寫法可能會更簡潔
        file.write(imageContent)
        file.close()
        time.sleep(0.5)
        # print(i)


dir = "Mask_data"
if not os.path.isdir(dir):
    os.makedirs(dir)


for p in range(2, 102):                 # 這邊延續換頁風格寫的，會保留主要是測試時間可以縮短
    driver.get(url)                   # 有上面的黑科技之後也許可以考慮直接拉到底下載

    driver.maximize_window()

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    pos = 0                            # 網路找到的Selenium 下拉滾輪寫法，
    for x in range(4):                 #  來源參考:https://medium.com/%E4%BC%81%E9%B5%9D%E4%B9%9F%E6%87%82%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88/python%E7%88%AC%E8%9F%B2-python-selenium-%E8%87%AA%E5%8B%95%E5%8C%96%E7%88%AC%E5%8F%96%E5%A4%A7%E9%87%8F%E5%9C%96%E7%89%87-a35d3c89c6d1
        pos += x * 500  # 每次下滾500
        js = "document.documentElement.scrollTop=%d" % pos
        driver.execute_script(js)
        time.sleep(1)

    pic_catch(soup)
    time.sleep(5)
    url = url_start + f"{p}"


driver.close()
