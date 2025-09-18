
import tkinter as tk
from math_utils import rgb_to_hex

def clamp_entry(event, callback=None):
    """
    Clamp the value in an entry widget to [0,255] and call callback().
    """
    entry = event.widget
    try:
        num = int(entry.get().strip())
    except Exception:
        num = 0
    num = max(0, min(255, num))
    entry.delete(0, tk.END)
    entry.insert(0, str(num))
    # ensure callback is executed after clamping
    if callback:
        callback()

def update_preview(preview, fg_rgb, bg_rgb):
    """
    Update preview canvas with bg rectangle and text in fg color.
    """
    preview.delete("all")
    preview.create_rectangle(0, 0, 300, 120, fill=rgb_to_hex(bg_rgb), outline="")
    preview.create_text(150, 60, text="Sample Text", fill=rgb_to_hex(fg_rgb), font=("Arial", 18, "bold"))

def wcag_badges(ratio):
    return "\n".join([
        f"AA (Normal 4.5:1): {'✅' if ratio >= 4.5 else '❌'}",
        f"AA (Large 3:1):    {'✅' if ratio >= 3 else '❌'}",
        f"AAA (Normal 7:1):  {'✅' if ratio >= 7 else '❌'}",
        f"AAA (Large 4.5:1): {'✅' if ratio >= 4.5 else '❌'}",
    ])
#accidentally messed up commit msg