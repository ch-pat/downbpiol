from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os
import postetools

LOGIN_PAGE = "https://idp-bpiol.poste.it/jod-idp-bpiol/cas/login.html"
URL_ESPORTA_MOVIMENTI = "https://bancopostaimpresaonline.poste.it/bpiol1/YCC.do?method=home&FUNCTIONCODESELECTED=YCC"
AZIENDA, USERNAME, PASSWORD = postetools.get_credentials()
XPATHS = postetools.get_xpaths()


def scarica_movimenti(pagina_movimenti):
    # Enter form frame
    pagina_movimenti.switch_to.frame("frSERVIZI")
    pagina_movimenti.switch_to.frame("frMAIN")

    # Operate on the form
    options = Select(pagina_movimenti.find_element_by_id("rapporti"))
    options.select_by_index(1)

    # Remember to exit the frames
    pagina_movimenti.switch_to.parent_frame()
    pagina_movimenti.switch_to.parent_frame()
    print(pagina_movimenti.page_source)


if __name__ == "__main__":
    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), "geckodriver.exe"))

    # headless options, uncomment for headless
    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(executable_path=gecko, options=options)

    # headed for dev
    driver = webdriver.Firefox(executable_path=gecko)

    # Get login page and wait for it to load
    driver.get(LOGIN_PAGE)    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.ID, "azienda")))
    
    # Find forms to fill
    form_azienda = driver.find_element_by_id("azienda")
    form_username = driver.find_element_by_id("username")
    form_pwd = driver.find_element_by_id("password")
    time.sleep(2)
    
    # Fill forms (clear them to be safe)
    form_azienda.clear()
    form_azienda.send_keys(AZIENDA)
    form_username.clear()
    form_username.send_keys(USERNAME)
    form_pwd.clear()
    form_pwd.send_keys(PASSWORD)
    #print("Sent all keys")
    time.sleep(2)
    form_pwd.send_keys(Keys.RETURN)
    time.sleep(4)

    # Premere continua
    continua_login_btn = driver.find_element_by_xpath(XPATHS["continua"])
    continua_login_btn.click()

    # Lista condomini
    tabella_condomini = driver.find_element_by_xpath(XPATHS["tabella_condomini"])
    time.sleep(2)
    link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)
    # for x in link_condomini_diz.items():
    #     print(x[1].text, x[0])

    # For loop that for each item in link_condomini_diz must:
    # 1. download each item's bank account movements
    # 2. download each item's 896 report (carefully choose starting date for these 2 items)
    # 3. print(?) the bank account movements
    for x in range(len(link_condomini_diz.keys())):
        # Seleziona il condominio
        print("Logging into: " + list(link_condomini_diz.keys())[x])
        time.sleep(2)
        link_condomini_diz[list(link_condomini_diz.keys())[x]].click()
        time.sleep(2)

        # Vai a scarica movimenti
        driver.get(URL_ESPORTA_MOVIMENTI)
        time.sleep(2)
        scarica_movimenti(driver)
        time.sleep(2)

        # All done with the current condominio, go back to selection
        cambio_azienda = driver.find_element_by_xpath(XPATHS["cambio_azienda"])
        cambio_azienda.click()
        
        #Re-get everything
        time.sleep(4)
        tabella_condomini = driver.find_element_by_xpath(XPATHS["tabella_condomini"])
        link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)
        ###################