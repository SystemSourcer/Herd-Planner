# Imports
import random
import pandas as pd # 
import tkinter as tk #
from tkinter import ttk, filedialog, simpledialog, messagebox #
from pathlib import Path #

# Functions
def main():
    '''
    The main function.
    Starts the GUI and connects it to the backend.
    '''
    h = Herd() #
    f = Farm() #
    hpgui = HPGT(h,f) # 

# Opjects
class Herd:
    '''
    Object definition for a herd.
    A herd 
    '''
    def __init__(self): 
        self.cols =['NAME','LOM_X','LOM_A','GEB_DATR','GESCHL_R','RASSE','LOM_MUTX','DAT_EIN','TIER_EINX','BNR15_VBX','BNR15_NBX','LAND_URX','GVE','LKALBDAT','KALBUNGANZ','ZKZ_DURCHT','COMPARTMENT']
        self.df = pd.DataFrame(columns=self.cols)
        print(f'\033[36mHerd: \n{self.df} \033[0m')

    def add_ind(self,value_list): 
        """
        Function that is called when a ind is added manual by user
        """
        self.df.loc[len(self.df)] = value_list
        print(f'\033[32mIndividual {value_list} added to herd.\033[0m')
        print(f'\033[36mHerd: \n{self.df} \033[0m')

    def del_ind(self,name):
        self.df = self.df[self.df['NAME'] != name].reset_index(drop=True)
        print(f'\033[32mIndividual {name} removed from herd.\033[0m')
        print(f'\033[36mHerd: \n{self.df} \033[0m')
    
    def import_csv(self,import_csv_path):
        """
        Function that is called when inds is added by csv import
        """
        import_csv_path = Path(import_csv_path) # Ensure that the path is a path object
        import_df = pd.read_csv(import_csv_path, sep=';') # read csv file 
        import_df = import_df.fillna('') # Leere Felder mit leerem String füllen
        if 'NAME' not in import_df.columns: 
            import_df.insert(loc = 0, column = 'NAME', value = '') # Add Name col
            self.df.loc[self.df["NAME"].eq(""), "NAME"] = self.df.loc[self.df["NAME"].eq(""), "LOM_X"] # copy Lom col in name col
        
        if 'COMPARTMENT' not in import_df.columns: import_df['COMPARTMENT'] = '' # Add name col
        
        for col in import_df:
            if col not in self.cols: del import_df[col] # del not needed / wanted cols

        print("Import-Data: \n", import_df) 

        self.df = (pd.concat([self.df, import_df], ignore_index=True).drop_duplicates(subset='NAME')) # NAME is the identifyer. all comus would leed to problems e.g. Compartment...

        print(f'\033[32mDatabase {import_csv_path} opend and imported.\033[0m')
        print(f'\033[36mHerd: \n{self.df} \033[0m')

    def export_csv(self, export_csv_path):
        self.df.to_csv(export_csv_path,sep=';',index=False)
        print(f'\033[32mDataFrame successfully saved in {export_csv_path}.\033[0m')

