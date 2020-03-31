from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import zipfile

DOWNLOAD_PATH = os.path.join(os.path.abspath(os.curdir), "downloads")

def set_options(headless=False) -> Options:
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", DOWNLOAD_PATH)
    options.set_preference("browser.download.forbid_open_with", True)
    options.set_preference("browser.download.manager.alertOnEXEOpen", False)
    options.set_preference("browser.helperApps.neverAsk.openFile", "application/unknown, application/x-www-form-urlencoded, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/unknown, application/x-www-form-urlencoded, application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
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

def rename_file(original, condo_name):
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