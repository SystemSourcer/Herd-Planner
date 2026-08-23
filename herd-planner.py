# Imports
import pandas as pd # 
import tkinter as tk #
from tkinter import ttk, filedialog, simpledialog, messagebox #
from pathlib import Path #

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
        self.name = name #
        self.lom = lom #
        self.gender = gender #
        self.born = born #
        self.compartment = None #

class Comparmtent:
    '''
    Object definition for compartment as part of an farm
    '''
    def __init__(self,name,count,age_min,age_max,gender):
        self.name = name #
        self.count = count #
        self.gender = gender #
        self.age_min = age_min #
        self.age_max = age_max #

class Herd:
    '''
    Object definition for a herd
    '''
    def __init__(self):
        self.cols = {'NAME','LOM_X','LOM_A','GEB_DATR','GESCHL_R','RASSE','LOM_MUTX','DAT_EIN','TIER_EINX','BNR15_VBX','BNR15_NBX','LAND_URX','GVE','LKALBDAT','KALBUNGANZ','ZKZ_DURCHT','COMPARTMENT'}
        self.df = None
        self.ind_list = []

    def add_ind(self,name,lom,born,gender):
        if self.df is None: self.df = pd.DataFrame(columns=self.cols)
        # append to df......
        self.ind_list.append(Cattle(name,lom,born,gender))

    def import_csv(self,csv_path):
        self.csv_path = Path(csv_path) # 
        self.df = pd.read_csv(self.csv_path, sep=';') # read csv file 
        self.df = self.df.fillna('') # Leere Felder mit leerem String füllen
        if 'NAME' not in self.df.columns: self.df.insert(loc = 0, column = 'NAME', value = '')
        if 'COMPARTMENT' not in self.df.columns: self.df['COMPARTMENT'] = ''
        
        for col in self.df:
            if col not in self.cols: del self.df[col]

        self.df.loc[self.df["NAME"].eq(""), "NAME"] = self.df.loc[self.df["NAME"].eq(""), "LOM_X"]

        print(self.df) 

        for row in self.df.itertuples(index=False):
            self.add_ind(row.NAME,row.LOM_X,row.GEB_DATR,row.GESCHL_R)

        
        print(f'\033[36mDatenbank {self.csv_path} geöffnet und geladen.\033[0m')
        self.save_csv()
        
    def save_csv(self):
        self.df.to_csv(self.csv_path,sep=';',index=False)
        print(f'\033[32mDataFrame erfolgreich in {self.csv_path} gespeichert\033[0m')


class Farm:
    '''
    Object definition for a farm
    '''
    def __init__(self):
        self.comp_list = []

    def add_comp(self,name,count,age_min,age_max,gender):
        self.comp_list.append(Comparmtent(name,count,age_min,age_max,gender))

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

        self.assignments = {}
        self.herd_window = None
        self.farm_window = None

        ttk.Label(self.window, text='Herde:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_herd).grid(row=0,column=2)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2herd).grid(row=0,column=3)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_ind).grid(row=0,column=4)
        ttk.Button(self.window, text='Entfernen', command=self.rm_from_herd).grid(row=0,column=5)

        ttk.Label(self.window, text='Abteile:', font=('',12,'bold')).grid(row=2,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2farm).grid(row=2,column=2)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_compartment).grid(row=2,column=3)
        ttk.Button(self.window, text='Entfernen', command=self.rm_compartment).grid(row=2,column=4)

        self.refresh_assignments()

        self.window.mainloop() 

######################################################################################################################################################

    def refresh_assignments(self):
        for widget in self.window.winfo_children():
            grid_info = widget.grid_info()
            if grid_info and int(grid_info["row"]) not in {0,2}: widget.destroy()
    
        self.unassigned_box = tk.Listbox(self.window, width=100, height=5, exportselection=False, selectmode='multiple')
        self.unassigned_box.grid(row=1,column=0,columnspan=6)
        for n, comp in enumerate(self.farm.comp_list):
            ttk.Button(self.window, text=comp.name, command=lambda comp_name=comp.name: self.re_assign(comp_name)).grid(row=3,column=n) #funktioinert nicht weil comp.name sich änder im loop. alle button dann für letzte
            self.assignments[comp.name] = tk.Listbox(self.window, width=15, height=15, exportselection=False, selectmode='multiple')
            self.assignments[comp.name].grid(row=4,column=n)

        for ind in self.herd.ind_list:
            if ind.compartment is None: self.unassigned_box.insert(0,ind.name)
            else: self.assignments[ind.compartment].insert(0,ind.name)

    def re_assign(self,comp):
        re_assign_list = []
        for i in self.unassigned_box.curselection():
            re_assign_list.append(self.unassigned_box.get(i))

        for value in self.assignments.values():
            print(value)
            for i in value.curselection():
                re_assign_list.append(value.get(i))

        for ind_name in re_assign_list:
            for ind in self.herd.ind_list:
                if ind.name == ind_name: 
                    if ind.compartment == comp: ind.compartment = None
                    else: ind.compartment = comp
             
        self.refresh_assignments()
        
