# Class for contacts page
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk

from messaging import Messaging
import query

class Contacts:
    def __init__(self, master, token):
        self.master = master
        self.next = None
        self.token = token
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

        self.contact_list = self.get_contacts()
        for contact in self.contact_list: 
            self.listbox.insert(tk.END, contact["name"]) 


        # Scroll Bar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 

        self.listbox.config(yscrollcommand = scrollbar.set) 

    def get_contacts(self):
        contact_list = query.get_contacts()

        return contact_list

    def select_contact(self):
        selected = self.listbox.curselection()[0]
        selected_contact = self.contact_list[selected]
        selected_contact_name = selected_contact["name"]

        self.master.destroy()
        self.next = "forward"
        self.window_name = selected_contact_name
        self.contact = selected_contact
        #root = tk.Tk(className=selected_contact_name)
        #app = Messaging(root, self.token, selected_contact)

if __name__ == "__main__":
    pass
    #root = tk.Tk(className="crypter")
    #app = Contacts(root)