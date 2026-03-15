# 🌿 Mint Plugins

The official plugin registry for the [Mint scripting language](https://github.com/fruzino/Mint).  
Install any plugin in one line directly from the Mint REPL or a `.mint` script.

```
cip.install(pi)
cip.install(strtools)
cip.list()
```

---

## 📦 Available Plugins

| Plugin | Namespace | Description |
|--------|-----------|-------------|
| `pi` | `pi` | Pi math utilities — `pi.value()`, `pi.rad()`, `pi.area()` |
| `strtools` | `str` | String manipulation — `str.upper()`, `str.replace()` |
| `cip` | `cip` | Mint package installer — `cip.install()`, `cip.list()` |

> More plugins are added as the community contributes. Run `cip.list()` in Mint to see the latest.

---

## 🚀 Installing Plugins

Make sure you have Mint installed, then in any `.mint` script or the REPL:

```
cip.install(pi)       # install a plugin
cip.remove(pi)        # remove a plugin
cip.update(pi)        # update to latest version
cip.list()            # browse all available plugins
cip.search(math)      # search by keyword
cip.info(pi)          # show details about a plugin
```

Plugins are placed into your `plugins\` folder automatically.  
Restart Mint after installing to load the new commands.

---

## 🛠️ Creating a Plugin

### Step 1 — Fork this repo

Click the **Fork** button at the top right of this page.  
Clone your fork:

```powershell
git clone https://github.com/YOUR_USERNAME/mintplugins.git
cd mintplugins
```

### Step 2 — Create your plugin folder

```
plugins/
  myplugin/
    Plugin.py       ← command handlers
    Plugin.plug     ← manifest
```

### Step 3 — Write Plugin.plug

```ini
script      = plugins/myplugin/Plugin.py
namespace   = myplugin
description = A short description of what your plugin does
author      = YourName
version     = 1.0.0
cmd         = hello
cmd         = shout
```

| Field | Required | Description |
|-------|----------|-------------|
| `script` | ✅ | Path to Plugin.py relative to mint.exe |
| `namespace` | ✅ | Dot-prefix for commands — `myplugin` → `myplugin.hello()` |
| `cmd` | ✅ | A subcommand to register. One line per command. |
| `description` | ☐ | Shown in `cip.list()` |
| `author` | ☐ | Your name or handle |
| `version` | ☐ | Semver e.g. `1.0.0` |
| `dep` | ☐ | A pip dependency. Auto-installed by `cip.install()`. One per line. |

### Step 4 — Write Plugin.py

```python
"""
Plugin.py  -  myplugin for Mint Shell
Namespace: myplugin
"""
import sys

def cmd_hello(args):
    name = args[0] if args else "World"
    print(f"Hello, {name}!")   # print() → captured into @_ in Mint

def cmd_shout(args):
    print(" ".join(args).upper())

DISPATCH = {
    "hello": cmd_hello,
    "shout": cmd_shout,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No subcommand provided", file=sys.stderr)
        sys.exit(1)
    fn = DISPATCH.get(sys.argv[1])
    if fn:
        fn(sys.argv[2:])
    else:
        print(f"Unknown: myplugin.{sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
```

> **Important:** Always `print()` your results — never `return` them.  
> Mint captures stdout and stores it in `@_` automatically.

### Step 5 — Test locally

Copy your plugin folder into `C:\Mint\Mint\plugins\myplugin\` and test:

```
myplugin.hello(Alice)
write(@_)

myplugin.shout(hello from mint)
write(@_)
```

### Step 6 — Push and open a Pull Request

```powershell
git add .
git commit -m "Add myplugin — short description"
git push origin main
```

Then go to `github.com/YOUR_USERNAME/mintplugins` → click **Contribute** → **Open pull request**.

Once merged your plugin is instantly available to everyone via `cip.install(myplugin)`. 🎉

---

## 📋 Plugin Rules

Before submitting a PR, make sure your plugin follows these rules:

- ✅ Folder name matches the plugin name
- ✅ `Plugin.py` and `Plugin.plug` are both present
- ✅ `namespace` field is set and is **unique** — check existing plugins first
- ✅ `description`, `author`, `version` fields are filled in
- ✅ All commands `print()` their output — never `return`
- ✅ Errors go to `stderr` with a clear message
- ✅ Plugin is tested locally before submitting
- ❌ No malicious, harmful, or destructive code
- ❌ No hardcoded credentials or API keys

A GitHub Action runs automatically on every PR and validates your plugin structure.  
Fix any errors it reports before asking for a review.

---

## 📁 Repo Structure

```
mintplugins/
  README.md
  .github/
    workflows/
      validate.yml      ← auto-validates every PR
  plugins/
    pi/
      Plugin.py
      Plugin.plug
    strtools/
      Plugin.py
      Plugin.plug
    cip/
      Plugin.py
      Plugin.plug
    _Template/          ← copy this to start a new plugin
      Plugin.py
      Plugin.plug
```

---

## 🤝 Contributing

All contributions welcome — bug fixes, new plugins, improvements to existing ones.  
Open an issue first if you're unsure whether your plugin fits.

Made with 🌿 by [Fruzio](https://github.com/fruzino)
