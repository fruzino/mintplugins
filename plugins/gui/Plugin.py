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

_STATE_FILE = os.path.join(os.path.dirname(__file__), "gui_state.json")

def _save_cmd(name, args):
    import json
    state = []
    if name != "window" and os.path.exists(_STATE_FILE):
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except:
            state = []
    
    if name == "window":
        state = [] # Reset on new window
    
    state.append({"cmd": name, "args": args})
    
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def _load_state():
    import json
    if not os.path.exists(_STATE_FILE):
        return []
    try:
        with open(_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# ── internal build ──────────────────────────────────────────────────────────

_root = None
_frame = None
_widgets = {}

def _apply_style(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    
    # Catppuccin Mocha Colors
    bg = "#1e1e2e"
    fg = "#cdd6f4"
    accent = "#89b4fa"
    surface = "#313244"
    
    root.configure(bg=bg)
    
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 11))
    style.configure("TButton", 
                    background=accent, 
                    foreground="#11111b", 
                    font=("Segoe UI", 10, "bold"),
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor=accent)
    style.map("TButton",
              background=[("active", "#b4befe"), ("pressed", "#74c7ec")])
    
    style.configure("TEntry", fieldbackground=surface, foreground=fg, insertcolor=fg, borderwidth=0)
    style.configure("TCombobox", fieldbackground=surface, foreground=fg, arrowcolor=accent)
    style.configure("Horizontal.TScale", background=bg, troughcolor=surface)

def _build_ui(state):
    global _root, _frame
    _root = tk.Tk()
    _apply_style(_root)
    
    # Default title/size if window() wasn't called first
    title = "Mint GUI"
    geom = "400x500"
    
    # First pass: find window config
    for item in state:
        if item["cmd"] == "window":
            title = item["args"][0] if item["args"] else title
            geom = item["args"][1] if len(item["args"]) > 1 else geom
            break
            
    _root.title(title)
    _root.geometry(geom)
    
    _frame = ttk.Frame(_root, padding=20)
    _frame.pack(fill="both", expand=True)
    
    # Second pass: build widgets
    for item in state:
        cmd = item["cmd"]
        args = item["args"]
        
        if cmd == "button":
            text = args[0] if args else "Button"
            mcmd = args[1] if len(args) > 1 else ""
            def make_handler(c): return lambda: os.system(f'mint -e "{c}"') if c else None
            btn = ttk.Button(_frame, text=text, command=make_handler(mcmd))
            btn.pack(pady=8, fill="x")
            
        elif cmd == "label":
            text = " ".join(args)
            ttk.Label(_frame, text=text).pack(pady=5, anchor="w")
            
        elif cmd == "image":
            path = args[0] if args else ""
            if path and os.path.exists(path):
                try:
                    img = tk.PhotoImage(file=path)
                    lbl = ttk.Label(_frame, image=img)
                    lbl.image = img
                    lbl.pack(pady=10)
                except: pass
        
        elif cmd == "text":
            content = " ".join(args)
            txt = tk.Text(_frame, height=6, font=("Segoe UI", 10), bg=surface, fg=fg,
                          insertbackground=fg, relief="flat", padx=10, pady=10)
            if content: txt.insert("1.0", content)
            txt.pack(pady=8, fill="both", expand=True)
            
        elif cmd == "checkbox":
            label = args[0] if args else "Option"
            var = tk.BooleanVar()
            ttk.Checkbutton(_frame, text=label, variable=var).pack(pady=4, anchor="w")
            
        elif cmd == "radio":
            label = args[0] if args else "Option"
            group = args[1] if len(args) > 1 else "default"
            if f"_radio_{group}" not in _widgets: _widgets[f"_radio_{group}"] = tk.StringVar(value="")
            var = _widgets[f"_radio_{group}"]
            ttk.Radiobutton(_frame, text=label, variable=var, value=label).pack(pady=4, anchor="w")
            
        elif cmd == "dropdown":
            values = args if args else ["Option 1", "Option 2"]
            combo = ttk.Combobox(_frame, values=values, state="readonly")
            combo.current(0)
            combo.pack(pady=8, fill="x")
            
        elif cmd == "slider":
            lo = float(args[0]) if args else 0
            hi = float(args[1]) if len(args) > 1 else 100
            ttk.Scale(_frame, from_=lo, to=hi, orient="horizontal").pack(pady=8, fill="x")

        elif cmd == "alert":
            msg = " ".join(args)
            messagebox.showinfo("Mint", msg)
            
        elif cmd == "confirm":
            msg = " ".join(args)
            res = messagebox.askyesno("Mint", msg)
            print("true" if res else "false")
            
        elif cmd == "prompt":
            msg = " ".join(args)
            res = simpledialog.askstring("Mint", msg)
            if res: print(res)
            
        elif cmd == "filedialog":
            path = tkfiledialog.askopenfilename()
            if path: print(path)
            
        elif cmd == "close":
            _root.destroy()




# ── commands ─────────────────────────────────────────────────────────────────

def cmd_window(args):
    """gui.window(title, widthxheight)"""
    _save_cmd("window", args)
    print("ok")

def cmd_button(args):
    """gui.button(text, mintcmd)"""
    _save_cmd("button", args)
    print("ok")

def cmd_label(args):
    """gui.label(text)"""
    _save_cmd("label", args)
    print("ok")

def cmd_image(args):
    """gui.image(path)"""
    _save_cmd("image", args)
    print("ok")

def cmd_input(args):
    """gui.input()"""
    _save_cmd("input", args)
    print("ok")

def cmd_text(args):
    """gui.text(content)"""
    _save_cmd("text", args)
    print("ok")

def cmd_checkbox(args):
    """gui.checkbox(label)"""
    _save_cmd("checkbox", args)
    print("ok")

def cmd_radio(args):
    """gui.radio(label, group)"""
    _save_cmd("radio", args)
    print("ok")

def cmd_dropdown(args):
    """gui.dropdown(opt1, opt2, ...)"""
    _save_cmd("dropdown", args)
    print("ok")

def cmd_slider(args):
    """gui.slider(min, max)"""
    _save_cmd("slider", args)
    print("ok")

def cmd_alert(args):
    """gui.alert(message)"""
    _save_cmd("alert", args)
    print("ok")

def cmd_confirm(args):
    """gui.confirm(message)"""
    _save_cmd("confirm", args)
    print("ok")

def cmd_prompt(args):
    """gui.prompt(message)"""
    _save_cmd("prompt", args)
    print("ok")

def cmd_filedialog(args):
    """gui.filedialog()"""
    _save_cmd("filedialog", args)
    print("ok")

def cmd_close(args):
    """gui.close()"""
    _save_cmd("close", args)
    print("ok")

def cmd_color(args):
    """gui.color(bg)"""
    _save_cmd("color", args)
    print("ok")


def cmd_show(args):
    """gui.show()  — run the tkinter main loop."""
    state = _load_state()
    if not state:
        print("ERROR: No window or widgets defined", file=sys.stderr)
        return
    _build_ui(state)
    _root.mainloop()
    # Clean up state after show
    if os.path.exists(_STATE_FILE):
        os.remove(_STATE_FILE)
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
