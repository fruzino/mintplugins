"""
Plugin.py  -  strtools plugin for Mint Shell
=============================================
Namespace: str

Usage in Mint:
    str.upper(hello)               -> HELLO
    str.lower(HELLO)               -> hello
    str.reverse(abc)               -> cba
    str.length(hello)              -> 5
    str.replace(hello, l, r)       -> herro
    str.contains(hello world, world) -> True
    str.trim(  hi  )               -> hi
    str.repeat(ha, 3)              -> hahaha
"""

import sys

def cmd_upper(args):
    print(args[0].upper() if args else "")

def cmd_lower(args):
    print(args[0].lower() if args else "")

def cmd_reverse(args):
    print(args[0][::-1] if args else "")

def cmd_length(args):
    print(len(args[0]) if args else 0)

def cmd_replace(args):
    if len(args) < 3:
        print("ERROR: str.replace needs text, old, new", file=sys.stderr)
        sys.exit(1)
    print(args[0].replace(args[1], args[2]))

def cmd_contains(args):
    if len(args) < 2:
        print("ERROR: str.contains needs text, search", file=sys.stderr)
        sys.exit(1)
    print("True" if args[1] in args[0] else "False")

def cmd_trim(args):
    print(args[0].strip() if args else "")

def cmd_repeat(args):
    if len(args) < 2:
        print("ERROR: str.repeat needs text, N", file=sys.stderr)
        sys.exit(1)
    try:
        print(args[0] * int(args[1]))
    except ValueError:
        print("ERROR: N must be a whole number", file=sys.stderr)
        sys.exit(1)

DISPATCH = {
    "upper":    cmd_upper,
    "lower":    cmd_lower,
    "reverse":  cmd_reverse,
    "length":   cmd_length,
    "replace":  cmd_replace,
    "contains": cmd_contains,
    "trim":     cmd_trim,
    "repeat":   cmd_repeat,
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
        print(f"ERROR: Unknown subcommand 'str.{command}'", file=sys.stderr)
        sys.exit(1)