######################################################################################################################################################

    def import_herd(self):
        csv_path = Path(filedialog.askopenfilename(title='CSV-Datei zum import auswählen', filetypes=[('CSV files', '*.csv')])) # CSV - File über GUI abfragen
        if not Path(csv_path).is_file(): return # in case of closing filedialog or selecting a directory
        self.herd.import_csv(csv_path)
        self.refresh_assignments()

    def load_herd_window(self):
        if self.herd_window is not None and self.herd_window.winfo_exists(): return # no double windows
        self.herd_window = tk.Toplevel()
        self.herd_frame = ttk.Frame(self.herd_window)
        self.herd_frame.pack(fill="both", expand=True)

    def add2herd(self):
        self.load_herd_window()
        self.herd_window.title('Add Individuum to Herd')
        ttk.Label(self.herd_frame, text='Tier zu Herde hinzufügen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        ttk.Label(self.herd_frame, text='Name:').grid(row=0,column=2)
        self.ind_name_add = ttk.Entry(self.herd_frame, width=15, justify='center')
        self.ind_name_add.grid(row=0,column=3)
        ttk.Label(self.herd_frame, text='LOM:').grid(row=0,column=4)
        self.ind_lom_add = ttk.Entry(self.herd_frame, width=20, justify='center')
        self.ind_lom_add.grid(row=0,column=5)
        ttk.Label(self.herd_frame, text='Geb:').grid(row=1,column=0)
        self.ind_born_add = ttk.Entry(self.herd_frame, width=10, justify='center')
        self.ind_born_add.grid(row=1,column=1)
        ttk.Label(self.herd_frame, text='Gender:').grid(row=1,column=2)
        self.ind_gender_add = ttk.Combobox(self.herd_frame, width=10, values=['M','W'], justify='center')
        self.ind_gender_add.grid(row=1,column=3)      
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
        self.herd.add_ind(self.ind_name_add.get(),self.ind_lom_add.get(),self.ind_born_add.get(),self.ind_gender_add.get())
        self.herd_window.destroy()
        self.refresh_assignments()

######################################################################################################################################################

    def load_farm_window(self):
        if self.farm_window is not None and self.farm_window.winfo_exists(): return # no double windows
        self.farm_window = tk.Toplevel()
        self.farm_window.title('Add Compartment to Farm')
        self.farm_frame = ttk.Frame(self.farm_window)
        self.farm_frame.pack(fill="both", expand=True)

    def add2farm(self):
        self.load_farm_window()
        self.farm_window.title('Add Compartment to Farm')
        ttk.Label(self.farm_frame, text='Abteil hinzufügen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)
        ttk.Label(self.farm_frame, text='Name:').grid(row=0,column=2)
        self.comp_name_add = ttk.Entry(self.farm_frame, width=15, justify='center')
        self.comp_name_add.grid(row=0,column=3)
        ttk.Label(self.farm_frame, text='Anzahl (max):').grid(row=0,column=4)
        self.comp_count_add = ttk.Entry(self.farm_frame, width=20, justify='center')
        self.comp_count_add.grid(row=0,column=5)
        ttk.Label(self.farm_frame, text='Alter (min)').grid(row=1,column=0)
        self.comp_agemin_add = ttk.Entry(self.farm_frame, width=10, justify='center')
        self.comp_agemin_add.grid(row=1,column=1)
        ttk.Label(self.farm_frame, text='Alter (max)').grid(row=1,column=2)
        self.comp_agemax_add = ttk.Entry(self.farm_frame, width=10, justify='center')
        self.comp_agemax_add.grid(row=1,column=3)
        ttk.Label(self.farm_frame, text='Gender:').grid(row=1,column=4)
        self.comp_gender_add = ttk.Combobox(self.farm_frame, width=10, values=['X','M','W'], justify='center')
        self.comp_gender_add.grid(row=1,column=5)      
        self.comp_gender_add.set('X')
        ttk.Button(self.farm_frame, text='Hinzufügen', command=self.add_comp).grid(row=2,column=5)

    def update_compartment(self):
        self.load_farm_window()
        self.farm_window.title('Update Compartment to Farm')
        ttk.Label(self.farm_frame, text='Abteil aktualisieren:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def rm_compartment(self):
        self.load_farm_window()
        self.farm_window.title('Remove Compartment to Farm')
        ttk.Label(self.farm_frame, text='Abteil entfernen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)

    def add_comp(self):
        self.farm.add_comp(self.comp_name_add.get(),self.comp_count_add.get(),self.comp_agemin_add.get(),self.comp_agemax_add.get(),self.comp_gender_add.get())
        self.farm_window.destroy()
        self.refresh_assignments()

######################################################################################################################################################

    def on_close(self):
        self.window.destroy()





# Global
if __name__ == '__main__': # 
    main() # 

# This is the last line of the Code :)