import tkinter as tk
from tkinter import colorchooser, filedialog
from tkinter import TclError


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



def luminance(r, g, b):
    vals = []
    for v in (r, g, b):
        v = v / 255
        vals.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]

def contrast_ratio(fg, bg):
    L1, L2 = luminance(*fg), luminance(*bg)
    return (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def get_rgb_from_entries(entry_r, entry_g, entry_b):
    def parse(e):
        txt = e.get().strip()
        try:
            return max(0, min(255, int(txt))) if txt != "" else 0
        except ValueError:
            return 0
    return (parse(entry_r), parse(entry_g), parse(entry_b))


def make_rgb_entry(parent, label):
    frame = tk.Frame(parent)
    e = tk.Entry(frame, width=5, font=("Arial", 16), justify="center")
    tk.Label(frame, text=label, font=("Arial", 12)).pack()
    e.pack()
    return frame, e

# --- clamp + refresh ---
def clamp_entry(event=None):
    entry = event.widget
    try:
        num = int(entry.get().strip())
    except ValueError:
        num = 0
    num = max(0, min(255, num))
    entry.delete(0, tk.END)
    entry.insert(0, str(num))
    check_contrast()

def set_entries_from_rgb(entries, rgb):
    for e, v in zip(entries, rgb):
        e.delete(0, tk.END)
        e.insert(0, str(int(v)))
    check_contrast()

def update_preview(fg_rgb, bg_rgb):
    preview.delete("all")
    preview.create_rectangle(0, 0, 300, 120, fill=rgb_to_hex(bg_rgb))
    preview.create_text(150, 60, text="Sample Text",
                        fill=rgb_to_hex(fg_rgb),
                        font=("Arial", 18, "bold"))

def wcag_badges(ratio):
    return "\n".join([
        f"AA (Normal 4.5:1): {'✅' if ratio >= 4.5 else '❌'}",
        f"AA (Large 3:1):    {'✅' if ratio >= 3 else '❌'}",
        f"AAA (Normal 7:1):  {'✅' if ratio >= 7 else '❌'}",
        f"AAA (Large 4.5:1): {'✅' if ratio >= 4.5 else '❌'}",
    ])

def check_contrast():
    fg = get_rgb_from_entries(R, G, B)
    bg = get_rgb_from_entries(R1, G1, B1)
    fg_hex_var.set(rgb_to_hex(fg))
    bg_hex_var.set(rgb_to_hex(bg))
    ratio = contrast_ratio(fg, bg)
    result_label.config(text=f"Contrast: {ratio:.2f}:1\n{wcag_badges(ratio)}")
    update_preview(fg, bg)

def _copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


def pick_fg_color():
    rgb_tuple, _ = colorchooser.askcolor(title="Pick Foreground")
    if rgb_tuple: set_entries_from_rgb((R, G, B), rgb_tuple)

def pick_bg_color():
    rgb_tuple, _ = colorchooser.askcolor(title="Pick Background")
    if rgb_tuple: set_entries_from_rgb((R1, G1, B1), rgb_tuple)


def save_palette():
    fg = fg_hex_var.get()
    bg = bg_hex_var.get()
    fg_rgb = get_rgb_from_entries(R, G, B)
    bg_rgb = get_rgb_from_entries(R1, G1, B1)
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files","*.txt")])
    if filename:
        with open(filename, "a") as f:
            f.write(f"FG {fg} {fg_rgb}, BG {bg} {bg_rgb}\n")

top_frame = tk.Frame(root); top_frame.pack(pady=10)
bot_frame = tk.Frame(root); bot_frame.pack(pady=10)
res_frame = tk.Frame(root); res_frame.pack(pady=10)


R_frame, R = make_rgb_entry(top_frame, "R"); R_frame.grid(row=0, column=0, padx=5)
G_frame, G = make_rgb_entry(top_frame, "G"); G_frame.grid(row=0, column=1, padx=5)
B_frame, B = make_rgb_entry(top_frame, "B"); B_frame.grid(row=0, column=2, padx=5)


R1_frame, R1 = make_rgb_entry(bot_frame, "R"); R1_frame.grid(row=0, column=0, padx=5)
G1_frame, G1 = make_rgb_entry(bot_frame, "G"); G1_frame.grid(row=0, column=1, padx=5)
B1_frame, B1 = make_rgb_entry(bot_frame, "B"); B1_frame.grid(row=0, column=2, padx=5)


for e in (R, G, B, R1, G1, B1):
    e.bind("<KeyRelease>", clamp_entry)
    e.bind("<FocusOut>", clamp_entry)


fg_hex_var, bg_hex_var = tk.StringVar(value="#ffffff"), tk.StringVar(value="#000000")
tk.Label(top_frame, textvariable=fg_hex_var, font=("Arial", 12)).grid(row=0, column=3, padx=10)
tk.Label(bot_frame, textvariable=bg_hex_var, font=("Arial", 12)).grid(row=0, column=3, padx=10)


result_label = tk.Label(res_frame, text="Contrast: —", font=("Arial", 16), justify="left")
result_label.grid(row=0, column=0, sticky="w")

preview = tk.Canvas(res_frame, width=300, height=120, highlightthickness=1, highlightbackground="#aaa")
preview.grid(row=0, column=1, padx=20)


btns = tk.Frame(root); btns.pack(pady=10)
tk.Button(btns, text="🎨 Pick FG", command=pick_fg_color).grid(row=0, column=1, padx=5)
tk.Button(btns, text="🎨 Pick BG", command=pick_bg_color).grid(row=0, column=2, padx=5)
tk.Button(btns, text="Copy FG HEX", command=lambda: _copy_to_clipboard(fg_hex_var.get())).grid(row=0, column=3, padx=5)
tk.Button(btns, text="Copy BG HEX", command=lambda: _copy_to_clipboard(bg_hex_var.get())).grid(row=0, column=4, padx=5)
tk.Button(btns, text="Save Palette", command=save_palette).grid(row=0, column=5, padx=5)


R.insert(0,"255"); G.insert(0,"255"); B.insert(0,"255")
R1.insert(0,"0"); G1.insert(0,"0"); B1.insert(0,"0")

check_contrast()
root.mainloop()
