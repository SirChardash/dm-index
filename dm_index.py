import os
import re
from tkinter import StringVar

import customtkinter
from PIL import Image

import config

visible_images = dict()
offset = (0, 0)
original_position = (0, 0)


def grab(e, i):
    global offset
    global original_position
    original_position = (i.winfo_rootx(), i.winfo_rooty())
    offset = (e.x, e.y)


def drop(e, i):
    i.place(x=i.winfo_x() + e.x - offset[0], y=i.winfo_y() + e.y - offset[1])


config.initialize()
customtkinter.set_appearance_mode(config.get('theme'))
app = customtkinter.CTk()
app.minsize(720, 520)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=8)
app.grid_rowconfigure(0, weight=1)
button_frame = customtkinter.CTkScrollableFrame(app)

button_frame.grid(row=0, column=0, sticky='news')
image_frame = customtkinter.CTkFrame(app)
image_frame.grid(row=0, column=1, sticky='news')


def toggle_image_visibility(path):
    if path in visible_images:
        visible_images.pop(path).destroy()
    else:
        image_file = Image.open(os.path.join(config.get('dir'), path))
        image = customtkinter.CTkImage(image_file, size=image_file.size)
        label = customtkinter.CTkLabel(image_frame, text="", image=image)
        label.place(x=0, y=0)
        label.bind('<Button-1>', lambda e, l=label: grab(e, l))
        label.bind('<B1-Motion>', lambda e, l=label: drop(e, l))
        visible_images[path] = label


search_value = StringVar(value='')
all_buttons = dict()


def filter_entries():
    for name, entry in all_buttons.items():
        if search_value.get().lower() not in name.lower() and search_value.get() != '':
            entry.pack_forget()
        else:
            entry.pack(pady=5, padx=5, fill='x')


filenames = next(os.walk(config.get('dir')), (None, None, []))[2]

search_box = customtkinter.CTkEntry(button_frame, textvariable=search_value, height=32)
search_box.pack(padx=5, pady=5, fill='x')
search_box.bind('<KeyRelease>', lambda e: filter_entries())


def format_label(string):
    result = re.sub('\\....$', '', string)  # remove ext
    result = re.sub('\\s#[A-Z]+', '', result)  # custom tags
    return result


for filename in filenames:
    button = customtkinter.CTkCheckBox(button_frame, text=format_label(filename))
    button.configure(command=lambda path=filename, b=button: toggle_image_visibility(path))
    button.pack(pady=5, padx=5, fill='x')
    all_buttons[filename] = button

app.mainloop()
