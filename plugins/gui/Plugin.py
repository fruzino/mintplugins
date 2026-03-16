"""
Plugin.py  -  gui plugin for Mint Shell
=============================================
GUI toolkit using tkinter.  Build windows, buttons, labels,
inputs, and more — all from Mint commands.

Namespace: gui
Commands:
  gui.window(title, widthxheight)  - Create a window
  gui.button(text, command)        - Add a button
  gui.label(text)                  - Add a label
  gui.input(placeholder)           - Add a text entry / input box
  gui.text(content)                - Add a multiline text area
  gui.checkbox(label)              - Add a checkbox
  gui.radio(label, group)          - Add a radio button
  gui.dropdown(opt1, opt2, ...)    - Add a dropdown / combobox
  gui.slider(min, max)             - Add a slider
  gui.image(path)                  - Display an image
  gui.color(bg)                    - Set background color
  gui.alert(message)               - Show an alert messagebox
  gui.confirm(message)             - Show a yes/no confirm dialog
  gui.prompt(message)              - Show a text input dialog
  gui.filedialog()                 - Open a file picker
  gui.close()                      - Close the window
  gui.show()                       - Run the main loop (show window)
"""

import sys
import os

# Force UTF-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog as tkfiledialog

# ── globals ──────────────────────────────────────────────────────────────────

_root = None
_frame = None
_widgets = {}
_widget_counter = 0

def _ensure_root(title="Mint GUI", geometry="400x300"):
    """Create the root window if it doesn't exist yet."""
    global _root, _frame
    if _root is None:
        _root = tk.Tk()
        _root.title(title)
        _root.geometry(geometry)
        _root.configure(bg="#1e1e2e")
        # Style
        style = ttk.Style(_root)
        style.theme_use("clam")
        style.configure("TButton",   padding=6, font=("Segoe UI", 10))
        style.configure("TLabel",    font=("Segoe UI", 10), background="#1e1e2e", foreground="#cdd6f4")
        style.configure("TEntry",    font=("Segoe UI", 10))
        style.configure("TCheckbutton", font=("Segoe UI", 10), background="#1e1e2e", foreground="#cdd6f4")
        style.configure("TRadiobutton", font=("Segoe UI", 10), background="#1e1e2e", foreground="#cdd6f4")

        _frame = ttk.Frame(_root, padding=12)
        _frame.pack(fill="both", expand=True)

def _next_id():
    global _widget_counter
    _widget_counter += 1
    return f"w{_widget_counter}"

# ── commands ─────────────────────────────────────────────────────────────────

def cmd_window(args):
    """gui.window(title, widthxheight)"""
    title = args[0].strip() if args else "Mint GUI"
    geom  = args[1].strip() if len(args) > 1 else "400x300"
    _ensure_root(title, geom)
    wid = _next_id()
    print(wid)

def cmd_button(args):
    """gui.button(text, mintcmd)"""
    _ensure_root()
    text = args[0].strip() if args else "Button"
    mint_cmd = args[1].strip() if len(args) > 1 else ""

    def on_click():
        if mint_cmd:
            os.system(f'mint -e "{mint_cmd}"')

    btn = ttk.Button(_frame, text=text, command=on_click)
    btn.pack(pady=4, fill="x")
    wid = _next_id()
    _widgets[wid] = btn
    print(wid)

def cmd_label(args):
    """gui.label(text)"""
    _ensure_root()
    text = " ".join(a.strip() for a in args) if args else ""
    lbl = ttk.Label(_frame, text=text)
    lbl.pack(pady=4, anchor="w")
    wid = _next_id()
    _widgets[wid] = lbl
    print(wid)

def cmd_input(args):
    """gui.input(placeholder)"""
    _ensure_root()
    placeholder = args[0].strip() if args else ""
    entry = ttk.Entry(_frame)
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(foreground="grey")
        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(foreground="black")
        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground="grey")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    entry.pack(pady=4, fill="x")
    wid = _next_id()
    _widgets[wid] = entry
    print(wid)

def cmd_text(args):
    """gui.text(content)"""
    _ensure_root()
    content = " ".join(a.strip() for a in args) if args else ""
    txt = tk.Text(_frame, height=6, font=("Consolas", 10), bg="#313244", fg="#cdd6f4",
                  insertbackground="#cdd6f4", relief="flat")
    if content:
        txt.insert("1.0", content)
    txt.pack(pady=4, fill="both", expand=True)
    wid = _next_id()
    _widgets[wid] = txt
    print(wid)

