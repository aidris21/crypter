# Class for message board
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk
from tkinter import font
import heapq as hq
import time
import datetime
#import pytz
import os
import pathlib

import query
from encrypt.rsa import encrypt, decrypt, RSA

class Messaging:
    def __init__(self, master, token, contact = None):
        # Frames
        self.master = master
        self.next = None
        self.sidetop_frame = None
        self.sidebot_frame = None

        # Class attributes
        self.token = token
        self.width = 50
        self.contact = contact
        self.contact_id = self.contact["_id"]
        self.contact_name = self.contact["name"]
        self.contact_key = self.contact["publicKey"]

        # Find conversations folder
        root = os.getcwd()
        for path, subdirs, files in os.walk(root):
            for directory in subdirs:
                if "conversations" in directory:
                    found = os.path.join(path, directory)
        self.conversation_path = found + "/" + self.contact_id + ".txt"

        # Find private_key folder
        root = os.getcwd()
        for path, subdirs, files in os.walk(root):
            for directory in subdirs:
                if "private_key" in directory:
                    found = os.path.join(path, directory)
        self.private_key_path = found + "/" + "key_file.txt"

        self.draw_messagebox()
        self.draw_messages()
        

        self.master.mainloop()

    def Refresher(self, event):
        self.top_frame.grid_forget()
        self.draw_messages()

    def draw_messages(self):
        self.top_frame = tk.Frame(self.master, width=300, height=400)
        #self.top_frame.pack_propagate(False)
        self.top_frame.grid(row=0, column = 0, columnspan = 2)

        self.get_messages() # Update Message File

        self.listbox = tk.Listbox(self.top_frame, selectmode=tk.SINGLE, width=self.width)
        helv14 = font.Font(family="Helvetica",size=14)
        self.listbox.config(font=helv14)
        self.listbox.grid(row=0, column = 0) 
        
        i = 0
        with open(self.conversation_path, 'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    # Split line into parts to get timestamp and sender
                    parts = line.split(",")

                    # Get message text without removing commas within
                    line = line.replace(",", "", 1)
                    message_start = line.index(",") + 1
                    message = line[message_start:]

                    if parts[1] == "You":
                        self.listbox.insert(tk.END, "You: " + message) 
                        self.listbox.itemconfig(i, {'bg':'#c1c1d7'})
                    else:
                        self.listbox.insert(tk.END, self.contact_name + ": " + message) 
                        self.listbox.itemconfig(i, {'bg':'#ffffff'})
                    i += 1

        # Scroll Bar
        scrollbar = tk.Scrollbar(self.top_frame)
        scrollbar.grid(row=0, column = 1) 

        self.listbox.config(yscrollcommand = scrollbar.set) 



    def draw_messagebox(self):
        self.bottom_frame = tk.Frame(self.master, width = 90, height= 80)
        self.bottom_frame.grid(row=1, column = 0, columnspan = 4)

        # Message box
        self.message_text = tk.StringVar()
        self.message_entry = tk.Entry(self.bottom_frame, textvariable = self.message_text, width=self.width)
        self.message_entry.bind("<KeyPress-Return>", self.send_message)
        self.message_entry.grid(row=1, column = 0)

        # Refresh button
        self.refreshButton = tk.Button(self.bottom_frame, text = 'Refresh', width = 5)
        self.refreshButton.bind("<Button-1>", self.Refresher)
        self.refreshButton.grid(row=1, column = 1)

        # Send button
        self.sendButton = tk.Button(self.bottom_frame, text = 'Send', width = 5)
        self.sendButton.bind("<Button-1>", self.send_message)
        self.sendButton.grid(row=1, column = 2)

        # Back Button
        self.backButton = tk.Button(self.bottom_frame, text = 'Back', width = 10)
        self.backButton.bind("<Button-1>", self.back)
        self.backButton.grid(row=1, column = 3)

    def back(self, event=None):
        self.master.destroy()
        self.next = "backward"
        self.window_name = "crypter"

    def send_message(self, event):
        message=self.message_text.get()
        if message != "":
            to = self.contact["_id"]
            #timestamp = datetime.datetime.now(pytz.utc)
            timestamp = int(time.time()*1000) # Unix time in milliseconds
            content = str(timestamp) + "," + "You" + "," + message
            with open(self.conversation_path, 'a') as f:
                f.write(content + "\n")

            encrypted_message = self.draw_encrypt(message)
            status = query.post_message(encrypted_message, self.token, to)
            print(status)

            self.message_text.set("")
            self.top_frame.grid_forget()
            self.draw_messages()

    # Encrypt message, draw relevant info on screen
    def draw_encrypt(self, message):
        if self.sidetop_frame:
            self.clear_encrypt()

        self.sidetop_frame = tk.Frame(self.master, width = 200, height= 400)
        self.sidetop_frame.grid(row=0, column = 2)

        # Original Message
        message_string = "Original Message: " + message + "\n" + "-----------"
        message_label = tk.Label(self.sidetop_frame, text=message_string)
        message_label.grid(row=1, column = 2)

        # Public Key
        pubkey_string = "Contact's public key: " + str(self.contact_key) + "\n" + "-----------"
        pubkey_label = tk.Label(self.sidetop_frame, text=pubkey_string)
        pubkey_label.grid(row=2, column = 2)
        self.master.update()

        # Equation
        equation_string = "Equation: " + "(char^pubkey[1])mod(pubkey[2])" + "\n" + "-----------"
        equation_label = tk.Label(self.sidetop_frame, text=equation_string)
        equation_label.grid(row=3, column = 2)
        self.master.update()

        # Encrypting...
        encrypting_label = tk.Label(self.sidetop_frame, text="Encrypting...")
        encrypting_label.grid(row=4, column = 2)
        self.master.update()

        # Encrypted Message
        encrypted_message = encrypt(message, self.contact_key)

        # Format string
        encrypted_string = list(encrypted_message)
        j = 0
        for i in range(0,len(encrypted_string)):
            if j >= 30 and encrypted_string[i]==",":
                j = 0
                encrypted_string[i] = encrypted_string[i] + "\n"
            j += 1
        encrypted_string = "".join(char for char in encrypted_string)

        encrypted_string = "Encrypted Message: " + encrypted_string
        encrypted_label = tk.Label(self.sidetop_frame, text=encrypted_string)
        encrypted_label.grid(row=5, column = 2)
        self.master.update()

        # Clear button
        self.clearButton = tk.Button(self.sidetop_frame, text = 'Clear', width = 10)
        self.clearButton.bind("<Button-1>", self.clear_encrypt)
        self.clearButton.grid(row=6, column = 2)
        self.master.update()

        return encrypted_message

    # Clear Encryption info
    def clear_encrypt(self, event=None):
        self.sidetop_frame.grid_forget()


    # Need to deal with timezones later
    # Get messages sent after last message stored in conversation
    def get_messages(self):
        
        if not os.path.isfile(self.conversation_path):
            self.create_conversation()
            return
        elif os.stat(self.conversation_path).st_size > 0:
            with open(self.conversation_path, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1].split(",")
                last_timestamp = int(last_line[0])
            
            new_messages = query.get_messages(self.token, self.contact_id, last_timestamp)
        else:
            new_messages = query.get_messages(self.token, self.contact_id)

        f = open(self.conversation_path, "a")
        for i in range(0, len(new_messages)):
            message = new_messages[i]
            if message["from"] == self.contact_id:
                if i == len(new_messages) - 1:
                    content = self.compile_message(message, draw=True)
                else:
                    content = self.compile_message(message)
                f.write(content + "\n")
        f.close()
    
    def create_conversation(self):
        path = self.conversation_path
        f = open(path, "x")

        messages = query.get_messages(self.token, self.contact_id)

        for i in range(0, len(messages)):
            message = messages[i]
            if message["from"] == self.contact_id:
                if i == len(messages) - 1:
                    content = self.compile_message(message, draw=True)
                else:
                    content = self.compile_message(message)
                f.write(content + "\n")
        
        f.close()

    # Decrypt incoming messages and compile content
    def compile_message(self, message, draw = False):
            user_from = message["from"]
            if user_from == self.contact_id:
                user_from = self.contact_name

                # Strip T and Z characters from string
                timestamp = message["createdAt"]
                timestamp = timestamp.replace('T', '')
                timestamp = timestamp.replace('Z', '')
                datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
                unix_time = int(time.mktime(datetime_obj.timetuple()))

                # Decrypt
                if draw:
                    decrypted_message = self.draw_decrypt(message["text"])
                else:
                    decrypted_message = self.decrypt_message(message["text"])

                content = str(unix_time) + "," + str(user_from) + "," + decrypted_message

                return content

    def draw_decrypt(self, message):
        if self.sidebot_frame:
            self.clear_decrypt()

        self.sidebot_frame = tk.Frame(self.master, width = 200, height= 40)
        self.sidebot_frame.grid(row=0, column = 3)

        # Get decryption attributes
        with open(self.private_key_path, 'r') as f:
            lines = f.read().splitlines()
            public_e = int(lines[0].split(":")[1])
            public_n = int(lines[1].split(":")[1])
            public_key = (public_e, public_n)
            private_key = int(lines[2].split(":")[1])

        # Encrypted Message
        # Format string
        encrypted_string = list(message)
        j = 0
        for i in range(0,len(encrypted_string)):
            if j >= 30 and encrypted_string[i]==",":
                j = 0
                encrypted_string[i] = encrypted_string[i] + "\n"
            j += 1
        encrypted_string = "".join(char for char in encrypted_string)

        encrypted_string = "Encrypted Message: " + encrypted_string + "\n" + "-----------"
        encrypted_label = tk.Label(self.sidebot_frame, text=encrypted_string)
        encrypted_label.grid(row=1, column = 3)

        # Public Key
        pubkey_string = "Your public key: " + str(public_key) + "\n" + "-----------"
        pubkey_label = tk.Label(self.sidebot_frame, text=pubkey_string)
        pubkey_label.grid(row=2, column = 3)

        # Private Key
        privkey_string = "Your private key: " + str(private_key) + "\n" + "-----------"
        privkey_label = tk.Label(self.sidebot_frame, text=privkey_string)
        privkey_label.grid(row=3, column = 3)

        # Equation
        equation_string = "(char^privkey)mod(pubkey[2])" + "\n" + "-----------"
        equation_label = tk.Label(self.sidebot_frame, text=equation_string)
        equation_label.grid(row=4, column = 3)

        # Decrypting...
        encrypting_label = tk.Label(self.sidebot_frame, text="Decrypting...")
        encrypting_label.grid(row=5, column = 3)

        # Decrypted Message
        decrypted_message = decrypt(message, private_key, public_key)

        decrypted_string = "Decrypted Message: " + decrypted_message
        decrypted_label = tk.Label(self.sidebot_frame, text=decrypted_string)
        decrypted_label.grid(row=6, column = 3)
        self.master.update()

        # Clear button
        self.clearButton = tk.Button(self.sidebot_frame, text = 'Clear', width = 10)
        self.clearButton.bind("<Button-1>", self.clear_decrypt)
        self.clearButton.grid(row=7, column = 3)
        self.master.update()

        return decrypted_message

    # Clear Decryption info
    def clear_decrypt(self, event=None):
        self.sidebot_frame.grid_forget()

    def decrypt_message(self, message):
        
        with open(self.private_key_path, 'r') as f:
            lines = f.read().splitlines()
            public_e = int(lines[0].split(":")[1])
            public_n = int(lines[1].split(":")[1])
            public_key = (public_e, public_n)
            private_key = int(lines[2].split(":")[1])

        print("Decrypting...")
        decrypted_message = decrypt(message, private_key, public_key)
        print("Encrypted Message: " + message)
        print("Your public key: " + str(public_key))
        print("Your private key: " + str(private_key))
        print("Decrypted Message: " + decrypted_message)

        return decrypted_message


    

if __name__ == "__main__":
    """root = tk.Tk(className="crypter")
    app = Messaging(root)"""

    """timestamp = "2021-03-0302:52:42.216"
    foo = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
    print(foo.date())
    print(foo.time())
    print(time.mktime(foo.timetuple()))
    #print(datetime.datetime.now(pytz.utc))
    print(time.time()*1000)
    print(os.getcwd())"""

    foo = "Hello, Bro"
    foo2 = foo.index(",")
    foo.remove(foo2)
    print(foo2)