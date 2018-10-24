from tkinter import Tk, messagebox, scrolledtext, Menu, Toplevel, Label, NW, NE, CENTER
from tkinter.ttk import Entry, Button, Radiobutton
from yaml import safe_load, dump
from os.path import isfile, abspath
from os import execl
from sys import executable, argv
from requests import get as rget
from requests import ConnectionError

def about():
    aboutWindow = Toplevel()
    aboutWindow["bg"] = "white"
    aboutWindow.wm_resizable(False, False)
    aboutWindow.focus_set()
    aboutWindow.grab_set()
    appName_label = Label(aboutWindow, text="TkDictionary v.0.1", font=('Segoe UI Bold', 18))
    appName_label["bg"] = "white"
    appName_label.pack()
    aboutMessage = "A dictionary application written in Python that uses\nWiktionary or Urban Dictionary.\n\n(C) Nguyen Thanh Nam (jkelol111) 2018\nLicensed under the MIT license."
    aboutMessage_label = Label(aboutWindow, text=aboutMessage, font=("Segoe UI", 12))
    aboutMessage_label["bg"] = "white"
    aboutMessage_label.pack()
    ok_button = Button(aboutWindow, text="OK", command=lambda: aboutWindow.destroy())
    ok_button.pack()
    mainWindow.update_idletasks()
    aboutWindow.update_idletasks()
    w = aboutWindow.winfo_width()
    h = aboutWindow.winfo_height()
    x = mainWindow.winfo_width()/2 + mainWindow.winfo_x()-180
    y = mainWindow.winfo_height()/2 + mainWindow.winfo_y()-80
    aboutWindow.geometry("%dx%d+%d+%d" % (w, h, x, y))
    aboutWindow.mainloop()

def settings():
    settingsWindow = Toplevel()
    settingsWindow["bg"] = "white"
    settingsWindow.wm_resizable(False, False)
    settingsWindow.focus_set()
    settingsWindow.grab_set()
    sourceLabel = Label(settingsWindow, text="Dictionary source:", font=("Segoe UI", 13))
    sourceLabel.pack(anchor=NE)
    wikiRadioButton = Radiobutton(settingsWindow, text="WikDictionary")
    wikiRadioButton.pack(anchor=NE)
    settingsWindow.mainloop()

def checkNetwork():
    turl='http://www.google.com/'
    tout=5
    try:
        testGoogle = rget(url=turl, timeout=tout)
        messagebox.showinfo("", "The network is available.\nTkDictionary should work.")
    except ConnectionError:
        messagebox.showerror("", "The network is unavailable.\nTkDictionary will not work.")

if not isfile("appcfg.yml"):
    createConfig = messagebox.askquestion("TkDictionary Error", "We couldn't find your configuration file. Do you want to create one?")
    if createConfig == "yes":
        try:
            with open("appcfg.yml", 'w') as config_file:
                config_contents = dict(language='en', source='wiktionary', theme="light")
                dump(config_contents, config_file)
        except:
            messagebox.showerror("TkDictionary error", "Could not make config file. The app will now quit.")
            exit()
        execl(executable, abspath(__file__), *argv) 
    else:
        messagebox.showerror("TkDictionary error", "We couldn't find your configuration file. The app will now exit.")
        exit()
else:
    try:
        with open("appcfg.yml", 'r') as config_file:
            config_contents = safe_load(config_file)
        lang = config_contents["language"]
        src = config_contents["source"]
    except Exception as e:
        print(str(e))

mainWindow = Tk()
mainWindow.title("TkDictionary")
mainWindow.wm_resizable(False, False)
mainWindow["bg"] = "white"

menubar = Menu(mainWindow)
actionMenu = Menu(menubar, tearoff=0)
actionMenu.add_command(label="Test network activity...", command=checkNetwork)
actionMenu.add_separator()
actionMenu.add_command(label="Settings...", command=settings)
menubar.add_cascade(label="Actions & others", menu=actionMenu)
aboutMenu = Menu(menubar, tearoff=0)
aboutMenu.add_command(label="About TkDictionary...", command=about)
menubar.add_cascade(label="About & help", menu=aboutMenu)

wordEntry = Entry(mainWindow, font=("Segoe UI Bold", 13), justify=CENTER, width=mainWindow.winfo_reqwidth()-160)
wordEntry.focus_set()
wordEntry.pack()

if src == "wiktionary":
    searchButton_text = "Search Wiktionary..."
elif src == "urbandictionary":
    searchButton_text = "Search Urban Dictionary..."
searchButton = Button(mainWindow, text=searchButton_text)
searchButton.pack()

dictionaryTextView = scrolledtext.ScrolledText(mainWindow, font=("Segoe UI", 12))
dictionaryTextView.pack()

mainWindow.config(menu=menubar)

mainWindow.update_idletasks()
w = mainWindow.winfo_reqwidth()
h = mainWindow.winfo_reqheight()
x = (mainWindow.winfo_screenwidth() - w) / 2
y = (mainWindow.winfo_screenheight() - h) / 2
mainWindow.geometry("%dx%d+%d+%d" % (w, h, x, y))

mainWindow.mainloop()