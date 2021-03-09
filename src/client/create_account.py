# Create Account Window
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk

from main import Main
from encrypt.rsa import RSA
import query

class createAccount:
    def __init__(self, master):
        self.width = 600
        self.height = 400
        self.master = master
        #self.bottomframe = tk.Frame(self.master)
        #self.bottomframe.grid(row=4)

        self.topframe = tk.Frame(self.master, width = 100, height= 50)
        #self.topframe.pack(side=tk.TOP)
        self.topframe.grid(row = 5, columnspan=3)
        self.toplabel = tk.Label(text="Create an Account", anchor=tk.CENTER)
        self.toplabel.grid(row=0, columnspan=2)

        self.draw_login()
        

        #self.button1 = tk.Button(self.topframe, text = 'Create New Account', width = 25, command = self.new_window)
        #self.button1.grid(row=4, columnspan=3)

        #self.set_dims()

        self.master.mainloop()

    def set_dims(self):
        dim_string = str(self.width) + "x" + str(self.height)
        self.master.geometry(dim_string)

    def draw_login(self):
        self.name_var=tk.StringVar()
        self.username_var=tk.StringVar()
        self.password_var=tk.StringVar()

        self.name_label = tk.Label(text="Enter your display name:")
        self.username_label = tk.Label(text="Choose a Username:")
        self.password_label = tk.Label(text="Choose a Password:")

        self.name_entry = tk.Entry(self.master, textvariable = self.name_var)
        self.username_entry = tk.Entry(self.master, textvariable = self.username_var)
        self.password_entry = tk.Entry(self.master, textvariable = self.password_var)

        self.name_label.grid(row=1, column=0, sticky=tk.E)
        self.username_label.grid(row=2, column=0, sticky=tk.E)
        self.password_label.grid(row=3, column=0, sticky=tk.E)
        self.name_entry.grid(row=1, column = 1)
        self.username_entry.grid(row=2, column = 1)
        self.password_entry.grid(row=3, column = 1)

        submit_btn=tk.Button(self.master,text = 'Create An Account', command = self.submit, width = 15)
        submit_btn.grid(row=4,columnspan=2)

    # Credit to: https://www.geeksforgeeks.org/python-tkinter-entry-widget/
    def submit(self):
        name=self.name_var.get()
        username=self.username_var.get()
        password=self.password_var.get()

        # POST account to server
        new_keys = RSA()
        public_key = new_keys.public_key
        status = query.post_account(name, username, password, public_key)
        print(status)

        # Create conversation and private key folder

        # Save public and private keys
     
        self.master.destroy()
        root = tk.Tk(className="crypter")
        app = Main(root)

        

def main(): 
    root = tk.Tk(className="crypter")
    app = Main(root)

if __name__ == '__main__':
    main()