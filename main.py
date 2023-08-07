# Imports

# Regular stuff
import re
from datetime import datetime, timedelta
import time
import functools
import ait
import py_helper as ph

# My Stuff
from py_helper import CmdLineMode, DebugMode, DbgMsg, Msg, DbgEnter, DbgExit, DebugMe, DbgNames, DbgAuto

# Selenium Stuff
import selenium.webdriver.support.wait as swait
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *


# Classes

class RecordingRecord:
    """RecordingRecord Class"""

    row = None
    cells = None
    data = None

    def __init__(self, row=None):
        """Init instance of RecordingRecord"""

        if row is not None:
            self.GetCells(row)

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

        try:
            self.cells = self.row.find_elements(By.CSS_SELECTOR, "td")
        except Exception as err:
            Msg("Shee-it!")
            breakpoint()

        data_from_cells = [str(cell.text) for cell in self.cells]

        self.data = dict(zip(header, data_from_cells))


class eDOM:
    """DOM Helper for WebElement"""

    Element = None

    def __init__(self, webElement):
        """Init Instance"""

        self.Element = webElement

    def __getitem__(self, key):
        """Get Item By Key"""

        # No try-except, we want this to fail technically
        result = self.Element.get_attribute(key)

        return result

    def keys(self):
        """Return A list of Keys"""

        standard_attributes = [
            "id",
            "name",
            "class",
            "style",
            "aria-class",
            "aria-role",
            "src",
            "alt",
            "rel",
            "href",
            "text",
            "value",
            "width",
            "height",
            "lang",
            "title",
            "accept",
            "accept-charset",
            "accesskey",
            "action",
            "align",
            "allow",
            "async",
            "autocapitalize",
            "autoplay",
            "background",
            "bgcolor",
            "border",
            "buffered",
            "capture",
            "charset",
            "checked",
            "cite",
            "color",
            "cols",
            "colspan",
            "content",
            "contenteditable",
            "controls",
            "coords",
            "crossorigin",
            "csp",
            "data",
            "datetime",
            "decoding",
            "default",
            "defer",
            "dir",
            "dirname",
            "disabled",
            "download",
            "draggable",
            "enctype",
            "enterkeyhint",
            "for",
            "form",
            "formaction",
            "formenctype",
            "formmethod",
            "formnovalidate",
            "formtarget",
            "headers",
            "hidden",
            "high",
            "hreflang",
            "http-equiv",
            "integrity",
            "intrinsicsize",
            "inputmode",
            "ismap",
            "itemprop",
            "kind",
            "label",
            "language",
            "loading",
            "list",
            "loop",
            "low",
            "manifest",
            "max",
            "maxlength",
            "minlength",
            "media",
            "method",
            "min",
            "multiple",
            "muted",
            "novalidate",
            "open",
            "optimum",
            "pattern",
            "ping",
            "placeholder",
            "playsinline",
            "poster",
            "preload",
            "readonly",
            "required",
            "reversed",
            "role",
            "rows",
            "rowspan",
            "sandbox",
            "scope",
            "scoped",
            "selected",
            "shape",
            "size",
            "sizes",
            "slot",
            "span",
            "spellcheck",
            "srcdoc",
            "srclang",
            "srcset",
            "start",
            "step",
            "summary",
            "tabindex",
            "target",
            "translate",
            "type",
            "usemap",
            "wrap"
        ]

        attributes_present = list()

        for attr in standard_attributes:
            try:
                value = self.Element.get_attribute(attr)

                if value is not None:
                    attributes_present.append(attr)
            except:
                pass

        return attributes_present

    def items(self):
        """Get Key-Value Pairs"""

        item_list = list()

        attrs = self.keys()

        for attr in attrs:
            value = self.Element.get_attribute(attr)

            item_list.append((attr, value))

        return item_list

    def values(self):
        """Get values of present Attributes"""

        attrs = self.keys()

        vals = dict()

        for attr in attrs:
            vals[attr] = self.ELement.get_attribute(attr)

        return vals

    def get(self, attr_name, altvalue=None):
        result = altvalue

        try:
            result = self.Element.get_attribute(attr_name)

            if result == None:
                result = altvalue
        except:
            result = None

        return result


