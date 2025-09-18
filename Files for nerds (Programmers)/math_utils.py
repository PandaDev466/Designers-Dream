def rgb_to_hex(rgb):
    """
    Convert an (r,g,b) tuple (numbers or strings) to a hex color string.
    """
    r, g, b = (int(round(float(c))) for c in rgb)
    r = max(0, min(255, r)); g = max(0, min(255, g)); b = max(0, min(255, b))
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def _clamp_int(value):
    """
    Parse value to int and clamp to [0,255]. Non-numeric -> 0.
    """
    try:
        v = int(float(value))
    except Exception:
        v = 0
    return max(0, min(255, v))


def get_rgb_from_entries(*entries):
    """
    Read values from tkinter Entry widgets and return (r,g,b) tuple of ints.
    Safe if an entry is missing/empty/invalid.
    """
    vals = []
    for e in entries:
        try:
            raw = e.get()
        except Exception:
            raw = 0
        vals.append(_clamp_int(raw))
    return tuple(vals)


def set_entries_from_rgb(entries, rgb):
    """
    Set tkinter Entry widgets from an (r,g,b) iterable.
    entries: iterable of 3 Entry widgets
    rgb: iterable of 3 numbers
    """
    for e, v in zip(entries, rgb):
        try:
            e.delete(0, "end")
            e.insert(0, str(_clamp_int(v)))
        except Exception:
            # ignore widgets that fail (keeps function robust)
            pass


def _luminance_component(c):
    """
    Convert a single sRGB component (0-255) to linear-light component.
    """
    s = c / 255.0
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    """
    Compute relative luminance for an (r,g,b) tuple (0-255).
    """
    r, g, b = (_clamp_int(x) for x in rgb)
    return 0.2126 * _luminance_component(r) + 0.7152 * _luminance_component(g) + 0.0722 * _luminance_component(b)


def calculate_contrast_ratio(fg_rgb, bg_rgb):
    """
    Calculate WCAG contrast ratio between two RGB tuples (0-255).
    Returns float >= 1.0 (higher = better contrast).
    """
    fg_l = luminance(fg_rgb)
    bg_l = luminance(bg_rgb)
    lighter = max(fg_l, bg_l)
    darker = min(fg_l, bg_l)
    return (lighter + 0.05) / (darker + 0.05)
#accidentally messed up commit msg