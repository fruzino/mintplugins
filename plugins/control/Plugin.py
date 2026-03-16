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

# ── Lazy pygame import ───────────────────────────────────────────────
# We import pygame only when the first command runs, so merely loading
# the plugin doesn't pop up a window.

_pg = None
_screen = None
_width = 800
_height = 600


def _ensure_pygame():
    global _pg
    if _pg is None:
        import pygame
        _pg = pygame


def _ensure_screen():
    """Ensure pygame is initialised and a display surface exists."""
    global _pg, _screen, _width, _height
    _ensure_pygame()
    if _screen is None:
        _pg.init()
        _screen = _pg.display.set_mode((_width, _height))
        _pg.display.set_caption("Mint Pygame")


def _parse_int(value, name="value"):
    try:
        return int(value)
    except (ValueError, TypeError):
        print(f"ERROR: expected integer for {name}, got '{value}'", file=sys.stderr)
        sys.exit(1)


# ── commands ─────────────────────────────────────────────────────────

def cmd_init(args):
    """Initialise pygame and create a window.  pg.init(width, height)"""
    global _width, _height, _screen
    if len(args) >= 2:
        _width = _parse_int(args[0], "width")
        _height = _parse_int(args[1], "height")
    _ensure_screen()
    print(f"Window created ({_width}x{_height})")


def cmd_quit(args):
    """Quit pygame."""
    global _screen
    _ensure_pygame()
    _pg.quit()
    _screen = None
    print("Pygame closed")


