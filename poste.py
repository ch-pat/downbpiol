from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import postetools

login_page = "https://idp-bpiol.poste.it/jod-idp-bpiol/cas/login.html"




if __name__ == "__main__":
    
    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), "geckodriver.exe"))

    driver = webdriver.Firefox(executable_path=gecko)
    driver.get(login_page)
    #print("got page")
    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.ID, "azienda")))

    #Login page
    
    form_azienda = driver.find_element_by_id("azienda")
    #print("found form: azienda")
    form_username = driver.find_element_by_id("username")
    #print("found form: username")
    form_pwd = driver.find_element_by_id("password")
    #print("found form: password")
    time.sleep(2)
    
    form_azienda.clear()
    form_azienda.send_keys("m000003842")
    form_username.clear()
    form_username.send_keys("CHMPRY91M12H501N")
    form_pwd.clear()
    form_pwd.send_keys("BPIOL.patryk4")
    #print("Sent all keys")
    time.sleep(2)

    form_pwd.send_keys(Keys.RETURN)
    time.sleep(4)

    # Premere continua
    continua_login_btn = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/p/button")
    continua_login_btn.click()

    # Lista condomini
    tabella_condomini = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/form/div/table")
    time.sleep(2)
    link_condomini_diz = postetools.extract_links_from_tabella_condomini(tabella_condomini)
    # for x in link_condomini_diz.items():
    #     print(x[1].text, x[0])

    # For loop that for each item in link_condomini_diz must:
    # 1. download each item's bank account movements
    # 2. download each item's 896 report (carefully choose starting date for these 2 items)
    # 3. print(?) the bank account movements