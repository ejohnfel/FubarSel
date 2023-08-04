
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def SetupBrowser(browser, url):
        browser.get(url)

def GeteBook(browser, url):
    SetupBrowser(browser, url)

    # https://www.browserstack.com/guide/download-file-using-selenium-python
    # https://www.selenium.dev/documentation/test_practices/discouraged/file_downloads/

    objDiv = browser.find_element(By.CSS_SELECTOR, "div[class='card__image']")
    anchor = objDiv.find_element(By.CSS_SELECTOR, "a")

    breakpoint()

def GetVoiceRecordings(browser, url):
    SetupBrowser(browser, url)

    element = None # Element that needs the double click
    ActionChains(browser).move_to_element(element).double_click().perform()

def GetTSA(browser, url):
    SetupBrowser(browser, url)

    inputbox = browser.find_element(By.CSS_SELECTOR, "input[id='ipt1']")

    inputbox.send_keys("Kewl!")

    button1 = browser.find_element(By.CSS_SELECTOR, "button[id='b1']")
    # button2 = browser.find_element(By.CSS_SELECTOR, "button[name='butn1']")

    time.sleep(2)

    button1.click()

    time.sleep(2)

    # alert = browser.switch_to.alert
    alert = Alert(browser)
    alert.accept()

    # Example XPath
    button4 = browser.find_element(By.XPATH, "//button[@id='b4']")

    pb = browser.find_element(By.XPATH, "//b[text()='Product 1']/../../p")

    match = re.search(r"\$\d+(\.\d+){0,1}", pb.text)
    price = "0.00"

    if match is not None:
        price = match[0][1:]

    time.sleep(2)

def GetStones(browser, url):
    SetupBrowser(browser, url)

    # Riddle of the rocks
    r1 = browser.find_element(By.CSS_SELECTOR, "input[id='r1Input']")
    r1btn = browser.find_element(By.CSS_SELECTOR, "button#r1Btn")
    r1.send_keys("rock")
    r1btn.click()

    r1div = browser.find_element(By.XPATH, "//div[@id='passwordBanner']/h4")
    password = r1div.text

    # Riddle of the secrets
    r2 = browser.find_element(By.CSS_SELECTOR, "input[id='r2Input']")
    r2btn = browser.find_element(By.CSS_SELECTOR, "button[id='r2Butn']")

    r2.send_keys(password)
    r2btn.click()

    r2div = browser.find_element(By.XPATH, "//div[@id='successBanner1']")

    if r2div.get_attribute("style") != "display: none":
        # Rich people shit

        rinput = browser.find_element(By.CSS_SELECTOR, "input[id='r3Input']")
        rbtn = browser.find_element(By.CSS_SELECTOR, "button[id='r3Butn']")

        # Find people

        items = browser.find_elements(By.XPATH, f"//div/span/b")

        people = dict()

        for item in items:
            value = int(browser.find_element(By.XPATH, f"//div/span/b[text()='{item.text}']/../../p").text)

            people[item.text] = value

        value = None

        for person in people:
            if value is None:
                value = people[person]
                rinput.clear()
                rinput.send_keys(person)
            else:
                tmpValue = people[person]

                if tmpValue > value:
                    rinput.clear()
                    rinput.send_keys(person)
                    value = tmpValue

        rbtn.click()
        rdiv = browser.find_element(By.XPATH, "//div[@id='successBanner2']")

        if rdiv.get_attribute("style") != "display: none":
            print("You cheeky bastard!")
        else:
            print("Better luck next time mate!")

        chkbtn = browser.find_element(By.CSS_SELECTOR, "button[id='checkButn']")

        chkbtn.click()

        div = browser.find_element(By.XPATH, "//div[@id='trialCompleteBanner']")

        if div.get_attribute("style") != "display: none;":
            print("You did it you magnificent bastard!")
        else:
            print("No bueno my friend!")

        assert div.get_attribute("style") != "display: none;"

        time.sleep(2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    urls = {
        "packt": "https://www.packtpub.com/free-learning/",
        "acs": "https://129.49.199.160/POWERplayWeb/",
        "tsa": "https://techstepacademy.com/training-ground/",
        "tsatrial": "https://techstepacademy.com/trial-of-the-stones/"
    }

    chrome = webdriver.Chrome()

    GetTSA(chrome, urls["tsa"])
    GetStones(chrome, urls["tsatrial"])

    # GeteBook(chrome, urls["packt"])
    # GetVoiceRecordings(chrome, urls["acs"])

    chrome.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
