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
from selenium.common.exceptions import TimeoutException
from application import postetools, drivertools, operations
from application.webelements import Urls, Xpaths
from application.gui import layouts, oneshot
import PySimpleGUI as sg
import time
import os


if __name__ == "__main__":
    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), "geckodriver.exe"))
    # False for Dev, True for release
    headless = True
    options = drivertools.set_options(headless)

    postetools.init_folder()
    driver = webdriver.Firefox(executable_path=gecko, options=options)

    while True:  # Login loop
        AZIENDA, USERNAME, PASSWORD = postetools.get_credentials()
        save_creds_flag = False
        if (AZIENDA, USERNAME, PASSWORD) == (None, None, None):
            AZIENDA, USERNAME, PASSWORD, save_creds_flag = oneshot.set_credentials_window()
        # Get login page and wait for it to load
        driver.get(Urls.LOGIN_PAGE)
        wait = WebDriverWait(driver, 5)
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
        form_pwd.send_keys(Keys.RETURN)

        # Premere continua
        try:  # try to press continue after successful login
            wait.until(EC.element_to_be_clickable((By.XPATH, Xpaths.CONTINUA)))
            continua_login_btn = driver.find_element_by_xpath(Xpaths.CONTINUA)
            continua_login_btn.click()
            break  # break out of the loop, login is successful
        except TimeoutException:
            # There are 2 causes for a Timeout here, either the credentials were wrong
            # and the login failed because of this, or the website threw us an oddball
            # error (or connection has problems, but nothing can be done about this)
            if drivertools.authentication_failed:
                # Delete previously saved credentials as to not block the account by repeated failed logins
                postetools.save_credentials(None, None, None)
                sg.popup_error("Autenticazione fallita: verificare che le credenziali inserite siano corrette e riprovare.")
    
    # Se siamo qui, le credenziali inserite erano sicuramente corrette, salvale
    if save_creds_flag:
        try:
            postetools.save_credentials(AZIENDA, USERNAME, PASSWORD)
        except IOError:
            pass

    # Lista condomini
    wait = WebDriverWait(driver, 20)
    link_condomini_diz = operations.get_condo_link_dict(driver, AZIENDA, USERNAME, PASSWORD)

    # FINESTRA PRINCIPALE
    ############################
    ############################
    # Inserire qui l'interfaccia grafica, dal quale estrarre:
    #   Lista di condomini da elaborare
    #   flag 896 e cbi per ogni condominio
    #   data di partenza per i file da scaricare
    #   altro?
    # Estrapolare il loop principale che segue in una funzione
    ############################
    window = sg.Window("downBPIOL - Download CBI-896 da BPIOL", layouts.main_layout(link_condomini_diz))
    while True:
        event, values = window.read(timeout=200)
        if event == sg.TIMEOUT_EVENT:
            continue

        if event == sg.WIN_CLOSED:
            window.close()
            driver.close()
            exit()

        if event == "-TUTTI-":
            layouts.permute_checkboxes(window, values)
        
        if event == "-SCARICA-":
            SCRIPT_START = time.time()

            chosen_downloads = postetools.chosen_downloads(values)
            max_count = postetools.chosen_max_counter(chosen_downloads)
            counter = 1
            progress_bar = window["-BAR-"]
            progress_bar.update_bar(counter, max=max_count)

            # For loop that for each item in link_condomini_diz must:
            # 1. download each item's bank account movements
            # 2. download each item's 896 report (carefully choose starting date for these 2 items)
            # 3. print(?) the bank account movements
            for x in range(len(link_condomini_diz.keys())):
                # Seleziona il condominio
                nome_condo = list(link_condomini_diz.keys())[x]

                # Procedi solo se c'è qualcosa da scaricare
                if chosen_downloads[nome_condo]["896"] or chosen_downloads[nome_condo]["CBI"]:
                    counter = layouts.update_bar_message(f"Logging into: {nome_condo}", counter, window)
                    print("Logging into: " + nome_condo)
                    
                    '''
                    XXX this is an *IMPORTANT* wait, as longer wait times seem to influence whether or not
                    XXX the login asks for app authentication or not, with shorter times making the
                    XXX authentication way more likely to be needed.
                    XXX (crazy spaghetti code, Poste Italiane)
                    '''
                    time.sleep(2) #XXX
                    window.refresh()
                    link_condomini_diz[nome_condo].click()
                    time.sleep(2)
                    window.refresh()


                    # Rimuovi avvisi indipendentemente dalla loro presenza o meno
                    driver.get(Urls.URL_PER_PROSEGUIRE)
                    time.sleep(1)
                    window.refresh()


                    if chosen_downloads[nome_condo]["CBI"]:
                        # Vai a scarica movimenti
                        driver.get(Urls.URL_ESPORTA_MOVIMENTI)
                        time.sleep(1)
                        window.refresh()

                        file_cbi = operations.scarica_movimenti(driver)
                        drivertools.rename_file(file_cbi, R"CBI\\" + nome_condo)
                        time.sleep(1)
                        window.refresh()
                        counter = layouts.update_bar_message(f"Scaricato CBI per {nome_condo}...", counter, window)
                        print(f"Scaricato CBI per {nome_condo}...")

                    if chosen_downloads[nome_condo]["896"]:
                        # Vai a scarica 896
                        driver.get(Urls.URL_ESPORTA_896)
                        time.sleep(1)
                        window.refresh()
                        file_896 = operations.scarica_896(driver)
                        drivertools.rename_file(file_896, R"896\\" + nome_condo)
                        time.sleep(1)
                        window.refresh()
                        counter = layouts.update_bar_message(f"Scaricato 896 per {nome_condo}...", counter, window)
                        print(f"Scaricato 896 per {nome_condo}...")
                    
                    # All done with the current condominio, go back to selection
                    counter = layouts.update_bar_message(f"Fine elaborazione per {nome_condo}", counter, window)
                    print(f"Fine elaborazione per {nome_condo}")
                    driver.get(Urls.URL_CAMBIO_AZIENDA)
                    
                    #Re-get everything
                    link_condomini_diz = operations.get_condo_link_dict(driver, AZIENDA, USERNAME, PASSWORD)
                    ###################
            window["-MESSAGE-"].update(f"Operazione completata in {time.time() - SCRIPT_START} secondi.")
            print(f"EXECUTION COMPLETE AFTER {time.time() - SCRIPT_START} SECONDS")

