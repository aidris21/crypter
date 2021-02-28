import tkinter as tk

class Messaging:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.width = 50
        
        self.frame.pack(fill=tk.X)
        self.master.mainloop()


    

if __name__ == "__main__":
    root = tk.Tk(className="crypter")
    app = Messaging(root)