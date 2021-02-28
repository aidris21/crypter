import tkinter as tk
import heapq as hq

time_counter = 3
message_list = [(1,"me", "hi"), (3,"them", "hi"), (2,"me", "you there?")]

class Messaging:
    def __init__(self, master, contact = None):
        self.time_counter = 3
        self.message_list = [(1,"me", "hi"), (3,"them", "hi"), (2,"me", "you there?")]

        self.master = master
        self.width = 50
        self.contact = contact

        self.draw_messagebox()
        self.draw_messages()
        
        self.master.mainloop()

    def draw_messages(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.X)

        hq.heapify(self.message_list)
        temp = []

        self.listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=self.width)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH) 
            
        i = 0
        while len(self.message_list):
            curr_message = hq.heappop(self.message_list)
            self.listbox.insert(tk.END, curr_message[1] + ": " + curr_message[2]) 

            if curr_message[1] == "me":
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

        self.time_counter += 1
        message_data = (self.time_counter, "me", message)
        self.message_list.append(message_data)
     
        self.message_text.set("")

        self.frame.pack_forget()
        self.draw_messages()

    

if __name__ == "__main__":
    root = tk.Tk(className="crypter")
    app = Messaging(root)