def cmd_checkbox(args):
    """gui.checkbox(label)"""
    _ensure_root()
    label = args[0].strip() if args else "Option"
    var = tk.BooleanVar()
    cb = ttk.Checkbutton(_frame, text=label, variable=var)
    cb.pack(pady=2, anchor="w")
    wid = _next_id()
    _widgets[wid] = (cb, var)
    print(wid)

def cmd_radio(args):
    """gui.radio(label, group)"""
    _ensure_root()
    label = args[0].strip() if args else "Option"
    group = args[1].strip() if len(args) > 1 else "default"
    # share a StringVar per group
    if f"_radio_{group}" not in _widgets:
        _widgets[f"_radio_{group}"] = tk.StringVar(value="")
    var = _widgets[f"_radio_{group}"]
    rb = ttk.Radiobutton(_frame, text=label, variable=var, value=label)
    rb.pack(pady=2, anchor="w")
    wid = _next_id()
    _widgets[wid] = (rb, var)
    print(wid)

def cmd_dropdown(args):
    """gui.dropdown(opt1, opt2, ...)"""
    _ensure_root()
    values = [a.strip() for a in args] if args else ["Option 1", "Option 2"]
    combo = ttk.Combobox(_frame, values=values, state="readonly")
    combo.current(0)
    combo.pack(pady=4, fill="x")
    wid = _next_id()
    _widgets[wid] = combo
    print(wid)

def cmd_slider(args):
    """gui.slider(min, max)"""
    _ensure_root()
    lo = float(args[0].strip()) if args else 0
    hi = float(args[1].strip()) if len(args) > 1 else 100
    scale = ttk.Scale(_frame, from_=lo, to=hi, orient="horizontal")
    scale.pack(pady=4, fill="x")
    wid = _next_id()
    _widgets[wid] = scale
    print(wid)

def cmd_image(args):
    """gui.image(path)"""
    _ensure_root()
    path = args[0].strip() if args else ""
    if not path or not os.path.isfile(path):
        print(f"ERROR: image file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        img = tk.PhotoImage(file=path)
        lbl = ttk.Label(_frame, image=img)
        lbl.image = img  # prevent GC
        lbl.pack(pady=4)
        wid = _next_id()
        _widgets[wid] = lbl
        print(wid)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_color(args):
    """gui.color(bg)"""
    _ensure_root()
    bg = args[0].strip() if args else "#1e1e2e"
    _root.configure(bg=bg)
    print("ok")

def cmd_alert(args):
    """gui.alert(message)"""
    _ensure_root()
    msg = " ".join(a.strip() for a in args) if args else "Alert"
    messagebox.showinfo("Mint", msg)
    print("ok")

def cmd_confirm(args):
    """gui.confirm(message)"""
    _ensure_root()
    msg = " ".join(a.strip() for a in args) if args else "Are you sure?"
    result = messagebox.askyesno("Mint", msg)
    print("true" if result else "false")

def cmd_prompt(args):
    """gui.prompt(message)"""
    _ensure_root()
    msg = " ".join(a.strip() for a in args) if args else "Enter value:"
    result = simpledialog.askstring("Mint", msg)
    print(result if result else "")

def cmd_filedialog(args):
    """gui.filedialog()"""
    _ensure_root()
    path = tkfiledialog.askopenfilename()
    print(path if path else "")

def cmd_close(args):
    """gui.close()"""
    global _root
    if _root:
        _root.destroy()
        _root = None
    print("ok")

def cmd_show(args):
    """gui.show()  — run the tkinter main loop."""
    _ensure_root()
    _root.mainloop()
    print("ok")

# ── dispatch ─────────────────────────────────────────────────────────────────

DISPATCH = {
    "window":     cmd_window,
    "button":     cmd_button,
    "label":      cmd_label,
    "input":      cmd_input,
    "text":       cmd_text,
    "checkbox":   cmd_checkbox,
    "radio":      cmd_radio,
    "dropdown":   cmd_dropdown,
    "slider":     cmd_slider,
    "image":      cmd_image,
    "color":      cmd_color,
    "alert":      cmd_alert,
    "confirm":    cmd_confirm,
    "prompt":     cmd_prompt,
    "filedialog": cmd_filedialog,
    "close":      cmd_close,
    "show":       cmd_show,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No command provided", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    args    = sys.argv[2:]

    fn = DISPATCH.get(command)
    if fn:
        fn(args)
    else:
        print(f"ERROR: Unknown gui command '{command}'", file=sys.stderr)
        sys.exit(1)
