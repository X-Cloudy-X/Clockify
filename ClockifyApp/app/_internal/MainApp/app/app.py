#   Employee Management System

import customtkinter as ctk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import tkinter as tk
# from PIL import Image, ImageTk
from datetime import *

import people_table, dates_table, home_table, auth

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

### LOGIN AND SIGNUP
auth.create_users_table()


def enable_widgets(home):
    home.configure(state='enabled')

  
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
        self.bind('<F11>', lambda event: self.f11_fs())
        #   quitting
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind('<Escape>', lambda event: self.esc_fs())
        
        #   widgets
        self.main = Main(self)
        self.home_btn_command = lambda: self.main.home_frame(self.main.my_font)
        self.people_btn_command = lambda: self.main.people_frame(self.main.my_font)
        self.dates_btn_command = lambda: self.main.dates_frame(self.main.my_font)

        self.menu_frame_widgets()
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

    def esc_fs(self):
        if self.fullscreen:
            self.attributes('-fullscreen', False)
            self.fullscreen = False
            

    #   end process on close
    def on_closing(self):
        self.destroy()
        sys.exit()


    def menu_frame_widgets(self):
        
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.place(relx=0.0125, rely=0.025, relwidth=0.2, relheight=0.95)
        
        self.side_widgets()


    def side_widgets(self):
        
        #   create widgets
            #   top
        app_name = ctk.CTkLabel(self.menu_frame, text='Clockify', font=self.my_font, corner_radius=8)
        self.home = ctk.CTkButton(self.menu_frame, text='Home', font=self.my_font, state='disabled', command=self.home_btn_command)
        
            #   mid
        self.people = ctk.CTkButton(self.menu_frame, text='People', font=self.my_font, state='disabled', command=self.people_btn_command)
        self.dates = ctk.CTkButton(self.menu_frame, text='Attendance', font=self.my_font, state='disabled', command=self.dates_btn_command)
        
            #   bottom
        color_mode = ctk.CTkButton(self.menu_frame, text='Color Mode', font=ctk.CTkFont(family="Ubuntu Sans Bold", size=24), command=clr_mode)
        
        
        #   place widgets   |   step    0.012   |   widget height   0.1175
            #   top
        app_name.place(relx=0.025, rely=0.012, relwidth=0.95, relheight=0.1175)
        self.home.place(relx=0.025, rely=0.247, relwidth=0.95, relheight=0.1175)
            #   mid
        self.people.place(relx=0.025, rely=0.482, relwidth=0.95, relheight=0.1175)
        self.dates.place(relx=0.025, rely=0.6115, relwidth=0.95, relheight=0.1175)
            #   bottom
        color_mode.place(relx=0.025, rely=0.8705, relwidth=0.95, relheight=0.1175)




