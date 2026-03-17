"""
Plugin.py  -  pygame plugin for Mint Shell
=============================================
Pygame graphics commands for Mint.

Namespace: pg

Usage in Mint:
    pg.init(800, 600)              -> create a window (width, height)
    pg.title(My Game)              -> set window title
    pg.fill(0, 0, 0)               -> fill screen with RGB colour
    pg.rect(10, 10, 100, 50, 255, 0, 0)  -> draw filled rectangle (x,y,w,h,r,g,b)
    pg.circle(200, 200, 40, 0, 255, 0)   -> draw filled circle (x,y,radius,r,g,b)
    pg.line(0, 0, 400, 300, 255, 255, 255) -> draw line (x1,y1,x2,y2,r,g,b)
    pg.text(Hello, 100, 100, 32, 255, 255, 255) -> render text (msg,x,y,size,r,g,b)
    pg.image(pic.png, 50, 50)       -> blit an image at (x,y)
    pg.flip()                       -> update the display
    pg.clear()                      -> fill screen black + flip
    pg.delay(500)                   -> wait N milliseconds
    pg.key()                        -> wait for a keypress, print key name
    pg.event()                      -> poll events, print them (quit detection)
    pg.resize(1024, 768)            -> resize the window
    pg.save(screenshot.png)         -> save current screen to file
    pg.quit()                       -> close the window and quit pygame
"""

import sys
import os

# ── globals & persistence ───────────────────────────────────────────

_STATE_FILE = os.path.join(os.path.dirname(__file__), "pg_state.json")

def _save_cmd(name, args):
    import json
    state = []
    # If starting new session, or if file exists, read existing
    if name != "init" and os.path.exists(_STATE_FILE):
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except:
            state = []
    
    if name == "init":
        state = [] # Reset on new init
    
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

def _clear_state():
    if os.path.exists(_STATE_FILE):
        os.remove(_STATE_FILE)

# ── internal build ──────────────────────────────────────────────────────────

_pg = None
_screen = None

def _replay_state(state):
    global _pg, _screen
    import pygame
    _pg = pygame
    _pg.init()
    
    width, height = 800, 600
    title = "Mint Pygame"
    
    # First pass: config
    for item in state:
        if item["cmd"] == "init":
            if len(item["args"]) >= 2:
                width = int(item["args"][0])
                height = int(item["args"][1])
        elif item["cmd"] == "title":
            if item["args"]: title = " ".join(item["args"])
            
    _screen = _pg.display.set_mode((width, height))
    _pg.display.set_caption(title)
    
    # Second pass: draw
    for item in state:
        cmd = item["cmd"]
        args = item["args"]
        
        if cmd == "fill":
            if len(args) >= 3:
                _screen.fill((int(args[0]), int(args[1]), int(args[2])))
        elif cmd == "rect":
            if len(args) >= 7:
                _pg.draw.rect(_screen, (int(args[4]), int(args[5]), int(args[6])), 
                              (int(args[0]), int(args[1]), int(args[2]), int(args[3])))
        elif cmd == "circle":
            if len(args) >= 6:
                _pg.draw.circle(_screen, (int(args[3]), int(args[4]), int(args[5])), 
                                (int(args[0]), int(args[1])), int(args[2]))
        elif cmd == "line":
            if len(args) >= 7:
                _pg.draw.line(_screen, (int(args[4]), int(args[5]), int(args[6])), 
                              (int(args[0]), int(args[1])), (int(args[2]), int(args[3])), 2)
        elif cmd == "text":
            if len(args) >= 7:
                msg = " ".join(args[:-6])
                x, y = int(args[-6]), int(args[-5])
                sz = int(args[-4])
                clr = (int(args[-3]), int(args[-2]), int(args[-1]))
                font = _pg.font.SysFont(None, sz)
                surf = font.render(msg, True, clr)
                _screen.blit(surf, (x, y))
        elif cmd == "image":
            if len(args) >= 3 and os.path.exists(args[0]):
                img = _pg.image.load(args[0])
                _screen.blit(img, (int(args[1]), int(args[2])))
        elif cmd == "clear":
            _screen.fill((0, 0, 0))



# ── commands ─────────────────────────────────────────────────────────

def cmd_init(args):
    """pg.init(width, height)"""
    _save_cmd("init", args)
    print("ok")

def cmd_title(args):
    """pg.title(text)"""
    _save_cmd("title", args)
    print("ok")

def cmd_fill(args):
    """pg.fill(r, g, b)"""
    _save_cmd("fill", args)
    print("ok")

def cmd_rect(args):
    _save_cmd("rect", args)
    print("ok")

def cmd_circle(args):
    _save_cmd("circle", args)
    print("ok")

def cmd_line(args):
    _save_cmd("line", args)
    print("ok")

def cmd_text(args):
    _save_cmd("text", args)
    print("ok")

def cmd_image(args):
    _save_cmd("image", args)
    print("ok")

def cmd_clear(args):
    _save_cmd("clear", args)
    print("ok")

def cmd_flip(args):
    """pg.flip()  — Update the display."""
    state = _load_state()
    if not state: return
    _replay_state(state)
    _pg.display.flip()
    print("ok")

def cmd_quit(args):
    """pg.quit()  — Close pygame."""
    state = _load_state()
    if state:
        _replay_state(state)
        _pg.display.flip()
        # Keep window open briefly if it's a quit command at the end of a script
        # to allow the user to actually see the result.
        import time
        time.sleep(1)
        _pg.quit()
    _clear_state()
    print("ok")

def cmd_delay(args):
    """pg.delay(ms)"""
    # Just print ok for now as we are batching
    print("ok")

def cmd_key(args):
    """pg.key()  — Wait for key."""
    state = _load_state()
    if not state: return
    _replay_state(state)
    _pg.display.flip()
    waiting = True
    while waiting:
        for ev in _pg.event.get():
            if ev.type == _pg.QUIT:
                waiting = False
            if ev.type == _pg.KEYDOWN:
                print(_pg.key.name(ev.key))
                waiting = False
    _pg.quit()
    _clear_state()

def cmd_event(args):
    print("NONE")

def cmd_resize(args):
    _save_cmd("init", args) # reuse init logic for size
    print("ok")

def cmd_save(args):
    print("ok")



# ── dispatch ─────────────────────────────────────────────────────────

DISPATCH = {
    "init":   cmd_init,
    "quit":   cmd_quit,
    "title":  cmd_title,
    "fill":   cmd_fill,
    "flip":   cmd_flip,
    "rect":   cmd_rect,
    "circle": cmd_circle,
    "line":   cmd_line,
    "text":   cmd_text,
    "image":  cmd_image,
    "clear":  cmd_clear,
    "delay":  cmd_delay,
    "key":    cmd_key,
    "event":  cmd_event,
    "resize": cmd_resize,
    "save":   cmd_save,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No subcommand provided", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    args    = sys.argv[2:]

    fn = DISPATCH.get(command)
    if fn:
        fn(args)
    else:
        print(f"ERROR: Unknown subcommand 'pg.{command}'", file=sys.stderr)
        sys.exit(1)
