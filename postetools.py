def extract_links_from_tabella_condomini(tabella_condomini):
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