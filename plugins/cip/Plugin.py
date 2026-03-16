"""
Plugin.py  -  cip plugin for Mint Shell
==========================================
Auto-discovering Mint Package Installer.
No index.json needed — scans the GitHub repo automatically.

Usage in Mint:
    cip.install(pi)
    cip.remove(pi)
    cip.update(pi)
    cip.list()
    cip.search(math)
    cip.info(pi)
"""

import sys
import os
import json
import shutil
import urllib.request
import urllib.error
import subprocess

# ── Config ────────────────────────────────────────────────────────────────────

GITHUB_USER   = "fruzino"
GITHUB_REPO   = "mintplugins"
GITHUB_BRANCH = "main"

# GitHub API — lists all folders in /plugins/ automatically
API_URL  = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/plugins"
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/plugins"

# Resolve plugins/ dir relative to this script (plugins/cip/ → plugins/)
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
PLUGINS_DIR = os.path.dirname(SCRIPT_DIR)

# ANSI colours
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"
T = "\033[96m"; B = "\033[1m";  X = "\033[0m"

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mint-cip/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"{R}Network error: {e}{X}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{R}Invalid response from server.{X}")
        sys.exit(1)

def fetch_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mint-cip/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode()
    except urllib.error.URLError as e:
        print(f"{R}Download failed: {e}{X}")
        return None

def get_all_plugins():
    """
    Hits the GitHub API to list all folders inside /plugins/.
    Returns a dict: { "pi": { name, url, raw_base }, ... }
    No index.json needed — it's all auto-discovered.
    """
    entries = fetch_json(API_URL)
    plugins = {}
    for entry in entries:
        if entry.get("type") != "dir":
            continue
        name = entry["name"]
        plugins[name] = {
            "name":     name,
            "api_url":  entry["url"],          # API url for this folder
            "raw_base": f"{RAW_BASE}/{name}",  # raw download base
        }
    return plugins

def get_plugin_meta(plugin):
    """
    Reads Plugin.plug from the repo to extract namespace/description.
    Falls back gracefully if not found.
    """
    plug_url = f"{plugin['raw_base']}/Plugin.plug"
    text = fetch_text(plug_url)
    meta = {"namespace": plugin["name"], "description": "", "version": "?", "author": "?", "dependencies": []}
    if not text:
        return meta
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("namespace"):
            meta["namespace"] = line.split("=", 1)[-1].strip()
        elif line.startswith("version"):
            meta["version"] = line.split("=", 1)[-1].strip()
        elif line.startswith("description"):
            meta["description"] = line.split("=", 1)[-1].strip()
        elif line.startswith("author"):
            meta["author"] = line.split("=", 1)[-1].strip()
        elif line.startswith("dep"):
            dep = line.split("=", 1)[-1].strip()
            if dep:
                meta["dependencies"].append(dep)
    return meta

def get_plugin_files(plugin):
    """
    Lists all files in a plugin folder via GitHub API.
    Returns list of filenames. No files.json needed.
    """
    entries = fetch_json(plugin["api_url"])
    return [e["name"] for e in entries if e.get("type") == "file"]

def plugin_path(name):
    return os.path.join(PLUGINS_DIR, name)

def is_installed(name):
    return os.path.isdir(plugin_path(name))

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_install(args):
    if not args:
        print(f"{R}Usage: cip.install(pluginname){X}"); sys.exit(1)
    name    = args[0].strip()
    plugins = get_all_plugins()

    if name not in plugins:
        print(f"{R}Plugin '{name}' not found.{X}")
        print(f"  Try {Y}cip.search({name}){X} or {Y}cip.list(){X}")
        sys.exit(1)

    if is_installed(name):
        print(f"{Y}'{name}' already installed.{X} Use {Y}cip.update({name}){X} to upgrade.")
        return

    plugin = plugins[name]
    meta   = get_plugin_meta(plugin)
    files  = get_plugin_files(plugin)

    print(f"{T}Installing {B}{name}{X}{T} — {meta['description']}{X}")

    dest = plugin_path(name)
    os.makedirs(dest, exist_ok=True)

    for fname in files:
        content = fetch_text(f"{plugin['raw_base']}/{fname}")
        if content is None:
            print(f"{R}  Failed to download {fname} — aborting.{X}")
            shutil.rmtree(dest, ignore_errors=True)
            sys.exit(1)
        with open(os.path.join(dest, fname), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  {G}✓{X} {fname}")

    for dep in meta.get("dependencies", []):
        print(f"  pip install {dep} ...", end=" ", flush=True)
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", dep, "--quiet"],
            capture_output=True
        )
        print(f"{G}✓{X}" if r.returncode == 0 else f"{R}failed{X}")

    print(f"\n{G}{B}'{name}' installed!{X} Restart Mint to use it.")
    print(f"  Namespace: {T}{meta['namespace']}{X}")