def cmd_title(args):
    """Set the window title.  pg.title(My Game)"""
    if not args:
        print("ERROR: pg.title() needs a title string", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    title = " ".join(args)
    _pg.display.set_caption(title)
    print(f"Title set to '{title}'")


def cmd_fill(args):
    """Fill the screen with an RGB colour.  pg.fill(r, g, b)"""
    if len(args) < 3:
        print("ERROR: pg.fill() needs r, g, b values", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    r = _parse_int(args[0], "r")
    g = _parse_int(args[1], "g")
    b = _parse_int(args[2], "b")
    _screen.fill((r, g, b))
    print(f"Filled ({r}, {g}, {b})")


def cmd_flip(args):
    """Update the display (push drawn content to screen)."""
    _ensure_screen()
    _pg.display.flip()
    print("Display updated")


def cmd_rect(args):
    """Draw a filled rectangle.  pg.rect(x, y, w, h, r, g, b)"""
    if len(args) < 7:
        print("ERROR: pg.rect() needs x, y, w, h, r, g, b", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    x = _parse_int(args[0], "x")
    y = _parse_int(args[1], "y")
    w = _parse_int(args[2], "w")
    h = _parse_int(args[3], "h")
    r = _parse_int(args[4], "r")
    g = _parse_int(args[5], "g")
    b = _parse_int(args[6], "b")
    _pg.draw.rect(_screen, (r, g, b), (x, y, w, h))
    print(f"Rect at ({x},{y}) size {w}x{h}")


def cmd_circle(args):
    """Draw a filled circle.  pg.circle(x, y, radius, r, g, b)"""
    if len(args) < 6:
        print("ERROR: pg.circle() needs x, y, radius, r, g, b", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    x = _parse_int(args[0], "x")
    y = _parse_int(args[1], "y")
    rad = _parse_int(args[2], "radius")
    r = _parse_int(args[3], "r")
    g = _parse_int(args[4], "g")
    b = _parse_int(args[5], "b")
    _pg.draw.circle(_screen, (r, g, b), (x, y), rad)
    print(f"Circle at ({x},{y}) r={rad}")


def cmd_line(args):
    """Draw a line.  pg.line(x1, y1, x2, y2, r, g, b)"""
    if len(args) < 7:
        print("ERROR: pg.line() needs x1, y1, x2, y2, r, g, b", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    x1 = _parse_int(args[0], "x1")
    y1 = _parse_int(args[1], "y1")
    x2 = _parse_int(args[2], "x2")
    y2 = _parse_int(args[3], "y2")
    r = _parse_int(args[4], "r")
    g = _parse_int(args[5], "g")
    b = _parse_int(args[6], "b")
    _pg.draw.line(_screen, (r, g, b), (x1, y1), (x2, y2), 2)
    print(f"Line ({x1},{y1})->({x2},{y2})")


def cmd_text(args):
    """Render text on screen.  pg.text(message, x, y, size, r, g, b)"""
    if len(args) < 7:
        print("ERROR: pg.text() needs message, x, y, size, r, g, b", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    # Last 6 args are: x, y, size, r, g, b — everything before is the message
    msg = " ".join(args[:-6])
    x = _parse_int(args[-6], "x")
    y = _parse_int(args[-5], "y")
    sz = _parse_int(args[-4], "size")
    r = _parse_int(args[-3], "r")
    g = _parse_int(args[-2], "g")
    b = _parse_int(args[-1], "b")
    font = _pg.font.SysFont(None, sz)
    surf = font.render(msg, True, (r, g, b))
    _screen.blit(surf, (x, y))
    print(f"Text '{msg}' at ({x},{y})")


def cmd_image(args):
    """Blit an image file onto the screen.  pg.image(path, x, y)"""
    if len(args) < 3:
        print("ERROR: pg.image() needs path, x, y", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    path = args[0]
    x = _parse_int(args[1], "x")
    y = _parse_int(args[2], "y")
    if not os.path.exists(path):
        print(f"ERROR: image not found '{path}'", file=sys.stderr)
        sys.exit(1)
    img = _pg.image.load(path)
    _screen.blit(img, (x, y))
    print(f"Image '{path}' at ({x},{y})")


def cmd_clear(args):
    """Clear screen to black and flip."""
    _ensure_screen()
    _screen.fill((0, 0, 0))
    _pg.display.flip()
    print("Screen cleared")


def cmd_delay(args):
    """Wait N milliseconds.  pg.delay(500)"""
    if not args:
        print("ERROR: pg.delay() needs milliseconds", file=sys.stderr)
        sys.exit(1)
    _ensure_pygame()
    ms = _parse_int(args[0], "ms")
    _pg.time.delay(ms)
    print(f"Delayed {ms}ms")


def cmd_key(args):
    """Wait for a single keypress and print the key name."""
    _ensure_screen()
    waiting = True
    while waiting:
        for ev in _pg.event.get():
            if ev.type == _pg.QUIT:
                print("QUIT")
                waiting = False
                break
            if ev.type == _pg.KEYDOWN:
                print(_pg.key.name(ev.key))
                waiting = False
                break


def cmd_event(args):
    """Poll and print all pending events (useful for game loops)."""
    _ensure_screen()
    events = _pg.event.get()
    if not events:
        print("NONE")
        return
    for ev in events:
        if ev.type == _pg.QUIT:
            print("QUIT")
        elif ev.type == _pg.KEYDOWN:
            print(f"KEYDOWN:{_pg.key.name(ev.key)}")
        elif ev.type == _pg.KEYUP:
            print(f"KEYUP:{_pg.key.name(ev.key)}")
        elif ev.type == _pg.MOUSEBUTTONDOWN:
            print(f"MOUSEDOWN:{ev.pos[0]},{ev.pos[1]}")
        elif ev.type == _pg.MOUSEBUTTONUP:
            print(f"MOUSEUP:{ev.pos[0]},{ev.pos[1]}")
        elif ev.type == _pg.MOUSEMOTION:
            print(f"MOUSEMOVE:{ev.pos[0]},{ev.pos[1]}")


def cmd_resize(args):
    """Resize the window.  pg.resize(width, height)"""
    global _screen, _width, _height
    if len(args) < 2:
        print("ERROR: pg.resize() needs width, height", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    _width = _parse_int(args[0], "width")
    _height = _parse_int(args[1], "height")
    _screen = _pg.display.set_mode((_width, _height))
    print(f"Resized to {_width}x{_height}")


def cmd_save(args):
    """Save the current screen to an image file.  pg.save(filename.png)"""
    if not args:
        print("ERROR: pg.save() needs a filename", file=sys.stderr)
        sys.exit(1)
    _ensure_screen()
    path = " ".join(args)
    _pg.image.save(_screen, path)
    print(f"Saved to {path}")


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
