import tkinter as tk
from tkinter import colorchooser, filedialog
from tkinter import TclError
import math_utils as maut
import ui_utils as uiu
import shared_utils as su

VER = "1.0.1"
DIMENSIONS = "800x600"

root = tk.Tk()
root.title(f"Designer's Dream V{VER}")
root.geometry(DIMENSIONS)
try:
    root.iconbitmap(False, "imageicon.ico")
except TclError as e:
    print("Icon load error:", e)
    print("Make sure 'imageicon.ico' is in the same directory as this script... continuing without ico")


def _copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def check_contrast():
    """
    Calculate the contrast ratio and update the result label and preview canvas.
    """
    # Get the foreground and background RGB values from the entry widgets
    fg_rgb = maut.get_rgb_from_entries(R, G, B)
    bg_rgb = maut.get_rgb_from_entries(R1, G1, B1)

    # Calculate the contrast ratio
    ratio = maut.calculate_contrast_ratio(fg_rgb, bg_rgb)

    # Update the result label with the contrast ratio and WCAG compliance badges
    result_label.config(text=f"Contrast: {ratio:.2f}\n{uiu.wcag_badges(ratio)}")

    # Update the preview canvas with the foreground and background colors
    uiu.update_preview(preview, fg_rgb, bg_rgb)

# ...existing code...

def pick_fg_color():
    rgb_tuple, _ = colorchooser.askcolor(title="Pick Foreground")
    if rgb_tuple:
        maut.set_entries_from_rgb((R, G, B), rgb_tuple)
        check_contrast()   # <-- ensure preview updates after picker

def pick_bg_color():
    rgb_tuple, _ = colorchooser.askcolor(title="Pick Background")
    if rgb_tuple:
        maut.set_entries_from_rgb((R1, G1, B1), rgb_tuple)
        check_contrast()   # <-- ensure preview updates after picker



def save_palette():
    fg = fg_hex_var.get()
    bg = bg_hex_var.get()
    fg_rgb = maut.get_rgb_from_entries(R, G, B)
    bg_rgb = maut.get_rgb_from_entries(R1, G1, B1)
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "a") as f:
            f.write(f"FG {fg} {fg_rgb}, BG {bg} {bg_rgb}\n")


top_frame = tk.Frame(root)
top_frame.pack(pady=10)
bot_frame = tk.Frame(root)
bot_frame.pack(pady=10)
res_frame = tk.Frame(root)
res_frame.pack(pady=10)

R_frame, R = su.make_rgb_entry(top_frame, "R")
R_frame.grid(row=0, column=0, padx=5)
G_frame, G = su.make_rgb_entry(top_frame, "G")
G_frame.grid(row=0, column=1, padx=5)
B_frame, B = su.make_rgb_entry(top_frame, "B")
B_frame.grid(row=0, column=2, padx=5)

R1_frame, R1 = su.make_rgb_entry(bot_frame, "R")
R1_frame.grid(row=0, column=0, padx=5)
G1_frame, G1 = su.make_rgb_entry(bot_frame, "G")
G1_frame.grid(row=0, column=1, padx=5)
B1_frame, B1 = su.make_rgb_entry(bot_frame, "B")
B1_frame.grid(row=0, column=2, padx=5)

for e in (R, G, B, R1, G1, B1):
    e.bind("<KeyRelease>", lambda event: uiu.clamp_entry(event, check_contrast))
    e.bind("<FocusOut>", lambda event: uiu.clamp_entry(event, check_contrast))

fg_hex_var, bg_hex_var = tk.StringVar(value="#ffffff"), tk.StringVar(value="#000000")
tk.Label(top_frame, textvariable=fg_hex_var, font=("Arial", 12)).grid(row=0, column=3, padx=10)
tk.Label(bot_frame, textvariable=bg_hex_var, font=("Arial", 12)).grid(row=0, column=3, padx=10)

result_label = tk.Label(res_frame, text="Contrast: —", font=("Arial", 16), justify="left")
result_label.grid(row=0, column=0, sticky="w")

preview = tk.Canvas(res_frame, width=300, height=120, highlightthickness=1, highlightbackground="#aaa")
preview.grid(row=0, column=1, padx=20)

btns = tk.Frame(root)
btns.pack(pady=10)
tk.Button(btns, text="🎨 Pick FG", command=pick_fg_color).grid(row=0, column=1, padx=5)
tk.Button(btns, text="🎨 Pick BG", command=pick_bg_color).grid(row=0, column=2, padx=5)
tk.Button(btns, text="Copy FG HEX", command=lambda: _copy_to_clipboard(fg_hex_var.get())).grid(row=0, column=3, padx=5)
tk.Button(btns, text="Copy BG HEX", command=lambda: _copy_to_clipboard(bg_hex_var.get())).grid(row=0, column=4, padx=5)
tk.Button(btns, text="Save Palette", command=save_palette).grid(row=0, column=5, padx=5)

R.insert(0, "255")
G.insert(0, "255")
B.insert(0, "255")
R1.insert(0, "0")
G1.insert(0, "0")
B1.insert(0, "0")

# Pass the canvas and result label to math_utils
maut.preview = preview
maut.result_label = result_label

check_contrast()
root.mainloop()