def cmd_remove(args):
    if not args:
        print(f"{R}Usage: cip.remove(pluginname){X}"); sys.exit(1)
    name = args[0].strip()
    if not is_installed(name):
        print(f"{Y}'{name}' is not installed.{X}"); return
    shutil.rmtree(plugin_path(name))
    print(f"{G}Removed '{name}'.{X}")


def cmd_update(args):
    if not args:
        print(f"{R}Usage: cip.update(pluginname){X}"); sys.exit(1)
    name = args[0].strip()
    if not is_installed(name):
        print(f"{Y}'{name}' not installed. Use {T}cip.install({name}){X}"); return
    print(f"{T}Updating '{name}'...{X}")
    shutil.rmtree(plugin_path(name))
    cmd_install(args)


def cmd_list(args):
    print(f"{T}Fetching plugin list...{X}\n")
    plugins = get_all_plugins()
    print(f"{T}{B}Available plugins ({len(plugins)}):{X}\n")
    for name, plugin in plugins.items():
        meta = get_plugin_meta(plugin)
        inst = f"{G}[installed]{X}" if is_installed(name) else ""
        print(f"  {B}{name:<16}{X} {meta['description'][:40]:<42} ns:{T}{meta['namespace']}{X} {inst}")
    print()


def cmd_search(args):
    if not args:
        print(f"{R}Usage: cip.search(query){X}"); sys.exit(1)
    q       = args[0].strip().lower()
    plugins = get_all_plugins()
    results = {}
    for name, plugin in plugins.items():
        if q in name.lower():
            results[name] = plugin
            continue
        # also check description from Plugin.plug
        meta = get_plugin_meta(plugin)
        if q in meta.get("description", "").lower() or q in meta.get("namespace","").lower():
            results[name] = (plugin, meta)

    if not results:
        print(f"{Y}No plugins found matching '{q}'.{X}"); return
    print(f"\n{T}{B}Results for '{q}':{X}\n")
    for name, data in results.items():
        plugin = data if isinstance(data, dict) and "api_url" in data else data[0]
        meta   = get_plugin_meta(plugin)
        inst   = f"{G}[installed]{X}" if is_installed(name) else ""
        print(f"  {B}{name}{X} — {meta.get('description','')} {inst}")


def cmd_info(args):
    if not args:
        print(f"{R}Usage: cip.info(pluginname){X}"); sys.exit(1)
    name    = args[0].strip()
    plugins = get_all_plugins()
    if name not in plugins:
        print(f"{R}Plugin '{name}' not found.{X}"); sys.exit(1)
    meta = get_plugin_meta(plugins[name])
    inst = f"{G}Yes{X}" if is_installed(name) else f"{R}No{X}"
    print(f"\n{T}{B}{name}{X}")
    print(f"  Description: {meta.get('description','')}")
    print(f"  Namespace:   {T}{meta.get('namespace', name)}{X}")
    print(f"  Author:      {meta.get('author','?')}")
    print(f"  Version:     {meta.get('version','?')}")
    print(f"  Installed:   {inst}")
    deps = meta.get("dependencies", [])
    if deps: print(f"  Depends on:  {', '.join(deps)}")
    print(f"  Repo:        https://github.com/{GITHUB_USER}/{GITHUB_REPO}/tree/main/plugins/{name}")
    print()


# ── Dispatch ──────────────────────────────────────────────────────────────────

DISPATCH = {
    "install":   cmd_install,
    "remove":    cmd_remove,
    "uninstall": cmd_remove,
    "update":    cmd_update,
    "list":      cmd_list,
    "search":    cmd_search,
    "info":      cmd_info,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{R}No subcommand provided.{X}"); sys.exit(1)
    command = sys.argv[1]
    args    = sys.argv[2:]
    fn = DISPATCH.get(command)
    if fn:
        fn(args)
    else:
        print(f"{R}Unknown cip command: '{command}'{X}"); sys.exit(1)