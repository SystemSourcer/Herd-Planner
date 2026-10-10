# Imports
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

    def add_ind(self,name,lom,born,gender): 
        """
        Function that is called when a ind is added manual by user
        """
        self.df.loc[len(self.df)] = [name,lom,'',born,gender,'','','','','','','','','','','','']
        print(f'\033[36mHerd: \n{self.df} \033[0m')
    
    def import_csv(self,import_csv_path):
        """
        Function that is called when a ind is added by csv import
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

        self.df = (pd.concat([self.df, import_df], ignore_index=True).drop_duplicates(subset='LOM_X')) # LOM_X is the identifyer. all comus would leed to problems e.g. Compartment...

        print(f'\033[32mDatenbank {import_csv_path} geöffnet und importiert.\033[0m')
        print(f'\033[36mHerd: \n{self.df} \033[0m')

    def export_csv(self, export_csv_path):
        self.df.to_csv(export_csv_path,sep=';',index=False)
        print(f'\033[32mDataFrame erfolgreich in {export_csv_path} gespeichert\033[0m')

class Farm:
    '''
    Object definition for a farm
    '''
    def __init__(self):
        self.cols = ['NAME','COUNT','AGE_Min','AGE_MAX','GENDER']
        self.df = pd.DataFrame(columns= self.cols)
        print(f'\033[33mFarm: \n{self.df} \033[0m')

    def add_comp(self,name,count,age_min,age_max,gender):
        self.df.loc[len(self.df)] = [name,count,age_min,age_max,gender]
        print(f'\033[33mFarm: \n{self.df} \033[0m')

    def import_csv(self):
        pass

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

        ttk.Label(self.window, text='Manage Farm:', font=('',12,'bold')).grid(row=0,column=0, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_farm).grid(row=0,column=1)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2farm).grid(row=0,column=2)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_compartment).grid(row=0,column=3)
        ttk.Button(self.window, text='Entfernen', command=self.rm_compartment).grid(row=0,column=4)
        ttk.Button(self.window, text='Export', command=self.export_farm).grid(row=0,column=5)

        ttk.Label(self.window, text='Manage Herd:', font=('',12,'bold')).grid(row=2,column=0, sticky='w', pady=25)
        ttk.Button(self.window, text='Import', command=self.import_herd).grid(row=2,column=1)
        ttk.Button(self.window, text='Hinzufügen', command=self.add2herd).grid(row=2,column=2)
        ttk.Button(self.window, text='Aktualisieren', command=self.update_ind).grid(row=2,column=3)
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
        self.farm_window.title('Add Compartment to Farm')
        self.farm_frame = ttk.Frame(self.farm_window)
        self.farm_frame.pack(fill="both", expand=True)

    def check(self):
        pass

    def suggest(self):
        pass

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