class Farm:
    '''
    Object definition for a farm
    '''
    def __init__(self):
        self.cols = ['NAME','COUNT','AGE_Min','AGE_MAX','GENDER']
        self.df = pd.DataFrame(columns= self.cols)
        print(f'\033[33mFarm: \n{self.df} \033[0m')

    def add_comp(self,value_list):
        self.df.loc[len(self.df)] = value_list
        print(f'\033[32mCompartment {value_list} added to farm.\033[0m')
        print(f'\033[33mFarm: \n{self.df} \033[0m')

    def del_comp(self,name):
        self.df = self.df[self.df['NAME'] != name].reset_index(drop=True)
        print(f'\033[32mCompartment {name} removed from farm.\033[0m')
        print(f'\033[36mFarm: \n{self.df} \033[0m')

    def import_csv(self,import_csv_path):
        """
        Function that is called when comps are added by csv import
        """
        import_csv_path = Path(import_csv_path) # Ensure that the path is a path object
        import_df = pd.read_csv(import_csv_path, sep=';') # read csv file 
        import_df = import_df.fillna('') # Leere Felder mit leerem String füllen
        if 'NAME' not in import_df.columns: 
            import_df.insert(loc = 0, column = 'NAME', value = '') # Add Name col
            self.df.loc[self.df["NAME"].eq(""), "NAME"] = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=12)) # set random name
        
        for col in import_df:
            if col not in self.cols: del import_df[col] # del not needed / wanted cols

        print("Import-Data: \n", import_df) 

        self.df = (pd.concat([self.df, import_df], ignore_index=True).drop_duplicates(subset='NAME')) # BNAME is the identifyer. all comus would leed to problems e.g. Compartment...

        print(f'\033[32mDatabase {import_csv_path} opend and imported.\033[0m')
        print(f'\033[36mFarm: \n{self.df} \033[0m')

    def export_csv(self, export_csv_path):
        self.df.to_csv(export_csv_path,sep=';',index=False)
        print(f'\033[32mDataFrame erfolgreich in {export_csv_path} gespeichert\033[0m')

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
        self.window.geometry('987x654') # Width x Height
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Menu', menu=self.filemenu)
        self.filemenu.add_command(label='Aufteilung Prüfen', command=self.check)
        self.filemenu.add_command(label='Aufteilung Vorschlagen', command=self.suggest)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Beenden', command=self.on_close)
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='About')

        self.assignments = dict()
        self.herd_window = None
        self.farm_window = None

        # Farm
        ttk.Label(self.window, text='Manage Farm:', font=('',12,'bold')).grid(row=0,column=0, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_farm).grid(row=0,column=1)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2farm).grid(row=0,column=2)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_farm).grid(row=0,column=3)
        ttk.Button(self.window, text='Entfernen', command=self.rm_from_farm).grid(row=0,column=4)
        ttk.Button(self.window, text='Export', command=self.export_farm).grid(row=0,column=5)
        
        # Herd
        ttk.Label(self.window, text='Manage Herd:', font=('',12,'bold')).grid(row=2,column=0, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_herd).grid(row=2,column=1)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2herd).grid(row=2,column=2)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_herd).grid(row=2,column=3)
        ttk.Button(self.window, text='Entfernen', command=self.rm_from_herd).grid(row=2,column=4)
        ttk.Button(self.window, text='Export', command=self.export_herd).grid(row=2,column=5)

        self.refresh_assignments()

        self.window.mainloop() 

######################################################################################################################################################

    def refresh_assignments(self):
        for widget in self.window.winfo_children():
            grid_info = widget.grid_info()
            if grid_info and int(grid_info["row"]) not in {0,2}: widget.destroy()
    
        self.unassigned_box = tk.Listbox(self.window, width=20, height=25, exportselection=False, selectmode='multiple')
        self.unassigned_box.grid(row=4,column=0)
        for comp in self.farm.df.itertuples(index=True):
            ttk.Button(self.window, text=comp.NAME, command=lambda comp_name=comp.NAME: self.re_assign(comp_name)).grid(row=3,column=comp.Index+1)
            self.assignments[comp.NAME] = tk.Listbox(self.window, width=20, height=25, exportselection=False, selectmode='multiple')
            self.assignments[comp.NAME].grid(row=4,column=comp.Index+1)

        for ind in self.herd.df.itertuples(index=True):
            if ind.COMPARTMENT == '' : self.unassigned_box.insert(0,ind.NAME)
            else: self.assignments[ind.COMPARTMENT].insert(0,ind.NAME)

    def re_assign(self,comp):
        re_assign_list = []
        for i in self.unassigned_box.curselection():
            re_assign_list.append(self.unassigned_box.get(i))

        for value in self.assignments.values():
            print(value)
            for i in value.curselection():
                re_assign_list.append(value.get(i))

        for ind_name in re_assign_list:
            for ind in self.herd.df.itertuples(index=True):
                if ind.NAME == ind_name: 
                    if ind.COMPARTMENT == comp: self.herd.df.at[ind.Index, "COMPARTMENT"] = ''
                    else: self.herd.df.at[ind.Index, "COMPARTMENT"] = comp
             
        self.refresh_assignments()
        
