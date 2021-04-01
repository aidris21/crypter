# Main GUI File containing main class 
# Written by Amir Idris, 2021


import tkinter as tk
import os
import shutil

from login import Login
from contacts import Contacts
from messaging import Messaging
from createAccount import createAccount


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

def create_account(): 
    root = tk.Tk(className="Create Account")
    app = createAccount(root)
    if app.next:
        main()


def main(): 
    root = tk.Tk(className="crypter")
    app = Login(root)
    if app.next:
        contact_window(app.window_name, app.token)
    elif app.stay:
        create_account()

if __name__ == '__main__':
    main()