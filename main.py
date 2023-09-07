# Imports

# Regular stuff
import os
import io
import sys
import argparse
import configparser
import shutil
import platform
import csv
import json
import re
import zipfile
import datetime as dt
from datetime import datetime, timedelta
import time
import inspect
import functools
import ait
import py_helper as ph
import requests
import urllib

# My Stuff
from py_helper import CmdLineMode, DebugMode, DbgMsg, Msg, DbgEnter, DbgExit, DebugMe, DbgNames, DbgAuto, ErrMsg

# Selenium Stuff
import selenium.webdriver.support.wait as swait
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import *

# Eventing Stuff

def Event(comment):
    """Register An Event"""

    global EventList

    if EventList is not None and comment is not None:
        EventList.append(comment)


def ClearEvents():
    """Clear Event List"""

    global EventList

    if EventList is not None:
        EventList.clear()


def PrintEvents():
    """Print Events"""

    global EventList

    if EventList is not None:
        for message in EventList:
            Msg(message)


def Eventing(start_message, end_message=None, leave=False):
    """Eventing Decorator"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ClearEvents()

            Event(start_message)

            results = func(*args, **kwargs)

            Event(end_message)

            if not leave:
                ClearEvents()

            return results
        return wrapper
    return decorator


# Classes

class SleepShortCuts:
    """Sleep Shortcuts"""

    def Sleep(self, interval=1):
        """Sleep given interval"""

        time.sleep(interval)

    def Tenth(self):
        """Sleep 1/10th of a Second"""

        self.Sleep(0.10)

    def Quarter(self):
        """Sleep Quarter Second"""

        self.Sleep(0.25)

    def Half(self):
        """Sleep Half Second"""

        self.Sleep(0.5)

    def Second(self):
        """Sleep a Second"""

        self.Sleep()


class Browser(SleepShortCuts):
    """Browser Instance Class"""

    browser = None
    options = None

    downloadPath = None

    url = None
    session_id = None

    def __init__(self, url, download_path):
        """Initialize Instance"""

        self.downloadPath = download_path

        self.options = DownloadOptions(download_path)
        self.browser = webdriver.Chrome(options=self.options)
        self.Get(url)

    def Maximize(self):
        """Maximize Browser Windows Helper"""

        self.browser.maximize_window()

    def Refresh(self):
        """Refresh Browser Window"""

        self.browser.refresh()

    def Reconnect(self):
        """Reconnect to lost session"""

        browser2 = webdriver.Remote(command_executor=self.url)

        if browser2.session_id != self.session_id:
            browser2.close()
            browser2.quit()

        browser2.session_id = self.session_id

        self.browser = browser2

    def Windows(self):
        """Show all window ID's and currently selected window"""

        Msg("All Window Handles\n==================")
        for handle in self.browser.window_handles:
            Msg(handle)

        Msg(f"Present Window : {self.browser.current_window_handle}")

    def ByType(self, searchType, path, msg="None"):
        """Search Single By Supplied Type"""

        dbgblk, dbglb = DbgNames(self.ByType)

        DbgEnter(dbgblk, dbglb)

        DbgMsg(f"Searching for : {path} / {msg}", dbglabel=dbglb)

        item = None

        try:
            if searchType == By.CSS_SELECTOR:
                item = self.ByCSS(path)
            else:
                item = self.ByXPATH(path)
        except TimeoutException:
            DbgMsg("Timeout reached exception", dbglabel=dbglb)
        except NoSuchElementException:
            DbgMsg("No such element exception", dbglabel=dbglb)
        except StaleElementReferenceException:
            DbgMsg("Stale element exception", dbglabel=dbglb)
        except Exception as err:
            DbgMsg(f"A generic error occurred while waiting or looking for a warning popup : {err}", dbglabel=dbglb)

        DbgExit(dbgblk, dbglb)

        return item

    def ByCSS(self, css, msg=''):
        """Get By CSS Shortcut"""

        dbgblk, dbglb = DbgNames(self.ByCSS)

        DbgEnter(dbgblk, dbglb)

        DbgMsg(f"Searching for : {css} / {msg}", dbglabel=dbglb)

        item = None

        try:
            item = self.browser.find_element(By.CSS_SELECTOR, css)
        except TimeoutException:
            DbgMsg("Timeout reached exception", dbglabel=dbglb)
        except NoSuchElementException:
            DbgMsg("No such element exception", dbglabel=dbglb)
        except StaleElementReferenceException:
            DbgMsg("Stale element exception", dbglabel=dbglb)
        except Exception as err:
            DbgMsg(f"A generic error occurred while waiting or looking for a warning popup : {err}", dbglabel=dbglb)

        DbgExit(dbgblk, dbglb)

        return item

    def MultiByCSS(self, css, msg=''):
        """Multi Get By CSS Shortcut"""

        dbgblk, dbglb = DbgNames(self.MultiByCSS)

        DbgEnter(dbgblk, dbglb)

        DbgMsg(f"Searching for : {css} / {msg}", dbglabel=dbglb)

        items = list()

        try:
            items = self.browser.find_elements(By.CSS_SELECTOR, css)
        except TimeoutException:
            Msg("Timeout reached exception")
        except NoSuchElementException:
            Msg("No such element exception")
        except StaleElementReferenceException:
            Msg("Stale element exception")
        except Exception as err:
            Msg(f"A generic error occurred while waiting or looking for a warning popup : {err}")

        DbgExit(dbgblk, dbglb)

        return items

    def ByXPATH(self, xpath, msg=''):
        """Get By XPATH Shortcut"""

        dbgblk, dbglb = DbgNames(self.ByXPATH)

        DbgEnter(dbgblk, dbglb)

        DbgMsg(f"Searching for : {xpath} / {msg}", dbglabel=dbglb)

        item = None

        try:
            item = self.browser.find_element(By.XPATH, xpath)
        except TimeoutException:
            Msg("Timeout reached exception")
        except NoSuchElementException:
            Msg("No such element exception")
        except StaleElementReferenceException:
            Msg("Stale element exception")
        except Exception as err:
            Msg(f"A generic error occurred while waiting or looking for a warning popup : {err}")

        DbgExit(dbgblk, dbglb)

        return item

    def MultiByXPATH(self, xpath, msg=''):
        """Multi Get By XPATH Shortcut"""

        dbgblk, dbglb = DbgNames(self.MultiByXPATH)

        DbgEnter(dbgblk, dbglb)

        DbgMsg(f"Searching for : {xpath} / {msg}", dbglabel=dbglb)

        items = list()

        try:
            items = self.browser.find_elements(By.XPATH, xpath)
        except TimeoutException:
            Msg("Timeout reached exception")
        except NoSuchElementException:
            Msg("No such element exception")
        except StaleElementReferenceException:
            Msg("Stale element exception")
        except Exception as err:
            Msg(f"A generic error occurred while waiting or looking for a warning popup : {err}")

        DbgExit(dbgblk, dbglb)

        return items

    def Get(self, url):
        """Get Call on Web Driver"""

        self.url = url
        self.browser.get(self.url)

    def SwitchContext(self, window, frame=None):
        """Switch Context, the easy way"""

        dbgblk, dbglb = DbgNames(self.SwitchContext)

        DbgEnter(dbgblk, dbglb)

        try:
            if window is not None:
                self.browser.switch_to.window(window)
            if frame is not None:
                self.browser.switch_to.frame(frame)
        except NoSuchWindowException:
            DbgMsg(f"No such window exception for {window}", dbglabel=dbglb)
        except NoSuchFrameException:
            DbgMsg(f"No such frame exception for {frame}", dbglabel=dbglb)
        except Exception as err:
            DbgMsg(f"A generic error occurred when trying to switch context : {err}", dbglabel=dbglb)

        DbgExit(dbgblk, dbglb)

    def SwitchFrame(self, name, pause=0):
        """Context/Content Switch Helper"""

        dbgblk, dbglb = DbgNames(self.SwitchFrame)

        success = False

        if pause > 0:
            self.Sleep(pause)

        try:
            self.browser.switch_to.frame(name)
            success = True
        except NoSuchFrameException:
            DbgMsg(f"No such frame {name}", dbglabel=dbglb)
        except Exception as err:
            Msg(f"Generic error when trying to switch to frame {name} : {err}")

        return success

    def SwitchWindow(self, window_handle):
        """Switch Between Windows"""

        dbgblk, dbglb = DbgNames(self.SwitchWindow)

        DbgEnter(dbgblk, dbglb)

        self.url = self.browser.command_executor._url
        self.session_id = self.browser.session_id

        try:
            try:
                self.Half()
                self.browser.switch_to.window(window_handle)
            except ConnectionResetError as crst:
                if DebugMode():
                    DbgMsg("We are disconnected, try to reconnect by stepping", dbglabel=dbglb)

                    breakpoint()
                self.Reconnect()
                self.browser.switch_to.window(window_handle)
        except Exception as err:
            ErrMsg(err, "A problem occurred switching browser windows")

            if DebugMode():
                breakpoint()

        DbgExit(dbgblk, dbglb)

    def SwitchTab(self, tab_handle):
        """Switch to tab"""

        self.SwitchWindow(tab_handle)

    def NewTab(self, url):
        """Open New Tab"""

        original_handle = self.browser.current_window_handle

        self.browser.switch_to.new_window('tab')

        tab_handle = self.browser.current_window_handle

        self.browser.get(url)

        self.SwitchWindow(original_handle)

        return tab_handle

    def NewSession(self, url):
        """New Session"""

        dbgblk, dbglb = DbgNames(self.NewSession)

        DbgEnter(dbgblk, dbglb)

        options = self.DownloadOptions(downloadPath)
        self.browser = webdriver.Chrome(options=options)

        self.SetupBrowser(url)

        DbgExit(dbgblk, dbglb)

        return self.browser

    def DownloadOptions(self, folder_path, with_caps=False):
        """Set Browser Download Path"""

        options = Options()

        if with_caps:
            # options.set_capability("browserVersion", "latest")
            # options.set_capability("platformName", "linux")
            options.set_capability("platformName", "Windows 10")

            # Folder path removed here for Grid system, can be added back in if path exists
            options.add_experimental_option("prefs", {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True})
        else:
            options.add_experimental_option("prefs", {
                "download.default_directory": folder_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True})

        options.add_argument('ignore-certificate-errors')

        return options

    def BadCert(self):
        """Helper for Getting Past Bad Certs"""

        adv_btn = self.ByCSS("button[id='details-button']")
        adv_btn.click()

        self.Half()

        anchor = self.ByCSS("div > p > a[id='proceed-link']")

        anchor.click()

        self.Sleep()

    def AttributeChanged(self, object, attribute, value):
            """Check if attribute Changed"""

            flag = False

            current_value = object.get_attribute(attribute)

            if value != current_value:
                flag = True

            return flag

    def TagToAppear(self, selector_type, selector, timeout=5):
        """Wait for Tag to Appear"""

        result = None

        try:
            WebDriverWait(self.browser, timeout).until(presence_of_element_located((selector_type, selector)))

            result = self.ByType(selector_type, selector)
        except Exception as err:
            ErrMsg(err, "An error occurred waiting for a tag to appear")

        return result

    def WaitUntilTrue(self, time_period, func, *args, **kwargs):
        """Wait Until Something is True"""

        start = datetime.now()
        result = True

        while not func(*args, *kwargs):
            self.Tenth()

            current = datetime.now()
            passed = current - start

            if passed.seconds >= time_period:
                result = False
                break

        return result

    def WaitPresenceCSS(self, timeout, selector):
        """Wait for Something to be present"""

        dbgblk, dbglb = DbgNames(self.WaitPresenceCSS)

        DbgEnter(dbgblk, dbglb)

        resultset = dict()

        resultset["present"] = False
        resultset["timeout"] = False
        resultset["stale"] = False
        resultset["nosuchelement"] = False
        resultset["error"] = (False, None)
        resultset["item"] = None

        try:
            DbgMsg(f"Waiting for : {selector}", dbglabel=dbglb)

            WebDriverWait(self.browser, timeout).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
            resultset["present"] = True

            resultset["item"] = self.ByCSS(selector)
        except TimeoutException as t_err:
            resultset["timeout"] = True
            resultset["error"] = (True, t_err)
        except NoSuchElementException as ns_err:
            resultset["nosuchelement"] = True
            resultset["error"] = (True, ns_err)
        except StaleElementReferenceException as s_err:
            resultset["stale"] = True
            resultset["error"] = (True, s_err)
        except Exception as err:
            resultset["error"] = (True, err)
            DbgMsg(f"Unexpected exception waiting for {selector} : {err}", dbglabel=dbglb)

        DbgExit(dbgblk, dbglb)

        return resultset

    def WaitVisibleCSS(self, selector, timeout=2):
        """Wait until Element is Visible"""

        results = ( True, None )

        try:
            WebDriverWait(self.browser, timeout).until(visibility_of_element_located((By.CSS_SELECTOR, selector)))
        except TimeoutException as t_err:
            results = ( False, t_err )
        except NoSuchElementException as ns_err:
            results = ( False, ns_err )
        except StaleElementReferenceException as s_err:
            results = ( False, s_err )
        except Exception as err:
            results = ( False, err )
            DbgMsg(f"Unexpected exception waiting for {selector} : {err}", dbglabel=dbglb)

        return results

    def WaitClickableCSS(self, selector, timeout=2):
        """Wait for element to be Clickable"""

        results = (True, None)

        try:
            WebDriverWait(self.browser, timeout).until(element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        except TimeoutException as t_err:
            results = (False, t_err)
        except NoSuchElementException as ns_err:
            results = (False, ns_err)
        except StaleElementReferenceException as s_err:
            results = (False, s_err)
        except Exception as err:
            results = (False, err)
            DbgMsg(f"Unexpected exception waiting for {selector} : {err}", dbglabel=dbglb)

        return results

    def ScrollIntoView(self, element):
        """Scroll Element Into View"""

        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)

    def ClickAction(self, selector=None, element=None):
        """Use Action to Click Element By Locator"""

        if selector is not None:
            element = self.ByCSS(selector)

        ActionChains(self.browser).move_to_element(element).click().perform()

    def DoubleClickAction(self, selector=None, element=None):
        """Use Action to Click Element By Locator"""

        if selector is not None:
            element = self.ByCSS(selector)

        ActionChains(self.browser).move_to_element(element).double_click().perform()


