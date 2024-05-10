#   Employee Management System

import customtkinter as ctk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import tkinter as tk
# from PIL import Image, ImageTk
from datetime import *

import people_table, dates_table, home_table

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

import sys
import os
#   https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


size = [
    round(ctk.CTk().winfo_screenwidth()/2), 
    round(ctk.CTk().winfo_screenheight()/2),
    round(ctk.CTk().winfo_screenwidth() - round(ctk.CTk().winfo_screenwidth()/1.2)),
    round(ctk.CTk().winfo_screenheight() - round(ctk.CTk().winfo_screenheight()/1.2))]

light = False
def clr_mode():
    global light
    if light:
        ctk.set_appearance_mode("dark")
        
        light = False
    else:
        ctk.set_appearance_mode("light")
                
        light = True

ctk.set_default_color_theme(resource_path('MainApp/attributes/themes/CloudApp.json'))

#   colors:
txt_color = ('#0b2813', '#d7f4df')
rear_color = ('#ebf9ee', '#061409')
prime_color = ('#227737', '#88dd9d')
sec_color = ('#c384db', '#62247b')
accent_color = ('#a32e69', '#d15c96')


# 1
# 2
# 3
# 4
# 5
#   DANGER LOGIC ZONE

# people_table.create_people_table()
# dates_table.create_dates_table()
# home_table.create_home_table()
#   Logic
#   ADD
def add_to_ptree(ptree):
    pdatas = people_table.fetch_people_data()
    ptree.delete(*ptree.get_children())
    
    for pdata in pdatas:
        ptree.insert('', END, values=pdata)


def add_to_dtree(dtree):
    ddatas = dates_table.fetch_dates_data()
    dtree.delete(*dtree.get_children())
    
    for ddata in ddatas:
        dtree.insert('', END, values=ddata)


def add_to_htree(htree):
    hdatas = home_table.fetch_home_data()
    htree.delete(*htree.get_children())
    
    for hdata in hdatas:
        htree.insert('', END, values=hdata)

#   INSERT
def pinsert(ptree, name, surname, role, gender, team):
    if not (name and surname and gender and role and team):
        messagebox.showerror('Error', 'Enter all fields!')
    elif gender == '---':
        messagebox.showerror('Error', 'Gender cant be null!')
    # elif people_table.id_exists(id):
    #     messagebox.showerror('Error', 'ID already in use.')
    else:
        people_table.insert_people_data(name, surname, gender, role, team)
        add_to_ptree(ptree)
        messagebox.showinfo('Success', 'Data were inserted.') 
        

def dinsert(dtree, uid, date, time):
    if not (uid and date and time):
        messagebox.showerror('Error', 'Enter all fields!')
    else:
        dates_table.insert_dates_data(uid, date, time)
        add_to_dtree(dtree)
        messagebox.showinfo('Success', 'Data were inserted.') 


def dautoinsert(dtree, uid, date, time, unix):
    if not (uid):
        messagebox.showerror('Error', 'Enter all fields!')
    else:
        dates_table.auto_insert_dates_data(uid, date, time, unix)
        add_to_dtree(dtree)
        messagebox.showinfo('Success', 'Data were inserted.')
        
def search_treeview(tree, text):
    for item in tree.get_children(''):
        if text not in tree.item(item)['values'][1]:  # Assuming the name is in the second column
            tree.delete(item)


#   DANGER LOGIC ZONE
# 5
# 4
# 3
# 2
# 1
#   main window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Clockify")
        self.geometry(f'{size[0]}x{size[1]}+{size[2]}+{size[3]}')
        self.minsize(size[0], size[1])
        self.iconbitmap(resource_path('MainApp/attributes/icons/datetime512.ico'))
        # self.resizable(False, False)
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=30)
        
        #   f11
        self.fullscreen = False
        self.bind('<F11>', self.f11_fs)
        #   quitting
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind('<Escape>', lambda event: self.quit())
        
        #   widgets
        self.main = Main(self)
        self.menu = Menu(self, self.my_font, self.main)
        # self.mod_p = ModifyP(self, self.my_font, self.main)

        #   run
        self.mainloop()
        
        #   fullscreen
    def f11_fs(self):
        if self.fullscreen:
            self.attributes('-fullscreen', False)
            self.fullscreen = False
        else:
            self.attributes('-fullscreen', True)
            self.fullscreen = True

    #   end process on close
    def on_closing(self):
        self.destroy()
        sys.exit()