######################################################################################################################################################

    def import_herd(self):
        csv_path = Path(filedialog.askopenfilename(title='CSV-Datei zum import der Herde auswählen', filetypes=[('CSV files', '*.csv')])) # CSV - File über GUI abfragen
        if not Path(csv_path).is_file(): return # in case of closing filedialog or selecting a directory | not shure if this works
        self.herd.import_csv(csv_path)
        self.refresh_assignments()

    def export_herd(self):
        csv_path = Path(filedialog.asksaveasfilename(title='Herde als CSV-Datei speichern', filetypes=[('CSV files', '*.csv')])) # CSV - File über GUI abfragen
        if csv_path == '' : return # in case of closing filedialog | not shure if this works
        self.herd.export_csv(csv_path)

    def load_herd_window(self):
        if self.herd_window is not None and self.herd_window.winfo_exists(): return # no double windows
        self.herd_window = tk.Toplevel()
        self.herd_frame = ttk.Frame(self.herd_window)
        self.herd_frame.pack(fill="both", expand=True)

    def add2herd(self):
        self.load_herd_window()
        self.herd_window.title('Add Individuum to Herd')
        ttk.Label(self.herd_frame, text='Tier zu Herde hinzufügen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)

        for i, col in enumerate(self.herd.cols):
            n_c = 6 # number of cols
            r = i // n_c + 1
            c = (i - i // n_c * n_c) * 2
            ttk.Label(self.herd_frame, text=col).grid(row=r,column=c)
            setattr(self,col,ttk.Entry(self.herd_frame, width=15, justify='center'))
            entry_field = getattr(self, col)
            entry_field.grid(row=r,column=c+1)
   
        ttk.Button(self.herd_frame, text='Hinzufügen', command=self.add_ind).grid(row=r+1,column=n_c*2-1)

    def update_herd(self):
        self.load_herd_window()
        self.herd_window.title('Update Individuum of Herd')
        ttk.Label(self.herd_frame, text='Tier in Herde aktualisieren:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        self.cbox_get_ind = ttk.Combobox(self.herd_frame, width=20, values=sorted(self.herd.df['NAME'].unique()))
        self.cbox_get_ind.grid(row=0,column=2)
        ttk.Button(self.herd_frame, text='Holen', command=self.get_ind).grid(row=0,column=3)

    def get_ind(self):
        ind = self.herd.df[self.herd.df['NAME']==self.cbox_get_ind.get()].iloc[0].to_dict()
        for i, (key, value) in enumerate(ind.items()):
            n_c = 6 # number of cols
            r = i // n_c + 1
            c = (i - i // n_c * n_c) * 2
            ttk.Label(self.herd_frame, text=key).grid(row=r,column=c)
            setattr(self,key,ttk.Entry(self.herd_frame, width=15, justify='center'))
            entry_field = getattr(self, key)
            entry_field.grid(row=r,column=c+1)
            entry_field.insert(0,value)

        ttk.Button(self.herd_frame, text='Aktualisieren', command=self.del_add_ind).grid(row=r+1,column=n_c*2-1)

    def rm_from_herd(self):
        self.load_herd_window()
        self.herd_window.title('Remove Individuum from Herd')
        ttk.Label(self.herd_frame, text='Tier aus Herde entfernen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)
        self.cbox_get_ind = ttk.Combobox(self.herd_frame, width=20, values=sorted(self.herd.df['NAME'].unique()))
        self.cbox_get_ind.grid(row=0,column=2)
        ttk.Button(self.herd_frame, text='Entfernen', command=self.del_ind).grid(row=0,column=3)

    def add_ind(self):
        vlaue_list = list()
        for col in self.herd.cols:
            entry_field = getattr(self, col)
            vlaue_list.append(entry_field.get())

        self.herd.add_ind(vlaue_list)
        self.herd_window.destroy()
        self.refresh_assignments()

    def del_add_ind(self):
        self.herd.del_ind(self.cbox_get_ind.get()) # direct via self.del_ind not possible because it closes the windows bevor add is executed
        self.add_ind()

    def del_ind(self):
        self.herd.del_ind(self.cbox_get_ind.get())
        self.herd_window.destroy()
        self.refresh_assignments()
        
######################################################################################################################################################

    def import_farm(self):
        csv_path = Path(filedialog.askopenfilename(title='CSV-Datei zum import der Farm auswählen', filetypes=[('CSV files', '*.csv')])) # CSV - File über GUI abfragen
        if not Path(csv_path).is_file(): return # in case of closing filedialog or selecting a directory | not shure if this works
        self.farm.import_csv(csv_path)
        self.refresh_assignments()

    def export_farm(self):
        csv_path = Path(filedialog.asksaveasfilename(title='Farm als CSV-Datei speichern', filetypes=[('CSV files', '*.csv')])) # CSV - File über GUI abfragen
        if csv_path == '' : return # in case of closing filedialog | not shure if this works
        self.farm.export_csv(csv_path)

    def load_farm_window(self):
        if self.farm_window is not None and self.farm_window.winfo_exists(): return # no double windows
        self.farm_window = tk.Toplevel()
        self.farm_frame = ttk.Frame(self.farm_window)
        self.farm_frame.pack(fill="both", expand=True)

    def check(self):
        pass

    def suggest(self):
        pass

    def add2farm(self):
        self.load_farm_window()
        self.farm_window.title('Add Compartment to farm')
        ttk.Label(self.farm_frame, text='Abbteil zu Farm hinzufügen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)

        for i, col in enumerate(self.farm.cols):
            n_c = 6 # number of cols
            r = i // n_c + 1
            c = (i - i // n_c * n_c) * 2
            ttk.Label(self.farm_frame, text=col).grid(row=r,column=c)
            setattr(self,col,ttk.Entry(self.farm_frame, width=15, justify='center'))
            entry_field = getattr(self, col)
            entry_field.grid(row=r,column=c+1)
   
        ttk.Button(self.farm_frame, text='Hinzufügen', command=self.add_comp).grid(row=r+1,column=n_c*2-1)

    def update_farm(self):
        self.load_farm_window()
        self.farm_window.title('Update Compartment of farm')
        ttk.Label(self.farm_frame, text='Abteil der Farm aktualisieren:', font=('',12,'bold')).grid(row=0,column=0,columnspan=2, sticky='w', pady=25)
        self.cbox_get_comp = ttk.Combobox(self.farm_frame, width=20, values=sorted(self.farm.df['NAME'].unique()))
        self.cbox_get_comp.grid(row=0,column=2)
        ttk.Button(self.farm_frame, text='Holen', command=self.get_comp).grid(row=0,column=3)

    def get_comp(self):
        comp = self.farm.df[self.farm.df['NAME']==self.cbox_get_comp.get()].iloc[0].to_dict()
        for i, (key, value) in enumerate(comp.items()):
            n_c = 6 # number of cols
            r = i // n_c + 1
            c = (i - i // n_c * n_c) * 2
            ttk.Label(self.farm_frame, text=key).grid(row=r,column=c)
            setattr(self,key,ttk.Entry(self.farm_frame, width=15, justify='center'))
            entry_field = getattr(self, key)
            entry_field.grid(row=r,column=c+1)
            entry_field.insert(0,value)

        ttk.Button(self.farm_frame, text='Aktualisieren', command=self.del_add_comp).grid(row=r+1,column=n_c*2-1)

    def rm_from_farm(self):
        self.load_farm_window()
        self.farm_window.title('Remove Compartment from farm')
        ttk.Label(self.farm_frame, text='Abteil aus Farm entfernen:', font=('',12,'bold')).grid(row=0,column=0,columnspan=1, sticky='w', pady=25)
        self.cbox_get_comp = ttk.Combobox(self.farm_frame, width=20, values=sorted(self.farm.df['NAME'].unique()))
        self.cbox_get_comp.grid(row=0,column=2)
        ttk.Button(self.farm_frame, text='Entfernen', command=self.del_comp).grid(row=0,column=3)

    def add_comp(self):
        vlaue_list = list()
        for col in self.farm.cols:
            entry_field = getattr(self, col)
            vlaue_list.append(entry_field.get())

        self.farm.add_comp(vlaue_list)
        self.farm_window.destroy()
        self.refresh_assignments()

    def del_add_comp(self):
        comp_name = self.cbox_get_comp.get()
        self.farm.del_comp(comp_name)
        del self.assignments[comp_name] # direct via self.del_comp not possible because it closes the windows bevor add is executed
        self.add_comp() # here no self.assignments management neccesary, because addition wors automatic within refresh function

    def del_comp(self):
        comp_name = self.cbox_get_comp.get()
        self.farm.del_comp(comp_name)
        del self.assignments[comp_name]
        self.farm_window.destroy()
        self.refresh_assignments()

######################################################################################################################################################

    def on_close(self):
        self.window.destroy()

# Global
if __name__ == '__main__': # 
    main() # 

# This is the last line of the Code :)