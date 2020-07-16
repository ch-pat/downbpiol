import PySimpleGUI as sg


def set_credentials_window() -> (str, str, str, bool):
    sg.theme("LightBlue3")
    layout = [
        [sg.T("Credenziali di accesso non trovate: inserire le credenziali.")],
        [sg.T("Azienda")],
        [sg.In(key="-AZIENDA-")],
        [sg.T("Username")],
        [sg.In(key="-USERNAME-")],
        [sg.T("Password")],
        [sg.In(key="-PASSWORD-", password_char="*")],
        [sg.B("Invia", bind_return_key=True), sg.Checkbox("Memorizza le credenziali", default=False, key="-MEMORIZZA-")]
    ]
    window = sg.Window("Inserisci credenziali di accesso a BPIOL", layout=layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            exit()

        if event == "Invia":
            if any((values["-AZIENDA-"] == "", values["-USERNAME-"] == "", values["-PASSWORD-"] == "")):
                continue
            window.close()
            return values["-AZIENDA-"], values["-USERNAME-"], values["-PASSWORD-"], values["-MEMORIZZA-"]
    window.close()
        