#   sidebar
class Menu(ctk.CTkFrame):
    def __init__(self, parent, my_font, main):
        super().__init__(parent)
        
        self.place(
            relx = 0.0125, 
            rely = 0.025, 
            relwidth = 0.2, 
            relheight = 0.95)
        
        self.side_widgets(my_font, main)
        
    def side_widgets(self, my_font, main):
        
        #   create widgets
            #   top
        app_name = ctk.CTkLabel(self, text='Clockify', font=my_font, corner_radius=8)
        home = ctk.CTkButton(self, text='Home', font=my_font, command=lambda: main.home_frame(my_font))
            #   mid
        people = ctk.CTkButton(self, text='People', font=my_font, command=lambda: main.people_frame(my_font))
        dates = ctk.CTkButton(self, text='Dates', font=my_font, command=lambda: main.dates_frame(my_font))
            #   bottom
        color_mode = ctk.CTkButton(self, text='Color Mode', font=ctk.CTkFont(family="Ubuntu Sans Bold", size=24), command=clr_mode)
        

        
        #   place widgets   |   step    0.012   |   widget height   0.1175
            #   top
        app_name.place(relx=0.025, rely=0.012, relwidth=0.95, relheight=0.1175)
        home.place(relx=0.025, rely=0.247, relwidth=0.95, relheight=0.1175)
            #   mid
        people.place(relx=0.025, rely=0.482, relwidth=0.95, relheight=0.1175)
        dates.place(relx=0.025, rely=0.6115, relwidth=0.95, relheight=0.1175)
            #   bottom
        color_mode.place(relx=0.025, rely=0.8705, relwidth=0.95, relheight=0.1175)



