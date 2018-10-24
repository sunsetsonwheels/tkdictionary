from tkinter import Tk, messagebox, scrolledtext, Menu, Toplevel, Label, StringVar, NW, NE, CENTER, END
from tkinter.ttk import Entry, Button, Radiobutton
from yaml import safe_load, dump
from os.path import isfile, abspath
from os import execl
from sys import executable, argv
from requests import get as rget
from requests import ConnectionError
from threading import Thread

def start_thread(function):
    t = Thread(target=function)
    t.start()

def print_to_textbox(message):
    dictionaryTextView.insert(END, message + "\n")
def clear_textbox():
    dictionaryTextView.delete('1.0', END)

def checkNetwork():
    turl='http://www.google.com/'
    tout=5
    try:
        testGoogle = rget(url=turl, timeout=tout)
        messagebox.showinfo("", "The network is available.\nTkDictionary should work.")
    except ConnectionError:
        messagebox.showerror("", "The network is unavailable.\nTkDictionary will not work.")

def about():
    aboutWindow = Toplevel()
    aboutWindow["bg"] = "white"
    aboutWindow.wm_resizable(False, False)
    aboutWindow.focus_set()
    aboutWindow.grab_set()
    appName_label = Label(aboutWindow, text="TkDictionary v.0.8", font=('Segoe UI Bold', 18))
    appName_label["bg"] = "white"
    appName_label.pack()
    aboutMessage = "A dictionary application written in Python that uses\nGoogle or Urban Dictionary.\n\n(C) Nguyen Thanh Nam (jkelol111) 2018\nLicensed under the MIT license."
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
    dictChoice = StringVar()
    langChoice = StringVar()
    langChoice.set(lang)
    themeChoice = StringVar()
    def restartAppToApplyChanges():
        restart = messagebox.askyesno("", "The app will restart for the changes to take effect.\nDo you want to restart the app now?")
        if restart == True:
            execl(executable, abspath(__file__), *argv)
        elif restart == False:
            messagebox.showwarning("", "Please save your work and restart the app as soon as possible for changes to take effect.")
    def resetSettings():
        settingsWindow.grab_release()
        resetY = messagebox.askyesno("", "This will reset TkDictionary to defaults. Do you want to continue?")
        if resetY == True:
            settingsWindow.destroy()
            with open("appcfg.yml", 'w') as config_file:
                config_contents = dict(language='en', source='googledictionary', theme="light")
                dump(config_contents, config_file)
            restartAppToApplyChanges()   
        elif resetY == False:
            settingsWindow.focus_set()
            settingsWindow.grab_set()         
    def saveSettings():
        settingsWindow.destroy()
        with open("appcfg.yml", 'w') as config_file:
            config_contents = dict(language=langChoice.get(), source=dictChoice.get(), theme=themeChoice.get())
            dump(config_contents, config_file)
        restartAppToApplyChanges()
    settingsWindow = Toplevel()
    settingsWindow["bg"] = "white"
    settingsWindow.wm_resizable(False, False)
    settingsWindow.focus_set()
    settingsWindow.grab_set()
    sourceLabel = Label(settingsWindow, text="Dictionary source:", font=("Segoe UI", 16))
    sourceLabel["bg"] = "white"
    sourceLabel.pack(anchor=NW)
    wikiRadioButton = Radiobutton(settingsWindow, text="Google Dictionary (not working)", variable=dictChoice, value="googledictionary")
    wikiRadioButton.pack(anchor=NW, padx=10)
    urbanRadioButton = Radiobutton(settingsWindow, text="Urban Dictionary", variable=dictChoice, value="urbandictionary")
    urbanRadioButton.pack(anchor=NW, padx=10)
    if src == "googledictionary":
        wikiRadioButton.invoke()
    elif src == "urbandictionary":
        urbanRadioButton.invoke()
    else:
        pass
    disclaimerLabel = Label(settingsWindow, text="All content belongs to their respective owners. Please agree to their respective terms and conditions before use.", font=("Segoe UI", 7))
    disclaimerLabel["bg"] = "white"
    disclaimerLabel.pack(anchor=NW)
    langLabel = Label(settingsWindow, text="Dictionary language:", font=("Segoe UI", 16))
    langLabel["bg"] = "white"
    langLabel.pack(anchor=NW)
    langInput = Entry(settingsWindow, textvariable=langChoice)
    langInput.pack(anchor=NW, padx=10)
    langInstructLabel1 = Label(settingsWindow, text="This option only works with Google Dictionary. Not all languages available.", font=("Segoe UI", 7))
    langInstructLabel1["bg"] = "white"
    langInstructLabel1.pack(anchor=NW)
    langInstructLabel2 = Label(settingsWindow, text="Example: English = en, Italian = it, French = fr, etc.", font=("Segoe UI", 7))
    langInstructLabel2["bg"] = "white"
    langInstructLabel2.pack(anchor=NW)
    themeLabel = Label(settingsWindow, text="App theme (not working):", font=("Segoe UI", 16))
    themeLabel["bg"] = "white"
    themeLabel.pack(anchor=NW)
    lightRadioButton = Radiobutton(settingsWindow, text="Light", variable=themeChoice, value="light")
    lightRadioButton.pack(anchor=NW, padx=10)
    darkRadioButton = Radiobutton(settingsWindow, text="Dark", variable=themeChoice, value="dark")
    darkRadioButton.pack(anchor=NW, padx=10)
    if theme == "light":
        lightRadioButton.invoke()
    elif theme == "dark":
        darkRadioButton.invoke()
    else:
        pass
    saveSettingsButton = Button(settingsWindow, text="Save settings", command=saveSettings)
    saveSettingsButton.pack()
    resetSettingsButton = Button(settingsWindow, text="Reset settings", command=resetSettings)
    resetSettingsButton.pack()
    mainWindow.update_idletasks()
    settingsWindow.update_idletasks()
    w = settingsWindow.winfo_width()
    h = settingsWindow.winfo_height()
    x = mainWindow.winfo_width()/2 + mainWindow.winfo_x()-218
    y = mainWindow.winfo_height()/2 + mainWindow.winfo_y()-130
    settingsWindow.geometry("%dx%d+%d+%d" % (w, h, x, y))
    settingsWindow.mainloop()