class ASCBrowser(Browser):
    """ACS Browser Class"""

    ascTab = None
    downloadsTab = None
    mainFrame = "applicationFrame"

    def __init__(self, url, download_path):
        """Intitialize Instance"""

        super().__init__(url, download_path)

        self.SetContexts()

    def SetContexts(self, frame="applicationFrame"):
        """Set Contexts"""

        dbgblk, dbglb = DbgNames(self.SetContexts)

        DbgEnter(dbgblk, dbglb)

        self.ascTab = self.browser.current_window_handle
        self.mainFrame = frame

        DbgExit(dbgblk, dbglb)

    def NewSessionWithLogin(self, url):
        """New Session With Expected Login"""

        dbgblk, dbglb = DbgNames(self.NewSessionWithLogin)

        DbgEnter(dbgblk, dbglb)

        options = self.DownloadOptions(downloadPath)
        self.browser = webdriver.Chrome(options=options)

        self.SetupBrowser(url)

        if self.SmartLogin():
            DbgExit(dbgblk, dbglb)

            return self.browser

        DbgExit(dbgblk, dbglb)

        return None

    def OpenDownloadsTab(self):
        """Open Downloads Tab"""

        dbgblk, dbglb = DbgNames(self.OpenDownloadsTab)

        DbgEnter(dbgblk, dbglb)

        current_window = self.browser.current_window_handle

        tab_handle = self.NewTab("chrome://downloads")

        DbgExit(dbgblk, dbglb)

        return current_window, tab_handle

    def CloseDownloadsTab(self):
        """Close Downloads Tab"""

        dbgblk, dbglb = DbgNames(self.CloseDownsTab)

        DbgEnter(dbgblk, dbglb)

        self.SwitchWindow(self.downloadsTab)

        self.browser.close()

        self.SwitchWindow(self.ascTab)

        DbgExit(dbgblk, dbglb)

    def MainContext(self):
        """Switch to Main Context"""

        dbgblk, dbglb = DbgNames(self.MainContext)

        DbgEnter(dbgblk, dbglb)

        self.SwitchContext(self.ascTab, self.mainFrame)

        DbgExit(dbgblk, dbglb)

    def CancelDialog(self):
        """Cancel Login Dialog Helper"""

        dbgblk, dbglb = DbgNames(self.CancelDialog)

        DbgEnter(dbgblk, dbglb)

        self.Sleep(3.0)

        ait.press("\t", "\t", "\t")
        self.Half()
        ait.press("\n")
        self.Half()

        DbgExit(dbgblk, dbglb)

    def DumbLogin(self, username, password):
        """Logging Into ACS, the Dumb Way, Ommmm"""

        dbgblk, dbglb = DbgNames(self.DumbLogin)

        DbgEnter(dbgblk, dbglb)

        self.Half()

        ait.write(username)
        ait.press("\t")
        ait.write(password)
        ait.press("\t", "\t")
        ait.press("\n")

        self.Second()

        DbgExit(dbgblk, dbglb)

    def SmartLogin(self, username, password):
        """Smart Login ACS"""

        dbgblk, dbglb = DbgNames(self.SmartLogin)

        DbgEnter(dbgblk, dbglb)

        success = False

        if self.SwitchFrame(0):
            DbgMsg("Logging in", dbglabel=dbglb)

            userInput = self.ByCSS("input[id='loginTabView:loginName:inputPanel:inputText']")
            passwordInput = self.ByCSS("input[id='loginTabView:loginPassword:inputPanel:inputPassword']")
            submitButton = self.ByCSS("button[id='loginTabView:loginButton']")

            userInput.send_keys(username)
            passwordInput.send_keys(password)

            self.Half()

            submitButton.click()

            self.Second()

            success = True
        else:
            Msg("*** Mucho problemo Jose!!! Can't log in")

        DbgExit(dbgblk, dbglb)

        return success

    def SmartLogout(self):
        """Logout Helper"""

        dbgblk, dbglb = DbgNames(self.SmartLogout)

        DbgEnter("Logging out", dbglb)

        span = "table[id='powpwfteaper27'] > tbody > tr > td > span[id='powpwfteaper28']"
        anchorID = "a[id='logoutMenuItem']"

        spanobj = self.ByCSS(span)

        WebDriverWait(self.browser, 30).until(presence_of_element_located((By.CSS_SELECTOR, anchorID)))

        logoffAnchor = self.ByCSS(anchorID)

        spanobj.click()

        WebDriverWait(self.browser, 30).until(visibility_of(logoffAnchor))

        logoffAnchor.click()

        DbgExit(dbgblk, dbglb)

    def FastQuit(self):
        """Fast Quit"""

        self.SmartLogout()
        self.browser.quit()

        sys.exit(-1)

    def BusySpinnerPresent(self, closeit=False):
        """Detect Busy Spinner"""

        dbgblk, dbglb = DbgNames(self.BusySpinnerPresent)

        DbgEnter(dbgblk, dbglb)

        busyCss = "div[id='statusDialogId']"
        imgCss = f"{busyCss} > div > img[id='aswpwfteapte18']"

        busyFlag = False

        try:
            busy = self.ByCSS(busyCss)

            if busy.is_displayed():
                busyFlag = True

                if closeit:
                    self.Half()
                    # Do Something
                    # aria-hidden=true, aria-live=off, class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidden-container ajaxStatusDialog"
                    # style=width: auto; height: auto; left: 649px; top: 600.5px; z-index: 1039; display: none;

                    self.browser.execute_script("document.getElementById('statusDialogId').style.display='none';")

                    self.Half()

        except Exception as err:
            DbgMsg(f"An error occurred : {err}")

        DbgExit(dbgblk, dbglb)

        return busyFlag

    def PopoutPresent(self, timeout=5):
        """Check to see if Popout is Present"""

        dbgblk, dbglb = DbgNames(self.PopoutPresent)

        DbgEnter(dbgblk, dbglb)

        italicsCss = "div[id='rightContent'] > table[id='aswpwfteapte42'] > tbody > tr > td > i[id='aswpwfteapte32']"
        italicsXpath = "//div[@id='rightContent']/table[@id='aswpwfteapte42']/tbody/tr/td/i[@id='aswpwfteapte32']"

        results = self.WaitPresenceCSS(timeout, italicsCss)

        success = results["present"]

        DbgExit(dbgblk, dbglb)

        return success

    def ClosePopOut(self, frame_name=None):
        """Close that fucking annoying pop out"""

        dbgblk, dbglb = DbgNames(self.ClosePopOut)

        DbgEnter(dbgblk, dbglabel=dbglb)

        self.MainContext()

        self.Second()

        italicsCss = "div[id='rightContent'] > table[id='aswpwfteapte42'] > tbody > tr > td > i[id='aswpwfteapte32']"
        italicsXpath = "//div[@id='rightContent']/table[@id='aswpwfteapte42']/tbody/tr/td/i[@id='aswpwfteapte32']"

        success = False

        try:
            self.Half()

            count = 0

            while not self.PopoutPresent() and count < 2:
                self.Half()
                count += 1

            if count > 1:
                raise NoSuchElementException("Popout didn't appear and this exception was raised while looking for it")

            self.Half()

            italics = self.ByCSS(italicsCss)

            if italics.is_displayed():
                self.Half()
                DbgMsg("Trying to close/click Popout", dbglabel=dbglb)
                italics.click()
                DbgMsg("Popout should be closed", dbglabel=dbglb)
                self.Half()

                success = True
        except NoSuchElementException as err_nse:
            DbgMsg(f"No such element, {italicsCss} present", dbglabel=dbglb)
        except StaleElementReferenceException:
            DbgMsg(f"Stale element exception when trying to clear pop out", dbglabel=dbglb)
        except TimeoutException:
            DbgMsg("Timed out looking for pop out", dbglabel=dbglb)
        except Exception as err:
            Msg(f"Generic error trying to clear pop out {err}")

        DbgExit(dbgblk, dbglabel=dbglb)

        return success

    def GetPageCount(self):
        """Get Search Results Page Count"""

        dbgblk, dbglb = DbgNames(self.GetPageCount)

        DbgEnter(dbgblk, dbglb)

        pagecountCss = "span[class='ui-paginator-current']"
        expr = r"^(?P<start>\d+)\s+-\s+(?P<end>\d+)\s+of\s+(?P<total>\d+)$"

        pageCountSpan = self.ByCSS(pagecountCss)

        results = (0, 0, -1)

        if pageCountSpan is not None:
            matches = re.search(expr, pageCountSpan.text)

            if matches is not None:
                start = int(matches.group("start"))
                end = int(matches.group("end"))
                total = int(matches.group("total"))

                results = (start, end, total)

        DbgExit(dbgblk, dbglb)

        return results

    def BlankRow(self, recording):
        """Check For Blank Row"""

        blank = False

        for column_value in recording.data.values():
            if column_value is not None and column_value != "":
                break
        else:
            blank = True

        return blank

    def GetRows(self):
        """Get Rows from Search"""

        dbgblk, dbglb = DbgNames(self.GetRows)

        DbgEnter(dbgblk, dbglb)

        rows = self.MultiByCSS("div[class='ui-datatable-scrollable-body'] > table > tbody[id='masterTable:ascTable_data'] > tr")

        DbgExit(dbgblk, dbglb)

        return rows

    @Eventing("Entering GetData", "Exiting GetData")
    def GetData(self, frame_name=None):
        """Get Data"""

        dbgblk, dbglb = DbgNames(self.GetData)

        DbgEnter(dbgblk, dbglb)

        if frame_name is not None:
            Event("Switching frame")
            self.SwitchFrame(frame_name)

        Event("Closing popout")
        if self.ClosePopOut():
            Event("Appears Popout was closed")
        else:
            Event("Appears Popout WAS NOT closed for some reason")

        Msg("************* >>>>>>>>>>>>> Getting Rows <<<<<<<<<<<<<")

        norecs = "No records found"

        retries = 1
        retry_count = 0
        retry = True
        last_rowkey = None

        try:
            Event("Entering try-while block")
            while retry:
                Event("Getting rows")
                rows = self.GetRows()

                records = list()

                Event(f"Retrieved {len(rows)}")

                count = 1
                for row in rows:
                    recording = RecordingRecord(row)

                    last_rowkey = recording.rowkey
                    Event(f"Processing {last_rowkey}")

                    if self.BlankRow(recording):
                        DbgMsg(f"Row for appears empty, skipping\n{recording.data}", dbglabel=dbglb)
                        continue

                    if DebugMode() and recording.data is None:
                        DbgMsg("Recording.data is none, why?")
                        breakpoint()

                    try:
                        Event("Checking for blanks, ie. no search results")
                        loaded = recording.data.get("Loaded", "xxx")
                        retry = False
                        Event("Checking for no search results seems to have succeeded")
                    except Exception as err:
                        Msg(f"Checking for 'Loaded' column seems to have failed : {err}", dbglabel=dbglb)
                        retry = True if retry_count < retries else False
                        retry_count += 1

                    if loaded != norecs and recording.data['Start Time'] != '':
                        DbgMsg(f"Processing {count} : {recording.data['Conversation ID']}", dbglabel=dbglb)
                        count += 1

                        records.append(recording)
                    elif loaded == norecs:
                        DbgMsg("No data for this time frame", dbglabel=dbglb)
                    else:
                        DbgMsg(f"Something other than no data rows has happened for processed item {count}",
                               dbglabel=dbglb)
                        DbgMsg(f"Record is\n{recording.data}", dbglabel=dbglb)

                    if BreakpointCheck(nobreak=True) and DebugMode():
                        DbgMsg(f"In {dbglb} when manual breakpoint detected", dbglabel=dbglb)
                        breakpoint()
        except Exception as err:
            PrintEvents()
            ErrMsg(err, "An error occurred while trying to process rows from the search")

            if DebugMode():
                DbgMsg(f"Last {last_rowkey} could not be processed", dbglabel=dbglb)

        DbgExit(dbgblk, dbglb)

        return records

    def PausePlayer(self, timeout=5):
        """Pause Player"""

        dbgblk, dbglb = DbgNames(self.PausePlayer)

        DbgEnter(dbgblk, dbglb)

        pauseBtnCss = "div[id='asc_playercontrols_pause_btn']"

        pauseBtn = self.ByCSS(pauseBtnCss)

        try:
            WebDriverWait(self.browser, timeout).until(visibility_of(pauseBtn))

            pauseBtn.click()
        except TimeoutException:
            DbgMsg("Timeout reached, player control is not visible or accessible, BAD", dbglabel=dbglb)
        except NoSuchElementException:
            DbgMsg("No such element error while looking for pause button", dbglabel=dbglb)
        except StaleElementReferenceException:
            DbgMsg("Stale element exception while looking for pause button", dbglabel=dbglb)
        except Exception as err:
            DbgMsg(f"A generic error occurred while trying to pause player : {err}", dbglabel=dbglb)

        DbgExit(dbgblk, dbglb)

    def StalledDownload(self, rowkey=None):
        """Check for Stalled Download"""

        dbgblk, dbglb = DbgNames(self.StalledDownload)

        DbgEnter(dbgblk, dbglb)

        saveBoxCss = "div[class='jBox-container'] > div[class='jBox-title jBox-draggable'] > div"
        btnOkCss = "div[class='jBox-footer'] > div[class='asc_dialog_footer'] > button[class='asc_jbox_ok_button']"
        btnCancelCss = "div[class='jBox-footer'] > div[class='asc_dialog_footer'] > button[class='asc_jbox_cancel_button']"

        prepPerCss = "div[id='asc_player_saveas_progress'] > div > span[id='asc_player_saveas_progressbar_percentage']"
        prepFileCss = "div[id='asc_player_saveas_progress'] > div > span[id='asc_player_saveas_progressbar_file_percentage']"

        stalled = False

        result = self.WaitPresenceCSS(3, saveBoxCss)

        if result["present"]:
            timechk = datetime.now()

            while result["present"] and not stalled:
                self.Quarter()

                result = self.WaitPresenceCSS(1, saveBoxCss)

                if result["present"]:
                    time_passed = datetime.now() - timechk

                    if time_passed.seconds > 8:
                        cancelBtn = self.ByCSS(btnCancelCss)
                        progress = self.ByCSS(prepPerCss)

                        if cancelBtn is not None and progress is not None and time_passed.seconds <= 10:
                            if progress.text == "0%":
                                cancelBtn.click()
                                stalled = True
                            elif progress.text == "":
                                try:
                                    # Last ditch chance to complete d/l
                                    okBtn = self.ByCSS(btnOkCSS)

                                    obBtn.click()
                                    DbgMsg("Came across case where save dialog was up and not stalled")
                                except Exception as err:
                                    DbgMsg("Save dialog stalled or not, can't tell")
                        elif time_passed.seconds > 10:
                            stalled = True
                            if cancelBtn is not None:
                                cancelBtn.click()

        if stalled and DebugMode():
            DbgMsg(f"Stalled on rowkey {rowkey}")

        DbgExit(dbgblk, dbglb)

        return stalled

    def WarningMsg(self, rowkey=None):
        """Check for a Warning Popup"""

        dbgblk, dbglb = DbgNames(self.WarningMsg)

        DbgEnter(dbgblk, dbglb)
        DbgMsg(f"Checking for warning on {rowkey}", dbglabel=dbglb)

        conditions = {"rowkey": ""}

        # Wait for error, set success to False if error pops up
        prefix = "div[id='globalHeaderMessage'] > div > div > div[id='headerMessages'] > div"
        errorCss = f"{prefix} > span"
        errMsg = f"{prefix} > ul > li > span[class='ui-messages-error-detail']"

        errmsg = ""

        msg = None
        warning = None

        try:
            self.ClosePopOut()

            result = self.WaitPresenceCSS(8, errorCss)

            if result["present"]:
                DbgMsg(f"Warning present", dbglabel=dbglb)

                warning = result["item"]

                self.Sleep(1.5)

                msg = self.ByCSS(errMsg)

                # Not because I want to, but because this WebUI is so fucking unpredictable in spots... this being one of them.
                if warning is not None:
                    try:
                        if warning.is_displayed():
                            pass
                    except Exception as err:
                        self.Second()
                        warning = self.ByCSS(errorCss)

                if warning.is_displayed() and warning.is_enabled():
                    errmsg = edom(msg)["innerText"]

                    DbgMsg(f"Warning is displayed AND enabled with '{errmsg}' for {rowkey}", dbglabel=dbglb)
                    warning.click()
                    self.Sleep(3)
                else:
                    DbgMsg(f"Warning detected for {rowkey}", dbglabel=dbglb)
                    vismsg = "Is visible" if warning.is_displayed() else "Is NOT visible"
                    enamsg = "Is enabled" if warning.is_enabled() else "Is NOT enabled"
                    errmesg = edom(msg)[
                        "innerText"]  # Named errmesg on purpose to prevent it messing with active errmsg

                    DbgMsg(f"Visibility\t: {vismsg}", dbglabel=dbglb)
                    DbgMsg(f"Enabled\t: {enamsg}", dbglabel=dbglb)
                    DbgMsg(f"With Msg\t: {errmesg}", dbglabel=dbglb)
            else:
                DbgMsg(f"Warning is not present for {rowkey}", dbglabel=dbglb)
        except StaleElementReferenceException as s_err:
            DbgMsg(f"Stale element error triggered during warning check : {s_err}", dbglabel=dbglb)
        except Exception as err:
            ErrMsg(err, "Something happened during warning check")

            if DebugMode():
                breakpoint()

        if BreakWhen(conditions, rowkey=rowkey):
            DbgMsg(f"Rowkey, {rowkey}, matches break condition", dbglabel=dbglb)
            breakpoint()

        BreakpointCheck()
        CheckForEarlyTerminate()

        DbgExit(dbgblk, dbglb)

        return errmsg

    def ActivateRow(self, row, rowkey=None):
        """Activate Row"""

        dbgblk, dbglb = DbgNames(self.ActivateRow)

        DbgEnter(dbgblk, dbglb)
        DbgMsg(f"Attempting to activate {rowkey}", dbglabel=dbglb)

        success = True

        conditions = {"rowkey": ""}

        try:
            self.DoubleClickAction(element=row)
            # ActionChains(self.browser).move_to_element(row).double_click().perform()
        except Exception as err:
            ErrMsg(err, "An error occurred while trying to activate a row")

            if DebugMode():
                breakpoint()

        self.Half()

        self.PausePlayer(timeout=3)

        response = self.WarningMsg(rowkey=rowkey)

        success = (response == "")

        if success:
            self.PausePlayer(timeout=2)

        if BreakWhen(conditions, rowkey=rowkey):
            DbgMsg(f"Rowkey, {rowkey}, matches for breakpoint", dbglabel=dbglb)
            breakpoint()

        DbgExit(dbgblk, dbglb)

        return success

    def GetDownloads(self, sleep_time=3):
        """Get List of Downloads In Download Tab"""

        dbgblk, dbglb = DbgNames(self.GetDownloads)

        DbgEnter(dbgblk, dbglb)

        if BreakpointCheck(nobreak=True) and DebugMode():
            DbgMsg("Manual breakpoint detected", dbglabel=dbglb)
            breakpoint()

        originalTab = self.browser.current_window_handle

        self.SwitchTab(self.downloadsTab)

        if sleep_time > 0:
            self.Sleep(sleep_time)

        downloadsScript = "return document.querySelector('downloads-manager').shadowRoot.querySelectorAll('#downloadsList downloads-item')"

        downloads = self.browser.execute_script(downloadsScript)

        downloadDict = dict()

        progress = {"value": "100"}

        for download in downloads:
            try:
                fname = edom(download.shadow_root.find_element(By.CSS_SELECTOR, "#file-link"))

                try:
                    progress = edom(download.shadow_root.find_element(By.CSS_SELECTOR, "#progress"))
                except NoSuchElementException:
                    DbgMsg("No such element error, progress is not available, assuming 100%", dbglabel=dbglb)

                downloadDict[fname["text"]] = int(progress["value"])
            except NoSuchElementException:
                DbgMsg("Could not file 'file-link' in shadow root of downloads-item")
            except Exception as err:
                Msg(f"Trouble getting download information : {err}")

        self.MainContext()

        DbgExit(dbgblk, dbglb)

        return downloadDict

    @Eventing("Starting Search")
    def Search(self, startDate, endDate):
        """Set and Conduct Search"""

        dbgblk, dbglb = DbgNames(self.Search)

        DbgEnter(dbgblk, dbglb)

        events = list()

        try:
            Event("Beginning Search Run")

            try:
                Event("Looking for general dropdown button")
                # Find "General dropdown
                general = self.ByCSS("a[id='conversationToolbar:commonFunctionsMenuBtn']")
                general.click()
                Event("General dropdown clicked")
            except Exception as err:
                Event(f"General dropdown button could not be found, {err}")

            self.Half()

            try:
                Event("Looking for search anchor")
                # Find Search anchor and click it
                anchor = self.ByCSS("a[id='conversationToolbar:toolbarSearchBtn']")
                anchor.click()
                Event("Anchor clicked")
            except Exception as err:
                Event(f"Anchor either not found or not clicked : {err}")

            self.Half()

            try:
                Event("Select box section")

                # Set Select box
                sbox = self.ByCSS("select[id='conversationObjectView:j_idt132:searchdatatable:0:searchMenu']")
                WebDriverWait(self.browser, 5).until(visibility_of(sbox))

                select = Select(sbox)
                # Set "between", then set dates. VALUE = "BETWEEN"
                select.select_by_value('BETWEEN')

                Event("Selection Completed")
            except Exception as err:
                Event(f"Search box not found or filled, an error occurred : {err}")

            self.Half()

            spinner = None

            try:
                Event(f"Beginning Search between {startDate} and {endDate}")

                WebDriverWait(self.browser, 5).until(presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarOne_input']")))
                WebDriverWait(self.browser, 5).until(presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarTwo_input']")))

                # Get begin and end date inputs
                startInput = self.ByCSS("input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarOne_input']")
                endInput = self.ByCSS("input[id='conversationObjectView:j_idt132:searchdatatable:0:betweenCalendarTwo_input']")
                searchBtn = self.ByCSS("button[id='conversationObjectView:j_idt413'")

                spinnerCss = "div[id='statusDialogId']"
                spinner = self.ByCSS(spinnerCss)

                closeAnchorCss = "div[id='conversationObjectView:searchDialog'] > div > a[class='ui-dialog-titlebar-icon ui-dialog-titlebar-close ui-corner-all']"
                closeAnchor = self.ByCSS(closeAnchorCss)

                startInput.clear()
                startInput.send_keys(startDate.strftime("%m/%d/%Y %I:%M:%S %p"))
                endInput.clear()
                endInput.send_keys(endDate.strftime("%m/%d/%Y %I:%M:%S %p"))

                DbgMsg(f"Conducting search between {startDate} and {endDate}", dbglabel=dbglb)

                # Start Search
                searchBtn.click()

                Event("Search completed")
            except Exception as err:
                Event(f"An error occurred while filling out the search : {err}")

            # Wait for search to complete

            self.Half()

            startSearch_Timestamp = datetime.now()

            flag = self.WaitUntilTrue(3600, AttributeChanged, spinner, "aria-hidden", "false")

            searchDuration = datetime.now() - startSearch_Timestamp

            Msg(f"Elapsed search time : {searchDuration}")

            # Close Search Box
            closeAnchor.click()

            Event("Close anchor clicked, we done")
        except Exception as err:
            ErrMsg(err, "An error occurred while trying to execute a search")

            Event(f"Bummer, an error occurred while attempting a search : {err}")

            if DebugMode():
                DbgMsg(
                    f"Something hit the fan during a search, you can checked the 'events' list to see the last successful or errored event")
                breakpoint()

        DbgExit(dbgblk, dbglb)

    def BeginDownload(self, vrec=None):
        """Begin Download"""

        dbgblk, dbglb = DbgNames(self.BeginDownload)

        DbgEnter(dbgblk, dbglb)

        success = True
        saveCss = "div[id='asc_playercontrols_savereplayables_btn']"
        mediaSrcsAudioCss = "li[class='mediasources_audio'] > label > input"
        mediaSrcsAudioCssDis = "li[class='mediasources_audio asc_disabled'] > label > input"
        mediaSrcsChat = "li[class='mediasources_chat'] > label > input"
        okBtnCss = "button[class='asc_jbox_ok_button']"
        cancelBtnCss = "button[class='asc_jbox_cancel_button']"

        self.ClosePopOut()

        saveBtn = self.ByCSS(saveCss)
        saveBtn.click()

        # Will Bring up dialog
        audioInputDis = None
        audioInput = self.ByCSS(mediaSrcsAudioCss, msg="AKA mediaSources Inputbox")

        if audioInput is None:
            audioInputDis = self.ByCSS(mediaSrcsAudioCssDis)

        cancelBtn = self.ByCSS(cancelBtnCss)

        self.Half()

        audioEnabled = False

        try:
            if audioInputDis is None and audioInput is not None and audioInput.is_displayed() and audioInput.is_enabled():
                audioEnabled = True

                aiObj = edom(audioInput)

                count = 0

                while not aiObj.get_prop("checked", False) and count < 3:
                    self.Half()
                    audioInput.click()

                    count += 1
                else:
                    if count > 0 and DebugMode():
                        DbgMsg("Audio checkbox appears to not be checked, look for spinner", dbglabel=dbglb)
                        breakpoint()

                self.Half()

                okBtn = self.ByCSS(okBtnCss)

                self.Half()

                okBtn.click()
            else:
                if DebugMode():
                    DbgMsg("Audio checkbox does not appear to be checked, look for spinner", dbglabel=dbglb)
                    breakpoint()

                success = False
                self.Half()
                cancelBtn.click()

            self.Half()
        except ElementClickInterceptedException:
            success = False

            if DebugMode():
                DbgMsg("audio checkbox unable to be clicked, likely disabled by CSS", dbglabel=dbglb)
        except Exception as err:
            ErrMsg(err, "Click to download failed")
            audioEnabled = False
            success = False

        DbgExit(dbgblk, dbglb)

        return success

    def Download(self, voice_recording, frame_name=None, rows=None):
        """Download Recording"""

        global global_temp, lastprocessed

        dbgblk, dbglb = DbgNames(self.Download)

        DbgEnter(dbgblk, dbglb)

        recording = voice_recording.recording

        success = False
        rowkey = recording.rowkey
        row = None

        if lastprocessed is None:
            last_rowkey = rowkey
        else:
            last_rowkey = lastprocessed.recording.rowkey

        conditions = {"rowkey": ""}

        if frame_name is not None:
            self.SwitchFrame(frame_name)

        try:
            if self.PopoutPresent(timeout=1):
                self.ClosePopOut(frame_name)

            stalled = self.StalledDownload(rowkey=last_rowkey)

            if stalled:
                lastprocessed.AddToBad()
                lastprocessed.progress = 100

                return success

            self.Half()

            rowXPath = f"//tr[@data-rk='{rowkey}']"
            row = self.ByXPATH(rowXPath)

            # Activate Row
            success = self.ActivateRow(row, rowkey)

            if success:
                # Begin Download
                global_temp = ("activation succeeded", rowkey)

                DbgMsg(f"Attempting download of {rowkey} from {voice_recording.Timestamp()}", dbglabel=dbglb)

                if not self.BeginDownload(vrec=voice_recording):
                    global_temp = ("save failed", rowkey)

                    success = False
                    voice_recording.AddToBad()

                    recording.data["Archived"] = "Audio Unavailable/Not Archived"
                    AppendRows(catalogFilename, recording.data)
                    Msg(f"Record {rowkey} for {recording.data['Start Time']} could not be downloaded")
            else:
                global_temp = ("activation failed", rowkey)
                Msg(f"Record {rowkey} for {recording.data['Start Time']} could not be downloaded")

                voice_recording.AddToBad()

                recording.data["Archived"] = "Damaged/Not Archived"
                recording.data["Expanded"] = "Warning received before download"
                AppendRows(catalogFilename, recording.data)
        except Exception as err:
            # check rowkey and list of rows
            Msg(f"Could not activate row with rowkey {rowkey} : {err}")

        if BreakWhen(conditions, rowkey=rowkey):
            DbgMsg(f"Rowkey, {rowkey}, matches for breakpoint", dbglabel=dbglb)
            breakpoint()

        if BreakpointCheck(nobreak=True) and DebugMode():
            DbgMsg("A manual breakpoint was detected... and so I am breakpointing, probably should check the stalled thingy")
            breakpoint()

        lastprocessed = voice_recording

        DbgExit(dbgblk, dbglb)

        return success

    def CompleteBadRecording(self, download):
        """Complete a bad download"""

        recording = download.recording
        myname, mypath = download.MyPath()

        if recording.data["Archived"] is None or recording.data["Archived"] == "" or recording.data["Archived"] == "0":
            recording.data["Archived"] = "No/Not Downloaded"

        recording.data["Expanded"] = "Missing after download"
        missing = os.path.join(mypath, "missing.txt")

        ph.Touch(missing)

        if not download.IsBad():
            download.AddToBad()

    def SaveMetaInfo(self, download):
        """Save Meta Info"""

        myname, mypath = download.MyPath()
        recording = download.recording

        if not os.path.exists(mypath):
            os.makedirs(mypath)

        metafile = os.path.join(mypath, "meta-data.csv")

        if not os.path.exists(metafile):
            AppendRows(metafile, recording.data)

        AppendRows(catalogFilename, recording.data)

    def CompleteDownload(self, download):
        """Complete Download"""

        dbgblk, dbglb = DbgNames(self.CompleteDownload)

        DbgEnter(dbgblk, dbglb)

        if not download.IsBad():
            myname, mypath = download.MyPath()

            os.makedirs(mypath, exist_ok=True)

            recording = download.recording

            # Unzip into mypath
            myzipfile = os.path.join(download.downloadPath, download.filename)

            try:
                if os.path.exists(myzipfile):
                    with zipfile.ZipFile(myzipfile, "r") as zip_ref:
                        zip_ref.extractall(mypath)

                    recording.data["Archived"] = "Yes/Downloaded"

                    os.remove(myzipfile)
                else:
                    self.CompleteBadRecording(download)

                self.SaveMetaInfo(download)
            except Exception as err:
                ErrMsg(err, f"Failed to complete download of {recording.data['Conversation ID']}")
        else:
            self.CompleteBadRecording(download)
            self.SaveMetaInfo(download)

        DbgExit(dbgblk, dbglb)

    def CheckActiveDownloads(self, activeDownloads, downloadCount, sleep_time=3, pause=2):
        """Check (and/or Wait for) Active Downloads"""

        dbgblk, dbglb = DbgNames(self.CheckActiveDownloads)

        DbgEnter(dbgblk, dbglb)

        completedCount = 0

        while len(activeDownloads) >= downloadCount:
            for activeDownload in activeDownloads:
                progress = activeDownload.GetDownloadProgress(self, sleep_time=sleep_time)

                if progress >= 100:
                    DbgMsg(f"Completing {activeDownload.ConversationID()}", dbglabel=dbglb)
                    self.CompleteDownload(activeDownload)

                    activeDownloads.remove(activeDownload)

                    completedCount += 1

            if len(activeDownloads) >= simultaneousDownloads and pause > 0:
                self.Sleep(pause)

            BreakpointCheck()
            CheckForEarlyTerminate()

        DbgExit(dbgblk, dbglb)

        return completedCount

    def BatchDownloading(self, interval):
        """Download Items"""

        dbgblk, dbglb = DbgNames(self.BatchDownloading)

        DbgEnter(dbgblk, dbglb)

        completed = 0
        errored = 0

        # Open Downloads Tab For Inspection
        ascTab, downloadTab = self.OpenDownloadsTab()

        self.downloadsTab = downloadTab

        self.Sleep(4)

        self.SwitchFrame(self.mainFrame, 3)

        nextClassDisabled = "ui-paginator-next ui-state-default ui-corner-all ui-state-disabled"
        nextButtonDisabledCss = f"a[class='{nextClassDisabled}']"
        nextButtonCss = "a[aria-label='Next Page']"

        nextBtn = self.ByCSS(nextButtonCss)

        # Search from start date to end date in increments of 5 downloads per until all files downloaded
        startDate = officialStart
        searchInterval = timedelta(days=interval.days, hours=11, minutes=59, seconds=59)
        correction = timedelta(seconds=1)

        activeDownloads = list()

        DbgMsg(f"Starting run between {startDate} and {officialEnd}", dbglabel=dbglb)

        while startDate < officialEnd:
            endDate = startDate + searchInterval

            self.MainContext()

            # Conduct a search between the given dates
            self.Search(startDate, endDate)

            self.Half()

            paginationInfo = self.GetPageCount()

            # Now, download the results X at a time and remember to page until you can't page anymore
            while True:
                self.MainContext()

                # Get Items on current page
                data = self.GetData(self.mainFrame)

                for recording in data:
                    # Check recording to see if it's already downloaded or discardable in some other way

                    vrec = VoiceDownload(recording, self.downloadPath)

                    recording_we_want = vrec.SelectForDownload()

                    if recording_we_want:
                        DbgMsg(f"Recording {recording.data['Conversation ID']} will be downloaded", dbglabel=dbglb)

                        # Only allow for X number of simultaneousDownloads
                        if self.Download(vrec, self.mainFrame, data):
                            success = vrec.GetDownloadInfo(self)

                            if success:
                                activeDownloads.append(vrec)
                        else:
                            errored += 1
                            vrec.AddToBad()
                            Msg(f"Download for recording {recording.data['Conversation ID']} had an error")
                    else:
                        DbgMsg(f"Recording {recording.data['Conversation ID']} will be skipped", dbglabel=dbglb)
                        continue

                    BreakpointCheck()
                    CheckForEarlyTerminate()

                    completed += self.CheckActiveDownloads(activeDownloads, simultaneousDownloads, 1.25)

                del data

                nextBtn = self.ByCSS(nextButtonCss)

                if nextBtn.get_attribute("class") != nextClassDisabled:
                    # More pages of items for this search to download
                    nextBtn.click()
                    self.Sleep(4)
                else:
                    # No more items to download for this search
                    # Now, make sure the D/Ls that are currently running complete

                    if len(activeDownloads) > 0:
                        completed += self.CheckActiveDownloads(activeDownloads, 1, 0)

                    present = self.BusySpinnerPresent(True)

                    break

            self.Sleep(5.0)
            DbgMsg("Refreshing browser instance", dbglabel=dbglb)
            self.Refresh()
            self.Sleep(8.0)

            startDate = endDate + correction
            endDate = (startDate + searchInterval)

        self.CloseDownloadsTab()

        Msg(f"Completed\t: {completed}\nErrored\t: {errored}")

        DbgExit(dbgblk, dbglb)

    def POC(self):
        """POC of download system"""

        # POC Search and D/L
        # Set Search Up
        self.Search(startOn, endOn)

        # Extract Current Rows
        data = self.GetData()

        # Conduct one download
        self.Download(data[0])

    def GetVoiceRecordings(self, interval, username, password):
        """Get ACS Voice Recordings... Probably"""

        dbgblk, dbglb = DbgNames(self.GetVoiceRecordings)

        DbgEnter(dbgblk, dbglb)

        # Cancel Login Dialog (Via Ait)
        self.CancelDialog()

        # Actual Login... but dumb... (via Ait)
        if self.SmartLogin(username, password):
            # Replace with wait
            self.Second()

            doPOC = False

            # Begin Searches and downloads

            if doPOC:
                self.POC()
            else:
                self.SwitchFrame(self.mainFrame)
                self.BatchDownloading(interval)

            self.SmartLogout()

        DbgExit(dbgblk, dbglb)


class RecordingRecord:
    """RecordingRecord Class"""

    rowkey = None
    row = None
    cells = None
    data = None

    def __init__(self, row=None):
        """Init instance of RecordingRecord"""

        if row is not None:
            self.GetCells(row)

    def __getitem__(self, key):
        """Get Item By Cell Name"""

        value = None

        if self.cells is not None:
            value = self.cells[key]

        return value

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
            "Department",
            "Conversation ID"
        ]

        self.row = row

        try:
            self.cells = self.row.find_elements(By.CSS_SELECTOR, "td")
            data_from_cells = [str(cell.text) for cell in self.cells]
            self.data = dict(zip(header, data_from_cells))
            self.rowkey = self.data["Conversation ID"]
        except Exception as err:
            Msg("Failed to find TD that contains the cells with information")

    def Print(self):
        print(f"Rowkey\t: {self.rowkey}")
        print(f"Row\t: {self.row}")
        print(f"Cells\t: {self.cells}")
        print(f"Data\t: {self.data}")


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
            "innerText",
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

    def get(self, attr_name, alt_value=None):
        result = alt_value

        try:
            result = self._wrapped_obj.get_attribute(attr_name)

            if result is None:
                result = alt_value
        except Exception as err:
            result = None

        return result

    def properties(self):
        props = [ "checked" ]

        vals = dict()

        for prop in props:
            vals[prop] = self._wrapped_obj.get_property(prop)

    def get_prop(self, prop_name, alt_value=None):
        result = alt_value

        try:
            result = self._wrapped_obj.get_property(prop_name)

            if result is None:
                result = alt_value
        except Exception as err:
            result = None

        return result


class VoiceDownload:
    """voice Download Class"""

    downloadPath = None
    recording = None
    filename = None
    progress = 0
    is_bad = False

    def __init__(self, recording, downloadPath):
        """Initialize Instance"""

        self.recording = recording
        self.downloadPath = downloadPath

    def GetDownloadInfo(self, browser, sleep_time=3):
        """Get Download Info"""

        dbgblk, dbglb = DbgNames(self.GetDownloadInfo)

        DbgEnter(dbgblk, dbglb)

        DbgMsg(f"Entering {dbgblk}", dbglabel=dbglb)

        success = True

        downloads = browser.GetDownloads(sleep_time)

        if len(downloads) == 0:
            success = False

        topitem = None

        for filename, progress in downloads.items():
            if topitem is None and self.filename is None:
                self.filename = filename
                self.progress = int(progress)
                topitem = (self.filename, self.progress)

                break

        browser.MainContext()

        DbgExit(dbgblk, dbglb)

        return success

    def GetDownloadProgress(self, browser, sleep_time=3):
        """Update Download Progress"""

        dbgblk, dbglb = DbgNames(self.GetDownloadProgress)

        DbgEnter(dbgblk, dbglb)

        downloads = browser.GetDownloads(sleep_time)

        for filename, progress in downloads.items():
            if filename == self.filename:
                self.progress = int(progress)

                break

        browser.MainContext()

        DbgExit(dbgblk, dbglb)

        return self.progress

    def ConversationID(self):
        """Get Conversation ID"""

        return self.recording.data["Conversation ID"]

    def TimestampStr(self):
        """Get Timestamp String"""

        return self.recording.data["Start Time"]

    def Timestamp(self):
        """Get Time Stamp"""

        timestamp = self.recording.data["Start Time"]

        mytimestamp = datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p")

        return mytimestamp

    def CalledPartyName(self):
        """Get the Called Party Name"""

        return self.recording.data["Called Party Name"]

    def DurationStr(self):
        """Get Duration String"""

        return self.recording.data["Duration"]

    def Duration(self):
        """Get Duration (as timedelta)"""

        strDuration = self.recording.data["Duration"]

        quads = strDuration.split(":")

        hours = int(quads[0])
        minutes = int(quads[1])
        seconds = int(quads[2])
        ms = int(quads[3])

        delta = timedelta(seconds=seconds, milliseconds=ms, minutes=minutes, hours=hours)

        return delta

    def ConnectedNumber(self):
        """Get number connected to"""

        return self.recording.data["1st-Connected Phone Number"]

    def ConnectedName(self):
        """Get Connected Name aka 1-st Connected Name"""

        return self.recording.data["1st-Connected Name"]

    def CalledNumber(self):
        """Get Called Number"""

        return self.recording.data["Called Party Phone Number"]

    def CallingNumber(self):
        """Get Calling Number"""

        return self.recording.data["Calling Party Phone Number"]

    def CalledPartyName(self):
        """Get Called Party Name"""

        return self.recording.data["Called Party Name"]

    def CallingPartyName(self):
        """Get Calling Party Name"""

        return self.recording.data["Calling Party Name"]

    def MyPath(self):
        """Construct My Path and Filename"""

        parentFolderSpec = "{:%Y%m%d}"
        fmtspec = "{:%Y%m%d%H%M%S}"
        conversationID = self.ConversationID()
        convoDirection = self.recording.data["Conversation Direction"]
        timestamp = self.Timestamp()
        parentFolder = parentFolderSpec.format(timestamp)
        timestampfldr = fmtspec.format(timestamp)
        calledpartyname = self.CalledPartyName()

        myname = f"{conversationID}.wav"

        # path /backup/called-party/timestamp/conversationID

        if convoDirection == "Unknown":
            calledpartyname = "radio"

        mypath = os.path.join(self.downloadPath, parentFolder, timestampfldr, conversationID)

        return myname, mypath

    def Exists(self):
        """Check to See if Voice Recording Archive Exists"""

        exists = False

        myname, mypath = self.MyPath()

        myfile = os.path.join(mypath, myname)

        if os.path.exists(myfile):
            exists = True

        return exists

    def AddToBad(self):
        """Add to Bad List"""

        self.is_bad = True

        if not self.InBad():
            with open(badRecordings, "at", newline='') as bad:
                writer = csv.writer(bad)

                row = [ self.ConversationID(), self.Timestamp() ]

                writer.writerow(row)

    def InBad(self):
        """Check Bad List"""

        convoid = self.ConversationID()
        is_bad = False

        if os.path.exists(badRecordings):
            with open(badRecordings, "rt", newline='') as bad:
                reader = csv.reader(bad)
                for row in reader:
                    convo_rec, timestamp = row
                    if convo_rec == convoid:
                        is_bad = True
                        break

        return is_bad

    def IsBad(self):
        """Return Is Bad Flag"""

        return self. is_bad

    def SelectForDownload(self):
        """Select For Download via Attributes"""

        # Was going to select for attributes, however, higher-ups said back it all up
        # Thus, we only need to see if has been already downloaded.
        download = True

        exists = self.Exists()

        if exists:
            myname, mypath = self.MyPath()

            flag = os.path.join(mypath, "missing.txt")

            if os.path.exists(flag):
                download = False
            else:
                download = False
        else:
            if self.InBad():
                download = False

        return download

    def Print(self):
        print(f"\t: {self.downloadPath}")
        print(f"\t: {self.filename}")
        print(f"\t: {self.progress}")
        print(f"\t: {self.is_bad}")
        self.recording.Print()


# Variables

downloadPathASC = r"S:\Backups\asc"
sessionASC = f"{downloadPathASC}\\session1"
downloadPathPackt = r"Y:\media\eBooks\Packt\freebies"

downloadPath = None

ConfigFile = "config.txt"

config = None

prefix = None

earlyTerminateFlag = None
breakpointFlag = None

runlogName = "runlog.txt"

# ASC Stuff
badrecordingsName = "bad_recordings.txt"
catalogfileName = "recordings_catalog.txt"

configFilename = os.path.join(sessionASC, ConfigFile)
catalogFilename = os.path.join(sessionASC, catalogfileName)
badRecordings = os.path.join(sessionASC, badrecordingsName)

# Date Intervals
officialStart = datetime(2017, 1, 1, 0, 0, 0)
officialEnd = datetime(2023, 8, 5, 0, 0, 0)

simultaneousDownloads = 5

interval = timedelta(days=2)
startOn = datetime.now() - interval
endOn = datetime.now()

ascTab = None
downloadTab = None
mainFrame = "applicationFrame"

recordingsCatalog = None

# Generic Stuff
runlog = None

global_temp = None
lastprocessed = None

Username = None
Password = None

# Breakpoint stuff
emergencyBreak = False
debugBypass = False

# List of BreakOn Conditions
BreakOn = list()

# List of Events Reported
EventList = list()

# Lambdas

# Decorators

# Functions

# Debugging Stuff

def BreakWhen(conditions, **kwargs):
    """Break When Conditions Met"""

    conditions_met = True

    for warg in kwargs:
        if warg in conditions:
            if kwargs[warg] != conditions[warg]:
                conditions_met = False
                break
        else:
            conditions_met = False
            break

    return conditions_met


"""
def read_single_keypress():
    Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns a tuple of characters of the key that was pressed - on Linux, 
    pressing keys like up arrow results in a sequence of characters. Returns 
    ('\x03',) on KeyboardInterrupt which can happen when a signal gets
    handled.

    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = []
    try:
        ret.append(sys.stdin.read(1)) # returns a single character
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
        c = sys.stdin.read(1) # returns a single character
        while len(c) > 0:
            ret.append(c)
            c = sys.stdin.read(1)
    except KeyboardInterrupt:
        ret.append('\x03')
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return tuple(ret)
"""


def SafeIO(*files):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            dbgblk, dbglb = DbgNames(SafeIO)

            DbgEnter(dbgblk, dbglb)

            ext = ".protected"

            # Protect files from write
            for file in files:
                pro = f"{file}{ext}"

                if DebugMode() and os.path.exists(pro):
                    DbgMsg(f"{file} is protected", dbglabel=dbglb)

                while os.path.exists(pro):
                    Sleep(0.1)

                ph.Touch(pro)

            # Files are protected

            results = None

            try:
                results = func(*args, **kwargs)
            except Exception as err:
                if DebugMode():
                    ErrMsg(err, "An error occurred while executing decorated function in SafeIO")

            # clean up
            for file in args:
                pro = f"{file}{ext}"

                if os.path.exists(pro):
                    os.remove(pro)

            DbgExit(dbgblk, dbglb)

            return results
        return wrapper
    return decorator


# Most likely deprecated
def MergeFiles(downloadFolder, *argv):
    """Merge Files with prefixes"""

    def Append(src, dest):
        with open(src, "rt") as infile:
            with open(dest, "at") as outfile:
                for line in infile:
                    outfile.write(line)

    items = GetFolder(downloadFolder)

    for arg in argv:
        for item in items:
            parent = os.path.dirname(item.path)
            mergewith = os.path.join(parent, arg)

            if item.name.endswith(arg):
                if os.path.exists(mergewith):
                    Append(item.path, mergewith)
                    os.remove(item.path)


def Pause(msg, pause=0, default=None, keyonly=False):
    """Pause for input or input before a time out"""

    result = default

    Msg(msg)

    startTime = datetime.now()
    expired = False

    if os.name == 'nt':
        import msvcrt

        while not msvcrt.kbhit():
            time.sleep(0.25)

            td = datetime.now() - startTime

            if pause > 0 and td.seconds >= pause:
                expired = True
                break

        if keyonly and not expired:
            result = msvcrt.getwch()
        elif not keyonly and not expired:
            result = input()
    else:
        import termios

        # Set to be non-blocking

        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


def CheckForEarlyTerminate(callerframe=None):
    """Check for Early Terminate Flag"""

    global earlyTerminateFlag

    if earlyTerminateFlag is not None and os.path.exists(earlyTerminateFlag):
        os.remove(earlyTerminateFlag)

        if callerframe is None:
            callerframe = inspect.currentframe().f_back

        module = callerframe.f_code.co_filename
        line = callerframe.f_lineno
        host = platform.node()

        caller_str = f"{host}[{module}({line})]"

        Msg(f"Manual Early Terminate detected at {caller_str}")

        sys.exit()


def BreakpointCheck(callerframe=None, nobreak=False):
    """Check for Breakpoint Flag in File System"""

    global breakpointFlag

    breakme = False

    if breakpointFlag is not None and os.path.exists(breakpointFlag):
        breakme = True

        count = 0

        while count < 2:
            try:
                # In case there is a race issue
                os.remove(breakpointFlag)
            except Exception as err:
                Quarter()
                count += 1

        if callerframe is None:
            callerframe = inspect.currentframe().f_back

        module = callerframe.f_code.co_filename
        line = callerframe.f_lineno
        host = platform.node()

        caller_str = f"{host}[{module}({line})]"

        Msg(f"Manual Breakpoint detected at {caller_str}")

        if not nobreak:
            breakpoint()

        return True


def Join(*argv, prefix=None) -> str:
    """Join Pathes Together"""

    pn = ""
    tail = argv[-1]

    for item in argv:
        if item == tail and prefix is not None:
            item = f"{prefix}_{item}"

        pn = os.path.join(pn, item)

    return pn


def RemoveFile(*args):
    """Remove File If it Exists"""

    for filename in args:
        if os.path.exists(filename):
            os.remove(filename)


def Sleep(time_period):
    """Sleep for the specified time interval"""

    time.sleep(time_period)


def Quarter():
    """Sleep a Quarter Second"""

    Sleep(0.25)


def Half():
    """Sleep Half Second"""

    Sleep(0.5)


def Second():
    """Sleep for a second"""

    Sleep(1)


def FileExistsAndNonZero(filename):
    """Determine if file exists and is NonZero Size"""

    exists_and_nonzero = False

    if os.path.exists(filename):
        statinfo = os.stat(filename)

        if statinfo.st_size > 0:
            exists_and_nonzero = True

    return exists_and_nonzero


def LoadRows(filename):
    """Load Recording Catalog"""

    rows = list()

    if FileExistsAndNonZero(filename):
        with open(filename, "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                rows.append(row)

    return rows


def AppendRows(filename, row):
    """Append Row To Catalog"""

    @SafeIO(filename)
    def AppendRowsInternal(filename, row):
        """Append To File"""

        skipme = False

        if os.path.exists(filename):
            with open(filename, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for file_row in reader:
                    if row == file_row:
                        skipme = True
                        break

        if not skipme:
            with open(filename, "a", newline='') as csvfile:
                header = row.keys()

                writer = csv.DictWriter(csvfile, header)

                writer.writerow(row)

    AppendRowsInternal(filename, row)


def SaveRows(filename, rows):
    """Save Recording Catalog"""

    @SafeIO(filename)
    def SaveRowsInternal(filename, rows):
        """Save Rows Internal"""

        header = None

        if len(rows) > 0:
            header = rows[0].keys()

            with open(filename, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, header)

                for row in rows:
                    writer.writerow(row)

    SaveRowsInternal(filename, rows)


def GetFolder(folder=downloadPath):
    """Get Folder Contents"""

    items = list()

    with os.scandir(folder) as fldr:
        for entry in fldr:
            items.append(entry)

    return items


def ClearZips(folder):
    """Celar Zips from Folder"""

    items = GetFolder(folder)

    for item in items:
        if item.is_file() and item.name.endswith(".zip"):
            os.remove(item.path)


def ClearFolder(folder, protected=None, disposables=None):
    """Clear folder of Disposables"""

    protected = protected if protected is not None else list()

    if disposables is not None:
        for item in disposables:
            if os.path.isfile(item):
                os.remove(item)

    items = GetFolder(folder)

    for item in items:
        if item.is_dir() or item.path in protected or item.name in protected:
            continue
        else:
            os.remove(item.path)


def ClearFolderMax(folder):
    """Clear a folder of files and folders recursively"""

    items = GetFolder(folder)

    for item in items:
        if item.is_file():
            os.remove(item.path)
        else:
            shutil.rmtree(item.path)


def ShowFolder(folder=downloadPath):
    """Show Folder Contents"""

    items = GetFolder(folder)

    for entry in items:
        if entry.is_dir():
            Msg(f"D -> {entry.name}")
        else:
            Msg(f"F -> {entry.name}")


def ShowCatalog(catalog=None):
    """Show Catalog (File or Live List)"""

    if catalog is None or type(catalog) is str:
        # Show Catalog file
        rows = LoadRows(catalog)
        header = "No data to show"

        if len(rows) > 0:
            header = str(rows[0].keys())

            Msg(header)
            for row in rows:
                Msg(str(row.values()))
        else:
            Msg(f"{header}")
    else:
        # Catalog is live list or single

        if type(catalog) is list and len(list) > 0:
            header = str(catalog[0].keys())
            Msg(header)
            for row in catalog:
                Msg(str(row.values()))
        else:
            Msg("No items in catalog to display")


# deprecated
def Maximize(browser):
    """Maximize Browser Windows Helper"""

    browser.maximize_window()


# deprecated
def Refresh(browser):
    """Refresh Browser Window"""

    browser.refresh()


# deprecated
def ByCSS(browser, css, msg=''):
    """Get By CSS Shortcut"""

    dbgblk, dbglb = DbgNames(ByCSS)

    DbgEnter(dbgblk, dbglb)

    DbgMsg(f"Searching for : {css} / {msg}", dbglabel=dbglb)

    item = None

    try:
        item = browser.find_element(By.CSS_SELECTOR, css)
    except TimeoutException:
        DbgMsg("Timeout reached exception", dbglabel=dbglb)
    except NoSuchElementException:
        DbgMsg("No such element exception", dbglabel=dbglb)
    except StaleElementReferenceException:
        DbgMsg("Stale element exception", dbglabel=dbglb)
    except Exception as err:
        DbgMsg(f"A generic error occurred while waiting or looking for a warning popup : {err}", dbglabel=dbglb)

    DbgExit(dbgblk, dbglb)

    return item


# deprecated
def MultiByCSS(browser, css, msg=''):
    """Multi Get By CSS Shortcut"""

    dbgblk, dbglb = DbgNames(MultiByCSS)

    DbgEnter(dbgblk, dbglb)

    DbgMsg(f"Searching for : {css} / {msg}", dbglabel=dbglb)

    items = list()

    try:
        items = browser.find_elements(By.CSS_SELECTOR, css)
    except TimeoutException:
        Msg("Timeout reached exception")
    except NoSuchElementException:
        Msg("No such element exception")
    except StaleElementReferenceException:
        Msg("Stale element exception")
    except Exception as err:
        Msg(f"A generic error occurred while waiting or looking for a warning popup : {err}")

    DbgExit(dbgblk, dbglb)

    return items


# deprecated
def ByXPATH(browser, xpath, msg=''):
    """Get By XPATH Shortcut"""

    dbgblk, dbglb = DbgNames(ByXPATH)

    DbgEnter(dbgblk, dbglb)

    DbgMsg(f"Searching for : {xpath} / {msg}", dbglabel=dbglb)

    item = None

    try:
        item = browser.find_element(By.XPATH, xpath)
    except TimeoutException:
        Msg("Timeout reached exception")
    except NoSuchElementException:
        Msg("No such element exception")
    except StaleElementReferenceException:
        Msg("Stale element exception")
    except Exception as err:
        Msg(f"A generic error occurred while waiting or looking for a warning popup : {err}")

    DbgExit(dbgblk, dbglb)

    return item


# deprecated
def MultiByXPATH(browser, xpath, msg=''):
    """Multi Get By XPATH Shortcut"""

    dbgblk, dbglb = DbgNames(MultiByXPATH)

    DbgEnter(dbgblk, dbglb)

    DbgMsg(f"Searching for : {xpath} / {msg}", dbglabel=dbglb)

    items = list()

    try:
        items = browser.find_elements(By.XPATH, xpath)
    except TimeoutException:
        Msg("Timeout reached exception")
    except NoSuchElementException:
        Msg("No such element exception")
    except StaleElementReferenceException:
        Msg("Stale element exception")
    except Exception as err:
        Msg(f"A generic error occurred while waiting or looking for a warning popup : {err}")

    DbgExit(dbgblk, dbglb)

    return items


# deprecated
def SwitchContext(browser, window, frame=None):
    """Switch Context, the easy way"""

    dbgblk, dbglb = DbgNames(SwitchContext)

    DbgEnter(dbgblk, dbglb)

    try:
        if window is not None:
            browser.switch_to.window(window)
        if frame is not None:
            browser.switch_to.frame(frame)
    except NoSuchWindowException:
        DbgMsg(f"No such window exception for {window}", dbglabel=dbglb)
    except NoSuchFrameException:
        DbgMsg(f"No such frame exception for {frame}", dbglabel=dbglb)
    except Exception as err:
        DbgMsg(f"A generic error occurred when trying to switch context : {err}", dbglabel=dbglb)

    DbgExit(dbgblk, dbglb)


# deprecated
def MainContext(browser):
    """Switch to Main Context"""

    dbgblk, dbglb = DbgNames(MainContext)

    DbgEnter(dbgblk, dbglb)

    SwitchContext(browser, ascTab, mainFrame)

    DbgExit(dbgblk, dbglb)


# deprecated
def SwitchFrame(browser, name, pause=0):
    """Context/Content Switch Helper"""

    dbgblk, dbglb = DbgNames(SwitchFrame)

    success = False

    if pause > 0:
        # browser.refresh()
        Sleep(pause)

    try:
        browser.switch_to.frame(name)
        success = True
    except NoSuchFrameException:
        DbgMsg(f"No such frame {name}", dbglabel=dbglb)
    except Exception as err:
        Msg(f"Generic error when trying to switch to frame {name} : {err}")

        if DebugMode() and not debugBypass:
            breakpoint()

    return success


# deprecated
def SwitchWindow(browser, windowHandle):
    """Switch Between Windows"""

    try:
        Half()
        browser.switch_to.window(windowHandle)
    except Exception as err:
        ErrMsg(err, "A problem occurred switching browser windows")

        if DebugMode():
            breakpoint()


# deprecated
def SwitchTab(browser, tabHandle):
    """Switch to tab"""

    SwitchWindow(browser, tabHandle)


# deprecated
def NewTab(browser, url):
    """Open New Tab"""

    originalHandle = browser.current_window_handle

    browser.switch_to.new_window('tab')

    tabHandle = browser.current_window_handle

    browser.get(url)

    SwitchWindow(browser, originalHandle)

    return tabHandle


# deprecated
def SetupBrowser(browser, url):
    """Helper for setting up the browser"""

    browser.get(url)


# deprecated
def DownloadOptions(folderPath, withcaps= False):
    """Set Browser Download Path"""

    options = Options()

    if withcaps:
        # options.set_capability("browserVersion", "latest")
        # options.set_capability("platformName", "linux")
        options.set_capability("platformName", "Windows 10")

        # Folder path removed here for Grid system, can be added back in if path exists
        options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True})
    else:
        options.add_experimental_option("prefs", {
        "download.default_directory": folderPath,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True})

    options.add_argument('ignore-certificate-errors')

    return options


def DoAit(seconds, key=None, write=None):
    """Helper for Doing Ait Stuff"""

    Sleep(seconds)

    if key is not None:
        ait.press(key)
    elif write is not None:
        ait.write(write)


# deprecated
def BadCert(browser):
    """Helper for Getting Past Bad Certs"""

    advBtn = browser.find_element(By.CSS_SELECTOR, "button[id='details-button']")
    advBtn.click()

    Half()

    anchor = browser.find_element(By.CSS_SELECTOR, "div > p > a[id='proceed-link']")

    anchor.click()

    Second()


# deprecated
def CancelDialog():
    """Cancel Login Dialog Helper"""

    dbgblk, dbglb = DbgNames(CancelDialog)

    DbgEnter(dbgblk, dbglb)

    Second()

    ait.press("\t", "\t", "\t")
    Half()
    ait.press("\n")
    Half()

    DbgExit(dbgblk, dbglb)


# deprecated
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


# deprecated
def SmartLogin(browser):
    """Smart Login ACS"""

    dbgblk, dbglb = DbgNames(SmartLogin)

    success = False

    if SwitchFrame(browser, 0):
        DbgMsg("Logging in",dbglabel=dbglb)

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


# deprecated
def SmartLogout(browser):
    """Logout Helper"""

    dbgblk, dbglb = DbgNames(SmartLogout)

    DbgEnter("Logging out", dbglb)

    span = "table[id='powpwfteaper27'] > tbody > tr > td > span[id='powpwfteaper28']"
    anchorID = "a[id='logoutMenuItem']"


    spanobj = browser.find_element(By.CSS_SELECTOR, span)

    WebDriverWait(browser, 30).until(presence_of_element_located((By.CSS_SELECTOR, anchorID)))

    logoffAnchor = browser.find_element(By.CSS_SELECTOR, anchorID)

    spanobj.click()

    WebDriverWait(browser, 30).until(visibility_of(logoffAnchor))

    logoffAnchor.click()

    DbgExit(dbgblk, dbglb)

# deprecated
def BusySpinnerPresent(browser, closeit=False):
    """Detect Busy Spinner"""

    busyCss = "div[id='statusDialogId']"
    imgCss = f"{busyCss} > div > img[id='aswpwfteapte18']"

    busyFlag = False

    try:
        busy = ByCSS(browser, busyCss)

        if busy.is_displayed():
            busyFlag = True

            if closeit:
                Half()
                # Do Something
                # aria-hidden=true, aria-live=off, class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidden-container ajaxStatusDialog"
                # style=width: auto; height: auto; left: 649px; top: 600.5px; z-index: 1039; display: none;

                browser.execute_script("document.getElementById('statusDialogId').style.display='none';")
                Half()

    except Exception as err:
        DbgMsg(f"An error occurred : {err}")

    return busyFlag


# deprecated
def PopoutPresent(browser, timeout=5):
    """Check to see if Popout is Present"""

    dbgblk, dbglb = DbgNames(PopoutPresent)

    DbgEnter(dbgblk, dbglb)

    italicsCss = "div[id='rightContent'] > table[id='aswpwfteapte42'] > tbody > tr > td > i[id='aswpwfteapte32']"
    italicsXpath = "//div[@id='rightContent']/table[@id='aswpwfteapte42']/tbody/tr/td/i[@id='aswpwfteapte32']"

    results = WaitPresenceCSS(browser, timeout, italicsCss)

    success = results["present"]

    DbgExit(dbgblk, dbglb)

    return success


# deprecated
def ClosePopOut(browser, frame_name=None):
    """Close that fucking annoying pop out"""

    dbgblk, dbglb = DbgNames(ClosePopOut)

    DbgEnter(dbgblk, dbglabel=dbglb)

    MainContext(browser)

    Second()

    italicsCss = "div[id='rightContent'] > table[id='aswpwfteapte42'] > tbody > tr > td > i[id='aswpwfteapte32']"
    italicsXpath = "//div[@id='rightContent']/table[@id='aswpwfteapte42']/tbody/tr/td/i[@id='aswpwfteapte32']"

    success = False

    try:
        Half()

        count = 0

        while not PopoutPresent(browser) and count < 2:
            Half()
            count += 1

        if count > 1:
            raise NoSuchElementException("Popout didn't appear and this exception was raised while looking for it")

        Half()

        italics = ByCSS(browser, italicsCss)
        # italics = browser.find_element(By.CSS_SELECTOR, italicsCss)

        if italics.is_displayed():
            Half()
            DbgMsg("Trying to close/click Popout", dbglabel=dbglb)
            italics.click()
            DbgMsg("Popout should be closed", dbglabel=dbglb)
            Half()

            success = True
    except NoSuchElementException as err_nse:
        DbgMsg(f"No such element, {italicsCss} present", dbglabel=dbglb)
    except StaleElementReferenceException:
        DbgMsg(f"Stale element exception when trying to clear pop out", dbglabel=dbglb)
    except TimeoutException:
        DbgMsg("Timed out looking for pop out", dbglabel=dbglb)
    except Exception as err:
        Msg(f"Generic error trying to clear pop out {err}")

    DbgExit(dbgblk, dbglabel=dbglb)

    return success


# deprecated
def GetPageCount(browser):
    """Get Search Results Page Count"""

    pagecountCss = "span[class='ui-paginator-current']"
    expr = r"^(?P<start>\d+)\s+-\s+(?P<end>\d+)\s+of\s+(?P<total>\d+)$"

    pageCountSpan = ByCSS(browser, pagecountCss)

    results = (0, 0, -1)

    if pageCountSpan is not None:
        matches = re.search(expr, pageCountSpan.text)
        #matches = re.search(expr, pageCountSpan.value)

        if matches is not None:
            start = int(matches.group("start"))
            end = int(matches.group("end"))
            total = int(matches.group("total"))

            results = (start, end, total)

    return results


# deprecated
def BlankRow(recording):
    """Check For Blank Row"""

    blank = False

    for column_value in recording.data.values():
        if column_value is not None and column_value != "":
            break
    else:
        blank = True

    return blank


# deprecated
def GetRows(browser):
    """Get Rows from Search"""

    dbgblk, dbglb = DbgNames(GetRows)

    # DbgEnter(dbgblk, dbglb)

    rows = browser.find_elements(By.CSS_SELECTOR, "div[class='ui-datatable-scrollable-body'] > table > tbody[id='masterTable:ascTable_data'] > tr")

    # DbgExit(dbgblk, dbglb)

    return rows

# deprecated
@Eventing("Entering GetData", "Exiting GetData")
def GetData(browser, frame_name=None):
    """Get Data"""

    dbgblk, dbglb = DbgNames(GetData)

    DbgEnter(dbgblk, dbglb)

    if frame_name is not None:
        Event("Switching frame")
        SwitchFrame(browser, frame_name)

    Event("Closing popout")
    if ClosePopOut(browser):
        Event("Appears Popout was closed")
    else:
        Event("Appears Popout WAS NOT closed for some reason")

    Msg("************* >>>>>>>>>>>>> Getting Rows <<<<<<<<<<<<<")

    norecs = "No records found"

    retries = 1
    retry_count = 0
    retry = True
    last_rowkey = None

    try:
        Event("Entering try-while block")
        while retry:
            Event("Getting rows")
            rows = GetRows(browser)

            records = list()

            Event(f"Retrieved {len(rows)}")

            count = 1
            for row in rows:
                recording = RecordingRecord(row)

                last_rowkey = recording.rowkey
                Event(f"Processing {last_rowkey}")

                if BlankRow(recording):
                    DbgMsg(f"Row for appears empty, skipping\n{recording.data}", dbglabel=dbglb)
                    continue

                if DebugMode() and recording.data is None:
                    DbgMsg("Recording.data is none, why?")
                    breakpoint()

                try:
                    Event("Checking for blanks, ie. no search results")
                    loaded = recording.data.get("Loaded", "xxx")
                    retry = False
                    Event("Checking for no search results seems to have succeeded")
                except Exception as err:
                    Msg(f"Checking for 'Loaded' column seems to have failed : {err}", dbglabel=dbglb)
                    retry = True if retry_count < retries else False
                    retry_count += 1

                if loaded != norecs and recording.data['Start Time'] != '':
                    DbgMsg(f"Processing {count} : {recording.data['Conversation ID']}", dbglabel=dbglb)
                    count += 1

                    records.append(recording)
                elif loaded == norecs:
                    DbgMsg("No data for this time frame", dbglabel=dbglb)
                else:
                    DbgMsg(f"Something other than no data rows has happened for processed item {count}", dbglabel=dbglb)
                    DbgMsg(f"Record is\n{recording.data}", dbglabel=dbglb)

                if BreakpointCheck(nobreak=True) and DebugMode():
                    DbgMsg(f"In {dbglb} when manual breakpoint detected", dbglabel=dbglb)
                    breakpoint()
    except Exception as err:
        PrintEvents()
        ErrMsg(err, "An error occurred while trying to process rows from the search")


        if DebugMode():
            DbgMsg(f"Last {last_rowkey} could not be processed", dbglabel=dbglb)

    DbgExit(dbgblk, dbglb)

    return records


# deprecated
def PausePlayer(browser, timeout=5):
    """Pause Player"""

    dbgblk, dbglb = DbgNames(PausePlayer)

    DbgEnter(dbgblk, dbglb)

    pauseBtnCss = "div[id='asc_playercontrols_pause_btn']"

    pauseBtn = browser.find_element(By.CSS_SELECTOR, pauseBtnCss)

    try:
        WebDriverWait(browser, timeout).until(visibility_of(pauseBtn))

        pauseBtn.click()
    except TimeoutException:
        DbgMsg("Timeout reached, player control is not visible or accessible, BAD", dbglabel=dbglb)
    except NoSuchElementException:
        DbgMsg("No such element error while looking for pause button", dbglabel=dbglb)
    except StaleElementReferenceException:
        DbgMsg("Stale element exception while looking for pause button", dbglabel=dbglb)
    except Exception as err:
        DbgMsg(f"A generic error occurred while trying to pause player : {err}", dbglabel=dbglb)

    DbgExit(dbgblk, dbglb)


# deprecated
def WaitPresenceCSS(browser, timeout, selector):
    """Wait for Something to be present"""

    dbgblk, dbglb = DbgNames(WaitPresenceCSS)

    DbgEnter(dbgblk, dbglb)

    resultset = dict()

    resultset["present"] = False
    resultset["timeout"] = False
    resultset["stale"] = False
    resultset["nosuchelement"] = False
    resultset["error"] = (False, None)
    resultset["item"] = None

    try:
        DbgMsg(f"Waiting for : {selector}", dbglabel=dbglb)

        WebDriverWait(browser, timeout).until(presence_of_element_located((By.CSS_SELECTOR, selector)))
        resultset["present"] = True

        resultset["item"] = browser.find_element(By.CSS_SELECTOR, selector)
    except TimeoutException as t_err:
        resultset["timeout"] = True
        resultset["error"] = (True, t_err)
    except NoSuchElementException as ns_err:
        resultset["nosuchelement"] = True
        resultset["error"] = (True, ns_err)
    except StaleElementReferenceException as s_err:
        resultset["stale"] = True
        resultset["error"] = (True, s_err)
    except Exception as err:
        resultset["error"] = (True, err)
        DbgMsg(f"Unexpected exception waiting for {selector} : {err}", dbglabel=dbglb)

    DbgExit(dbgblk, dbglb)

    return resultset


# deprecated
def StalledDownload(browser, rowkey=None):
    """Check for Stalled Download"""

    dbgblk, dbglb = DbgNames(StalledDownload)

    DbgEnter(dbgblk, dbglb)

    saveBoxCss = "div[class='jBox-container'] > div[class='jBox-title jBox-draggable'] > div"
    btnOkCss = "div[class='jBox-footer'] > div[class='asc_dialog_footer'] > button[class='asc_jbox_ok_button']"
    btnCancelCss = "div[class='jBox-footer'] > div[class='asc_dialog_footer'] > button[class='asc_jbox_cancel_button']"

    prepPerCss = "div[id='asc_player_saveas_progress'] > div > span[id='asc_player_saveas_progressbar_percentage']"
    prepFileCss = "div[id='asc_player_saveas_progress'] > div > span[id='asc_player_saveas_progressbar_file_percentage']"

    stalled = False

    result = WaitPresenceCSS(browser, 3, saveBoxCss)

    if result["present"]:
        timechk = datetime.now()

        while result["present"] and not stalled:
            Quarter()

            result = WaitPresenceCSS(browser, 1, saveBoxCss)

            if result["present"]:
                time_passed = datetime.now() - timechk

                if time_passed.seconds > 8:
                    cancelBtn = ByCSS(browser, btnCancelCss)
                    progress = ByCSS(browser, prepPerCss)

                    if cancelBtn is not None and progress is not None and time_passed.seconds <= 10:
                        if progress.text == "0%":
                            cancelBtn.click()
                            stalled = True
                        elif progress.text == "":
                            try:
                                # LAst ditch chance to complete d/l
                                okBtn = ByCSS(btnOkCSS)

                                obBtn.click()
                                DbgMsg("Came across case where save dialog was up and not stalled")
                            except Exception as err:
                                DbgMsg("Save dialog stalled or not, can't tell")
                    elif time_passed.seconds > 10:
                        stalled = True
                        if cancelBtn is not None:
                            cancelBtn.click()

    if stalled and DebugMode():
        DbgMsg(f"Stalled on rowkey {rowkey}")

    DbgExit(dbgblk, dbglb)

    return stalled


# deprecated
def WarningMsg(browser, rowkey=None):
    """Check for a Warning Popup"""

    dbgblk, dbglb = DbgNames(WarningMsg)

    DbgEnter(dbgblk, dbglb)
    DbgMsg(f"Checking for warning on {rowkey}", dbglabel=dbglb)

    conditions = {"rowkey":""}

    # Wait for error, set success to False if error pops up
    prefix = "div[id='globalHeaderMessage'] > div > div > div[id='headerMessages'] > div"
    errorCss = f"{prefix} > span"
    errMsg = f"{prefix} > ul > li > span[class='ui-messages-error-detail']"

    errmsg = ""

    msg = None
    warning = None

    try:
        ClosePopOut(browser)

        result = WaitPresenceCSS(browser, 8, errorCss)

        if result["present"]:
            DbgMsg(f"Warning present", dbglabel=dbglb)

            warning = result["item"]

            Sleep(1.5)

            msg = ByCSS(browser, errMsg)

            # Not because I want to, but because this WebUI is so fucking unpredictable in spots... this being one of them.
            if warning is not None:
                try:
                    if warning.is_displayed():
                        pass
                except Exception as err:
                    Second()
                    warning = ByCSS(browser, errorCss)

            if warning.is_displayed() and warning.is_enabled():
                errmsg = edom(msg)["innerText"]

                DbgMsg(f"Warning is displayed AND enabled with '{errmsg}' for {rowkey}", dbglabel=dbglb)
                warning.click()
                Sleep(3)
            else:
                DbgMsg(f"Warning detected for {rowkey}", dbglabel=dbglb)
                vismsg = "Is visible" if warning.is_displayed() else "Is NOT visible"
                enamsg = "Is enabled" if warning.is_enabled() else "Is NOT enabled"
                errmesg = edom(msg)["innerText"]    # Named errmesg on purpose to prevent it messing with active errmsg

                DbgMsg(f"Visibility\t: {vismsg}", dbglabel=dbglb)
                DbgMsg(f"Enabled\t: {enamsg}", dbglabel=dbglb)
                DbgMsg(f"With Msg\t: {errmesg}", dbglabel=dbglb)
        else:
            DbgMsg(f"Warning is not present for {rowkey}", dbglabel=dbglb)
    except StaleElementReferenceException as s_err:
        DbgMsg(f"Stale element error triggered during warning check : {s_err}", dbglabel=dbglb)
    except Exception as err:
        ErrMsg(err, "Something happened during warning check")

        if DebugMode():
            breakpoint()

    if BreakWhen(conditions, rowkey=rowkey):
        DbgMsg(f"Rowkey, {rowkey}, matches break condition", dbglabel=dbglb)
        breakpoint()

    BreakpointCheck()
    CheckForEarlyTerminate()

    DbgExit(dbgblk, dbglb)

    return errmsg


# deprecated
def ActivateRow(browser, row, rowkey=None):
    """Activate Row"""

    dbgblk, dbglb = DbgNames(ActivateRow)

    DbgEnter(dbgblk, dbglb)
    DbgMsg(f"Attempting to activate {rowkey}", dbglabel=dbglb)

    success = True

    conditions = {"rowkey": ""}

    try:
        ActionChains(browser).move_to_element(row).double_click().perform()
    except Exception as err:
        ErrMsg(err, "An error occurred while trying to activate a row")

        if DebugMode():
            breakpoint()

    Half()

    PausePlayer(browser, timeout=3)

    response = WarningMsg(browser, rowkey=rowkey)

    success = (response == "")

    if success:
        PausePlayer(browser, timeout=2)

    if BreakWhen(conditions, rowkey=rowkey):
        DbgMsg(f"Rowkey, {rowkey}, matches for breakpoint", dbglabel=dbglb)
        breakpoint()

    DbgExit(dbgblk, dbglb)

    return success


# deprecated
def OpenDownloadsTab(browser):
    """Open Downloads Tab"""

    dbgblk, dbglb = DbgNames(OpenDownloadsTab)

    DbgEnter(dbgblk, dbglb)

    originalHandle = browser.current_window_handle

    tabHandle = NewTab(browser, "chrome://downloads")

    DbgExit(dbgblk, dbglb)

    return originalHandle, tabHandle


# deprecated
def GetDownloads(browser, downloadsTab, sleep_time=3):
    """Get List of Downloads In Download Tab"""

    dbgblk, dbglb = DbgNames(GetDownloads)

    DbgEnter(dbgblk, dbglb)

    if BreakpointCheck(nobreak=True) and DebugMode():
        DbgMsg("Manual breakpoint detected", dbglabel=dbglb)
        breakpoint()

    originalTab = browser.current_window_handle

    SwitchTab(browser, downloadsTab)

    if sleep_time > 0:
        Sleep(sleep_time)

    downloadsScript = "return document.querySelector('downloads-manager').shadowRoot.querySelectorAll('#downloadsList downloads-item')"

    downloads = browser.execute_script(downloadsScript)

    downloadDict = dict()

    progress = {"value": "100"}

    for download in downloads:
        try:
            fname = edom(download.shadow_root.find_element(By.CSS_SELECTOR, "#file-link"))

            try:
                progress = edom(download.shadow_root.find_element(By.CSS_SELECTOR, "#progress"))
            except NoSuchElementException:
                DbgMsg("No such element error, progress is not available, assuming 100%", dbglabel=dbglb)

            downloadDict[fname["text"]] = int(progress["value"])
        except NoSuchElementException:
            DbgMsg("Could not file 'file-link' in shadow root of downloads-item")
        except Exception as err:
            Msg(f"Trouble getting download information : {err}")

    MainContext(browser)

    DbgExit(dbgblk, dbglb)

    return downloadDict


# deprecated
def CloseDownloadsTab(browser, originalTab, downloadsTab):
    """Close Downloads Tab"""

    SwitchWindow(browser, downloadsTab)

    browser.close()

    SwitchWindow(browser, originalTab)


# deprecated
def AttributeChanged(object, attribute, value):
    """Check if attribute Changed"""

    flag = False

    current_value = object.get_attribute(attribute)

    if value != current_value:
        flag = True

    return flag


# deprecated
def TagToAppear(browser, selectorType, selector, timeout=5):
    """Wait for Tag to Appear"""

    result = None

    try:
        WebDriverWait(browser, timeout).until(presence_of_element_located((selectorType, selector)))

        result = browser.find_element(selectorType, selector)
    except:
        pass

    return result


# deprecated
def WaitUntilTrue(time_period, func, *args, **kwargs):
    """Wait Until Something is True"""

    start = datetime.now()
    result = True

    while not func(*args, *kwargs):
        Sleep(0.10)

        current = datetime.now()
        passed = current - start

        if passed.seconds >= time_period:
            result = False
            break

    return result


# deprecated
@Eventing("Starting Search")
def Search(browser, startDate, endDate):
    """Set and Conduct Search"""

    dbgblk, dbglb = DbgNames(Search)

    DbgEnter(dbgblk, dbglb)

    events = list()

    try:
        Event("Beginning Search Run")

        try:
            Event("Looking for general dropdown button")
            # Find "General dropdown
            general = browser.find_element(By.CSS_SELECTOR, "a[id='conversationToolbar:commonFunctionsMenuBtn']")
            general.click()
            Event("General dropdown clicked")
        except Exception as err:
            Event(f"General dropdown button could not be found, {err}")

        Half()

        try:
            Event("Looking for search anchor")
            # Find Search anchor and click it
            anchor = browser.find_element(By.CSS_SELECTOR, "a[id='conversationToolbar:toolbarSearchBtn']")
            anchor.click()
            Event("Anchor clicked")
        except Exception as err:
            Event(f"Anchor either not found or not clicked : {err}")

        Half()

        try:
            Event("Select box section")

            # Set Select box
            sbox = browser.find_element(By.CSS_SELECTOR,
                                        "select[id='conversationObjectView:j_idt132:searchdatatable:0:searchMenu']")
            WebDriverWait(browser, 5).until(visibility_of(sbox))

            select = Select(sbox)
            # Set "between", then set dates. VALUE = "BETWEEN"
            select.select_by_value('BETWEEN')

            Event("Selection Completed")
        except Exception as err:
            Event(f"Search box not found or filled, an error occurred : {err}")

        Half()

        try:
            Event(f"Beginning Search between {startDate} and {endDate}")

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

            DbgMsg(f"Conducting search between {startDate} and {endDate}", dbglabel=dbglb)

            # Start Search
            searchBtn.click()

            Event("Search completed")
        except Exception as err:
            Event(f"An error occurred while filling out the search : {err}")

        # Wait for search to complete

        Half()

        startSearch_Timestamp = datetime.now()

        flag = WaitUntilTrue(3600, AttributeChanged, spinner, "aria-hidden", "false")

        # WebDriverWait(browser, 7200).until(AttributeChanged(spinner, "aria-hidden", "false"))

        searchDuration = datetime.now() - startSearch_Timestamp

        Msg(f"Elapsed search time : {searchDuration}")

        # Close Search Box
        closeAnchor.click()

        Event("Close anchor clicked, we done")
    except Exception as err:
        ErrMsg(err, "An error occurred while trying to execute a search")

        Event(f"Bummer, an error occurred while attempting a search : {err}")

        if DebugMode():
            DbgMsg(f"Something hit the fan during a search, you can checked the 'events' list to see the last successful or errored event")
            breakpoint()

    DbgExit(dbgblk, dbglb)


# deprecated
def BeginDownload(browser, vrec=None):
    """Begin Download"""

    dbgblk, dbglb = DbgNames(BeginDownload)

    DbgEnter(dbgblk, dbglb)

    success = True
    saveCss = "div[id='asc_playercontrols_savereplayables_btn']"
    mediaSrcsAudioCss = "li[class='mediasources_audio'] > label > input"
    mediaSrcsAudioCssDis = "li[class='mediasources_audio asc_disabled'] > label > input"
    mediaSrcsChat = "li[class='mediasources_chat'] > label > input"
    okBtnCss = "button[class='asc_jbox_ok_button']"
    cancelBtnCss = "button[class='asc_jbox_cancel_button']"

    ClosePopOut(browser)

    saveBtn = ByCSS(browser, saveCss)
    saveBtn.click()

    # Will Bring up dialog
    audioInputDis = None
    audioInput = ByCSS(browser, mediaSrcsAudioCss, msg="AKA mediaSources Inputbox")

    if audioInput is None:
        audioInputDis = ByCSS(browser, mediaSrcsAudioCssDis)

    cancelBtn = ByCSS(browser, cancelBtnCss)

    Half()

    audioEnabled = False

    try:
        if audioInputDis is None and audioInput is not None and audioInput.is_displayed() and audioInput.is_enabled():
            audioEnabled = True

            aiObj = edom(audioInput)

            count = 0

            while not aiObj.get_prop("checked", False) and count < 3:
                Half()
                audioInput.click()

                count += 1

            Half()

            okBtn = ByCSS(browser, okBtnCss)

            Half()

            okBtn.click()
        else:
            success = False
            Half()
            cancelBtn.click()

        Half()
    except ElementClickInterceptedException:
        success = False

        if DebugMode():
            DbgMsg("audio checkbox unable to be clicked, likely disabled by CSS", dbglabel=dbglb)
    except Exception as err:
        ErrMsg(err, "Click to download failed")
        audioEnabled = False
        success = False

    DbgExit(dbgblk, dbglb)

    return success


# deprecated
def Download(browser, voice_recording, frame_name=None, rows=None):
    """Download Recording"""

    global global_temp, lastprocessed

    dbgblk, dbglb = DbgNames(Download)

    DbgEnter(dbgblk, dbglb)

    recording = voice_recording.recording

    success = False
    rowkey = recording.rowkey
    row = None

    if lastprocessed is None:
        last_rowkey = rowkey
    else:
        last_rowkey = lastprocessed.recording.rowkey

    conditions = {"rowkey": ""}

    if frame_name is not None:
        SwitchFrame(browser, frame_name)

    try:
        if PopoutPresent(browser, timeout=1):
            ClosePopOut(browser, frame_name)

        stalled = StalledDownload(browser, rowkey=last_rowkey)

        if stalled:
            lastprocessed.AddToBad()
            lastprocessed.progress = 100

        Half()

        rowXPath = f"//tr[@data-rk='{rowkey}']"
        row = ByXPATH(browser, rowXPath)

        # row = browser.find_element(By.XPATH, rowXPath)

        # Active Row
        success = ActivateRow(browser, row, rowkey)

        if success:
            # Begin Download
            global_temp = ("activation succeeded", rowkey)

            DbgMsg(f"Attempting download of {rowkey} from {voice_recording.Timestamp()}", dbglabel=dbglb)

            if not BeginDownload(browser, vrec=voice_recording):
                global_temp = ("save failed", rowkey)

                success = False
                voice_recording.AddToBad()

                recording.data["Archived"] = "Audio Unavailable/Not Archived"
                AppendRows(catalogFilename, recording.data)
                Msg(f"Record {rowkey} for {recording.data['Start Time']} could not be downloaded")
        else:
            global_temp = ("activation failed", rowkey)
            Msg(f"Record {rowkey} for {recording.data['Start Time']} could not be downloaded")

            voice_recording.AddToBad()

            recording.data["Archived"] = "Damaged/Not Archived"
            recording.data["Expanded"] = "Warning received before download"
            AppendRows(catalogFilename, recording.data)
    except Exception as err:
        # check rowkey and list of rows
        Msg(f"Could not activate row with rowkey {rowkey} : {err}")

    if BreakWhen(conditions, rowkey=rowkey):
        DbgMsg(f"Rowkey, {rowkey}, matches for breakpoint", dbglabel=dbglb)
        breakpoint()

    if BreakpointCheck(nobreak=True) and DebugMode():
        DbgMsg("A manual breakpoint was detected... and so I am breakpointing, probably should check the stalled thingy")
        breakpoint()

    lastprocessed = voice_recording

    DbgExit(dbgblk, dbglb)

    return success


# deprecated
def CompleteBadRecording(download):
    """Complete a bad download"""

    recording = download.recording
    myname, mypath = download.MyPath()

    if recording.data["Archived"] is None or recording.data["Archived"] == "" or recording.data["Archived"] == "0":
        recording.data["Archived"] = "No/Not Downloaded"

    recording.data["Expanded"] = "Missing after download"
    missing = os.path.join(mypath, "missing.txt")

    ph.Touch(missing)

    if not download.IsBad():
        download.AddToBad()


# deprecated
def SaveMetaInfo(download):
    """Save Meta Info"""

    myname, mypath = download.MyPath()
    recording = download.recording

    if not os.path.exists(mypath):
        os.makedirs(mypath)

    metafile = os.path.join(mypath, "meta-data.csv")

    if not os.path.exists(metafile):
        AppendRows(metafile, recording.data)

    AppendRows(catalogFilename, recording.data)


# deprecated
def CompleteDownload(download):
    """Complete Download"""

    dbgblk, dbglb = DbgNames(CompleteDownload)

    DbgEnter(dbgblk, dbglb)

    if not download.IsBad():
        myname, mypath = download.MyPath()

        os.makedirs(mypath, exist_ok=True)

        recording = download.recording

        # Unzip into mypath
        myzipfile = os.path.join(download.downloadPath, download.filename)

        try:
            if os.path.exists(myzipfile):
                with zipfile.ZipFile(myzipfile, "r") as zip_ref:
                    zip_ref.extractall(mypath)

                recording.data["Archived"] = "Yes/Downloaded"

                os.remove(myzipfile)
            else:
                CompleteBadRecording(download)

            SaveMetaInfo(download)
        except Exception as err:
            ErrMsg(err, f"Failed to complete download of {recording.data['Conversation ID']}")
    else:
        CompleteBadRecording(download)
        SaveMetaInfo(download)

    DbgExit(dbgblk, dbglb)


# deprecated
def CheckActiveDownloads(browser, downloadTab, activeDownloads, downloadCount, sleep_time=3, pause=2):
    """Check (and/or Wait for) Active Downloads"""

    dbgblk, dbglb = DbgNames(CheckActiveDownloads)

    DbgEnter(dbgblk, dbglb)

    completedCount = 0

    while len(activeDownloads) >= downloadCount:
        for activeDownload in activeDownloads:
            progress = activeDownload.GetDownloadProgress(browser, downloadTab, sleep_time=sleep_time)

            if progress >= 100:
                DbgMsg(f"Completing {activeDownload.ConversationID()}", dbglabel=dbglb)
                CompleteDownload(activeDownload)

                activeDownloads.remove(activeDownload)

                completedCount += 1

        if len(activeDownloads) >= simultaneousDownloads and pause > 0:
            Sleep(pause)

        BreakpointCheck()
        CheckForEarlyTerminate()

    DbgExit(dbgblk, dbglb)

    return completedCount


# deprecated
def BatchDownloading(browser, downloadpath):
    """Download Items"""

    global ascTab, downloadTab, mainFrame, interval

    dbgblk, dbglb = DbgNames(BatchDownloading)

    DbgEnter(dbgblk, dbglb)

    completed = 0
    errored = 0

    # Open Downloads Tab For Inspection
    ascTab, downloadTab = OpenDownloadsTab(browser)

    mainTab = ascTab
    dlTab = downloadTab

    Sleep(4)

    SwitchFrame(browser, mainFrame, 3)

    nextClassDisabled = "ui-paginator-next ui-state-default ui-corner-all ui-state-disabled"
    nextButtonDisabledCss = f"a[class='{nextClassDisabled}']"
    nextButtonCss = "a[aria-label='Next Page']"

    nextBtn = ByCSS(browser, nextButtonCss)

    # Search from start date to end date in increments of 5 downloads per until all files downloaded
    startDate = officialStart
    searchInterval = timedelta(days=interval.days, hours=11, minutes=59, seconds=59)
    correction = timedelta(seconds=1)

    activeDownloads = list()

    DbgMsg(f"Starting run between {startDate} and {officialEnd}", dbglabel=dbglb)

    while startDate < officialEnd:
        endDate = startDate + searchInterval

        MainContext(browser)

        # Conduct a search between the given dates
        Search(browser, startDate, endDate)

        Half()

        paginationInfo = GetPageCount(browser)

        # Now, download the results X at a time and remember to page until you can't page anymore
        while True:
            MainContext(browser)

            # Get Items on current page
            data = GetData(browser, mainFrame)

            for recording in data:
                # Check recording to see if it's already downloaded or discardable in some other way

                vrec = VoiceDownload(recording, downloadpath)

                recording_we_want = vrec.SelectForDownload()

                if recording_we_want:
                    DbgMsg(f"Recording {recording.data['Conversation ID']} will be downloaded", dbglabel=dbglb)

                    # Only allow for X number of simultaneousDownloads
                    if Download(browser, vrec, mainFrame, data):
                        success = vrec.GetDownloadInfo(browser, downloadTab)

                        if success:
                            activeDownloads.append(vrec)
                    else:
                        errored += 1
                        vrec.AddToBad()
                        Msg(f"Download for recording {recording.data['Conversation ID']} had an error")
                else:
                    DbgMsg(f"Recording {recording.data['Conversation ID']} will be skipped", dbglabel=dbglb)
                    continue

                BreakpointCheck()
                CheckForEarlyTerminate()

                completed += CheckActiveDownloads(browser, downloadTab, activeDownloads, simultaneousDownloads, 1.25)

            del data

            nextBtn = browser.find_element(By.CSS_SELECTOR, nextButtonCss)

            if nextBtn.get_attribute("class") != nextClassDisabled:
                # More pages of items for this search to download
                nextBtn.click()
                Sleep(4)
            else:
                # No more items to download for this search
                # Now, make sure the D/Ls that are currently running complete

                if len(activeDownloads) > 0:
                    completed += CheckActiveDownloads(browser, downloadTab, activeDownloads, 1, 0)

                BusySpinnerPresent(browser, True)

                break

        Sleep(5.0)
        DbgMsg("Refreshing browser instance", dbglabel=dbglb)
        Refresh(browser)
        Sleep(8.0)

        startDate = endDate + correction
        endDate = (startDate + searchInterval)

    CloseDownloadsTab(browser, ascTab, downloadTab)

    Msg(f"Completed\t: {completed}\nErrored\t: {errored}")

    DbgExit(dbgblk, dbglb)


# deprecated
def POC(browser):
    """POC of download system"""

    # POC Search and D/L
    # Set Search Up
    Search(browser, startOn, endOn)

    # Extract Current Rows
    data = GetData(browser)

    # Conduct one download
    Download(browser, data[0])


# deprecated
def GetVoiceRecordings(browser, url, downloadpath):
    """Get ACS Voice Recordings... Probably"""

    global Username, Password, mainFrame, recordingsCatalog

    dbgblk, dbglb = DbgNames(GetVoiceRecordings)

    DbgEnter(dbgblk, dbglb)

    # Setup the Browser (i.e. Navigate to URL)
    SetupBrowser(browser, url)

    # Cancel Login Dialog (Via Ait)
    CancelDialog()

    # Actual Login... but dumb... (via Ait)
    if SmartLogin(browser):
        # Replace with wait
        Second()

        doPOC = False

        # Begin Searches and downloads

        if doPOC:
            POC(browser)
        else:
            SwitchFrame(browser, mainFrame)
            BatchDownloading(browser, downloadpath)

        SmartLogout(browser)

    DbgExit(dbgblk, dbglb)


def VoiceDev(browser, url):
    """Voice Dev"""

    global Username, Password, mainFrame

    dbgblk, dbglb = DbgNames(GetVoiceRecordings)

    DbgEnter(dbgblk, dbglb)

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

        # Nav to bidness page

        SwitchFrame(browser, mainFrame)

        startts = datetime(2017, 4, 2, 0, 0, 0)
        endts = datetime(2017, 5, 2, 23, 59, 59)

        Search(browser, startts, endts)

        breakpoint()

        SmartLogout(browser)

    DbgExit(dbgblk, dbglb)


def GeteBook(browser):
    """Grab Free Daily eBooks from Packt"""

    # https://www.browserstack.com/guide/download-file-using-selenium-python
    # https://www.selenium.dev/documentation/test_practices/discouraged/file_downloads/

    global Username, Password, config

    SetupBrowser(browser, config["packt"]["url1"])
    #SetupBrowser(browser, "https://account.packtpub.com/login?returnUrl=referrer")

    Sleep(20)

    packtTab, downloadsTab = OpenDownloadsTab(browser)

    usernameBox = browser.find_element(By.CSS_SELECTOR, "input[name='email']")
    passwordBox = browser.find_element(By.CSS_SELECTOR, "input[name='password']")
    loginButton = browser.find_element(By.CSS_SELECTOR, "form[class='ng-untouched ng-pristine ng-invalid'] > button[type='submit']")

    usernameBox.send_keys(Username)
    passwordBox.send_keys(Password)

    Half()

    loginButton.click()

    Sleep(3)

    Maximize(browser)

    browser.get(config["packt"]["url2"])

    btnCss = "button[id='freeLearningClaimButton']"

    WebDriverWait(browser, 120).until(presence_of_element_located((By.CSS_SELECTOR, btnCss)))

    getAccessButton = browser.find_element(By.CSS_SELECTOR, btnCss)

    getAccessButton.click()

    dlBtn = TagToAppear(browser, By.CSS_SELECTOR, "button[id='d4']", timeout=120)

    while not (dlBtn.is_displayed() and dlBtn.is_enabled()):
        Half()

    dlBtn.click()

    pdfLink = browser.find_element(By.XPATH, "//div[@class='download-container book']/a[text()='PDF']")
    pdfLink.click()

    downloads = GetDownloads(browser, downloadsTab)

    terminate = False

    while not terminate:
        for file, progress in downloads.items():
            Msg(f"{file} : {progress}")

            if progress == 100:
                Half()
                terminate = True

    CloseDownloadsTab(browser, packtTab, downloadsTab)

    if not DebugMode():
        logoutLink = browser.find_element(By.XPATH, "//a[text()='Sign Out']")


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

    if DebugMode():
        breakpoint()


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


def BuildParser():
    """Build Parser"""

    parser = argparse.ArgumentParser(prog="opfubar", description="OpFubar", epilog="There is no help in this place")

    parser.add_argument("cmd", nargs="*", choices=["asc", "packt", "dev"], default="asc", help="Scraper to call")
    parser.add_argument("--clearlog", action="store_true", help="Clear Run Log")
    parser.add_argument("--clearcat", action="store_true", help="Clear catalog")
    parser.add_argument("--clearfolder", action="store_true", help="Clear download folder of disposable logs")
    parser.add_argument("--clearmax", action="store_true", help="Clear the entire folder, no survivors")
    parser.add_argument("--cleanzips", action="store_true", help="Clear Zip Archives from download folder")
    parser.add_argument("-d", "--debug", action="store_true", help="Enter debug mode")
    parser.add_argument("-q", "--quit", action="store_true", help="Early quit")
    parser.add_argument("-s", "--session", default="session1", help="Session name")
    parser.add_argument("--term", action="store_true", help="Force an early terminate")
    parser.add_argument("--bp", action="store_true", help="Force a manual breakpoint")
    parser.add_argument("--int", help=f"Interval in days, between searches, default = {interval.days}")
    parser.add_argument("--start", help="Start date [at midnight, m/d/y]")
    parser.add_argument("--end", help="End date [just before midnight, m/d/y]")
    parser.add_argument("--test", action="store_true", help="Enter test mode")
    parser.add_argument("--env", action="store_true", help="Show environment settings")
    parser.add_argument("--config", help="Alternate config file")

    return parser


def testmode():
    """Test Mode"""

    DebugMode(True)
    CmdLineMode(True)

    breakpoint()


if __name__ == '__main__':
    CmdLineMode(True)
    DebugMode(True)

    parser = BuildParser()
    config = configparser.ConfigParser()

    args = parser.parse_args()

    if args.debug:
        DebugMode(True)

        if os.path.exists("dbglabels.txt"):
            DbgMsg("Loading Debug Label Enablement file")
            ph.LoadDebugEnableFile("dbglabels.txt")
    else:
        DebugMode(False)

    sessionName = args.session

    if args.config is not None and os.path.exists(args.config):
        config.read(args.config)
    elif os.path.exists(configFilename):
        config.read(configFilename)
    else:
        Msg(f"Supplied or default config file does not exist, {configFilename}/{args.config}")
        #quit()

    urls = {
        "packt": "https://www.packtpub.com/free-learning/",
        "asc": "https://129.49.122.190/POWERplayWeb/",
        "tsa": "https://techstepacademy.com/training-ground/",
        "tsatrial": "https://techstepacademy.com/trial-of-the-stones/"
    }

    chrome = None

    BreakOn.extend(["GetDownloadInfo", "GetDownloadProgress"])

    cmd = None

    if len(args.cmd) > 0:
        if type(args.cmd) is str:
            cmd = args.cmd
        else:
            cmd = args.cmd[0]

    if args.test:
        testmode()
    elif cmd in ["asc", ""] or cmd is None:
        url = urls["asc"]

        Username = config["asc_creds"]["username"]
        Password = config["asc_creds"]["password"]

        downloadPath = config["asc"]["downloadpath"]

        sessionASC = config.get(sessionName, "logpath", fallback=sessionASC)

        interval_days = int(config["asc"]["interval"])
        interval = timedelta(days=interval_days)
        catalogfileName = config["asc"]["catalogfile"]
        badrecordingsName = config["asc"]["badrecordings"]

        catalogFilename = os.path.join(sessionASC, catalogfileName)
        badRecordings = os.path.join(sessionASC, badrecordingsName)

        earlyTerminateFlag = Join(sessionASC, "terminate.txt")
        breakpointFlag = Join(sessionASC, "breakpoint.txt")
        RemoveFile(breakpointFlag, earlyTerminateFlag)

        ph.Logfile = runlog = Join(sessionASC, runlogName)

        if args.term:
            ph.Touch(earlyTerminateFlag)
            sys.exit(0)
        if args.bp:
            ph.Touch(breakpointFlag)
            sys.exit(0)

        if args.clearmax:
            ClearFolderMax(downloadPath)
        else:
            if args.clearlog:
                RemoveFile(runlog)

            if args.clearcat:
                RemoveFile(catalogFilename)

            if args.clearfolder:
                ClearFolder(downloadPath, protected=[catalogFilename, badRecordings], disposables=[runlog])

            if args.cleanzips:
                ClearZips(downloadPath)

        tsc = ph.TimestampConverter()

        if args.int is not None:
            interval = timedelta(days=int(args.int))

        if args.start is not None:
            officialStart = tsc.ConvertTimestamp(args.start)
            officialEnd = officialStart + timedelta(days=365)
        else:
            officialStart = tsc.ConvertTimestamp(config.get(sessionName, "start", fallback="1/1/2017"))
            officialEnd = officialStart + timedelta(days=365)

        if args.end is not None and args.start is not None:
            officialEnd = tsc.ConvertTimestamp(args.end)
        else:
            value = config.get(sessionName,"end", fallback=None)

            if value is None:
                officialEnd = officialStart + timedelta(days=365)
            else:
                officialEnd = tsc.ConvertTimestamp(value)

        if args.env:
            Msg("Environment\n============")
            Msg(f"Download\t: {downloadPath}")
            Msg(f"Run log\t\t: {runlog}")
            Msg(f"Catalog\t\t: {catalogFilename}")
            Msg(f"Bad Recs\t: {badRecordings}")
            Msg(f"Start On\t: {startOn}")
            Msg(f"End On\t\t: {endOn}")
        else:
            asc_browser = ASCBrowser(url, downloadPath)

            asc_browser.GetVoiceRecordings(interval, Username, Password)
    elif cmd == "dev":
        Username = config["asc_creds"]["username"]
        Password = config["asc_creds"]["password"]

        downloadPath = config["asc"]["downloadpath"]
        interval = int(config["asc"]["interval"])
        catalogfileName = config["asc"]["catalogfile"]
        badrecordingsName = config["asc"]["badrecordings"]

        earlyTerminateFlag = Join(downloadPath, "terminate.txt")
        breakpointFlag = Join(downloadPath, "breakpoint.txt")
        RemoveFile(breakpointFlag, earlyTerminateFlag)

        ph.Logfile = runlog = Join(downloadPath, runlogName)

        if args.clearfolder:
            ClearFolder(downloadPath)
        else:
            if args.clearlog:
                os.remove(runlog)

            if args.clearcat:
                os.remove(catalogFilename)

        options = DownloadOptions(downloadPath)
        chrome = webdriver.Chrome(options=options)

        VoiceDev(chrome, urls["acs"])
    elif cmd == "packt":
        Username = config["packt_creds"]["username"]
        Password = config["packt_creds"]["password"]

        downloadPath = config["packt"]["downloadpath"]

        ph.Logfile = runlog = Join(downloadPath, runlogName)

        if args.clearlog:
            os.remove(runlog)

        # Example of downloading a file
        # urllib.request.urlretrieve(src,downloadpath)

        options = DownloadOptions(downloadPath, withcaps=True)
        #chrome = webdriver.Chrome(options=options)

        chrome = webdriver.Remote(command_executor="http://merry.digitalwicky.biz:4444", options=options)

        GeteBook(chrome)
    else:
        chrome = webdriver.Chrome()

        GetTSA(chrome, urls["tsa"])
        # GetStones(chrome, urls["tsatrial"])

    chrome.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Notes
# NoSuchElementException, ElementNotInteractableException, TimeoutException, StaleElementReferenceException