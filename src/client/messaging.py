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
from encrypt.rsa import encrypt, decrypt, RSA

class Messaging:
    def __init__(self, master, token, contact = None):
        # Frames
        self.master = master
        self.side_frame = None

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
        self.private_key_path = found + "/" + "key.txt"

        self.draw_messagebox()
        self.draw_messages()
        
        self.Refresher()
        self.master.mainloop()

    def Refresher(self):
        self.top_frame.pack_forget()
        self.draw_messages()
        self.master.after(10000, self.Refresher)

    def draw_messages(self):
        self.top_frame = tk.Frame(self.master, width=300, height=400)
        #self.top_frame.pack_propagate(False)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.get_messages() # Update Message File

        self.listbox = tk.Listbox(self.top_frame, selectmode=tk.SINGLE, width=self.width)
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
        scrollbar = tk.Scrollbar(self.top_frame)
        scrollbar.pack(side = tk.LEFT, fill = tk.BOTH) 

        self.listbox.config(yscrollcommand = scrollbar.set) 



    def draw_messagebox(self):
        self.bottom_frame = tk.Frame(self.master, width = 70, height= 40)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Message box
        self.message_text = tk.StringVar()
        self.message_entry = tk.Entry(self.bottom_frame, textvariable = self.message_text, width=self.width)
        self.message_entry.bind("<KeyPress-Return>", self.send_message)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH)

        # Send button
        self.selectButton = tk.Button(self.bottom_frame, text = 'Send', width = 10)
        self.selectButton.bind("<Button-1>", self.send_message)
        self.selectButton.pack(side=tk.LEFT)

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
            self.top_frame.pack_forget()
            self.draw_messages()

    # Encrypt message, draw relevant info on screen
    def draw_encrypt(self, message):
        if self.side_frame:
            self.side_frame.pack_forget()

        self.side_frame = tk.Frame(self.master, width = 200, height= 40)
        self.side_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Original Message
        message_string = "Original Message: " + message + "\n" + "-----------"
        message_label = tk.Label(self.side_frame, text=message_string)
        message_label.pack(side=tk.TOP)

        # Public Key
        pubkey_string = "Contact's public key: " + str(self.contact_key) + "\n" + "-----------"
        pubkey_label = tk.Label(self.side_frame, text=pubkey_string)
        pubkey_label.pack(side=tk.TOP)

        # Equation
        equation_string = "(char^pubkey[1])mod(pubkey^2)" + "\n" + "-----------"
        equation_label = tk.Label(self.side_frame, text=equation_string)
        equation_label.pack(side=tk.TOP)

        # Encrypting...
        encrypting_label = tk.Label(self.side_frame, text="Encrypting...")
        encrypting_label.pack(side=tk.TOP)

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
        encrypted_label = tk.Label(self.side_frame, text=encrypted_string)
        encrypted_label.pack(side=tk.TOP)
        self.master.update()

        # Clear button
        self.clearButton = tk.Button(self.side_frame, text = 'Clear', width = 10)
        self.clearButton.bind("<Button-1>", self.clear)
        self.clearButton.pack(side=tk.TOP)
        self.master.update()

        return encrypted_message

    # Clear Encryption info
    def clear(self, event):
        self.side_frame.pack_forget()


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

    # Decrypt incoming messages and compile content
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

                # Decrypt
                decrypted_message = self.decrypt_message(message["text"])

                content = str(timestamp) + "," + str(user_from) + "," + decrypted_message

                return content

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

    timestamp = "2021-03-0302:52:42.216"
    foo = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
    print(foo.date())
    print(foo.time())
    print(time.mktime(foo.timetuple()))
    print(datetime.datetime.now(pytz.utc))
    print(time.time()*1000)
    print(os.getcwd())