#   mainbar
class Main(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        
        self.ptoplevel_window = None
        self.dtoplevel_window = None
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=30)
        self.place(relx = 0.225, rely = 0.025, relwidth = 0.765, relheight = 0.95)
        
        #   widgets & assets        
        self.p_table_frame = ctk.CTkFrame(self)
        self.p_label = ctk.CTkLabel(self, text="People:", font=self.my_font, corner_radius=8)
        
        self.ptoplevel_window = None
        self.ptree = None
        
        self.d_table_frame = ctk.CTkFrame(self)
        self.d_label = ctk.CTkLabel(self, text="Attendance:", font=self.my_font, corner_radius=8)
        
        self.dtoplevel_window = None
        self.dtree = None
        
        self.h_table_frame = ctk.CTkFrame(self)
        self.h_label = ctk.CTkLabel(self, text="Home:", font=self.my_font, corner_radius=8)

        self.htoplevel_window = None
        self.htree = None
        
        
        self.auth_widget_frame = ctk.CTkFrame(self)
        self.auth_label = ctk.CTkLabel(self, text="Login / Register", font=self.my_font, corner_radius=8)
        
        
        self.login_window = None
        self.signup_window = None
        
        self.auth_frame()
    
    def auth_frame(self):
        
        self.auth_label.place(relx=0.0125, rely=0.012, relwidth=0.45, relheight=0.1175)
        self.auth_widget_frame.place(relx=0.25, rely=0.3, relwidth=0.5, relheight=0.4)
        
        
        login_btn = ctk.CTkButton(self.auth_widget_frame, text='Log-in', font=self.my_font, command=self.login_toplevel)
        login_btn.place(relx=0.12, rely=0.175, relwidth=0.76, relheight=0.2375)

        signup_btn = ctk.CTkButton(self.auth_widget_frame, text='Register', font=self.my_font, command=self.signup_toplevel)
        signup_btn.place(relx=0.12, rely=0.5875, relwidth=0.76, relheight=0.2375)
    
    
    def login_toplevel(self):
        if self.login_window is None or not self.login_window.winfo_exists():
            self.login_window = Login(self)
        else:
            self.login_window.lift()
        if self.signup_window and self.signup_window.winfo_exists():
            self.signup_window.destroy()

    def signup_toplevel(self):
        if self.signup_window is None or not self.signup_window.winfo_exists():
            self.signup_window = Signup(self)
        else:
            self.signup_window.lift()
        if self.login_window and self.login_window.winfo_exists():
            self.login_window.destroy()
    
    def forget_auth_frame(self):
        self.auth_widget_frame.place_forget()
        self.auth_label.place_forget()
        #
        try:
            self.login_window.destroy()
        except:
            pass
        try:
            self.signup_window.destroy()
        except:
            pass
        
        self.parent.home.configure(state='normal')
        self.parent.people.configure(state='normal')
        self.parent.dates.configure(state='normal')
        self.home_frame(self.my_font)
        
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
        
        other_font = ctk.CTkFont(family="Ubuntu Sans", size=16)
                
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', font=("Ubuntu Sans", 12), foreground='#0A090C', background='#55aa6a', fieldbackground='#3a3335', rowheight=25)
        style.map('Treeview', background=[('selected', '#9254ab')])

        ptree = ttk.Treeview(self.p_table_frame)

        ptree['columns'] = ('uID', 'Name', 'Surname', 'Gender', 'Role', 'Group')
    
        ptree.column('#0', width=0, stretch=tk.NO)
        ptree.column('uID', anchor=tk.W, minwidth=50, width=75, stretch=tk.YES)
        ptree.column('Name', anchor=tk.W, minwidth=40, width=100, stretch=tk.YES)
        ptree.column('Surname', anchor=tk.W, minwidth=40, width=100, stretch=tk.YES)
        ptree.column('Gender', anchor=tk.W, minwidth=40, width=50, stretch=tk.YES)
        ptree.column('Role', anchor=tk.W, minwidth=40, width=110, stretch=tk.YES)
        ptree.column('Group', anchor=tk.W, minwidth=40, width=150, stretch=tk.YES)

        ptree.heading('uID', text='uID', anchor=tk.W)
        ptree.heading('Name', text='Name', anchor=tk.W)
        ptree.heading('Surname', text='Surname', anchor=tk.W)
        ptree.heading('Gender', text='Gender', anchor=tk.W)
        ptree.heading('Role', text='Role', anchor=tk.W)
        ptree.heading('Group', text='Group', anchor=tk.W)
        
        ptree.place(relx=0.0125, rely=0.2, relwidth=0.975, relheight=0.775)

        ptree.bind('<Motion>', 'break')
        
        return ptree
        
    
    def open_ptoplevel(self):
        if self.ptoplevel_window is None or not self.ptoplevel_window.winfo_exists():
            self.ptoplevel_window = ModifyP(self, self.ptree)
        else:
            self.ptoplevel_window.focus_force()



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
        
        other_font = ctk.CTkFont(family="Ubuntu Sans", size=16)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', font=("Ubuntu Sans", 12), foreground='#0A090C', background='#55aa6a', fieldbackground='#3a3335', rowheight=25)
        style.map('Treeview', background=[('selected', '#9254ab')])

        dtree = ttk.Treeview(self.d_table_frame)

        dtree['columns'] = ('uID', 'Role', 'Group', 'Date', 'Time')
    
        dtree.column('#0', width=0, stretch=tk.NO)
        dtree.column('uID', anchor=tk.W, minwidth=50, width=75, stretch=tk.YES)
        dtree.column('Role', anchor=tk.W, minwidth=40, width=110, stretch=tk.YES)
        dtree.column('Group', anchor=tk.W, minwidth=40, width=150, stretch=tk.YES)
        dtree.column('Date', anchor=tk.CENTER, minwidth=40, width=100, stretch=tk.YES)
        dtree.column('Time', anchor=tk.CENTER, minwidth=40, width=50, stretch=tk.YES)

        dtree.heading('uID', text='uID', anchor=tk.W)
        dtree.heading('Role', text='Role', anchor=tk.W)
        dtree.heading('Group', text='Group', anchor=tk.W)
        dtree.heading('Date', text='Date', anchor=tk.CENTER)
        dtree.heading('Time', text='Time', anchor=tk.CENTER)

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
        
        other_font = ctk.CTkFont(family="Ubuntu Sans", size=16)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', font=("Ubuntu Sans", 15), foreground='#0A090C', background='#55aa6a', fieldbackground='#3a3335', rowheight=30)
        style.map('Treeview', background=[('selected', '#9254ab')])

        htree = ttk.Treeview(self.h_table_frame)

        htree['columns'] = ('uID', 'Name', 'Surname', 'Date', 'Time')

        htree.column('#0', width=0, stretch=tk.NO)
        htree.column('uID', anchor=tk.W, minwidth=50, width=75, stretch=tk.YES)
        htree.column('Name', anchor=tk.W, minwidth=40, width=100, stretch=tk.YES)
        htree.column('Surname', anchor=tk.W, minwidth=40, width=100, stretch=tk.YES)
        htree.column('Date', anchor=tk.CENTER, minwidth=40, width=100, stretch=tk.YES)
        htree.column('Time', anchor=tk.CENTER, minwidth=40, width=50, stretch=tk.YES)

        htree.heading('uID', text='uID', anchor=tk.W)
        htree.heading('Name', text='Name', anchor=tk.W)
        htree.heading('Surname', text='Surname', anchor=tk.W)
        htree.heading('Date', text='Date', anchor=tk.CENTER)
        htree.heading('Time', text='Time', anchor=tk.CENTER)

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

        team_label = ctk.CTkLabel(self, font=self.my_font, text='Group:', corner_radius=8)
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
        self.title('Manage Attendance')
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
        elif uid not in self.uids:
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
        elif uid not in self.uids:
            messagebox.showerror('Error', "Select a valid uID!")
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

