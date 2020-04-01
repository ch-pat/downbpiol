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