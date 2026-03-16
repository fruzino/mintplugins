"""
Plugin.py  -  math+ plugin for Mint Shell
=============================================
Advanced math utilities beyond basic arithmetic.

Namespace: math
Commands:
  math.sin(x)          - Sine (x in degrees)
  math.cos(x)          - Cosine (x in degrees)
  math.tan(x)          - Tangent (x in degrees)
  math.log(x)          - Natural logarithm
  math.log2(x)         - Base-2 logarithm
  math.log10(x)        - Base-10 logarithm
  math.ceil(x)         - Round up
  math.floor(x)        - Round down
  math.round(x, n)     - Round to n decimal places (default 0)
  math.abs(x)          - Absolute value
  math.factorial(n)    - n!
  math.gcd(a, b)       - Greatest common divisor
  math.lcm(a, b)       - Least common multiple
  math.hypot(a, b)     - Hypotenuse sqrt(a^2 + b^2)
  math.deg(rad)        - Radians to degrees
  math.rad(deg)        - Degrees to radians
  math.min(a, b, ...)  - Minimum value
  math.max(a, b, ...)  - Maximum value
  math.clamp(x, lo, hi)- Clamp x between lo and hi
  math.lerp(a, b, t)   - Linear interpolation
  math.map(x, a1,a2, b1,b2) - Map x from range [a1,a2] to [b1,b2]
  math.avg(a, b, ...)  - Average of values
  math.sum(a, b, ...)  - Sum of values
  math.isprime(n)      - Check if n is prime
  math.fib(n)          - Nth Fibonacci number
  math.e()             - Euler's number
  math.tau()           - Tau (2*pi)
  math.phi()           - Golden ratio
  math.rand()          - Random float 0-1
  math.randint(a, b)   - Random integer in [a, b]
  math.hex(n)          - Decimal to hexadecimal
  math.bin(n)          - Decimal to binary
  math.oct(n)          - Decimal to octal
"""

import sys
import math
import random

# ── helpers ──────────────────────────────────────────────────────────────────

def _float(args, index=0, name="arg"):
    """Safely pull a float from args."""
    try:
        return float(args[index].strip())
    except (IndexError, ValueError):
        print(f"ERROR: expected a number for {name}", file=sys.stderr)
        sys.exit(1)

def _int(args, index=0, name="arg"):
    """Safely pull an int from args."""
    try:
        return int(float(args[index].strip()))
    except (IndexError, ValueError):
        print(f"ERROR: expected an integer for {name}", file=sys.stderr)
        sys.exit(1)

# ── commands ─────────────────────────────────────────────────────────────────

def cmd_sin(args):
    print(math.sin(math.radians(_float(args, 0, "x"))))

def cmd_cos(args):
    print(math.cos(math.radians(_float(args, 0, "x"))))

def cmd_tan(args):
    print(math.tan(math.radians(_float(args, 0, "x"))))

def cmd_log(args):
    print(math.log(_float(args, 0, "x")))

def cmd_log2(args):
    print(math.log2(_float(args, 0, "x")))

def cmd_log10(args):
    print(math.log10(_float(args, 0, "x")))

def cmd_ceil(args):
    print(int(math.ceil(_float(args, 0, "x"))))

def cmd_floor(args):
    print(int(math.floor(_float(args, 0, "x"))))

def cmd_round(args):
    x = _float(args, 0, "x")
    n = _int(args, 1, "n") if len(args) > 1 else 0
    print(round(x, n))

def cmd_abs(args):
    print(abs(_float(args, 0, "x")))

def cmd_factorial(args):
    print(math.factorial(_int(args, 0, "n")))

def cmd_gcd(args):
    print(math.gcd(_int(args, 0, "a"), _int(args, 1, "b")))

