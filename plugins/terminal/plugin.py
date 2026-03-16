"""
Plugin.py  -  terminal plugin for Mint Shell
==============================================
Terminal & OS utilities for Mint.

Namespace: term

Usage in Mint:
    term.run(dir)                   -> execute a shell command, capture output
    term.env(PATH)                  -> read an environment variable
    term.setenv(MY_VAR, hello)      -> set an environment variable (session)
    term.cwd()                      -> print current working directory
    term.chdir(C:\\Users)            -> change working directory
    term.ls()                       -> list current directory
    term.ls(some\\path)              -> list given directory
    term.exists(file.txt)           -> True / False
    term.sysinfo()                  -> OS, platform, hostname, user
    term.read(file.txt)             -> print file contents
    term.write(file.txt, content)   -> write text to a file
    term.del(file.txt)              -> delete a file
    term.mkdir(dirname)             -> create a directory (incl. parents)
    term.size(file.txt)             -> file size in bytes
    term.clip(text to copy)         -> copy text to clipboard
    term.sleep(2)                   -> pause for N seconds
"""

import sys
import os
import platform
import subprocess
import time
import shutil


# ── commands ──────────────────────────────────────────────────────────

def cmd_run(args):
    """Execute a shell command and print its stdout."""
    if not args:
        print("ERROR: term.run() needs a command string", file=sys.stderr)
        sys.exit(1)
    command = " ".join(args)
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout.strip()
        if output:
            print(output)
        if result.returncode != 0 and result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("ERROR: command timed out (30 s limit)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_env(args):
    """Print the value of an environment variable."""
    if not args:
        print("ERROR: term.env() needs a variable name", file=sys.stderr)
        sys.exit(1)
    value = os.environ.get(args[0], "")
    print(value)


def cmd_setenv(args):
    """Set an environment variable for the current session."""
    if len(args) < 2:
        print("ERROR: term.setenv() needs NAME, VALUE", file=sys.stderr)
        sys.exit(1)
    os.environ[args[0]] = args[1]
    print(f"{args[0]}={args[1]}")


def cmd_cwd(args):
    """Print the current working directory."""
    print(os.getcwd())


def cmd_chdir(args):
    """Change the current working directory."""
    if not args:
        print("ERROR: term.chdir() needs a path", file=sys.stderr)
        sys.exit(1)
    target = " ".join(args)
    try:
        os.chdir(target)
        print(os.getcwd())
    except FileNotFoundError:
        print(f"ERROR: directory not found '{target}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_ls(args):
    """List directory contents (current dir if no arg given)."""
    target = " ".join(args) if args else "."
    try:
        entries = os.listdir(target)
        for entry in sorted(entries):
            full = os.path.join(target, entry)
            tag = "[DIR] " if os.path.isdir(full) else "      "
            print(f"{tag}{entry}")
    except FileNotFoundError:
        print(f"ERROR: directory not found '{target}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_exists(args):
    """Check whether a file or directory exists."""
    if not args:
        print("ERROR: term.exists() needs a path", file=sys.stderr)
        sys.exit(1)
    target = " ".join(args)
    print("True" if os.path.exists(target) else "False")


def cmd_sysinfo(args):
    """Print basic system information."""
    info_lines = [
        f"OS       : {platform.system()} {platform.release()}",
        f"Platform : {platform.platform()}",
        f"Machine  : {platform.machine()}",
        f"Hostname : {platform.node()}",
        f"User     : {os.getlogin()}",
        f"Python   : {platform.python_version()}",
    ]
    print("\n".join(info_lines))


def cmd_read(args):
    """Read and print the contents of a file."""
    if not args:
        print("ERROR: term.read() needs a file path", file=sys.stderr)
        sys.exit(1)
    target = " ".join(args)
    try:
        with open(target, "r", encoding="utf-8") as f:
            print(f.read(), end="")
    except FileNotFoundError:
        print(f"ERROR: file not found '{target}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_write(args):
    """Write text to a file (overwrites existing content)."""
    if len(args) < 2:
        print("ERROR: term.write() needs filepath, content", file=sys.stderr)
        sys.exit(1)
    filepath = args[0]
    content = " ".join(args[1:])
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote {len(content)} bytes to {filepath}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_del(args):
    """Delete a file."""
    if not args:
        print("ERROR: term.del() needs a file path", file=sys.stderr)
        sys.exit(1)
    target = " ".join(args)
    try:
        os.remove(target)
        print(f"Deleted {target}")
    except FileNotFoundError:
        print(f"ERROR: file not found '{target}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_mkdir(args):
    """Create a directory (including parents)."""
    if not args:
        print("ERROR: term.mkdir() needs a directory name", file=sys.stderr)
        sys.exit(1)
    target = " ".join(args)
    try:
        os.makedirs(target, exist_ok=True)
        print(f"Created {target}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_size(args):
    """Print a file's size in bytes."""
    if not args:
        print("ERROR: term.size() needs a file path", file=sys.stderr)
        sys.exit(1)
    target = " ".join(args)
    try:
        print(os.path.getsize(target))
    except FileNotFoundError:
        print(f"ERROR: file not found '{target}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_clip(args):
    """Copy text to the system clipboard (Windows)."""
    if not args:
        print("ERROR: term.clip() needs text to copy", file=sys.stderr)
        sys.exit(1)
    text = " ".join(args)
    try:
        process = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
        process.communicate(text.encode("utf-8"))
        print(f"Copied to clipboard ({len(text)} chars)")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_sleep(args):
    """Pause execution for N seconds."""
    if not args:
        print("ERROR: term.sleep() needs a number of seconds", file=sys.stderr)
        sys.exit(1)
    try:
        seconds = float(args[0])
        time.sleep(seconds)
        print(f"Slept for {seconds}s")
    except ValueError:
        print(f"ERROR: expected a number, got '{args[0]}'", file=sys.stderr)
        sys.exit(1)


# ── dispatch ─────────────────────────────────────────────────────────

DISPATCH = {
    "run":     cmd_run,
    "env":     cmd_env,
    "setenv":  cmd_setenv,
    "cwd":     cmd_cwd,
    "chdir":   cmd_chdir,
    "ls":      cmd_ls,
    "exists":  cmd_exists,
    "sysinfo": cmd_sysinfo,
    "read":    cmd_read,
    "write":   cmd_write,
    "del":     cmd_del,
    "mkdir":   cmd_mkdir,
    "size":    cmd_size,
    "clip":    cmd_clip,
    "sleep":   cmd_sleep,
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
        print(f"ERROR: Unknown subcommand 'term.{command}'", file=sys.stderr)
        sys.exit(1)
