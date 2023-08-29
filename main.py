import tkinter as tk
from tkinter import ttk
import keyboard
from core import CoreLogic

core = CoreLogic()

root = tk.Tk()
root.title("Bookworm Solver")

# Create a listbox to display the words
listbox = tk.Listbox(root)
listbox.pack()

# Init progress bar
progressbar = ttk.Progressbar(root, mode='indeterminate')


def start():
    clearList()
    progressbar.pack()
    available_words = core.main()
    for i, word in enumerate(available_words):
        listbox.insert(i, word)

    progressbar.pack_forget()


def clearList():
    listbox.delete(0, tk.END)


keyboard.add_hotkey('ctrl+alt+d', start)
keyboard.add_hotkey('ctrl+alt+n', clearList)

progressbar.start()
root.mainloop()
