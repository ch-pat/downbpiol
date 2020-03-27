from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os

def set_options(headless=False) -> Options:
    options = Options()
    path = r"C:\Users\Utente\Download"
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", path)
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
    path = r"C:\Users\Utente\Download"
    original_file = os.path.join(path, original)
    new_name = os.path.join(path, condo_name + ".zip")
    os.rename(original_file, new_name)