class edom(object):
    """Wrapper for WebElement"""

    def __init__(self, obj):
        self._wrapped_obj = obj

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)

        return getattr(self._wrapped_obj, attr)

    def __getitem__(self, key):
        """Get Item By Key"""

        # No try-except, we want this to fail technically
        result = self._wrapped_obj.get_attribute(key)

        return result

    def keys(self):
        """Return A list of Keys"""

        standard_attributes = [
            "id",
            "name",
            "class",
            "style",
            "aria-class",
            "aria-role",
            "src",
            "alt",
            "rel",
            "href",
            "text",
            "value",
            "width",
            "height",
            "lang",
            "title",
            "accept",
            "accept-charset",
            "accesskey",
            "action",
            "align",
            "allow",
            "async",
            "autocapitalize",
            "autoplay",
            "background",
            "bgcolor",
            "border",
            "buffered",
            "capture",
            "charset",
            "checked",
            "cite",
            "color",
            "cols",
            "colspan",
            "content",
            "contenteditable",
            "controls",
            "coords",
            "crossorigin",
            "csp",
            "data",
            "datetime",
            "decoding",
            "default",
            "defer",
            "dir",
            "dirname",
            "disabled",
            "download",
            "draggable",
            "enctype",
            "enterkeyhint",
            "for",
            "form",
            "formaction",
            "formenctype",
            "formmethod",
            "formnovalidate",
            "formtarget",
            "headers",
            "hidden",
            "high",
            "hreflang",
            "http-equiv",
            "integrity",
            "intrinsicsize",
            "inputmode",
            "ismap",
            "itemprop",
            "kind",
            "label",
            "language",
            "loading",
            "list",
            "loop",
            "low",
            "manifest",
            "max",
            "maxlength",
            "minlength",
            "media",
            "method",
            "min",
            "multiple",
            "muted",
            "novalidate",
            "open",
            "optimum",
            "pattern",
            "ping",
            "placeholder",
            "playsinline",
            "poster",
            "preload",
            "readonly",
            "required",
            "reversed",
            "role",
            "rows",
            "rowspan",
            "sandbox",
            "scope",
            "scoped",
            "selected",
            "shape",
            "size",
            "sizes",
            "slot",
            "span",
            "spellcheck",
            "srcdoc",
            "srclang",
            "srcset",
            "start",
            "step",
            "summary",
            "tabindex",
            "target",
            "translate",
            "type",
            "usemap",
            "wrap"
        ]

        attributes_present = list()

        for attr in standard_attributes:
            try:
                value = self._wrapped_obj.get_attribute(attr)

                if value is not None:
                    attributes_present.append(attr)
            except:
                pass

        return attributes_present

    def items(self):
        """Get Key-Value Pairs"""

        item_list = list()

        attrs = self.keys()

        for attr in attrs:
            value = self._wrapped_obj.get_attribute(attr)

            item_list.append((attr, value))

        return item_list

    def values(self):
        """Get values of present Attributes"""

        attrs = self.keys()

        vals = dict()

        for attr in attrs:
            vals[attr] = self._wrapped_obj.get_attribute(attr)

        return vals

    def get(self, attr_name, altvalue=None):
        result = altvalue

        try:
            result = self._wrapped_obj.get_attribute(attr_name)

            if result == None:
                result = altvalue
        except:
            result = None

        return result


# Variables

Username = "swong"
Password = "7VnXD5rZKIVv"

# Date Intervals
officialStart = datetime(2017, 1, 1, 0, 0, 0)
officialEnd = datetime(2023, 8, 5, 0, 0, 0)

simultaneousDownloads = 5

interval = timedelta(days=30)
startOn = datetime.now() - interval
endOn = datetime.now()


# Decorators

# Functions

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


def Switch(browser, name, pause=0, breakme=False):
    """Context/Content Switch Helper"""

    success = False

    if pause > 0:
        Sleep(pause)

    try:
        browser.switch_to.frame(name)
        success = True
    except Exception as err:
        Msg(f"Switching Content...:\nWell... that failed... : {err}")

        if breakme:
            breakpoint()

    return success


def SetupBrowser(browser, url):
    """Helper for setting up the browser"""

    browser.get(url)


