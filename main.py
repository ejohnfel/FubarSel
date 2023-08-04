
import re
import time
import functools
import ait
import selenium.webdriver.support.wait as swait

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

class RecordingRecord:
    """RecordingRecord Class"""


    row = None
    cells = None
    data = None

    def __init__(self,row=None):
        """Init instance of RecordingRecord"""

        if row is not None:
            GetCells(row)

    def GetCells(self, row):
        """Get Cells From Row"""

        header = [
            "Loaded",
            "Start Time",
            "Duration",
            "Conversation Direction",
            "1st-Connected Phone Number",
            "Calling Party Phone Number",
            "Calling Party Name",
            "Calling Party Employee Number",
            "Calling Party Device name",
            "Called Party Phone Number",
            "Called Party Name",
            "Called Party Employee Number",
            "Called Party Device Name",
            "1st-Connected Name",
            "1st-Connected Device Name",
            "Archived",
            "Expanded",
            "Conversation ID of Callback Request",
            "FirstNameLastName",
            "Call_ID",
            "Extension",
            "Department"
        ]

        self.row = row

        self.cells = self.row.find_element(By.CSS_SELECTOR, "td")

        data_from_cells = [ str(cell.text) for cell in cells ]

        self.data = dict(zip(header,data_from_cells))

# Variables

Debug = True

Username = "swong"
Password = "7VnXD5rZKIVv"

# Date Interval
interval = timedelta(days=30)
startOn = datetime.now() - interval
endOn = datetime.now()

# Functions

DbgNames = lambda object: [ object.__qualname__, object.__name__ ]

