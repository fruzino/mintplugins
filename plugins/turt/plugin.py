"""
Plugin.py  -  turt plugin for Mint Shell
==========================================
Turtle graphics commands for Mint.

Namespace: turt

Usage in Mint:
    turt.forward(100)
    turt.backward(50)
    turt.left(90)
    turt.right(45)
    turt.pup()
    turt.pdown()
    turt.circ(50)
    turt.circ(50, 180)
    turt.color(red)
    turt.speed(5)
    turt.clear()
    turt.done()
"""

import sys
import turtle

def cmd_forward(args):
    if not args:
        print("ERROR: turt.forward() needs a distance", file=sys.stderr); sys.exit(1)

    turtle.forward(int(args[0]))

def cmd_backward(args):
    if not args:
        print("ERROR: turt.backward() needs a distance", file=sys.stderr); sys.exit(1)
        
    turtle.backward(int(args[0]))

def cmd_left(args):
    if not args:
        print("ERROR: turt.left() needs an angle", file=sys.stderr); sys.exit(1)

    turtle.left(float(args[0]))

def cmd_right(args):
    if not args:
        print("ERROR: turt.right() needs an angle", file=sys.stderr); sys.exit(1)
        
    turtle.right(float(args[0]))

def cmd_pup(args):
    turtle.penup()

def cmd_pdown(args):
    turtle.pendown()

def cmd_circ(args):
    if not args:
        print("ERROR: turt.circ() needs a radius", file=sys.stderr); sys.exit(1)

    radius  = int(args[0])
    extent  = float(args[1]) if len(args) > 1 else 360
    turtle.circle(radius, extent)

def cmd_color(args):
    if not args:
        print("ERROR: turt.color() needs a color name", file=sys.stderr); sys.exit(1)

    turtle.color(args[0])

def cmd_speed(args):
    if not args:
        print("ERROR: turt.speed() needs a value 0-10", file=sys.stderr); sys.exit(1)
        
    turtle.speed(int(args[0]))

def cmd_clear(args):
    turtle.clear()

def cmd_reset(args):
    turtle.reset()

def cmd_goto(args):
    if len(args) < 2:
        print("ERROR: turt.goto() needs x and y", file=sys.stderr); sys.exit(1)
    turtle.goto(int(args[0]), int(args[1]))

def cmd_done(args):
    turtle.done()  

DISPATCH = {
    "forward":  cmd_forward,
    "backward": cmd_backward,
    "left":     cmd_left,
    "right":    cmd_right,
    "pup":      cmd_pup,
    "pdown":    cmd_pdown,
    "circ":     cmd_circ,
    "color":    cmd_color,
    "speed":    cmd_speed,
    "clear":    cmd_clear,
    "reset":    cmd_reset,
    "goto":     cmd_goto,
    "done":     cmd_done,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No subcommand provided", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    args    = sys.argv[2:]

    fn = DISPATCH.get(command)
    if fn:
        fn(args)
    else:
        print(f"ERROR: Unknown subcommand 'turt.{command}'", file=sys.stderr)
        sys.exit(1)