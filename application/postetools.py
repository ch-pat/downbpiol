from datetime import datetime, timedelta
from getpass import getpass
import time, os, json


def init_folder():
    if "config.json" not in os.listdir():
        with open("config.json", "w+") as f:
            data = {
                "azienda": None,
                "username": None,
                "password": None
            }
            json.dump(data, f, indent=2)
    if not os.path.isdir("downloads"):
        os.mkdir("downloads")
        os.mkdir("downloads/896")
        os.mkdir("downloads/CBI")

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
    returns (azienda, username, password) or (None, None, None) if absent
    '''
    # Case for missing credentials / first run
    if not "config.json" in os.listdir():
        return None, None, None

    # Read existing credentials    
    with open("config.json", "r") as f:
        contents = json.load(f)
    
    return contents["azienda"], contents["username"], contents["password"]

def calculate_start_date() -> (str, str, str):
    '''
    finds starting date for forms
    --for a first version, this simply gives the date 15 days ago
    --next versions must keep track of latest download via script
    '''
    cur = datetime.today()
    two_weeks = timedelta(days=15)
    start_date = cur - two_weeks
    return str(start_date.day), str(start_date.month), str(start_date.year)

""" def create_credentials(): # not called in GUI
    '''
    Routine for setting login credentials for the first time of when resetting them
    '''
    prompt = "q"
    while prompt in "qQ" and prompt != "":
        azienda = input("Inserire AZIENDA:\t")
        username = input("Inserire USERNAME:\t")
        password = getpass("Inserire PASSWORD:\t")
        prompt = input("Verificare le credenziali inserite. Se si desidera procedere, premere INVIO. Se si desidera re-inserire le credenziali, immettere Q.\n")
    
    #TODO: could add here a try to login and respond based on HTTP status code received
    with open("application/config/.credentials", "w+") as f:
        f.writelines(line + "\n" for line in (azienda, username, password))
    print("Credenziali salvate")
    return azienda, username, password """

def save_credentials(azienda: str, username: str, password: str):
    with open("config.json", "r") as f:
        data = json.load(f)
    data["azienda"], data["username"], data["password"] = azienda, username, password
    with open("config.json", "w+") as f:
        json.dump(data, f, indent=2)

def chosen_downloads(values: dict) -> dict:
    """
    Takes values from the PySimpleGUI window and returns a dict with the chosen downloads formatted as:
    {
        "condo1": {"896": True, "CBI": True},
        "condo2": ...
    }

    this function and the corresponding dict could be expanded to include "last downloaded dates", which can be saved into the config file
    """
    chosen = {}
    for k in values.keys():
        if isinstance(k, tuple):
            chosen[k[1]] = {"896": None, "CBI": None}
    for k in values.keys():
        if isinstance(k, tuple):
            chosen[k[1]][k[0]] = values[k]
    return chosen

def chosen_max_counter(chosen_downloads: dict) -> int:
    items = 0
    for k in chosen_downloads.keys():
        if chosen_downloads[k]["896"] or chosen_downloads[k]["CBI"]:
            items += 2
        if chosen_downloads[k]["896"]:
            items += 1
        if chosen_downloads[k]["CBI"]:
            items += 1
    return items