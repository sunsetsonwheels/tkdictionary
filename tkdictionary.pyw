from tkinter import Tk, messagebox, scrolledtext, Menu, Toplevel, Label, StringVar, NW, NE, CENTER, END, DISABLED
from tkinter.ttk import Entry, Button, Radiobutton
from os.path import abspath
from os import execl
from sys import executable, argv
from requests import get as rget
from requests import ConnectionError
from threading import Thread
from wiktionaryparser import WiktionaryParser
from localStoragePy import localStoragePy
import json

localStorage = localStoragePy("me.jkelol111.tkdictionary", "text")

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
    aboutWindow.wm_resizable(False, False)
    aboutWindow.focus_set()
    aboutWindow.grab_set()
    appName_label = Label(aboutWindow, text="TkDictionary v.0.8")
    appName_label.pack()
    aboutMessage = "A dictionary application written in Python that uses\nWiki or Urban Dictionary.\n\n(C) Nguyen Thanh Nam (jkelol111) 2018\nLicensed under the MIT license."
    aboutMessage_label = Label(aboutWindow, text=aboutMessage)
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
            config_contents = dict(language='english', source='urbandictionary', theme="light")
            localStorage.setItem("config.json", json.dumps(config_contents))
            restartAppToApplyChanges()   
        elif resetY == False:
            settingsWindow.focus_set()
            settingsWindow.grab_set()         
    def saveSettings():
        settingsWindow.destroy()
        config_contents = dict(language=langChoice.get(), source=dictChoice.get(), theme=themeChoice.get())
        localStorage.setItem("config.json", json.dumps(config_contents))
        restartAppToApplyChanges()
    settingsWindow = Toplevel()
    settingsWindow.wm_resizable(False, False)
    settingsWindow.focus_set()
    settingsWindow.grab_set()
    sourceLabel = Label(settingsWindow, text="Dictionary source:")
    sourceLabel.pack(anchor=NW)
    wikiRadioButton = Radiobutton(settingsWindow, text="Wiktionary", variable=dictChoice, value="wiktionary")
    wikiRadioButton.pack(anchor=NW, padx=10)
    urbanRadioButton = Radiobutton(settingsWindow, text="Urban Dictionary", variable=dictChoice, value="urbandictionary")
    urbanRadioButton.pack(anchor=NW, padx=10)
    if src == "wiktionary":
        wikiRadioButton.invoke()
    elif src == "urbandictionary":
        urbanRadioButton.invoke()
    else:
        pass
    disclaimerLabel = Label(settingsWindow, text="All content belongs to their respective owners. Please agree to their respective terms and conditions before use.")
    disclaimerLabel.pack(anchor=NW)
    langLabel = Label(settingsWindow, text="Dictionary language:")
    langLabel.pack(anchor=NW)
    langInput = Entry(settingsWindow, textvariable=langChoice)
    langInput.pack(anchor=NW, padx=10)
    langInstructLabel1 = Label(settingsWindow, text="This option only works with Wiktionary. Not all languages available.")
    langInstructLabel1.pack(anchor=NW)
    langInstructLabel2 = Label(settingsWindow, text="Example: English = english, Italian = italian, French = french, etc.")
    langInstructLabel2.pack(anchor=NW)
    themeLabel = Label(settingsWindow, text="App theme (not working):")
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
    if src == "wiktionary":
        parser = WiktionaryParser()
        result = parser.fetch(word, language=lang)
        clear_textbox()
        from pprint import pprint
        pprint(result)
        print_to_textbox(word)
        print_to_textbox("\nMeanings:")
        for n in result[0]["definitions"]:
            print(len(n))
            for i in result[0]["definitions"][len(n)]["text"]:
                print_to_textbox(i)
    elif src == "urbandictionary":
        parameters2 = {"term": word}
        result2 = rget("http://api.urbandictionary.com/v0/define", params=parameters2).json()
        clear_textbox()
        print_to_textbox(result2["list"][0]["word"])
        print_to_textbox("\nMost-voted definition:\n"+result2["list"][0]["definition"])
        print_to_textbox("\nExamples:\n"+result2["list"][0]["example"])
        print_to_textbox("\nBy user: "+result2["list"][0]["author"]+"        "+"Votes: UP: "+str(result2["list"][0]["thumbs_up"])+" DOWN: "+str(result2["list"][0]["thumbs_down"]))
    else:
        clear_textbox()
        errmessage = "Dictionary with name null not found. Check your settings in 'Actions & others' above!"
        print_to_textbox(errmessage)
        messagebox.showerror("TkDictionary Error", errmessage)

if not localStorage.getItem("config.json"):
    createConfig = messagebox.askquestion("TkDictionary Error", "We couldn't find your configuration file. Do you want to create one?")
    if createConfig == "yes":
        try:
            localStorage.setItem("config.json", json.dumps(dict(language='en', source='urbandictionary', theme="light")))
        except:
            messagebox.showerror("TkDictionary error", "Could not make config file. The app will now quit.")
            exit()
        execl(executable, abspath(__file__), *argv) 
    else:
        messagebox.showerror("TkDictionary error", "We couldn't find your configuration file. The app will now exit.")
        exit()
else:
    try:
        config_contents = json.loads(localStorage.getItem("config.json"))
        lang = config_contents["language"]
        src = config_contents["source"]
        theme = config_contents["theme"]
    except Exception as e:
        print(str(e))

mainWindow = Tk()
mainWindow.title("TkDictionary")
mainWindow.wm_resizable(False, False)
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

wordEntry = Entry(mainWindow, justify=CENTER, width=mainWindow.winfo_reqwidth()-160)
wordEntry.focus_set()
wordEntry.pack()

if src == "wiktionary":
    searchButton_text = "Search Wiktionary..."
elif src == "urbandictionary":
    searchButton_text = "Search Urban Dictionary..."
else:
    searchButton_text = "Config Error! Check settings!"
searchButton = Button(mainWindow, text=searchButton_text, command=lambda: start_thread(searchWord))
searchButton.pack()

dictionaryTextView = scrolledtext.ScrolledText(mainWindow)
dictionaryTextView.pack()

mainWindow.config(menu=menubar)

mainWindow.update_idletasks()
w = mainWindow.winfo_reqwidth()
h = mainWindow.winfo_reqheight()
x = (mainWindow.winfo_screenwidth() - w) / 2
y = (mainWindow.winfo_screenheight() - h) / 2
mainWindow.geometry("%dx%d+%d+%d" % (w, h, x, y))

mainWindow.mainloop()