# Login and Create Account File containing main class 
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk
import os
import shutil

from contacts import Contacts
import query
from encrypt.rsa import RSA

class Login:
    def __init__(self, master):
        self.width = 600
        self.height = 400
        self.master = master
        self.next = False
        #self.bottomframe = tk.Frame(self.master)
        #self.bottomframe.grid(row=4)

        self.topframe = tk.Frame(self.master, width = 100, height= 50)
        #self.topframe.pack(side=tk.TOP)
        self.topframe.grid(row = 5, columnspan=3)
        self.toplabel = tk.Label(text="Welcome", anchor=tk.CENTER)
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
        self.password_var=tk.StringVar()

        self.username_label = tk.Label(text="Username:")
        self.password_label = tk.Label(text="Password:")
        self.username_entry = tk.Entry(self.master, textvariable = self.name_var)
        self.password_entry = tk.Entry(self.master, textvariable = self.password_var)
        self.username_label.grid(row=1, column=0, sticky=tk.E)
        self.password_label.grid(row=2, column=0, sticky=tk.E)
        self.username_entry.grid(row=1, column = 1)
        self.password_entry.grid(row=2, column = 1)

        submit_btn=tk.Button(self.master,text = 'Submit', command = self.submit)
        submit_btn.grid(row=3,columnspan=2)
        create_account_btn=tk.Button(self.master,text = 'Create New Account', command = self.create_account)
        create_account_btn.grid(row=4,columnspan=2)

    # Credit to: https://www.geeksforgeeks.org/python-tkinter-entry-widget/
    def submit(self):
        name=self.name_var.get()
        password=self.password_var.get()

        self.login(name, password)
     
        self.name_var.set("")
        self.password_var.set("")


    def login(self, username, password):
        token = query.login(username, password)

        self.master.destroy()
        #root = tk.Tk(className="crypter")
        #app = Contacts(root, token)
        self.next = True
        self.window_name = "crypter"
        self.token = token

    
    def create_account(self):
        self.master.destroy()
        root = tk.Tk(className="Create Account")
        app = createAccount(root)

# Create and Account
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
        
        if status.status_code == 400 and status.json()["reason"] == "User name is taken":
            self.account_taken()
            return

        # Find client folder and change to that directory
        root = os.getcwd()
        for path, subdirs, files in os.walk(root):
            for directory in subdirs:
                if "client" in directory:
                    found = os.path.join(path, directory)
                    found += "/"
                    os.chdir(found)

        # Create conversation and private key folder
        conversation_path = './conversations'
        private_key_path = './private_key'
        if os.path.exists(conversation_path):
            shutil.rmtree(conversation_path)
        if os.path.exists(private_key_path):
            shutil.rmtree(private_key_path)
        os.makedirs(conversation_path)
        os.makedirs(private_key_path)

        # Save public and private keys
        key_file_path = private_key_path + "/key_file.txt"
        with open(key_file_path, 'x') as f:
            f.write("public e:" + str(public_key[0]) + "\n") # public e
            f.write("public n:" + str(public_key[1]) + "\n") # public n
            f.write("private key:" + str(int(new_keys.private_key)) + "\n") # private key
            f.write("prime 1:" + str(new_keys.prime1) + "\n") # first prime number
            f.write("prime 2:" + str(new_keys.prime2) + "\n") # second prime number
            f.write("phi:" + str(new_keys.phi) + "\n") # Phi
     
        # Return to login screen
        self.master.destroy()
        root = tk.Tk(className="crypter")
        app = Main(root)

    def account_taken(self):
        warning_label = tk.Label(text="That username is already taken!", anchor=tk.CENTER)
        warning_label.grid(row=5, columnspan=2)

        self.name_var.set("")
        self.username_var.set("")
        self.password_var.set("")

        

def main(): 
    root = tk.Tk(className="crypter")
    app = Main(root)

if __name__ == '__main__':
    main()