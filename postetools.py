from selenium.webdriver.support.ui import Select
import time

def extract_links_from_tabella_condomini(tabella_condomini) -> dict:
    '''
    tabella_condomini is a WebElement representation of a table
    returns a {"name": clickable_element} dict
    '''
    table_body = tabella_condomini.find_element_by_tag_name("tbody")
    clickable_elements = []
    for element in table_body.find_elements_by_tag_name("td"):
        # print("element.text: " + element.text)
        clickable_elements.append(element)
    name_click_diz = {n.text:c for (n,c) in zip(clickable_elements[1:len(clickable_elements):2], clickable_elements[0:-1:2])}
    return name_click_diz

def get_credentials() -> (str, str, str):
    '''
    needs a .credentials file in the directory
    returns (azienda, username, password)
    '''
    with open(".credentials", "r") as f:
        contents = f.read()
        creds = contents.splitlines()
    return creds[0], creds[1], creds[2]

def get_xpaths() -> dict:
    '''
    needs a .xpaths file in the directory
    returns a dictionary of xpaths
    '''
    #TODO: find some way to document the existing xpaths
    xpaths = {}
    with open(".xpaths", "r") as f:
        contents = f.read()
        for line in contents.splitlines():
            name, path = line.split()
            xpaths[name] = path
    return xpaths