#   mainbar
class Main(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.ptoplevel_window = None
        self.dtoplevel_window = None
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=30)
        self.place(
            relx = 0.225,
            rely = 0.025,
            relwidth = 0.765,
            relheight = 0.95)
        
        #   widgets & assets        
        self.p_table_frame = ctk.CTkFrame(self)
        self.p_label = ctk.CTkLabel(self, text="People:", font=self.my_font, corner_radius=8)
        
        self.ptoplevel_window = None
        self.ptree = None
        
        self.d_table_frame = ctk.CTkFrame(self)
        self.d_label = ctk.CTkLabel(self, text="Dates:", font=self.my_font, corner_radius=8)
        
        self.dtoplevel_window = None
        self.dtree = None
        
        self.h_table_frame = ctk.CTkFrame(self)
        self.h_label = ctk.CTkLabel(self, text="Home:", font=self.my_font, corner_radius=8)

        self.htoplevel_window = None
        self.htree = None
    
    
    
    #   people_table



    def people_frame(self, my_font):
        self.d_label.place_forget()
        self.d_table_frame.place_forget()
        self.h_label.place_forget()
        self.h_table_frame.place_forget()
        self.close_toplevels()
        
        
        self.p_label.place(relx=0.0125, rely=0.012, relwidth=0.45, relheight=0.1175)
        self.p_table_frame.place(relx=0.0125, rely=0.15, relwidth=0.975, relheight=0.825)

        
        mod_p = ctk.CTkButton(self.p_table_frame, text='Manage', font=my_font, command=self.open_ptoplevel)
        mod_p.place(relx=0.0125, rely=0.0125, relwidth=0.225, relheight=0.175)
        
        self.search_button = ctk.CTkButton(self.p_table_frame, text='Search', font=ctk.CTkFont(family="Ubuntu Sans Bold", size=18), command=self.search_people)
        self.search_button.place(relx=0.375, rely=0.0125, relwidth=0.225, relheight=0.08125)
        
        self.search_clear_button = ctk.CTkButton(self.p_table_frame, text='Clear Search', font=ctk.CTkFont(family="Ubuntu Sans Bold", size=18), command=self.clear_search)
        self.search_clear_button.place(relx=0.375, rely=0.10625, relwidth=0.225, relheight=0.08125)

        self.search_entry = ctk.CTkEntry(self.p_table_frame, font=ctk.CTkFont(family="Ubuntu Sans Bold", size=15), width=180)
        self.search_entry.place(relx=0.6125, rely=0.0125, relwidth=0.375, relheight=0.175)
        
        
        self.ptree = self.p_table(my_font)
        add_to_ptree(self.ptree)


    def p_table(self, my_font):
        
        other_font = ctk.CTkFont(family="Ubuntu Sans", size=20)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', font=my_font, foreground='#0A090C', background='#55aa6a', fieldbackground='#3a3335', rowheight=25)
        style.map('Treeview', background=[('selected', '#9254ab')])

        ptree = ttk.Treeview(self.p_table_frame)

        ptree['columns'] = ('uID', 'Name', 'Surname', 'Gender', 'Role', 'Team')
    
        ptree.column('#0', width=0, stretch=tk.NO)
        ptree.column('uID', anchor=tk.CENTER, width=50)
        ptree.column('Name', anchor=tk.CENTER, width=120)
        ptree.column('Surname', anchor=tk.CENTER, width=120)
        ptree.column('Gender', anchor=tk.CENTER, width=80)
        ptree.column('Role', anchor=tk.CENTER, width=120)
        ptree.column('Team', anchor=tk.CENTER, width=120)

        ptree.heading('uID', text='uID')
        ptree.heading('Name', text='Name')
        ptree.heading('Surname', text='Surname')
        ptree.heading('Gender', text='Gender')
        ptree.heading('Role', text='Role')
        ptree.heading('Team', text='Team')
        
        ptree.place(relx=0.0125, rely=0.2, relwidth=0.975, relheight=0.775)

        ptree.bind('<Motion>', 'break')
        
        return ptree
        
    
    def open_ptoplevel(self):
        if self.ptoplevel_window is None or not self.ptoplevel_window.winfo_exists():
            self.ptoplevel_window = ModifyP(self, self.ptree)
        else:
            self.ptoplevel_window.focus()
    


    #   dates_table

    
    
    def dates_frame(self, my_font):
        
        self.p_label.place_forget()
        self.p_table_frame.place_forget()
        self.h_label.place_forget()
        self.h_table_frame.place_forget()
        self.close_toplevels()
        

        self.d_label.place(relx=0.0125, rely=0.012, relwidth=0.45, relheight=0.1175)
        self.d_table_frame.place(relx=0.0125, rely=0.15, relwidth=0.975, relheight=0.825)


        mod_d = ctk.CTkButton(self.d_table_frame, text='Manage', font=my_font, command=self.open_dtoplevel)
        mod_d.place(relx=0.0125, rely=0.0125, relwidth=0.225, relheight=0.175)
        
        self.search_button = ctk.CTkButton(self.d_table_frame, text='Search', font=ctk.CTkFont(family="Ubuntu Sans Bold", size=18), command=self.search_dates)
        self.search_button.place(relx=0.375, rely=0.0125, relwidth=0.225, relheight=0.08125)
        
        self.search_clear_button = ctk.CTkButton(self.d_table_frame, text='Clear Search', font=ctk.CTkFont(family="Ubuntu Sans Bold", size=18), command=self.clear_search_dates)
        self.search_clear_button.place(relx=0.375, rely=0.10625, relwidth=0.225, relheight=0.08125)

        self.search_entry = ctk.CTkEntry(self.d_table_frame, font=ctk.CTkFont(family="Ubuntu Sans Bold", size=15), width=180)
        self.search_entry.place(relx=0.6125, rely=0.0125, relwidth=0.375, relheight=0.175)
        
        
        self.dtree = self.d_table(my_font)
        add_to_dtree(self.dtree)
                
        
    def d_table(self, my_font):
        
        other_font = ctk.CTkFont(family="Ubuntu Sans", size=20)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', font=my_font, foreground='#0A090C', background='#55aa6a', fieldbackground='#3a3335', rowheight=25)
        style.map('Treeview', background=[('selected', '#9254ab')])

        dtree = ttk.Treeview(self.d_table_frame)

        dtree['columns'] = ('uID', 'Role', 'Team', 'Date', 'Time')
    
        dtree.column('#0', width=0, stretch=tk.NO)
        dtree.column('uID', anchor=tk.CENTER, width=30)
        dtree.column('Role', anchor=tk.CENTER, width=120)
        dtree.column('Team', anchor=tk.CENTER, width=120)
        dtree.column('Date', anchor=tk.CENTER, width=120)
        dtree.column('Time', anchor=tk.CENTER, width=120)

        dtree.heading('uID', text='uID')
        dtree.heading('Role', text='Role')
        dtree.heading('Team', text='Team')
        dtree.heading('Date', text='Date')
        dtree.heading('Time', text='Time')

        dtree.place(relx=0.0125, rely=0.2, relwidth=0.975, relheight=0.775)
        
        dtree.bind('<Motion>', 'break')
        
        return dtree


    def open_dtoplevel(self):
        if self.dtoplevel_window is None or not self.dtoplevel_window.winfo_exists():
            self.dtoplevel_window = ModifyD(self, self.dtree)
        else:
            self.dtoplevel_window.focus()

    
    def close_toplevels(self):
        if self.ptoplevel_window and self.ptoplevel_window.winfo_exists():
            self.ptoplevel_window.destroy()
            self.ptoplevel_window = None
        if self.dtoplevel_window and self.dtoplevel_window.winfo_exists():
            self.dtoplevel_window.destroy()
            self.dtoplevel_window = None

    

    #   home_table



    def home_frame(self, my_font):
        
        self.p_label.place_forget()
        self.p_table_frame.place_forget()
        self.d_label.place_forget()
        self.d_table_frame.place_forget()
        self.close_toplevels()
        
        
        self.h_label.place(relx=0.0125, rely=0.012, relwidth=0.45, relheight=0.1175)
        self.h_table_frame.place(relx=0.0125, rely=0.15, relwidth=0.975, relheight=0.825)

        
        self.htree = self.h_table(my_font)                
        add_to_htree(self.htree)


    def h_table(self, my_font):
        
        other_font = ctk.CTkFont(family="Ubuntu Sans", size=20)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', font=my_font, foreground='#0A090C', background='#55aa6a', fieldbackground='#3a3335', rowheight=25)
        style.map('Treeview', background=[('selected', '#9254ab')])

        htree = ttk.Treeview(self.h_table_frame)

        htree['columns'] = ('uID', 'Name', 'Surname', 'Date', 'Time')

        htree.column('#0', width=0, stretch=tk.NO)
        htree.column('uID', anchor=tk.CENTER, width=30)
        htree.column('Name', anchor=tk.CENTER, width=120)
        htree.column('Surname', anchor=tk.CENTER, width=120)
        htree.column('Date', anchor=tk.CENTER, width=120)
        htree.column('Time', anchor=tk.CENTER, width=120)

        htree.heading('uID', text='uID')
        htree.heading('Name', text='Name')
        htree.heading('Surname', text='Surname')
        htree.heading('Date', text='Date')
        htree.heading('Time', text='Time')

        htree.place(relx=0.0125, rely=0.0125, relwidth=0.975, relheight=0.975)
        
        htree.bind('<Motion>', 'break')

        return htree
        
        
    #   search tree
    
    def search_people(self):
        search_term = self.search_entry.get()
        if search_term:
            self.ptree.delete(*self.ptree.get_children())
            people_data = people_table.search_people_data(search_term)
            for pdata in people_data:
                self.ptree.insert('', END, values=(pdata[1], pdata[2], pdata[3], pdata[4], pdata[5], pdata[6]))

    def clear_search(self):
        self.search_entry.delete(0, END)
        self.ptree.delete(*self.ptree.get_children())
        add_to_ptree(self.ptree)
    
    
    
    def search_dates(self):
        search_term = self.search_entry.get()
        if search_term:
            self.dtree.delete(*self.dtree.get_children())
            dates_data = dates_table.search_dates_data(search_term)
            for ddata in dates_data:
                self.dtree.insert('', END, values=(ddata[1], ddata[3], ddata[2], ddata[4], ddata[5]))

    def clear_search_dates(self):
        self.search_entry.delete(0, END)
        self.dtree.delete(*self.dtree.get_children())
        add_to_dtree(self.dtree)

    


