from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import postetools
import drivertools

LOGIN_PAGE = "https://idp-bpiol.poste.it/jod-idp-bpiol/cas/login.html"
URL_ESPORTA_MOVIMENTI = "https://bancopostaimpresaonline.poste.it/bpiol1/YCC.do?method=home&FUNCTIONCODESELECTED=YCC"
URL_CAMBIO_AZIENDA = "https://bancopostaimpresaonline.poste.it/bpiol1/login.do?method=cambioAzienda&MENUNAME=LOGIN%20OPERATORE&PAGENAME=&LNAME=cpw.gif&ALT_TEST=alt.cambio.azienda&FUNCTIONCODESELECTED=XXX"
AZIENDA, USERNAME, PASSWORD = postetools.get_credentials()
XPATHS = postetools.get_xpaths()
SCRIPT_START = time.time()

def scarica_movimenti(pagina_movimenti) -> str:
    '''
    Downloads cbi file and returns the name of the file downloaded
    '''
    # Enter form frame
    wait = WebDriverWait(pagina_movimenti, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it(((By.NAME, "frSERVIZI"))))
    wait.until(EC.frame_to_be_available_and_switch_to_it(((By.NAME, "frMAIN"))))

    # Operate on the form
    options = Select(pagina_movimenti.find_element_by_id("rapporti"))
    options.select_by_index(1)

    # Fill form date
    d, m, y = postetools.calculate_start_date()
    giorno_inizio = pagina_movimenti.find_element_by_xpath(XPATHS["movimenti_form_giorno"])
    giorno_inizio.clear()
    giorno_inizio.send_keys(d)
    giorno_inizio.send_keys(Keys.TAB)
    actions = ActionChains(pagina_movimenti)
    actions.send_keys(m)
    actions.send_keys(Keys.TAB)
    actions.send_keys(y)

    # Export file
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    actions.reset_actions()
    time.sleep(1)
    pagina_movimenti.back()

    # Go to download page
    wait.until(EC.visibility_of_element_located((By.XPATH, XPATHS["movimenti_form_giorno"])))
    giorno_inizio = pagina_movimenti.find_element_by_xpath(XPATHS["movimenti_form_giorno"])
    giorno_inizio.clear()
    giorno_inizio.send_keys(d)
    actions = ActionChains(pagina_movimenti)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB) 
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.RETURN)
    actions.perform()

    # Download file
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS["ultimo_cbi"])))
    download_button = pagina_movimenti.find_element_by_xpath(XPATHS["ultimo_cbi"])
    download_button.click()
    filename = pagina_movimenti.find_element_by_xpath(XPATHS["nome_ultimo_cbi"]).text
    time.sleep(1)

    return filename


if __name__ == "__main__":
    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), "geckodriver.exe"))

    # False for Dev, True for release
    headless = True
    options = drivertools.set_options(headless)

    driver = webdriver.Firefox(executable_path=gecko, options=options)

    # Get login page and wait for it to load
    driver.get(LOGIN_PAGE)    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.ID, "azienda")))
    print(f"OVERHEAD TIME: {time.time() - SCRIPT_START} SECONDS")
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
    form_pwd.send_keys(Keys.RETURN)

    # Premere continua
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS["continua"])))
    continua_login_btn = driver.find_element_by_xpath(XPATHS["continua"])
    continua_login_btn.click()

    # Lista condomini
    wait.until(EC.visibility_of_element_located((By.XPATH, XPATHS["tabella_condomini"])))    
    tabella_condomini = driver.find_element_by_xpath(XPATHS["tabella_condomini"])
    link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)

    # For loop that for each item in link_condomini_diz must:
    # 1. download each item's bank account movements
    # 2. download each item's 896 report (carefully choose starting date for these 2 items)
    # 3. print(?) the bank account movements
    for x in range(len(link_condomini_diz.keys())):
        # Seleziona il condominio
        nome_condo = list(link_condomini_diz.keys())[x]
        print("Logging into: " + nome_condo)
        
        '''
        XXX this is an *IMPORTANT* wait, as longer wait times seem to influence whether or not
        XXX the login asks for app authentication or not, with shorter times making the
        XXX authentication way more likely to be needed.
        XXX (crazy spaghetti code, Poste Italiane)
        '''
        time.sleep(2) #XXX
        link_condomini_diz[nome_condo].click()
        time.sleep(2)

        # Vai a scarica movimenti
        driver.get(URL_ESPORTA_MOVIMENTI)
        time.sleep(1)
        file_cbi = scarica_movimenti(driver)
        drivertools.rename_file(file_cbi, nome_condo)
        time.sleep(1)

        # All done with the current condominio, go back to selection
        driver.get(URL_CAMBIO_AZIENDA)
        
        #Re-get everything
        wait.until(EC.visibility_of_element_located((By.XPATH, XPATHS["tabella_condomini"])))    
        tabella_condomini = driver.find_element_by_xpath(XPATHS["tabella_condomini"])
        link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)
        ###################

print(f"EXECUTION COMPLETE AFTER {time.time() - SCRIPT_START} SECONDS")