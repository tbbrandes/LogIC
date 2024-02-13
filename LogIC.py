import time
import webbrowser
import os
from os.path import expanduser, isfile
import re
import configparser
#import chime
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilenames
import customtkinter as ctk

# Set global vars for timestamps
def get_time(pick):
    time_tpl = time.localtime()
    time_str = time.strftime("%d.%m.%Y %H:%M:%S", time_tpl)
    time_filename = time.strftime("%d%m%Y_%H%M%S", time_tpl)
    if pick == "tstr":
        return time_str
    if pick == "tfn":
        return time_filename

# Get home diretory of user

work_dir=os.path.dirname(os.path.realpath(__file__))
home = expanduser("~")
config = configparser.ConfigParser()
config_file=f"{work_dir}\\user_config.ini"

# Write the config file if doensn't exist

if os.path.isfile(config_file) != True:
    config.add_section('default')
    config.set('default', 'default-dir', f'{home}')
    config.set('default', 'theme', 'System')
    config.set('default', 'scale', '100')
    config.set('default', 'color', 'blue')
    config.set('default', 'language', 'English')
    config.add_section('filter')
    config.set('filter', 'default-dir', f'{home}')
    config.add_section('settings')
    config.set('settings', 'theme', 'System')
    config.set('settings', 'scale', '100')
    config.set('settings', 'color', 'blue')
    config.set('settings', 'language', 'English')
    with open(rf"{config_file}", 'w') as user_config:
        config.write(user_config)

elif os.path.isfile(config_file) == True:
    config_var = configparser.ConfigParser()
    config_var.read(f"{config_file}")
    u_filter = config_var["filter"]
    u_set = config_var["settings"]
    default_dir = u_filter["default-dir"]
    app_theme = u_set["theme"]
    app_scale = int(u_set["scale"])
    app_color = u_set["color"]
    app_lang = u_set["language"]

    # Set fallback default values
if default_dir is None:
    default_dir=home
if app_scale is None:
    app_scale=100
if app_lang is None:
    app_lang="English" 
if app_theme is None:
    app_theme="System" 
ctk.set_appearance_mode(app_theme)  # Modes: "System" (standard), "Dark", "Light"
if app_color is None:
    app_color="blue"
ctk.set_default_color_theme(app_color)  # Themes: "blue" (standard), "green", "dark-blue"

 
url="www.belobrandes.org" # Link to documentation
license_info=f"{work_dir}\\license.txt"



