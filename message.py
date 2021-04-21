from tkinter import messagebox
from tkinter import Tk

message = Tk()
message.eval('tk::PlaceWindow %s center' % message.winfo_toplevel())
message.iconbitmap(r"Icon/wave.ico")
message.withdraw()


def display(destinationPath):
    messagebox.showinfo('Friendly Remainder',
                        "Your file is at: " + destinationPath)


def TitleError():
    messagebox.showinfo('Friendly Remainder', "Please enter a title")


def LinkError():
    messagebox.showinfo('Friendly Remainder', "Please enter a link")
