from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from application.webelements import Urls, Xpaths
import os
import zipfile


DOWNLOAD_PATH = os.path.join(os.path.abspath(os.curdir), "downloads")

def set_options(headless: bool, driver_to_use: str) -> Options:
    '''
    Many content types are set to not show download dialogs to prevent headaches, but the main ones are the following:
    CBI: application/unknown
    896: application/x-download
    '''
    
    if driver_to_use == "Firefox":
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", DOWNLOAD_PATH)
        options.set_preference("browser.download.forbid_open_with", True)
        options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        options.set_preference("browser.helperApps.neverAsk.openFile", "application/unknown, application/x-www-form-urlencoded, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/x-download, application/octet-stream")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/unknown, application/x-www-form-urlencoded, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/x-download, application/octet-stream")
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.manager.focusWhenStarting", False)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.alwaysAsk.force", False)
        options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        options.set_preference("browser.download.manager.closeWhenDone", True)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.download.manager.useWindow", False)
        options.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
        options.set_preference("pdfjs.disabled", True)
        options.set_headless(headless)
        return options
    if driver_to_use == "Chrome":
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": DOWNLOAD_PATH + "\\", # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True
                 }
        options.headless = headless
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("prefs", prefs)
        return options

def rename_file(original, condo_name):
    original = sanitize_filename(original)
    original_file = os.path.join(DOWNLOAD_PATH, original)
    new_name = os.path.join(DOWNLOAD_PATH, condo_name + ".txt")
    extracted_file = os.path.join(DOWNLOAD_PATH, unzip_file(original_file))
    if os.path.exists(new_name):
        os.remove(new_name)
    os.renames(extracted_file, new_name)
    os.remove(original_file)

def unzip_file(filename):
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(path=os.path.dirname(filename))
    return zfile.namelist()[0]

def sanitize_filename(filename: str) -> str:
    '''
    Removes all occurrences of illegal characters from the filename given
    Returns sanitized filename
    '''
    illegal_chars = "><:\"/\\|?*"
    for c in illegal_chars:
        filename = filename.replace(c, "")
    return filename


def authentication_failed(driver: webdriver.Firefox):
    failure = driver.find_elements_by_xpath(Xpaths.AUTENTICAZIONE_FALLITA)
    if failure:
        if "fallita" in failure[0].text:
            return True
    return False


def locate_driver() -> str:
    d = os.listdir()
    if "chromedriver.exe" in d:
        return "Chrome"
    if "geckodriver.exe" in d:
        return "Firefox"
    return None