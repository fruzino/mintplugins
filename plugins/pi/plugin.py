"""
Plugin.py  -  pi plugin for Mint Shell
=============================================
Pi utility commands for Mint.

Commands:
  pi              - Returns the value of pi (3.14159...)
  estpi           - Returns pi rounded to 2 decimal places (3.14)
  rad(value)      - Multiplies a number by pi (convert to radians * pi)
"""

import sys
import math

def calculate_pi(args):
    """Multiply a given number by pi."""
    try:
        if not args:
            print("ERROR: rad() requires a numeric argument", file=sys.stderr)
            sys.exit(1)
        value = float(args[0].strip())   # FIX: convert string → float
        result = value * math.pi         # FIX: use math.pi for accuracy
        print(result)                    # FIX: print so Mint can read stdout
    except ValueError:
        print(f"ERROR: rad() expected a number, got '{args[0]}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def return_pi(args):
    """Return the value of pi."""
    try:
        print(math.pi)                   # FIX: print, don't return
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def round_pi(args):
    """Return pi rounded to 2 decimal places."""
    try:
        print(round(math.pi, 2))         # FIX: round(), not //
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

DISPATCH = {
    "rad":   calculate_pi,
    "pi":    return_pi,
    "estpi": round_pi,
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
        print(f"ERROR: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)