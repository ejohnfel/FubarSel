
from selenium import webdriver
from selenium.webdriver.common.by import By


def SetupBrowser(browser, url):
        browser.get(url)

def GeteBook(browser, url):
    SetupBrowser(browser, url)

    objDiv = browser.find_element(By.CSS_SELECTOR, "div[class='card__image']")
    anchor = objDiv.find_element(By.CSS_SELECTOR, "a")

    breakpoint()

def GetVoiceRecordings(browser, url):
    SetupBrowser(browser, url)

def GetTSA(browser, url):
    SetupBrowser(browser, url)

    inputbox = browser.find_element(By.CSS_SELECTOR, "input[id='ipt1']")

    inputbox.send_keys("Kewl!")

    button1 = browser.find_element(By.CSS_SELECTOR, "button[id='b1']")
    button2 = browser.find_element(By.CSS_SELECTOR, "button[name='butn1']")

    button1.click()

    breakpoint()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urls = {
        "packt": "https://www.packtpub.com/free-learning/",
        "acs": "https://129.49.199.160/POWERplayWeb/",
        "tsa" : "https://techstepacademy.com/training-ground/"
    }

    chrome = webdriver.Chrome()

    GetTSA(chrome,urls["tsa"])
    # GeteBook(chrome, urls["packt"])
    # GetVoiceRecordings(chrome, urls["acs"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
