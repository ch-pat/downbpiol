import PySimpleGUI as sg


def set_credentials_window() -> (str, str, str):
    sg.theme("LightBlue3")
    layout = [
        [sg.T("Credenziali di accesso non trovate: inserire le credenziali.")],
        [sg.T("Azienda")],
        [sg.In(key="-AZIENDA-")],
        [sg.T("Username")],
        [sg.In(key="-USERNAME-")],
        [sg.T("Password")],
        [sg.In(key="-PASSWORD-", password_char="*")],
        [sg.B("Salva")]
    ]
    window = sg.Window("Inserisci credenziali di accesso a BPIOL", layout=layout)
    event, values = window.read()
    window.close()
    if (values["-AZIENDA-"], values["-USERNAME-"], values["-PASSWORD-"]) == (None, None, None) or event == sg.WIN_CLOSED:
        exit()
    return values["-AZIENDA-"], values["-USERNAME-"], values["-PASSWORD-"]