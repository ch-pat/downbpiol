from datetime import datetime, timedelta
from getpass import getpass
import time, os


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
    if not ".credentials" in os.listdir("application/config"):
        return None, None, None

    # Read existing credentials    
    with open("application/config/.credentials", "r") as f:
        contents = f.read()
        creds = contents.splitlines()
    
    # Offer the opportunity to reset credentials
    print("Si sta per accedere con le seguenti credenziali:\n")
    print(f"AZIENDA:\t{creds[0]}")
    print(f"USERNAME:\t{creds[1]}")
    print(f"PASSWORD:\t{'*' * len(creds[2])}")
    prompt = input("Premere INVIO per confermare. Oppure, immettere Q per reimpostare le credenziali.")
    if prompt in "qQ" and prompt != "":
        return create_credentials()
    
    # Return already existing credentials if unmodified
    return creds[0], creds[1], creds[2]

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

def create_credentials():
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
    return azienda, username, password
