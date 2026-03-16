"""
Plugin.py  -  rand plugin for Mint Shell
==========================================
Random number and choice utilities.

Namespace: rand

Usage in Mint:
    rand.int(1, 10)          -> random integer between 1 and 10
    rand.float(1, 10)        -> random float between 1.0 and 10.0
    rand.choice(a, b, c)     -> pick one item randomly from the list
    rand.shuffle(a, b, c)    -> return items in random order
    rand.chance(30)          -> True with 30% probability, else False
    rand.uuid()              -> generate a random UUID
"""

import sys
import random
import uuid

def cmd_int(args):
    if len(args) < 2:
        print("ERROR: rand.int() needs two numbers e.g. rand.int(1, 10)", file=sys.stderr)
        sys.exit(1)
    try:
        low  = int(args[0].strip())
        high = int(args[1].strip())
        if low > high:
            low, high = high, low
        print(random.randint(low, high))
    except ValueError:
        print(f"ERROR: rand.int() expected integers, got '{args}'", file=sys.stderr)
        sys.exit(1)


def cmd_float(args):
    if len(args) < 2:
        print("ERROR: rand.float() needs two numbers e.g. rand.float(1, 10)", file=sys.stderr)
        sys.exit(1)
    try:
        low  = float(args[0].strip())
        high = float(args[1].strip())
        if low > high:
            low, high = high, low
        print(round(random.uniform(low, high), 6))
    except ValueError:
        print(f"ERROR: rand.float() expected numbers, got '{args}'", file=sys.stderr)
        sys.exit(1)


def cmd_choice(args):
    if not args:
        print("ERROR: rand.choice() needs at least one item", file=sys.stderr)
        sys.exit(1)
    items = [a.strip() for a in args]
    print(random.choice(items))


def cmd_shuffle(args):
    if not args:
        print("ERROR: rand.shuffle() needs at least one item", file=sys.stderr)
        sys.exit(1)
    items = [a.strip() for a in args]
    random.shuffle(items)
    print(", ".join(items))


def cmd_chance(args):
    if not args:
        print("ERROR: rand.chance() needs a percentage e.g. rand.chance(30)", file=sys.stderr)
        sys.exit(1)
    try:
        pct = float(args[0].strip())
        print("True" if random.random() * 100 < pct else "False")
    except ValueError:
        print(f"ERROR: rand.chance() expected a number, got '{args[0]}'", file=sys.stderr)
        sys.exit(1)

def cmd_uuid(args):
    print(str(uuid.uuid4()))

DISPATCH = {
    "int":     cmd_int,
    "float":   cmd_float,
    "choice":  cmd_choice,
    "shuffle": cmd_shuffle,
    "chance":  cmd_chance,
    "uuid":    cmd_uuid,
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
        print(f"ERROR: Unknown subcommand 'rand.{command}'", file=sys.stderr)
        sys.exit(1)