def searchWord():
    word = wordEntry.get()
    clear_textbox()
    print_to_textbox("Loading, please wait...")
    if src == "googledictionary":
        parameters = {"define": word, "lang": lang}
        result = rget("https://googledictionaryapi.eu-gb.mybluemix.net/", params=parameters).json()
        from pprint import pprint
        pprint(result)
        clear_textbox()
        print_to_textbox(word)
        print_to_textbox("\nPhonetic: "+str(result["phonetic"]))
    elif src == "urbandictionary":
        parameters2 = {"term": word}
        result2 = rget("http://api.urbandictionary.com/v0/define", params=parameters2).json()
        clear_textbox()
        print_to_textbox(word)
        print_to_textbox("\nMost-voted definition:\n"+result2["list"][0]["definition"])
        print_to_textbox("\nExamples:\n"+result2["list"][0]["example"])
        print_to_textbox("\nBy user: "+result2["list"][0]["author"]+"        "+"Votes: UP: "+str(result2["list"][0]["thumbs_up"])+" DOWN: "+str(result2["list"][0]["thumbs_down"]))

if not isfile("appcfg.yml"):
    createConfig = messagebox.askquestion("TkDictionary Error", "We couldn't find your configuration file. Do you want to create one?")
    if createConfig == "yes":
        try:
            with open("appcfg.yml", 'w') as config_file:
                config_contents = dict(language='en', source='googledictionary', theme="light")
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
        theme = config_contents["theme"]
    except Exception as e:
        print(str(e))

mainWindow = Tk()
mainWindow.title("TkDictionary")
mainWindow.wm_resizable(False, False)
mainWindow["bg"] = "white"
mainWindow.focus_get()

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

if src == "googledictionary":
    searchButton_text = "Search Google Dictionary..."
elif src == "urbandictionary":
    searchButton_text = "Search Urban Dictionary..."
else:
    searchButton_text = "Search null..."
searchButton = Button(mainWindow, text=searchButton_text, command=lambda: start_thread(searchWord))
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