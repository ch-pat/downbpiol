import PySimpleGUI as sg


def main_layout(condo_dict: dict) -> list:
    """
    Layout for the main window, needs the condo dict to show all condos
    """
    layout = [
        [sg.Checkbox("Seleziona tutti", default=True, key="-TUTTI-", enable_events=True)],
        [sg.Frame("Seleziona i tracciati da scaricare", layout=[[sg.Col(layout=[[sg.Checkbox("896", default=True, key=("896", x))] + 
                                                                                [sg.Checkbox("CBI", default=True, key=("CBI", x))] + 
                                                                                [sg.T(x, pad=(5, 0))] for x in condo_dict.keys()],
                                                                                scrollable=True, vertical_scroll_only=True, size=(650, 700))]])
        ],
        [sg.ProgressBar(100, orientation="horizontal", style="winnative", key="-BAR-", size=(20, 20)), sg.T("In attesa...", key="-MESSAGE-", size=(40, 2), font="Consolas 12")],
        [sg.Button("Scarica selezionati", key="-SCARICA-")]
    ]
    return layout


def update_bar_message(message: str, counter: int, window: sg.Window):
    """
    Updates progress bar and output message, returns counter +1
    """
    msg = window["-MESSAGE-"]
    bar = window["-BAR-"]
    counter += 1
    bar.update_bar(counter)
    msg.update(message)
    window.refresh()
    return counter

def permute_checkboxes(window: sg.Window, values: dict):
    new_value = values["-TUTTI-"]
    checkboxes = [window[key] for key in values if isinstance(key, tuple) and key[0] in ("896", "CBI")]
    for cb in checkboxes:
        cb.update(new_value)