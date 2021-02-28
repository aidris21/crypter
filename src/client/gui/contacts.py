# Main GUI File containing main class 
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk
from messaging import Messaging

class Contacts:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.width = 50
        self.list_contacts()


        self.selectButton = tk.Button(text = 'Go To Messages', width = 25, command = self.select_contact)
        self.selectButton.pack(side=tk.BOTTOM)
        self.frame.pack(fill=tk.X)
        self.master.mainloop()


    def list_contacts(self):
        # Contact List
        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=self.width)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH) 

        contact_list = self.get_contacts()
        for name in contact_list: 
            self.listbox.insert(tk.END, name) 


        # Scroll Bar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 

        self.listbox.config(yscrollcommand = scrollbar.set) 

    def get_contacts(self):
        contact_list = range(100)
        return contact_list

    def select_contact(self):
        selected = str(self.listbox.curselection()[0])
        self.master.destroy()
        root = tk.Tk(className=selected)
        app = Messaging(root, selected)

if __name__ == "__main__":
    root = tk.Tk(className="crypter")
    app = Contacts(root)