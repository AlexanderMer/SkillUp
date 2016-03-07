from tkinter import *
import pickle


root = Tk()
CONTACTS = []


def init_root():
    global btn_new
    global txt_box
    txt_box = Text(root, bg="grey", state="disabled", width=50)
    txt_box.pack()
    btn_new = Button(root, text="Add New", command=init_new_window)
    btn_new.pack()
    load()

def init_new_window():
    global bla
    global entr_name
    global entr_phone
    btn_new.config(state="disabled")
    bla = Tk()
    bla.protocol("WM_DELETE_WINDOW", on_close)
    bla.title("New Contact")
    Label(bla, text="Name", padx=50).grid(row=0, column=0)
    Label(bla, text="Phone", padx=50).grid(row=0, column=1)
    entr_name = Entry(bla, width="30")
    entr_name.grid(row=1, column=0)
    entr_phone = Entry(bla, width="30")
    entr_phone.grid(row=1, column=1)
    btn_save = Button(bla, text="Save", command=add_new)
    btn_save.grid(row=2, column=1)
    btn_cancel = Button(bla, text="Cancel", command=cancel)
    btn_cancel.grid(row=2, column=0)

def add_new():
    global entr_name
    global entr_phone
    CONTACTS.append([entr_name.get(), entr_phone.get()])
    pickle.dump(CONTACTS, open('contacts.cnts', 'wb'))
    print('added')
    bla.destroy()
    update_contacts_diplay()
    btn_new.config(state="normal")

def load():
    global CONTACTS
    try:
        CONTACTS = pickle.load(open('Contacts.cnts', 'rb'))
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
        txt_box.insert(INSERT, c[0] + " ")
        txt_box.insert(INSERT, c[1] + "\n")
    txt_box.config(state="disabled")

def on_close():
    btn_new.config(state="normal")
    bla.destroy()

init_root()
root.mainloop()
