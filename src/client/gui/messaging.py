# Class for message board
# Written by Amir Idris, 2021
    # structure credit: https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter as tk
import heapq as hq
import time
import datetime

import query

time_counter = 3
message_list = [(1,"me", "hi"), (3,"them", "hi"), (2,"me", "you there?")]

class Messaging:
    def __init__(self, master, token, contact = None):
        self.master = master
        self.token = token
        self.width = 50
        self.contact = contact

        self.draw_messagebox()
        self.draw_messages()
        
        self.master.mainloop()

    def draw_messages(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.X)
        self.message_list = self.get_messages()

        hq.heapify(self.message_list)
        temp = []

        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=self.width)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH) 
            
        i = 0
        while len(self.message_list):
            curr_message = hq.heappop(self.message_list)
            self.listbox.insert(tk.END, curr_message[1] + ": " + curr_message[2]) 

            if curr_message[1] == "You":
                self.listbox.itemconfig(i, {'bg':'green'})
            else:
                self.listbox.itemconfig(i, {'bg':'blue'})

            i += 1
            hq.heappush(temp, curr_message)

        # Return messages to list
        self.message_list = temp

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

        # Encrypt message

        status = query.post_message(message, self.token, to)

        self.message_text.set("")
        self.frame.pack_forget()
        self.draw_messages()

    # Need to deal with timezones later
    def get_messages(self):
        contact_id = self.contact["_id"]
        contact_name = self.contact["name"]
        messages = query.get_messages(self.token, contact_id)
        message_list = []

        for message in messages:
            user_from = message["from"]
            if user_from == contact_id:
                user_from = contact_name
            else:
                user_from = "You"

            # Strip T and Z characters from string
            timestamp = message["createdAt"]
            timestamp = timestamp.replace('T', '')
            timestamp = timestamp.replace('Z', '')
            datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
            unix_time = time.mktime(datetime_obj.timetuple())

            content = (unix_time, user_from, message["text"])
            message_list.append(content)

        return message_list


    

if __name__ == "__main__":
    """root = tk.Tk(className="crypter")
    app = Messaging(root)"""

    timestamp = "2021-03-0302:52:42.216"
    foo = datetime.datetime.strptime(timestamp, '%Y-%m-%d%H:%M:%S.%f')
    print(foo.date())
    print(foo.time())
    print(time.mktime(foo.timetuple()))