def cmd_lcm(args):
    a, b = _int(args, 0, "a"), _int(args, 1, "b")
    print(abs(a * b) // math.gcd(a, b) if a and b else 0)

def cmd_hypot(args):
    print(math.hypot(_float(args, 0, "a"), _float(args, 1, "b")))

def cmd_deg(args):
    print(math.degrees(_float(args, 0, "radians")))

def cmd_rad(args):
    print(math.radians(_float(args, 0, "degrees")))

def cmd_min(args):
    vals = [float(a.strip()) for a in args]
    print(min(vals))

def cmd_max(args):
    vals = [float(a.strip()) for a in args]
    print(max(vals))

def cmd_clamp(args):
    x  = _float(args, 0, "x")
    lo = _float(args, 1, "lo")
    hi = _float(args, 2, "hi")
    print(max(lo, min(hi, x)))

def cmd_lerp(args):
    a = _float(args, 0, "a")
    b = _float(args, 1, "b")
    t = _float(args, 2, "t")
    print(a + (b - a) * t)

def cmd_map(args):
    x  = _float(args, 0, "x")
    a1 = _float(args, 1, "a1")
    a2 = _float(args, 2, "a2")
    b1 = _float(args, 3, "b1")
    b2 = _float(args, 4, "b2")
    print(b1 + (x - a1) * (b2 - b1) / (a2 - a1))

def cmd_avg(args):
    vals = [float(a.strip()) for a in args]
    print(sum(vals) / len(vals))

def cmd_sum(args):
    vals = [float(a.strip()) for a in args]
    print(sum(vals))

def cmd_isprime(args):
    n = _int(args, 0, "n")
    if n < 2:
        print("false"); return
    if n < 4:
        print("true"); return
    if n % 2 == 0 or n % 3 == 0:
        print("false"); return
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            print("false"); return
        i += 6
    print("true")

def cmd_fib(args):
    n = _int(args, 0, "n")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    print(a)

def cmd_e(args):
    print(math.e)

def cmd_tau(args):
    print(math.tau)

def cmd_phi(args):
    print((1 + math.sqrt(5)) / 2)

def cmd_rand(args):
    print(random.random())

def cmd_randint(args):
    a = _int(args, 0, "a")
    b = _int(args, 1, "b")
    print(random.randint(a, b))

def cmd_hex(args):
    print(hex(_int(args, 0, "n")))

def cmd_bin(args):
    print(bin(_int(args, 0, "n")))

def cmd_oct(args):
    print(oct(_int(args, 0, "n")))

def cmd_power(args):
    print(_float(args, 0, "x") ** _float(args, 1, "y"))

def cmd_triangular(args):
    n = _int(args, 0, "n")
    print(n * (n + 1) // 2)

def cmd_pentagonal(args):
    n = _int(args, 0, "n")
    print(n * (3 * n - 1) // 2)

def cmd_hexagonal(args):
    n = _int(args, 0, "n")
    print(n * (2 * n - 1))

def cmd_heptagonal(args):
    n = _int(args, 0, "n")
    print(n * (5 * n - 3) // 2)

def cmd_octagonal(args):
    n = _int(args, 0, "n")
    print(n * (3 * n - 2))

def cmd_nonagonal(args):
    n = _int(args, 0, "n")
    print(n * (7 * n - 5) // 2)

def cmd_decagonal(args):
    n = _int(args, 0, "n")
    print(n * (4 * n - 3))

def cmd_dodecagonal(args):
    """Nth dodecagonal number: n*(5n-4)"""
    n = _int(args, 0, "n")
    print(n * (5 * n - 4))

def cmd_fibonacci(args):
    """Print the first n Fibonacci numbers as a comma-separated list."""
    n = _int(args, 0, "n")
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(str(a))
        a, b = b, a + b
    print(", ".join(seq))


# ── dispatch ─────────────────────────────────────────────────────────────────

DISPATCH = {
    "sin":       cmd_sin,
    "cos":       cmd_cos,
    "tan":       cmd_tan,
    "log":       cmd_log,
    "log2":      cmd_log2,
    "log10":     cmd_log10,
    "ceil":      cmd_ceil,
    "floor":     cmd_floor,
    "round":     cmd_round,
    "abs":       cmd_abs,
    "factorial": cmd_factorial,
    "gcd":       cmd_gcd,
    "lcm":       cmd_lcm,
    "hypot":     cmd_hypot,
    "deg":       cmd_deg,
    "rad":       cmd_rad,
    "min":       cmd_min,
    "max":       cmd_max,
    "clamp":     cmd_clamp,
    "lerp":      cmd_lerp,
    "map":       cmd_map,
    "avg":       cmd_avg,
    "sum":       cmd_sum,
    "isprime":   cmd_isprime,
    "fib":       cmd_fib,
    "e":         cmd_e,
    "tau":       cmd_tau,
    "phi":       cmd_phi,
    "rand":      cmd_rand,
    "randint":   cmd_randint,
    "hex":       cmd_hex,
    "bin":       cmd_bin,
    "oct":       cmd_oct,
    "power":     cmd_power,
    "tri":       cmd_triangular,
    "penta":     cmd_pentagonal,
    "hexa":      cmd_hexagonal,
    "hepta":     cmd_heptagonal,
    "octa":      cmd_octagonal,
    "nona":      cmd_nonagonal,
    "deca":      cmd_decagonal,
    "dodeca":    cmd_dodecagonal,
    "fibonacci": cmd_fibonacci,
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
        print(f"ERROR: Unknown math command '{command}'", file=sys.stderr)
        sys.exit(1)
