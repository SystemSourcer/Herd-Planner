# Imports
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Functions
def main():
    '''
    The main function.
    Starts the GUI and connects it to the backend
    '''
    h = Herd() #
    f = Farm() #
    hpgui = HPGT(h,f) # 

# Opjects
class Cattle: 
    '''
    Object definition for cattle as individum of an herd
    '''
    def __init__(self,name,lom,born,gender):
        self.name = name
        self.lom = lom
        self.gender = gender
        self.born = born
        self.compartemnt = None

class Comparmtent:
    '''
    Object definition for compartment as part of an farm
    '''
    def __init__(self,name,age,gender):
        self.name = name
        self.gender = gender
        self.born = age   

class Herd:
    '''
    Object definition for a herd
    '''
    def __init__(self):
        self.ind_list = []

    def add_ind(self,name,lom,born,gender):
        self.ind_list.append(Cattle(name,lom,born,gender))

class Farm:
    '''
    Object definition for a farm
    '''
    def __init__(self):
        self.comp_list = []

    def add_com(self,name,age,gender):
        self.ind_list.append(Comparmtent(name,age,gender))

class HPGT(): # Herd Planner GUI Tools
    '''
    Docstring für Herd Planner GUI Tools
    '''
    def __init__(self,h,f):
        '''
        Docstring für __init__
        '''
        self.herd = h
        self.farm = f

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

        self.refresh_assignments = {}
        self.herd_window = None
        self.farm_window = None

        ttk.Label(self.window, text='Herde:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_herd).grid(row=0,column=2)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2herd).grid(row=0,column=3)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_ind).grid(row=0,column=4)
        ttk.Button(self.window, text='Entfernen', command=self.rm_from_herd).grid(row=0,column=5)

        ttk.Label(self.window, text='Abteile:', font=('',12,'bold')).grid(row=2,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Button(self.window, text='Hinzufügen', command=self.add_compartment).grid(row=2,column=2)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_compartment).grid(row=2,column=3)
        ttk.Button(self.window, text='Entfernen', command=self.rm_compartment).grid(row=2,column=4)

        self.window.mainloop() 

    def refresh_assignments(self):
        self.unassigned_box = tk.Listbox(self.window, width=100, height=5, exportselection=False)
        self.unassigned_box.grid(row=1,column=1,columnspan=6)
        for n, comp in enumerate(self.farm.comp_list):
            self.refresh_assignments[comp.name] = tk.Listbox(self.window, width=10, height=10, exportselection=False)
            self.refresh_assignments[comp.name].grid(row=3,column=n)


    def load_herd_window(self):
        if self.herd_window is not None and self.herd_window.winfo_exists(): return # no double windows
        self.herd_window = tk.Toplevel()
        self.herd_frame = ttk.Frame(self.herd_window)
        self.herd_frame.pack(fill="both", expand=True)

    def import_herd(self):
        self.load_herd_window()
        self.herd_window.title('Import Herd')
        ttk.Label(self.herd_frame, text='Herde Importieren:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def add2herd(self):
        self.load_herd_window()
        self.herd_window.title('Add Individuum to Herd')
        ttk.Label(self.herd_frame, text='Tier zu Herde hinzufügen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Label(self.herd_frame, text='Name:').grid(row=0,column=2)
        self.entry_name_add = ttk.Entry(self.herd_frame, width=15, justify='center')
        self.entry_name_add.grid(row=0,column=3)
        ttk.Label(self.herd_frame, text='LOM:').grid(row=0,column=4)
        self.entry_lom_add = ttk.Entry(self.herd_frame, width=20, justify='center')
        self.entry_lom_add.grid(row=0,column=5)
        ttk.Label(self.herd_frame, text='Geb:').grid(row=1,column=0)
        self.entry_born_add = ttk.Entry(self.herd_frame, width=10, justify='center')
        self.entry_born_add.grid(row=1,column=1)
        ttk.Label(self.herd_frame, text='Gender:').grid(row=1,column=2)
        self.cbox_gender_add = ttk.Combobox(self.herd_frame, width=10, values=['m','w'], justify='center')
        self.cbox_gender_add.grid(row=1,column=3)      
        ttk.Button(self.herd_frame, text='Hinzufügen', command=self.add_ind).grid(row=1,column=4)

    def update_ind(self):
        self.load_herd_window()
        self.herd_window.title('Update Individuum to Herd')
        ttk.Label(self.herd_frame, text='Tier in Herde aktualisieren:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def rm_from_herd(self):
        self.load_herd_window()
        self.herd_window.title('Remove Individuum to Herd')
        ttk.Label(self.herd_frame, text='Tier aus Herde entfernen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def add_ind(self):
        self.herd.add_ind(self.entry_name_add.get(),self.entry_lom_add.get(),self.entry_born_add(),self.cbox_gender_add.get())
        self.edit_window.destroy()
        self.update_show()

######################################################################################################################################################

    def load_farm_window(self):
        if self.farm_window is not None and self.farm_window.winfo_exists(): return # no double windows
        self.farm_window = tk.Toplevel()
        self.farm_window.title('Add Compartment to Farm')
        self.farm_frame = ttk.Frame(self.farm_window)
        self.farm_frame.pack(fill="both", expand=True)

    def add_compartment(self):
        self.load_farm_window()
        self.farm_window.title('Add Compartment to Farm')
        ttk.Label(self.farm_frame, text='Abteil hinzufügen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def update_compartment(self):
        self.load_farm_window()
        self.farm_window.title('Update Compartment to Farm')
        ttk.Label(self.farm_frame, text='Abteil aktualisieren:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def rm_compartment(self):
        self.load_farm_window()
        self.farm_window.title('Remove Compartment to Farm')
        ttk.Label(self.farm_frame, text='Abteil entfernen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def on_close(self):
        self.window.destroy()







# Global
if __name__ == '__main__': # 
    main() # 

# This is the last line of the Code :)