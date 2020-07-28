'''
Contains all useful constants for navigating and locating web elements, such as URLs and XPATHS
'''
class Urls():
    LOGIN_PAGE = "https://idp-bpiol.poste.it/jod-idp-bpiol/cas/login.html"
    URL_ESPORTA_MOVIMENTI = "https://bancopostaimpresaonline.poste.it/bpiol1/YCC.do?method=home&FUNCTIONCODESELECTED=YCC"
    URL_CAMBIO_AZIENDA = "https://bancopostaimpresaonline.poste.it/bpiol1/login.do?method=cambioAzienda&MENUNAME=LOGIN%20OPERATORE&PAGENAME=&LNAME=cpw.gif&ALT_TEST=alt.cambio.azienda&FUNCTIONCODESELECTED=XXX"
    URL_ESPORTA_896 = "https://bancopostaimpresaonline.poste.it/bpiol1/loadDeSearch.do?method=loadDeSearchPage&MNAME=mname.cbi.esportadati&PNAME=pname.rendicontazionebollettiniincassati&LNAME=urb.gif&ALT_TEST=alt.esportazioni&FUNCTIONCODESELECTED=XEB"
    URL_PER_PROSEGUIRE = "https://bancopostaimpresaonline.poste.it/bpiol1/login.do?method=openSession&gestisciMessaggiBloccanti=true"

class Xpaths():
    CONTINUA = "/html/body/div[2]/div/div/div/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/p/button"
    TABELLA_CONDOMINI = "/html/body/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/form/div/table"
    CAMBIO_AZIENDA = "/html/body/div[1]/div[2]/div/div/div/div[3]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[3]/p/a[3]"
    FUNZIONI_GENERALI = "/html/body/div[1]/div[2]/div/div/div/div[3]/div/table[2]/tbody/tr/td[8]/a"
    MOVIMENTI_DROP_DOWN_CONTO = '//*[@id="rapporti"]'
    MOVIMENTI_FORM_GIORNO = '//*[@id="dataIniG"]'
    ULTIMO_CBI = "/html/body/table[3]/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/a"
    NOME_ULTIMO_CBI = "/html/body/table[3]/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]"
    FORM_GIORNO_896 = '//*[@id="dataIniG"]'
    ULTIMO_896 = "/html/body/div[1]/table[1]/tbody/tr[3]/td/div/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[2]/a"
    NOME_ULTIMO_896 = "/html/body/div[1]/table[1]/tbody/tr[3]/td/div/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]"
    CONTINUA_ERRORE_GENERICO = "/html/body/div[3]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/p[2]/button"
    AUTENTICAZIONE_FALLITA = "/html/body/div[4]/div[1]/div/div[1]/div/div/div/div/div/form/div[1]/div/div/div/h3"
