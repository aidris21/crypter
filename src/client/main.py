# Main GUI File containing main class 
# Written by Amir Idris, 2021


import tkinter as tk
import os
import shutil

from login import Main
from contacts import Contacts
from messaging import Messaging


def contact_window(window_name = None, token = None):
    root = tk.Tk(className=window_name)
    app = Contacts(root, token)
    if app.next == "forward":
        message_window(app.window_name, app.token, app.contact)

def message_window(window_name, token, contact):
    root = tk.Tk(className=window_name)
    app = Messaging(root, token, contact)
    if app.next == "backward":
        contact_window(app.window_name, app.token)


def main(): 
    root = tk.Tk(className="crypter")
    app = Main(root)
    if app.next:
        contact_window(app.window_name, app.token)

if __name__ == '__main__':
    main()