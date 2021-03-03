# Main GUI File containing main class 
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk
from contacts import Contacts
import query

class Main:
    def __init__(self, master):
        self.width = 600
        self.height = 400
        self.master = master
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
        root = tk.Tk(className="crypter")
        app = Contacts(root, token)

        

def main(): 
    root = tk.Tk(className="crypter")
    app = Main(root)

if __name__ == '__main__':
    main()