#
#
#

class Signup(ctk.CTkToplevel):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main = main
        self.geometry("500x200")
        self.title('Register')
        self.resizable(False,False)
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=16)
        
        self.signup_widgets()
    
    def signup_widgets(self):
        
        
        #   widgets
        suser_label=ctk.CTkLabel(self, text='Enter Username:', font=self.my_font, corner_radius=8)
        suser_label.place(relx=0.05, rely=0.1, relwidth=0.29, relheight=0.2)
        
        self.suser_entry=ctk.CTkEntry(self, font=self.my_font)
        self.suser_entry.place(relx=0.39, rely=0.1, relwidth=0.56, relheight=0.2)
                
        spassword_label=ctk.CTkLabel(self, text='Enter Password:', font=self.my_font, corner_radius=8)
        spassword_label.place(relx=0.05, rely=0.4, relwidth=0.29, relheight=0.2)
        
        self.spassword_entry=ctk.CTkEntry(self, font=self.my_font, show='*')
        self.spassword_entry.place(relx=0.39, rely=0.4, relwidth=0.56, relheight=0.2)
        
        button=ctk.CTkButton(self, text='Submit', font=self.my_font, command=self.user_signup)
        button.place(relx=0.39, rely=0.7, relwidth=0.56, relheight=0.2)
        
    def user_signup(self):
        susername = self.suser_entry.get()
        spassword = self.spassword_entry.get()
        
        if not (susername and spassword):
            messagebox.showerror('Error', 'Enter all fields.')
        elif " " in spassword:
            messagebox.showerror('Error', "Invalid characters in password!")
        elif " " in susername:
            messagebox.showerror('Error', "Invalid characters in Username!")
        elif (len(susername) < 5) or (len(susername) > 20):
            messagebox.showerror('Error', 'Username must be between 5 and 20 characters.')
        elif len(spassword) < 8:
            messagebox.showerror('Error', 'Password must be at least 8 characters long.')
        elif auth.check_user(susername):
            messagebox.showerror('Error', 'User already exists.')
        else:
            auth.insert_user(susername, spassword)
            messagebox.showinfo('Success!', 'You registered.')
            self.main.forget_auth_frame()
            

#
#
#

class Login(ctk.CTkToplevel):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main = main
        self.geometry("500x200")
        self.title('Log-in')
        self.resizable(False,False)
        
        self.my_font = ctk.CTkFont(family="Ubuntu Sans Bold", size=16)
        
        self.login_widgets()
    
    def login_widgets(self):
        
        
        #   widgets
        luser_label=ctk.CTkLabel(self, text='Enter Username:', font=self.my_font, corner_radius=8)
        luser_label.place(relx=0.05, rely=0.1, relwidth=0.29, relheight=0.2)
        
        self.luser_entry=ctk.CTkEntry(self, font=self.my_font)
        self.luser_entry.place(relx=0.39, rely=0.1, relwidth=0.56, relheight=0.2)
                
        lpassword_label=ctk.CTkLabel(self, text='Enter Password:', font=self.my_font, corner_radius=8)
        lpassword_label.place(relx=0.05, rely=0.4, relwidth=0.29, relheight=0.2)
        
        self.lpassword_entry=ctk.CTkEntry(self, font=self.my_font, show='*')
        self.lpassword_entry.place(relx=0.39, rely=0.4, relwidth=0.56, relheight=0.2)
        
        button=ctk.CTkButton(self, text='Submit', font=self.my_font, command=self.user_login)
        button.place(relx=0.39, rely=0.7, relwidth=0.56, relheight=0.2)
        
    def user_login(self):
        lusername = self.luser_entry.get()
        lpassword = self.lpassword_entry.get()
        
        if not (lusername and lpassword):
            messagebox.showerror('Error', 'Enter all fields.')
        elif " " in lpassword:
            messagebox.showerror('Error', "Invalid characters in password!")
        elif " " in lusername:
            messagebox.showerror('Error', "Invalid characters in Username!")
        elif len(lusername) <= 3:
            messagebox.showerror('Error', 'Username too short.')
        elif len(lusername) > 20:
            messagebox.showerror('Error', 'Username too long.')
        elif len(lpassword) < 8:
            messagebox.showerror('Error', 'Password too short.')
        elif auth.login_check(lusername, lpassword) == False:
            messagebox.showerror('Error', 'Wrong username or Password.')
        elif auth.login_check(lusername, lpassword):
            messagebox.showinfo('Success!', 'You logged in.')
            self.main.forget_auth_frame()



#   launch the app
App()