def DownloadOptions(folderPath):
    """Set Browser Download Path"""

    options = Options()

    options.add_experimental_option("prefs", {
        "download.default_directory": folderPath,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    return options


def DoAit(seconds, key=None, write=None):
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
    ait.press("\t", "\t")
    ait.press("\n")

    Second()


def SmartLogin(browser):
    """Smart Login ACS"""

    success = False

    if Switch(browser, 0):
        DbgMsg("Logging in")

        userInput = browser.find_element(By.CSS_SELECTOR, "input[id='loginTabView:loginName:inputPanel:inputText']")
        passwordInput = browser.find_element(By.CSS_SELECTOR,
                                             "input[id='loginTabView:loginPassword:inputPanel:inputPassword']")
        submitButton = browser.find_element(By.CSS_SELECTOR, "button[id='loginTabView:loginButton']")

        userInput.send_keys(Username)
        passwordInput.send_keys(Password)

        Half()

        submitButton.click()

        Second()

        success = True
    else:
        Msg("*** Mucho problemo Jose!!! Can't log in")

    return success


def SmartLogout(browser):
    """Logout Helper"""

    span = "table[id='powpwfteaper27'] > tbody > tr > td > span[id='powpwfteaper28']"
    anchorID = "a[id='logoutMenuItem']"

    DbgMsg("Logging out")

    spanobj = browser.find_element(By.CSS_SELECTOR, span)

    WebDriverWait(browser, 30).until(presence_of_element_located((By.CSS_SELECTOR, anchorID)))

    logoffAnchor = browser.find_element(By.CSS_SELECTOR, anchorID)

    spanobj.click()

    WebDriverWait(browser, 30).until(visibility_of(logoffAnchor))

    logoffAnchor.click()


def GetRows(browser):
    """Get Rows from Search"""

    rows = browser.find_elements(By.CSS_SELECTOR, "div[class='ui-datatable-scrollable-body'] > table > tbody > tr")

    return rows


def ClosePopOut(browser):
    """Close that fucking annoying pop out"""

    italicsCss = "table[id='aswpwfteapte42'] > tbody > tr > td > i[id='aswpwfteapte32']"
    italics = browser.find_element(By.CSS_SELECTOR, italicsCss)

    if italics.is_displayed():
        try:
            italics.click()
        except Exception as err:
            Msg("Popup element was stale... or something", prefix="********* >>>>>>>>>>")


def GetData(browser):
    """Get Data"""

    ClosePopOut(browser)

    Msg("************* >>>>>>>>>>>>> Getting Rows <<<<<<<<<<<<<")

    rows = GetRows(browser)

    records = list()

    for row in rows:
        recording = RecordingRecord(row)

        if recording.data['Start Time'] != '':
            records.append(RecordingRecord(row))

    return records


def PausePlayer(browser):
    """Pause Player"""

    pauseBtn = browser.find_element(By.CSS_SELECTOR, "div[id='asc_playercontrols_pause_btn']")

    WebDriverWait(browser, 5).until(visibility_of(pauseBtn))

    pauseBtn.click()


def BeginDownload(browser):
    """Begin Download"""

    saveCss = "div[id='asc_playercontrols_savereplayables_btn']"
    mediaSrcsAudioCss = "li[class='mediasources_audio'] > label > input"
    mediaSrcsChat = "li[class='mediasources_chat'] > label > input"
    okBtnCss = "button[class='asc_jbox_ok_button']"

    ClosePopOut(browser)

    saveBtn = browser.find_element(By.CSS_SELECTOR, saveCss)

    saveBtn.click()

    # Will Bring up dialog
    audioInput = browser.find_element(By.CSS_SELECTOR, mediaSrcsAudioCss)
    Half()

    try:
        audioInput.click()
    except Exception as err:
        Msg("Click to download failed")
        if DebugMode():
            breakpoint()

    okBtn = browser.find_element(By.CSS_SELECTOR, okBtnCss)

    okBtn.click()


def ActivateRow(browser, row):
    """Activate Row"""

    ActionChains(browser).move_to_element(row).double_click().perform()

    PausePlayer(browser)


def AttributeChanged(object, attribute, value):
    """Check if attribute Changed"""

    flag = False

    current_value = object.get_attribute(attribute)

    if value != current_value:
        flag = True

    return flag


def WaitUntilTrue(interval, func, *args, **kwargs):
    """Wait Until Something is True"""

    start = datetime.now()
    result = True

    while not func(*args, *kwargs):
        Sleep(0.10)

        current = datetime.now()
        passed = current - start

        if passed.seconds >= interval:
            result = False
            break

    return result


def Download(browser, recording):
    """Download Recording"""

    row = recording.row

    # Active Row
    ActivateRow(browser, row)
    # Begin Download
    BeginDownload(browser)


def BatchDownloading(browser):
    """Download Items"""

    nextClassDisabled = "ui-paginator-next ui-state-default ui-corner-all ui-state-disabled"
    nextButtonDisabledCss = f"a[class='{nextClassDisabled}']"
    nextButtonCss = "a[aria-label='Next Page']"

    nextBtn = browser.find_element(By.CSS_SELECTOR, nextButtonCss)

    # Search from start date to end date in increments of 5 downloads per until all files downloaded
    startDate = officialStart
    searchInterval = timedelta(days=30)
    correction = timedelta(seconds=1)

    activeDownloads = list()

    while startDate < officialEnd:
        endDate = startDate + searchInterval

        Search(browser, startDate, endDate)

        while True:
            data = GetData(browser)

            for recording in data:
                cells = recording.data

                recording_we_want = False
                # check cells for correct recordings to D/L
                # TODO Get info for recordings to keep
                # TODO Check recording to see if it's already downloaded

                if recording_we_want:
                    # Only allow for simultaneousDownloads
                    activeDownloads.append(recording)
                    Download(browser, recording)

                    if len(activeDownloads) >= simultaneousDownloads:
                        # Wait loop for download completion
                        # TODO Create wait and rename/unzip, categorize, log stuff
                        # Remove files from activeDownloads as completed
                        pass

            if nextBtn.get_attribute("class") != nextClassDisabled:
                nextBtn.click()
                Sleep(4)
            else:
                break

        startDate = endDate + correction
        endDate = (startDate + searchInterval) - correction

def Search(browser, startDate, endDate):
    """Set and Conduct Search"""

    # Find "General dropdown
    general = browser.find_element(By.CSS_SELECTOR, "a[id='conversationToolbar:commonFunctionsMenuBtn']")
    general.click()

    # Find Search anchor and click it
    anchor = browser.find_element(By.CSS_SELECTOR, "a[id='conversationToolbar:toolbarSearchBtn']")
    anchor.click()

    Quarter()

    # Set Select box

    sbox = browser.find_element(By.CSS_SELECTOR,
                                "select[id='conversationObjectView:j_idt132:searchdatatable:0:searchMenu']")
    WebDriverWait(browser, 5).until(visibility_of(sbox))

    select = Select(sbox)
    # Set "between", then set dates. VALUE = "BETWEEN"
    select.select_by_value('BETWEEN')

    Quarter()

    WebDriverWait(browser, 5).until(presence_of_element_located(
        (By.CSS_SELECTOR, "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarOne_input']")))
    WebDriverWait(browser, 5).until(presence_of_element_located(
        (By.CSS_SELECTOR, "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarTwo_input']")))

    # Get begin and end date inputs
    startInput = browser.find_element(By.CSS_SELECTOR,
                                      "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarOne_input']")
    endInput = browser.find_element(By.CSS_SELECTOR,
                                    "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarTwo_input']")
    searchBtn = browser.find_element(By.CSS_SELECTOR, "button[id='conversationObjectView:j_idt413'")

    spinnerCss = "div[id='statusDialogId']"
    spinner = browser.find_element(By.CSS_SELECTOR, spinnerCss)

    closeAnchorCss = "div[id='conversationObjectView:searchDialog'] > div > a[class='ui-dialog-titlebar-icon ui-dialog-titlebar-close ui-corner-all']"
    closeAnchor = browser.find_element(By.CSS_SELECTOR, closeAnchorCss)

    startInput.clear()
    startInput.send_keys(startDate.strftime("%m/%d/%Y %I:%M:%S %p"))
    endInput.clear()
    endInput.send_keys(endDate.strftime("%m/%d/%Y %I:%M:%S %p"))

    # Start Search
    searchBtn.click()

    # Wait for search to complete

    Half()

    startSearch_Timestamp = datetime.now()

    flag = WaitUntilTrue(7200, AttributeChanged, spinner, "aria-hidden", "false")

    # WebDriverWait(browser, 7200).until(AttributeChanged(spinner, "aria-hidden", "false"))

    searchDuration = datetime.now() - startSearch_Timestamp

    Msg(f"Elapsed search time : {searchDuration}")

    # Close Search Box
    closeAnchor.click()


def GetVoiceRecordings(browser, url):
    """Get ACS Voice Recordings... Probably"""

    global Username, Password

    # Setup the Browser (i.e. Navigate to URL)
    SetupBrowser(browser, url)

    # Make us bigggggg
    # Maximize(browser)

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

        Download(browser, data[0])

        if DebugMode():
            DbgMsg("*** <<< Last breakpoint before termination >>>")
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

    ebtn = edom(button1)

    if DebugMode():
        breakpoint()

    Sleep(2)

    button1.click()

    Sleep(2)

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

    Sleep(2)


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
    CmdLineMode(True)
    DebugMode(True)

    ascVoiceRecordings = True
    urls = {
        "packt": "https://www.packtpub.com/free-learning/",
        "acs": "https://129.49.122.190/POWERplayWeb/",
        "tsa": "https://techstepacademy.com/training-ground/",
        "tsatrial": "https://techstepacademy.com/trial-of-the-stones/"
    }

    chrome = None

    if ascVoiceRecordings:
        options = DownloadOptions(r"D:\Backups\asc")
        chrome = webdriver.Chrome(options=options)
    else:
        chrome = webdriver.Chrome()

    if ascVoiceRecordings:
        GetVoiceRecordings(chrome, urls["acs"])
    else:
        GetTSA(chrome, urls["tsa"])
        # GetStones(chrome, urls["tsatrial"])

        # GeteBook(chrome, urls["packt"])

    chrome.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
