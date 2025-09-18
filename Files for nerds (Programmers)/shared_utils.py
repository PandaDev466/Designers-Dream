# filepath: c:\Users\pickl\Documents\python Apps\DesignersDream\Files for nerds (Programmers)\shared_utils.py

import tkinter as tk

def make_rgb_entry(parent, label_text):
    """
    Create an RGB entry widget with a label.
    """
    frame = tk.Frame(parent)
    label = tk.Label(frame, text=label_text)
    label.pack(side="left")
    entry = tk.Entry(frame, width=5)
    entry.pack(side="right")
    return frame, entry