def DebugMe(func):
    """Debug Decorator/Helper"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dbgblk, dbglb = DbgNames(func)

        print(f"Debugging : {dbgblk}")

        results = None

        try:
            results = func(*args,**kwargs)
        except Exception as err:
            print(f"{dbgblk} : Well, that didn't work out to well\n{err}")
            if Debug: breakpoint()

        return results

    return wrapper

def Sleep(interval):
    """Sleep for the specified time interval"""

    time.sleep(interval)

def Quarter():
    """Sleep a Quarter Second"""

    Sleep(0.25)

def Half():
    """Sleep Half Second"""

    Sleep(0.5)

def Second():
    """Sleep for a second"""

    Sleep(1)

def Maximize(browser):
    """Maximize Browser Windows Helper"""

    browser.maximize_window()

def Switch(browser,name,pause=0,breakme=False):
    """Context/Content Switch Helper"""

    succeed = False

    if pause > 0:
        Sleep(pause)

    try:
        browser.switch_to.frame(name)
        succeed = True
    except Exception as err:
        print(f"Switching Content...:\nWell... that failed... : {err}")

        if breakme:
            breakpoint()

    return succeed

def SetupBrowser(browser, url):
    """Helper for setting up the browser"""

    browser.get(url)

def DoAit(seconds,key=None,write=None):
    """Helper for Doing Ait Stuff"""

    Sleep(seconds)

    if key is not None:
        ait.press(key)
    elif write is not None:
        ait.write(write)

def BadCert(browser):
    """Helper for Getting Past Bad Certs"""

    advBtn = browser.find_element(By.CSS_SELECTOR, "button[id='details-button']")
    advBtn.click()

    Half()

    anchor = browser.find_element(By.CSS_SELECTOR, "div > p > a[id='proceed-link']")

    anchor.click()

    Second()

def CancelDialog():
    """Cancel Login Dialog Helper"""

    print("In CancelDialog")
    ait.press("\t", "\t", "\t")
    Half()
    ait.press("\n")
    Half()

def DumbLogin():
    """Logging Into ACS, the Dumb Way, Ommmm"""

    global Username, Password

    Half()
    ait.write(Username)
    ait.press("\t")
    ait.write(Password)
    ait.press("\t","\t")
    ait.press("\n")

    Second()

def SmartLogin(browser):
    """Smart Login ACS"""

    success = False

    if Switch(browser, 0):
        userInput = browser.find_element(By.CSS_SELECTOR, "input[id='loginTabView:loginName:inputPanel:inputText']")
        passwordInput = browser.find_element(By.CSS_SELECTOR, "input[id='loginTabView:loginPassword:inputPanel:inputPassword']")
        submitButton = browser.find_element(By.CSS_SELECTOR, "button[id='loginTabView:loginButton']")

        userInput.send_keys(Username)
        passwordInput.send_keys(Password)

        Half()

        submitButton.click()

        Second()

        success = True
    else:
        print("*** Mucho problemo Jose!!! Can't log in")

    return success

def SmartLogout(browser):
    """Logout Helper"""

    anchorID = "a[id='logoutMenuItem']"

    WebDriverWait(browser, 5).until(presence_of_element_located((By.CSS_SELECTOR, anchorID)))

    logoffAnchor = browser.find_element(By.CSS_SELECTOR, "a[id='logoutMenuItem']")

    WebDriverWait(browser, 5).until(visibility_of(logoffAnchor))

    logoffAnchor.click()

def GetRows(browser):
    """Get Rows from Search"""

    rows = browser.find_elements(By.CSS_SELECTOR, "div[class='ui-datatable-scrollable-body'] > table > tbody > tr")

    return rows

def GetData(browser):
    """Get Data"""

    rows = GetRows(browser)

    records = list()

    for row in rows:
        records.append(RecordingRecord(row))

    return records

def PausePlayer(browser):
    """Pause Player"""

    pauseBtn = browser.find_element(By.CSS_SELECTOR, "div[id='asc_playercontrols_pause_btn']")

    if Debug:
        breakpoint()

    WebDriverWait(browser, 5).until(visibility_of(pauseBtn))

    pauseBtn.click()

def ActivateRow(browser,row):
    """Activate Row"""

    ActionChains(browser).move_to_element(row).double_click().perform()

    PausePlayer(browser)

    if Debug: breakpoint()

    Sleep(5)

@DebugMe
def Search(browser,startDate,endDate):
    """Set and Conduct Search"""

    # Find "General dropdown
    general = browser.find_element(By.CSS_SELECTOR, "a[id='conversationToolbar:commonFunctionsMenuBtn']")
    general.click()

    # Find Search anchor and click it
    anchor = browser.find_element(By.CSS_SELECTOR, "a[id='conversationToolbar:toolbarSearchBtn']")
    anchor.click()

    Quarter()

    # Set Select box

    sbox = browser.find_element(By.CSS_SELECTOR, "select[id='conversationObjectView:j_idt132:searchdatatable:0:searchMenu']")
    WebDriverWait(browser, 5).until(visibility_of(sbox))

    select = Select(sbox)
    # Set "between", then set dates. VALUE = "BETWEEN"
    select.select_by_value('BETWEEN')

    Half()

    breakpoint()

    WebDriverWait(browser, 5).until(presence_of_element_located((By.CSS_SELECTOR, "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarOne_input']")))
    WebDriverWait(browser, 5).until(presence_of_element_located((By.CSS_SELECTOR, "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarTwo_input']")))

    breakpoint()

    # Get begin and end date inputs
    startInput = browser.find_element(By.CSS_SELECTOR,"input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarOne_input']")
    endInput = browser.find_element(By.CSS_SELECTOR,"input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarTwo_input']")
    searchBtn = browser.find_element(By.CSS_SELECTOR, "button[id='conversationObjectView:j_idt413'")
    closeAnchor = browser.find_element(By.CSS_SELECTOR, "a[class='ui-dialog-titlebar-icon ui-dialog-titlebar-close ui-corner-all']")

    startInput.clear()
    startInput.send_keys(startDate.strftime("%m/%d/%Y %I:%M:%S %p"))
    endInput.clear()
    endInput.send_keys(endDate.strftime("%m/%d/%Y %I:%M:%S %p"))

    # Start Search
    searchBtn.click()

    # Wait for search to complete

    # WebDriveWait(browser).until()

    if Debug: breakpoint()

    # Close Search Box
    closeAnchor.click()

@DebugMe
def GetVoiceRecordings(browser, url):
    """Get ACS Voice Recordings... Probably"""

    global Username, Password

    # Setup the Browser (i.e. Navigate to URL)
    SetupBrowser(browser, url)

    # Make us bigggggg
    Maximize(browser)

    # Get past bad cert
    BadCert(browser)

    # Cancel Login Dialog (Via Ait)
    CancelDialog()

    # Actual Login... but dumb... (via Ait)
    if SmartLogin(browser):
        # Replace with wait
        Second()

        # Begin Searches and downloads

        # POC Search and D/L
        # Set Search Up
        Search(browser, startOn, endOn)

        # Extract Current Rows
        data = GetData(browser)

        if Debug:
            print("*** <<< Last breakpoint before termination >>>")
            breakpoint()

        SmartLogout(browser)

def GeteBook(browser, url):
    """Grab Free Daily eBooks from Packt"""

    SetupBrowser(browser, url)

    # https://www.browserstack.com/guide/download-file-using-selenium-python
    # https://www.selenium.dev/documentation/test_practices/discouraged/file_downloads/

    objDiv = browser.find_element(By.CSS_SELECTOR, "div[class='card__image']")
    anchor = objDiv.find_element(By.CSS_SELECTOR, "a")

    breakpoint()

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
        "acs": "https://129.49.122.190/POWERplayWeb/",
        "tsa": "https://techstepacademy.com/training-ground/",
        "tsatrial": "https://techstepacademy.com/trial-of-the-stones/"
    }

    chrome = webdriver.Chrome()

    # GetTSA(chrome, urls["tsa"])
    # GetStones(chrome, urls["tsatrial"])

    # GeteBook(chrome, urls["packt"])
    GetVoiceRecordings(chrome, urls["acs"])

    chrome.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