class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("")
        self.geometry("500x400") 
        self.additional_textbox = ctk.CTkTextbox(self, width = 500)
        self.additional_textbox.grid(sticky="nsew")
        self.additional_textbox.pack(expand=True, fill=tk.BOTH)
        self.lift()
        self.attributes('-topmost',True)
        #self.after_idle(self.attributes,'-topmost',False)

    

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("LogIC")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar with frame with logo
        self.sidebar_frame = ctk.CTkFrame(self, width = 40, corner_radius = 0, fg_color="transparent")
        self.sidebar_frame.grid(row = 0, column = 0, sticky = "n")
        self.sidebar_frame.grid_rowconfigure(4, weight = 1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text = "LogIC", font = ctk.CTkFont(size = 20, weight = "bold"))
        self.logo_label.grid(row = 0, column = 0, padx = 0, pady = (10, 10))
        
        # create tabs
        self.tabview = ctk.CTkTabview(self, width = 250, height = 210)
        self.tabview.grid(row = 0, column = 0, padx = (20, 0), pady = (40, 0), sticky = "new")
        self.tabview.add("Filter")
        self.tabview.add("Settings")
        self.tabview.add("Help")
        self.tabview.tab("Filter").grid_columnconfigure(0, weight = 1) 
        self.tabview.tab("Settings").grid_columnconfigure(0, weight = 1)

        # Filter Tab
        self.filtertab_label1 = ctk.CTkLabel(self.tabview.tab("Filter"), text = "Mode:", anchor="w")
        self.filtertab_label1.grid(row=0, column=0, padx = 10, pady = (0, 0), sticky = "nw")
        self.filtertab_menu1 = ctk.CTkOptionMenu(self.tabview.tab("Filter"), anchor="center",
                                                        values=["search", "monitor"],
                                                        command=self.change_app_mode)
        self.filtertab_menu1.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="ne")

        self.filtertab_label2 = ctk.CTkLabel(self.tabview.tab("Filter"), text="Default folder:", anchor="w")
        self.filtertab_label2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.filtertab_button1 = ctk.CTkButton(self.tabview.tab("Filter"), text="Change directory",
                                                          command=self.default_dir_button_event)
        self.filtertab_button1.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="ne")

        self.filtertab_label3 = ctk.CTkLabel(self.tabview.tab("Filter"), text="Search level:", anchor="w")
        self.filtertab_label3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.filtertab_menu3 = ctk.CTkOptionMenu(self.tabview.tab("Filter"), anchor="center", state="enabled",
                                                          values=["File", "Directory"],
                                                          command=self.change_app_level)
        self.filtertab_menu3.grid(row=2, column=0, padx=0, pady=(10, 0), sticky="ne")

        self.filtertab_switch_label = ctk.CTkLabel(self.tabview.tab("Filter"), text="Audio Alarm:", anchor="w")
        self.filtertab_switch_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.filtertab_switch = ctk.CTkSwitch(self.tabview.tab("Filter"), text="OFF",
                                                                             onvalue="ON", offvalue="OFF",
                                                                             command=self.filtertab_switch_event)
        self.filtertab_switch.grid(row=3, column=0, padx=0, pady=(10, 0), sticky="ne")

        #Settings Tab
        self.settingstab_label1 = ctk.CTkLabel(self.tabview.tab("Settings"), text="Appearance:", anchor="w")
        self.settingstab_label1.grid(row=0, column=0, padx=10, pady=(0, 0), sticky="nw")
        self.settingstab_menu1 = ctk.CTkOptionMenu(self.tabview.tab("Settings"),anchor="center",
                                                          values=["Light", "Dark", "System"],
                                                                       command=self.settingstab_menu1_event)
        self.settingstab_menu1.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="ne")

        self.settingstab_label2 = ctk.CTkLabel(self.tabview.tab("Settings"), text="UI Scaling:", anchor="w")
        self.settingstab_label2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.settingstab_menu2 = ctk.CTkOptionMenu(self.tabview.tab("Settings"), anchor="center",
                                                         values=["80%", "90%", "100%", "110%", "120%"],
                                                                        command=self.settingstab_menu2_event)
        self.settingstab_menu2.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="ne")

        self.settingstab_label3 = ctk.CTkLabel(self.tabview.tab("Settings"), text="Color:", anchor="w")
        self.settingstab_label3.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.settingstab_menu3 = ctk.CTkOptionMenu(self.tabview.tab("Settings"), anchor="center",
                                                         values=["blue", "green", "dark-blue"],
                                                                        command=self.settingstab_menu3_event)
        self.settingstab_menu3.grid(row=2, column=0, padx=0, pady=(10, 0), sticky="ne")

        self.settingstab_label4 = ctk.CTkLabel(self.tabview.tab("Settings"), text="Language:", anchor="w")
        self.settingstab_label4.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.settingstab_menu4 = ctk.CTkOptionMenu(self.tabview.tab("Settings"), state="disabled", anchor="center", 
                                                         values=["English", "Deutsch", "Português ", "Español ", "Türkçe"],
                                                                        command=self.settingstab_menu4_event)
        self.settingstab_menu4.grid(row=3, column=0, padx=0, pady=(10, 0), sticky="ne")

        # Help Tab

        self.helptab_label1 = ctk.CTkLabel(self.tabview.tab("Help"), text="LogIC Version: 1.0.0\nTimur Belo Brandes\n\n\n\n\n\n\n Report bugs to:\n hello@belobrandes.org")
        self.helptab_label1.grid(row=0, column=0, padx=50, pady=0)         
        self.helptab_button1 = ctk.CTkButton(self.tabview.tab("Help"), text="Documentation", width=138,
                                            command=lambda:self.open_documentation(url))
        self.helptab_button1.grid(row=0, column=0, padx=50, pady=(45, 0), sticky="n")
        self.helptab_button2 = ctk.CTkButton(self.tabview.tab("Help"), text="License", width=138,
                                                          command=lambda:self.open_seperate_textbox(license_info))
        self.helptab_button2.grid(row=0, column=0, padx=50, pady=(80, 0), sticky="n")

        # create scrollable list of directories

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Selected Files")
        self.scrollable_frame.grid(row=0, rowspan=3, column=0, padx=(20, 0), pady=(270, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        

        # create search bar and file explorer button
        self.entry_file = ctk.CTkEntry(self, placeholder_text=default_dir)
        self.entry_file.grid(row=0, column=1, padx=(200, 0), pady=(10, 10), sticky="new")

        self.findfile_button = ctk.CTkButton(master=self, text= "Select Files", fg_color="transparent", border_width=2, 
                                                                                      text_color=("gray10", "#DCE4EE"),
                                                                                 command=self.selectfiles_button_event)
        self.findfile_button.grid(row=0, column=3, padx=(20, 20), pady=(10, 10), sticky="new")

        self.export_button = ctk.CTkButton(master=self, text= "Export Report", fg_color="transparent", border_width=2, 
                                                                                      text_color=("gray10", "#DCE4EE"),
                                                                                      command=self.export_button_event)                                            
        self.export_button.grid(row=0, column=1, padx=(40, 0), pady=(10, 0), sticky="nw")


        # create filter entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter keyword")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(200, 0), pady=(20, 20), sticky="nsew")

        self.search_button_1 = ctk.CTkButton(master=self, text= "Search", fg_color="transparent", border_width=2, state="enabled" ,
                                                                                text_color=("gray10", "#DCE4EE"), hover="True",
                                                                                command=self.search_button_event)
        self.search_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.bind('<Return>', lambda event=None: self.search_button_1.invoke())

        self.date_filter_button = ctk.CTkButton(master=self, text= "Filter dates", fg_color="transparent", border_width=2, state="disabled",
                                                                                         text_color=("gray10", "#DCE4EE"))
                                                       
                                                        
                                                        
        self.date_filter_button.grid(row=3, column=1, padx=(40, 0), pady=(20, 20), sticky="sw")

        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, rowspan=3, column= 1, columnspan=3, padx=(20, 0), pady=(50, 0), sticky="nsew")
        self.textbox.insert("0.0", f" [ {get_time("tstr")} ] - started LogIC Version 1.0.0  \n\n")

        # set default values
        
        self.settingstab_menu1.set(app_theme)
        self.settingstab_menu2.set(f"{app_scale}%")
        self.settingstab_menu3.set(app_color)
        self.filtertab_menu1.set("search")
        self.filtertab_menu3.set("File")

        self.toplevel_window = None

        
    # Main functions

    def open_seperate_textbox(self, i_file):
       # if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
        self.toplevel_window = ToplevelWindow(self)
<<<<<<< Updated upstream
        #print ("element at the index 0 is: " , tup[0])
        with open(i_file) as ifile:
=======
        with open(i_file, "r") as ifile:
>>>>>>> Stashed changes
            while True:
                line = ifile.readline()
                if not line:
                    break
                self.toplevel_window.additional_textbox.insert(tk.END, line)
               

    def selectfiles_button_event(self):
        if  self.filtertab_menu3.get() == "File":
            fname = askopenfilenames(initialdir = default_dir, title = "Select Files", filetypes = (("Log File",
                                                                                "*.log*"),("all Files", "*.*")))
            if len(fname) == 0:
                return
            else:
                files_dir_list= []
                fname = {i : fname[i] for i, _ in enumerate(fname)}
                for index, key in enumerate(fname):
                        ifile_name = os.path.basename(fname[key])
                        i_file = fname[key]
                        

                        entry = ctk.CTkButton(master=self.scrollable_frame, text=f"{ifile_name}", text_color=("gray10", "#DCE4EE"),
                                                        fg_color=("gray70", "gray40"), border_width=1, 
                                                        border_color=("gray10", "#DCE4EE"), anchor="w",
                                                                    command=lambda i_file = i_file:self.open_seperate_textbox(i_file))
                        entry.grid(row=key, column=0, padx=10, pady=(0, 10), sticky="nsew")
                    
                        files_dir_list.append(i_file)
                

        if  self.filtertab_menu3.get() == "Directory":
            fdir = tk.filedialog.askdirectory()
            if fdir == "":
                return
            files_dir_list= []
            for count, d_fname in enumerate(os.listdir(fdir)):
                if d_fname.endswith(('.txt','.log')):
                    d_ffname=os.path.join(fdir, d_fname) 
                    entry = ctk.CTkButton(master=self.scrollable_frame, text=f"{d_fname}", text_color=("gray10", "#DCE4EE"),
                                                        fg_color=("gray70", "gray40"), border_width=1, 
                                                        border_color=("gray10", "#DCE4EE"), anchor="w",
                                                             command=lambda d_ffname = d_ffname:self.open_seperate_textbox(d_ffname))
                    entry.grid(row=count, column=0, padx=10, pady=(0, 10), sticky="nsew")
                    
                    files_dir_list.append(d_ffname)
        global files_dirlist
        files_dirlist = files_dir_list
                

    def search_button_event(self):
        keyword = self.entry.get()
        global files_dirlist
        if not files_dirlist:
            return

<<<<<<< Updated upstream
        if keyword is None:
            return    
        keyc = re.compile(keyword)
        self.textbox.tag_config("search", background="green")
        for current_file in files_dirlist:
            with open(current_file) as curfile:
                print ("test1")
                self.textbox.insert(tk.END, f" \n\n## Start of file: {current_file} ##\n\n")
                #self.textbox.tag_config("start", background="#EE0000")
                #self.textbox.tag_add("start", pos, "%s + %sc" % (pos, countVar.get()))
                print("test2")
                while True:
                    line = curfile.readline()
                    if not line:
                        self.textbox.insert(tk.END, f" ## End of file: {current_file} ##\n\n")
                        break
                    if keyc.search(line, re.I):
                        self.textbox.insert(tk.END, f"{line}")
        start_pos = "1.0"
        for tag in self.textbox.tag_names():
            self.textbox.tag_remove(tag, "1.0", 'end')
            countVar = tk.StringVar()
            while start_pos != 'end':
                pos = self.textbox.search(keyword, start_pos, stopindex='end', 
                count=countVar)
                start_pos =  "%s + %sc" % (pos, int(countVar.get())+1)
                self.textbox.tag_config("search", background="#EE0000")
                self.textbox.tag_add("search", pos, "%s + %sc" % (pos, countVar.get()))
=======
        #self.textbox.tag_config("search", background="green")
        self.textbox.delete("2.0", tk.END)
        if self.filtertab_menu1.get() == "search":
            if keyword == "" or keyword.isspace() is True:
                return    
            keyc = re.compile(keyword)
            for current_file in files_dirlist:
                with open(current_file, "r") as curfile:
                    self.textbox.insert(tk.END, f" \n\n## Start of file: {current_file} ##\n\n")
                    #self.textbox.tag_config("start", background="#EE0000")
                    #self.textbox.tag_add("start", pos, "%s + %sc" % (pos, countVar.get()))
                    while True:
                        line = curfile.readline()
                        if not line:
                            self.textbox.insert(tk.END, f" ## End of file: {current_file} ##\n\n")
                            break
                        if keyc.search(line, re.I):
                            self.textbox.insert(tk.END, f"{line}")
            start_pos = "1.0"
            for tag in self.textbox.tag_names():
                self.textbox.tag_remove(tag, "1.0", 'end')
                countVar = tk.StringVar()
                while start_pos != 'end':
                    pos = self.textbox.search(keyword, start_pos, stopindex='end', 
                    count=countVar)
                    start_pos =  "%s + %sc" % (pos, int(countVar.get())+1)
                    self.textbox.tag_config("search", background="#EE0000")
                    self.textbox.tag_add("search", pos, "%s + %sc" % (pos, countVar.get()))

        if self.filtertab_menu1.get() == "monitor":
            if keyword == "" or keyword.isspace() is True:
                self.textbox.insert(tk.END, f"\n\n [ {get_time("tstr")} ] - started monitoring")
               # for current_file in files_dirlist:
                #with open(files_dirlist, "r") as curfile:
                  #  curfile.seek(0,2)
                   # while True:
                  #      line = curfile.readline()
                   #     if not line:
                  #          time.sleep(0.1)
                  #          continue
                  #      yield line
            else:
                self.textbox.insert(tk.END, f"\n\n [ {get_time("tstr")} ] - started monitoring for string: {keyword}")
>>>>>>> Stashed changes
        

         

    def export_button_event(self):
        savefname = None
        savefname = tk.filedialog.asksaveasfilename(initialdir = default_dir,
                                         title = "Save as",
                                          defaultextension = ".txt",
                                          initialfile = f"LogIC_export_{get_time("tfn")}",
                                          filetypes = (("Text File",
                                                        ".txt"),
                                                       ("all Files",
                                                        "*.*")))
        if savefname is None or savefname == '':
            return
        else:
            textbox_content = str(self.textbox.get(1.0, tk.END)) 
            with open(savefname ,"w+")as ofile:
                ofile.write(textbox_content)


    def alarm_sound(self):
       # chime.warning
        pass
        

    def write_config(self, sect, ent, val):
        config.read(config_file)
        sect_val = config[sect]
        sect_val[ent] = val
        with open(rf"{config_file}", 'w') as config_f:
            config.write(config_f)

    # Filtertab functions
    
    def change_app_mode(self, mode):
        if mode == "search":
            
            self.filtertab_menu3.configure(state="enabled")
            self.date_filter_button.configure(state="enabled")
            self.search_button_1.configure(text="Search")
            
        if mode == "monitor":

            self.filtertab_menu3.set("File")
            self.findfile_button.configure(text="Select Files")
            self.filtertab_menu3.configure(state="disabled")
            self.date_filter_button.configure(state="disabled")
            self.search_button_1.configure(text="Start")
        
        
    def change_app_level(self, level):
        if level == "File":
            self.findfile_button.configure(text="Select Files")
        if level == "Directory":
             self.findfile_button.configure(text="Select Folder")

    def default_dir_button_event(self):
         selected_dir = tk.filedialog.askdirectory()
         if selected_dir == () or selected_dir == "":
          return
         global default_dir
         default_dir = selected_dir
         self.entry_file.configure(placeholder_text=f" Default folder: {default_dir}")
         self.write_config('filter', 'default-dir', f'{default_dir}' )
           


    def filtertab_switch_event(self):
        switch_val=(self.filtertab_switch.get())
        if switch_val == "ON":
            self.filtertab_switch.configure(text="ON") 
        if switch_val == "OFF":
            self.filtertab_switch.configure(text="OFF")
        #with open("log.log" 'r') as f:
        #    for line in f:
        #        if "O:NVS:VOICE" in line:
         #           print line
                
    # Settingstab functions
                
    def settingstab_menu1_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.write_config('settings', 'theme', new_appearance_mode )

        
    
    def settingstab_menu2_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        new_scaling_float = new_scaling_float * 100
        new_scaling_float=int(new_scaling_float)
        self.write_config('settings', 'scale', str(new_scaling_float) )


    def settingstab_menu3_event(self, color: str):
        ctk.set_default_color_theme(color)
        self.write_config('settings', 'color', color )
                            
    def settingstab_menu4_event(self, lang: str):
        self.write_config('settings', 'language', lang )

    # Helptab functions
    def open_documentation(self, url):
        webbrowser.open(url)
        

<<<<<<< Updated upstream
      
    
        
    
   # Tool functions
    #def pygrep ():
        #for line in sys.stdin:
	   #     regex_pattern = sys.argv[1]
	    ##    pattern = re.compile(regex_pattern)
	      #  if pattern.search(line):
	    	#    sys.stdout.write(line)
    
    
    #    self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
     #   self.checkbox_3.configure(state="disabled")
      #  self.checkbox_1.select()
       # self.scrollable_frame_switches[0].select()
#        self.scrollable_frame_switches[4].select()
#        self.radio_button_3.configure(state="disabled")
#        self.appearance_mode_optionemenu.set("Dark")
#        self.set_default_color_theme(new_color)
#        self.scaling_optionemenu.set("100%")
#        self.optionmenu_1.set("CTkOptionmenu")
#        self.combobox_1.set("CTkComboBox")
#        self.slider_1.configure(command=self.progressbar_2.set)
#        self.slider_2.configure(command=self.progressbar_3.set)
#        self.progressbar_1.configure(mode="indeterminnate")
#        self.progressbar_1.start()
#        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
#        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
#        self.seg_button_1.set("Value 2")
        
=======
    app_scale = int(app_scale) / 100
    ctk.set_widget_scaling(app_scale) 
    
>>>>>>> Stashed changes
if __name__ == "__main__":
    app = App()
    app.mainloop()
    