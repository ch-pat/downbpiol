from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from application import postetools
from application.webelements import Urls, Xpaths
import time


def scarica_movimenti(pagina_movimenti) -> str:
    '''
    Downloads cbi file and returns the name of the file downloaded
    '''
    # Enter form frame
    wait = WebDriverWait(pagina_movimenti, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it(((By.NAME, "frSERVIZI"))))
    wait.until(EC.frame_to_be_available_and_switch_to_it(((By.NAME, "frMAIN"))))

    # Operate on the form
    wait.until(EC.presence_of_element_located ((By.ID, "rapporti")))
    options = Select(pagina_movimenti.find_element_by_id("rapporti"))
    options.select_by_index(1)

    # Fill form date
    d, m, y = postetools.calculate_start_date()
    giorno_inizio = pagina_movimenti.find_element_by_xpath(Xpaths.MOVIMENTI_FORM_GIORNO)
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

    # chrome's .back() method takes driver back out of the frame
    if isinstance(pagina_movimenti, webdriver.Chrome):
        wait.until(EC.frame_to_be_available_and_switch_to_it(((By.NAME, "frSERVIZI"))))
        wait.until(EC.frame_to_be_available_and_switch_to_it(((By.NAME, "frMAIN"))))

    # Go to download page
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpaths.MOVIMENTI_FORM_GIORNO)))
    giorno_inizio = pagina_movimenti.find_element_by_xpath(Xpaths.MOVIMENTI_FORM_GIORNO)
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
    wait.until(EC.element_to_be_clickable((By.XPATH, Xpaths.ULTIMO_CBI)))
    download_button = pagina_movimenti.find_element_by_xpath(Xpaths.ULTIMO_CBI)
    download_button.click()
    filename = pagina_movimenti.find_element_by_xpath(Xpaths.NOME_ULTIMO_CBI).text
    time.sleep(1)

    return filename

def scarica_896(pagina_896) -> str:
    '''
    Downloads 896 file and returns the name of the file downloaded
    '''
    wait = WebDriverWait(pagina_896, 30)

    # Choose account from drop down
    wait.until(EC.presence_of_element_located((By.ID, "idAccount")))
    options = Select(pagina_896.find_element_by_id("idAccount"))
    options.select_by_index(1)

    # Fill form date
    d, m, y = postetools.calculate_start_date()
    giorno_inizio = pagina_896.find_element_by_xpath(Xpaths.FORM_GIORNO_896)
    giorno_inizio.clear()
    giorno_inizio.send_keys(d)
    giorno_inizio.send_keys(Keys.TAB)
    actions = ActionChains(pagina_896)
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
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    actions.reset_actions()
    time.sleep(1)
    pagina_896.back()

    # Go to download page
    wait.until(EC.visibility_of_element_located((By.XPATH, Xpaths.FORM_GIORNO_896)))
    giorno_inizio = pagina_896.find_element_by_xpath(Xpaths.FORM_GIORNO_896)
    giorno_inizio.clear()
    giorno_inizio.send_keys(d)
    giorno_inizio.send_keys(Keys.TAB)
    actions = ActionChains(pagina_896)
    actions.send_keys(m)
    actions.send_keys(Keys.TAB)
    actions.send_keys(y)
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
    wait.until(EC.element_to_be_clickable((By.XPATH, Xpaths.ULTIMO_896)))
    download_button = pagina_896.find_element_by_xpath(Xpaths.ULTIMO_896)
    download_button.click()
    filename = pagina_896.find_element_by_xpath(Xpaths.NOME_ULTIMO_896).text
    time.sleep(1)

    return filename

def get_condo_link_dict(driver, AZIENDA, USERNAME, PASSWORD) -> dict:
    '''
    wraps postetools.extract_links_from_tabella_condomini
    returns a {"name": clickable_element} dict
    '''
    wait = WebDriverWait(driver, 30)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, Xpaths.TABELLA_CONDOMINI)))    
        tabella_condomini = driver.find_element_by_xpath(Xpaths.TABELLA_CONDOMINI)
        link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)
        return link_condomini_diz
    except:
        wait.until(EC.visibility_of_element_located((By.XPATH, Xpaths.CONTINUA_ERRORE_GENERICO)))  
        continua_btn = driver.find_element_by_xpath(Xpaths.CONTINUA_ERRORE_GENERICO)  
        continua_btn.click()
        
        # Ci riporta alla pagina di login, rifacciamo il login
        wait.until(EC.visibility_of_element_located((By.ID, "azienda")))
        form_azienda = driver.find_element_by_id("azienda")
        form_username = driver.find_element_by_id("username")
        form_pwd = driver.find_element_by_id("password")
        time.sleep(2)

        form_azienda.clear()
        form_azienda.send_keys(AZIENDA)
        form_username.clear()
        form_username.send_keys(USERNAME)
        form_pwd.clear()
        form_pwd.send_keys(PASSWORD)
        form_pwd.send_keys(Keys.RETURN)

        wait.until(EC.element_to_be_clickable((By.XPATH, Xpaths.CONTINUA)))
        continua_login_btn = driver.find_element_by_xpath(Xpaths.CONTINUA)
        continua_login_btn.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, Xpaths.TABELLA_CONDOMINI)))    
        tabella_condomini = driver.find_element_by_xpath(Xpaths.TABELLA_CONDOMINI)
        link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)
        return link_condomini_diz

