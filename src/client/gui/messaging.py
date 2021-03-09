# Class for message board
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk
import heapq as hq
import time
import datetime
import pytz
import os
import pathlib

import query

class Messaging:
    def __init__(self, master, token, contact = None):
        self.master = master
        self.token = token
        self.width = 50
        self.contact = contact
        self.contact_id = self.contact["_id"]
        self.contact_name = self.contact["name"]

        # Find conversations folder
        root = os.getcwd()
        for path, subdirs, files in os.walk(root):
            for directory in subdirs:
                if "conversations" in directory:
                    found = os.path.join(path, directory)
        self.conversation_path = found + "/" + self.contact_id + ".txt"

        self.draw_messagebox()
        self.draw_messages()
        
        self.Refresher()
        self.master.mainloop()

    def Refresher(self):
        self.frame.pack_forget()
        self.draw_messages()
        self.master.after(10000, self.Refresher)

    def draw_messages(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.X)
        self.get_messages() # Update Message File

        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=self.width)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH) 
        
        i = 0
        with open(self.conversation_path, 'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    line = line.split(",")
                    if line[1] == "You":
                        self.listbox.insert(tk.END, "You: " + line[2]) 
                        self.listbox.itemconfig(i, {'bg':'green'})
                    else:
                        self.listbox.insert(tk.END, self.contact_name + ": " + line[2]) 
                        self.listbox.itemconfig(i, {'bg':'blue'})
                    i += 1

        # Scroll Bar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 

        self.listbox.config(yscrollcommand = scrollbar.set) 



    def draw_messagebox(self):
        # Message box
        self.message_text = tk.StringVar()
        self.message_entry = tk.Entry(self.master, textvariable = self.message_text, width=self.width)
        self.message_entry.pack(side=tk.BOTTOM)

        # Send button
        self.selectButton = tk.Button(text = 'Send', width = 20, command = self.send_message)
        self.selectButton.pack(side=tk.RIGHT)

    def send_message(self):
        message=self.message_text.get()
        to = self.contact["_id"]
        #timestamp = datetime.datetime.now(pytz.utc)
        timestamp = int(time.time()*1000) # Unix time in milliseconds
        content = str(timestamp) + "," + "You" + "," + message
        with open(self.conversation_path, 'a') as f:
            f.write(content + "\n")

        # Encrypt message

        status = query.post_message(message, self.token, to)

        self.message_text.set("")
        self.frame.pack_forget()
        self.draw_messages()

    # Need to deal with timezones later
    # Get messages sent after last message stored in conversation
    def get_messages(self):
        
        if not os.path.isfile(self.conversation_path):
            self.create_conversation()
        elif os.stat(self.conversation_path).st_size > 0:
            with open(self.conversation_path, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1].split(",")
                last_timestamp = int(last_line[0])
            
            new_messages = query.get_messages(self.token, self.contact_id, last_timestamp)

            f = open(self.conversation_path, "a")
            for message in new_messages:
                if message["from"] == self.contact_id:
                    content = self.compile_message(message)
                    f.write(content + "\n")
            f.close()
        else:
            new_messages = query.get_messages(self.token, self.contact_id)

            f = open(self.conversation_path, "a")
            for message in new_messages:
                if message["from"] == self.contact_id:
                    content = self.compile_message(message)
                    f.write(content + "\n")
            f.close()

    
    def create_conversation(self):
        path = self.conversation_path
        f = open(path, "x")

        messages = query.get_messages(self.token, self.contact_id)

        for message in messages:
            if message["from"] == self.contact_id:
                content = self.compile_message(message)
                f.write(content + "\n")
        
        f.close()

    def compile_message(self, message):
            user_from = message["from"]
            if user_from == self.contact_id:
                user_from = self.contact_name

                # Strip T and Z characters from string
                timestamp = message["createdAt"]
                timestamp = timestamp.replace('T', '')
                timestamp = timestamp.replace('Z', '')
                datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
                unix_time = time.mktime(datetime_obj.timetuple())

                content = str(timestamp) + "," + str(user_from) + "," + message["text"]

                return content


    

if __name__ == "__main__":
    """root = tk.Tk(className="crypter")
    app = Messaging(root)"""

    timestamp = "2021-03-0302:52:42.216"
    foo = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
    print(foo.date())
    print(foo.time())
    print(time.mktime(foo.timetuple()))
    print(datetime.datetime.now(pytz.utc))
    print(time.time()*1000)