class ModifyP(ctk.CTkToplevel):
    def __init__(self, main, ptree, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main = main
        self.ptree = ptree
        
        self.title('Manage People')
        self.geometry(f"{round(size[0]/1.25)}x{size[1]/1.5}")
        self.resizable(False,False)
        
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=30)
        self.modp_widgets()
        
        self.ptree.bind('<<TreeviewSelect>>', self.display_data)
        
    
    def modp_widgets(self):
        
        #   widgets     |   step    0.0125  |   height  0.1375
        name_label = ctk.CTkLabel(self, font=self.my_font, text='Name:', corner_radius=8)
        name_label.place(relx=0.0125, rely=0.0125, relwidth=0.25, relheight=0.1375)

        surname_label = ctk.CTkLabel(self, font=self.my_font, text='Surname:', corner_radius=8)
        surname_label.place(relx=0.0125, rely=0.2125, relwidth=0.25, relheight=0.1375)

        gender_label = ctk.CTkLabel(self, font=self.my_font, text='Gender:', corner_radius=8)
        gender_label.place(relx=0.0125, rely=0.425, relwidth=0.25, relheight=0.1375)

        role_label = ctk.CTkLabel(self, font=self.my_font, text='Role:', corner_radius=8)
        role_label.place(relx=0.0125, rely=0.6375, relwidth=0.25, relheight=0.1375)

        team_label = ctk.CTkLabel(self, font=self.my_font, text='Team:', corner_radius=8)
        team_label.place(relx=0.0125, rely=0.85, relwidth=0.25, relheight=0.1375)


        #   entry fields
        self.name_entry = ctk.CTkEntry(self, font=self.my_font, width=180)
        self.name_entry.place(relx=0.275, rely=0.0125, relwidth=0.35, relheight=0.1375)

        self.surname_entry = ctk.CTkEntry(self, font=self.my_font, width=180)
        self.surname_entry.place(relx=0.275, rely=0.2125, relwidth=0.35, relheight=0.1375)

        options = ['Male', 'Female', 'Other']   #   IDC what you might say you m.p.o.c.
        self.gender_var = StringVar()

        self.gender_options = ctk.CTkOptionMenu(self, font=self.my_font, variable=self.gender_var, values=options, state='readonly')
        self.gender_options.set('---')
        self.gender_options.place(relx=0.275, rely=0.425, relwidth=0.35, relheight=0.1375)

        self.role_entry = ctk.CTkEntry(self, font=self.my_font, width=180)
        self.role_entry.place(relx=0.275, rely=0.6375, relwidth=0.35, relheight=0.1375)

        self.team_entry = ctk.CTkEntry(self, font=self.my_font, width=180)
        self.team_entry.place(relx=0.275, rely=0.85, relwidth=0.35, relheight=0.1375)
    
    
        #   buttons
        add_button = ctk.CTkButton(self, font=self.my_font, text='Add', width=260, command=self.pinsert_data)
        add_button.place(relx=0.6375, rely=0.0125, relwidth=0.35, relheight=0.1375)

        clear_button = ctk.CTkButton(self, font=self.my_font, text='New', width=260, command=lambda: self.clear_entries(True))
        clear_button.place(relx=0.6375, rely=0.2125, relwidth=0.35, relheight=0.1375)

        update_button = ctk.CTkButton(self, font=self.my_font, text='Update', width=260, command=self.pupdate_data)
        update_button.place(relx=0.6375, rely=0.6375, relwidth=0.35, relheight=0.1375)

        delete_button = ctk.CTkButton(self, font=self.my_font, text='Delete', width=260, command=self.pdelete_data)
        delete_button.place(relx=0.6375, rely=0.85, relwidth=0.35, relheight=0.1375)
        
        
        
    def pinsert_data(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        role = self.role_entry.get()
        gender = self.gender_var.get()
        team = self.team_entry.get()
        
        if not (name and surname and gender and role and team):
            messagebox.showerror('Error', 'Enter all fields.')
        elif gender == '---':
            messagebox.showerror('Error', 'Gender cant be null.')
        else:
            pinsert(self.ptree, name, surname, role, gender, team)
            self.clear_entries()
        
        
    def display_data(self, event):
        selected_item = self.ptree.focus()
        if selected_item:
            row = self.ptree.item(selected_item)['values']
            if self.winfo_exists():
                self.clear_entries()
                self.name_entry.insert(0, row[1])
                self.surname_entry.insert(0, row[2])
                self.gender_var.set(row[3])
                self.role_entry.insert(0, row[4])
                self.team_entry.insert(0, row[5])
        else:
            pass
        
        
    def clear_entries(self, clicked=False):
        if clicked:
            self.ptree.selection_remove(self.ptree.focus())
            self.ptree.focus('')
        self.name_entry.delete(0, END)
        self.surname_entry.delete(0, END)
        self.gender_var.set('---')
        self.role_entry.delete(0, END)
        self.team_entry.delete(0, END)


    def pupdate_data(self):
        selected_item = self.ptree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Unable to update null.')
        else:
            name = self.name_entry.get()
            surname = self.surname_entry.get()
            role = self.role_entry.get()
            gender = self.gender_var.get()
            team = self.team_entry.get()
            
            if not (name and surname and gender and role and team):
                messagebox.showerror('Error', 'Enter all fields.')
            elif gender == '---':
                messagebox.showerror('Error', 'Gender cant be null.')
            else:
                uid = self.ptree.item(selected_item)['values'][0]
                people_table.update_people_data(name, surname, gender, role, team, uid)
                add_to_ptree(self.ptree)
                self.clear_entries()
                messagebox.showinfo('Success', 'Update success.')


    def pdelete_data(self):
        selected_item = self.ptree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Unable to delete null.')
        else:
            uid = self.ptree.item(selected_item)['values'][0]
            people_table.delete_people_data(uid)
            add_to_ptree(self.ptree)
            self.clear_entries()
            messagebox.showinfo('Success', 'Delete success.')



class ModifyD(ctk.CTkToplevel):
    def __init__(self, main, dtree, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main = main
        self.dtree = dtree
        
        # self.mod_popup = ctk.CTkToplevel()
        self.title('Manage Dates')
        self.geometry(f"{round(size[0]/1.25)}x{size[1]/1.5}")
        self.resizable(False,False)
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=30)
        self.modp_widgets()
        
        self.dtree.bind('<<TreeviewSelect>>', self.display_data)
        # self.cal.bind('<<CalendarSelected>>', lambda event: print(self.cal.selection_get()))
        
    
    def modp_widgets(self):
        
        #   widgets     |   step    0.016 . 0.013   |   height  0.23  .  width   0.316
        uid_label = ctk.CTkLabel(self, font=self.my_font, text='uID:', corner_radius=8)
        uid_label.place(relx=0.013, rely=0.016, relwidth=0.316, relheight=0.23)

        hour_label = ctk.CTkLabel(self, font=self.my_font, text='Hours:', corner_radius=8)
        hour_label.place(relx=0.013, rely=0.262, relwidth=0.316, relheight=0.23)

        minute_label = ctk.CTkLabel(self, font=self.my_font, text='Minutes:', corner_radius=8)
        minute_label.place(relx=0.342, rely=0.262, relwidth=0.316, relheight=0.23)


        #   entry fields
        def uids_validate():
            if self.uids == []:
                self.uid_var.set("---")

        self.uids = people_table.export_uids()
        self.uid_var = tk.StringVar()
        self.uid_var.set("---")
        self.uid_spinbox = ttk.Spinbox(self, font=self.my_font, values=self.uids, textvariable=self.uid_var, command=uids_validate)
        self.uid_spinbox.place(relx=0.342, rely=0.0125, relwidth=0.316, relheight=0.23)
        
        def hour_validate():
            hour = self.hour_int.get()
            if hour < 0:
                self.hour_int.set(0)
        
        def minute_validate():
            minute = self.minute_int.get()
            if minute < 0:
                self.minute_int.set(0)
            
        self.hour_int = tk.IntVar()
        self.hour_spinbox = ttk.Spinbox(self, font=self.my_font, from_ = -1, to = 23, state="readonly", textvariable=self.hour_int, command=hour_validate)
        self.hour_spinbox.place(relx=0.013, rely=0.508, relwidth=0.316, relheight=0.23)

        self.minute_int = tk.IntVar()
        self.minute_spinbox = ttk.Spinbox(self, font=self.my_font, from_ = -1, to = 59, increment=5, state="readonly", textvariable=self.minute_int, command=minute_validate)
        self.minute_spinbox.place(relx=0.342, rely=0.508, relwidth=0.316, relheight=0.23)
        
        
        #   buttons
        submit_button = ctk.CTkButton(self, font=self.my_font, text='Add', width=260, command=self.dinsert_data)
        submit_button.place(relx=0.013, rely=0.754, relwidth=0.1035, relheight=0.23)

        autosub_button = ctk.CTkButton(self, font=self.my_font, text='Auto Add', width=260, command=self.dautoinsert_data)
        autosub_button.place(relx=0.1315, rely=0.754, relwidth=0.1975, relheight=0.23)

        delete_button = ctk.CTkButton(self, font=self.my_font, text='Delete', width=260, command=self.ddelete_data)
        delete_button.place(relx=0.342, rely=0.754, relwidth=0.316, relheight=0.23)
        
        
        #   calendar
        dtn = datetime.now()
        self.date_var = tk.StringVar()
        self.date_var.set(f'{dtn.strftime('%m')}-{dtn.strftime('%d')}-{dtn.strftime('%Y')}')
        
        self.cal = Calendar(self, font=ctk.CTkFont(family="Ubuntu Sans", size=14), selectmode='day', date_pattern='dd-mm-y', textvariable=self.date_var)
        #   year=int(datetime.now().strftime('%Y')), month=int(datetime.now().strftime('%m')), day=int(datetime.now().strftime('%d'))
        self.cal.place(relx=0.671, rely=0.016, relwidth=0.316, relheight=0.968)

    
    
    
    def dinsert_data(self):
        uid = self.uid_var.get()
        date = self.date_var.get()
        hours = self.hour_int.get()
        minutes = self.minute_int.get()
        
        if not (uid):
            messagebox.showerror('Error', 'Enter the uID!')
        elif uid == '---':
            messagebox.showerror('Error', "uID can't be empty!")
        else:
            if len(str(hours)) == 1:
                hours = f'0{hours}'
            if len(str(minutes)) == 1:
                minutes = f'0{minutes}'
            
            time = f'{hours}:{minutes}'
            
            
            dinsert(self.dtree, uid, date, time)
            self.clear_entries()
        
    def dautoinsert_data(self):
        uid = self.uid_var.get()
        date = datetime.now().strftime('%d-%m-%Y')
        time = datetime.now().strftime('%H:%M')
        unix = round(datetime.now().timestamp())
        
        if not (uid):
            messagebox.showerror('Error', 'Enter uid!')
        elif uid == '---':
            messagebox.showerror('Error', "uID can't be empty!")
        else:
            dautoinsert(self.dtree, uid, date, time, unix)
            self.clear_entries()
        
        
    def display_data(self, event):
        selected_item = self.dtree.focus()
        if selected_item:
            row = self.dtree.item(selected_item)['values']
            if self.winfo_exists():
                self.clear_entries()
                self.uid_var.set(row[0])
                self.date_var.set(row[3])
                self.hour_int.set(row[4][:2])
                self.minute_int.set(row[4][3:])
        else:
            pass
        
        
    def clear_entries(self, clicked=False):
        if clicked:
            self.dtree.selection_remove(self.dtree.focus())
            self.dtree.focus('')
        
        dtn = datetime.now()
        self.date_var.set(f'{dtn.strftime('%d')}-{dtn.strftime('%m')}-{dtn.strftime('%Y')}')
        self.uid_var.set('---')
        self.hour_int.set(0)
        self.minute_int.set(0)
                


    def ddelete_data(self):
        selected_item = self.dtree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Unable to delete null!')
        else:
            uid = self.dtree.item(selected_item)['values'][0]
            date = self.dtree.item(selected_item)['values'][3]
            time = self.dtree.item(selected_item)['values'][4]
            dates_table.delete_dates_data(uid, date, time)
            add_to_dtree(self.dtree)
            self.clear_entries()
            messagebox.showinfo('Success', 'Delete success.')




#   launch the app
App()