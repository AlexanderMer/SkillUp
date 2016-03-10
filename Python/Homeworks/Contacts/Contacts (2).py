from tkinter import *
from tkinter import filedialog 
import pickle


root = Tk()
root.resizable(0,0)
menubar = Menu(root)
menubar.add_command(label="Hello!")
menubar.add_command(label="Quit!")
CONTACTS = []

def show_help():
    help_win = Tk()
    t = Text(help_win, width=15, height=15, font="Arial 10", bg="#00BD56")
    t.pack()
    t.insert(INSERT, "Help me!")
    t.config(state="disabled")

def save_it():
    ftypes = [('Contact files', '*.cnts'), ('All files', '*')]
    dlg = filedialog.SaveAs(filetypes = ftypes)
    fl = dlg.show()
    pickle.dump(CONTACTS, open(fl, 'wb'))

def init_root():
    global btn_new
    global txt_box
     #  Menu
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=custom_load)
    filemenu.add_command(label="Save", command=save_it)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=show_help)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)


    Label(root, text="Name", font="Arial 15").grid(row=0, column=0)
    Label(root, text="Adress", font="Arial 15", padx=20).grid(row=0, column=1)
    Label(root, text="Phone", font="Arial 15").grid(row=0, column=2)
    txt_box = Text(root, bg="cyan", state="disabled", width=40, height=5)
    txt_box.grid(row=1, column=0, columnspan=5)
    btn_new = Button(root, text="Add New", command=init_new_window)
    btn_new.grid(row=2, column=1)
    load()

    scrollbar = Scrollbar(root)
    scrollbar.grid(row=1, column=5, rowspan=3, sticky=N+S)
    txt_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=txt_box.yview)
    load()

def init_new_window():
    global bla
    global entr_name
    global ent_addr
    global entr_phone


    btn_new.config(state="disabled")
    bla = Tk()
    bla.resizable(0,0)
    bla.protocol("WM_DELETE_WINDOW", on_close)
    bla.title("New Contact")
    Label(bla, text="Name", padx=50).grid(row=0, column=0)
    Label(bla, text="Adress", padx=50).grid(row=0, column=1)
    Label(bla, text="Phone", padx=50).grid(row=0, column=2)
    entr_name = Entry(bla, width="30")
    entr_name.grid(row=1, column=0)
    ent_addr = Entry(bla, width="30")
    ent_addr.grid(row=1, column=1)
    entr_phone = Entry(bla, width="30")
    entr_phone.grid(row=1, column=2)
    btn_save = Button(bla, text="Save", command=add_new, bg="green")
    btn_save.grid(row=2, column=2)
    btn_cancel = Button(bla, text="Cancel", command=cancel, bg="red")
    btn_cancel.grid(row=2, column=0)

def add_new():
    global entr_name
    global entr_addr
    global ent_phone

    CONTACTS.append([entr_name.get(),ent_addr.get() ,entr_phone.get()])
    pickle.dump(CONTACTS, open('contacts.cnts', 'wb'))
    print('added')
    bla.destroy()
    update_contacts_diplay()
    btn_new.config(state="normal")

def load(file = 'Contacts.cnts'):
    global CONTACTS
    try:
        CONTACTS = pickle.load(open(file, 'rb'))
        update_contacts_diplay()
    except FileNotFoundError:
        print('No Contacts to load')

def cancel():
    global  bla
    bla.destroy()

def update_contacts_diplay():
    global txt_box
    txt_box.config(state="normal")
    txt_box.delete("1.0", END)
    for c in CONTACTS:
        txt_box.insert(INSERT, c[0] + " " * (15 - len(c[0])))
        txt_box.insert(INSERT, c[1] + " " * (15 - len(c[1])))
        txt_box.insert(INSERT, c[2] + "\n")
    txt_box.config(state="disabled")

def on_close():
    btn_new.config(state="normal")
    bla.destroy()

def custom_load():
    ftypes = [('Contact files', '*.cnts'), ('All files', '*')]
    dlg = filedialog.Open(filetypes = ftypes)
    fl = dlg.show()
    load(fl)

init_root()
root.mainloop()
