# Imports
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Functions
def main():
    '''
    The main function.
    Starts the GUI and connects it to the backend
    '''
    h = Herd()
    hpgui = HPGT(h) # 






# Opjects
class Cattle: 
    def __init__(self,name,gender,age):
        self.name = name
        self.gender = gender
        self.age = age

class Herd:
    def __init__(self):
        self.ind_list = []

    def add_ind(self,name,gender,age):
        self.ind_list.append(Cattle(name,gender,age))

class HPGT(): # Herd Planner GUI Tools
    '''
    Docstring für Herd Planner GUI Tools
    '''
    def __init__(self,h):
        '''
        Docstring für __init__
        '''
        self.herd = h

        self.window = tk.Tk()
        self.window.title('Herd Planner')
        self.window.geometry('678x345') # Width x Height
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Herde', menu=self.filemenu)
        self.filemenu.add_command(label='Herde importieren', command=self.import_herd)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Beenden', command=self.on_close)
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='About')

        self.show_window = None
        self.edit_window = None

    
        ttk.Label(self.window, text='Herde:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_herd).grid(row=0,column=2)
        ttk.Button(self.window, text='Bearbeiten', command=self.import_herd).grid(row=0,column=3)
      
        
        ttk.Label(self.window, text='Management:', font=('',12,'bold')).grid(row=2,column=0,columnspan=2, sticky='w', pady=25)
        listbox = tk.Listbox(self.window, width=30, height=15, exportselection=False)
        listbox.grid(row=3,column=1)


        self.window.mainloop() 

    def import_herd(self):
        pass

    def on_close(self):
        self.window.destroy()







# Global
if __name__ == '__main__': # 
    main() # 

# This is the last line of the Code :)