"""
Plugin.py  -  extract plugin for Mint Shell
=============================================
Namespace: extract

Extracts structured data from chat-style text using user-defined regex patterns.

Usage in Mint:
    extract.text(<Alice> I live in London phone is 12345 <Bob> I lived in Paris phone is 67890)
    extract.field(Location, (?:live[sd]?|living)\s+in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*))
    extract.field(Phone, phone\s+is\s+(\S+))
    extract.run()
    extract.save(output.csv)
    extract.clear()
"""

import sys
import re
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE  = os.path.join(SCRIPT_DIR, "_extract_temp.json")

def save_temp(data):
    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_temp():
    if not os.path.exists(TEMP_FILE):
        return {"text": "", "fields": [], "rows": [], "headers": []}
    with open(TEMP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def cmd_text(args):
    """Store the chat text to extract from."""
    if not args:
        print("ERROR: extract.text() needs text as argument", file=sys.stderr)
        sys.exit(1)
    data = load_temp()
    data["text"] = " ".join(args)
    data["fields"] = []   # reset fields when new text is set
    data["rows"] = []
    data["headers"] = []
    save_temp(data)
    print(f"Text loaded. {len(re.findall(r'<([^>]+)>', data['text']))} user(s) found.")

def cmd_field(args):
    """
    Add a field to extract.
    Usage: extract.field(FieldName, regex_with_one_capture_group)
    The first capture group () is what gets extracted.
    """
    if len(args) < 2:
        print("ERROR: extract.field() needs a field name and a regex", file=sys.stderr)
        sys.exit(1)
    name  = args[0].strip()
    regex = " ".join(args[1:]).strip()  # regex may contain spaces

    # Validate regex
    try:
        re.compile(regex)
    except re.error as e:
        print(f"ERROR: Invalid regex '{regex}': {e}", file=sys.stderr)
        sys.exit(1)

    data = load_temp()
    # Remove existing field with same name if present
    data["fields"] = [f for f in data.get("fields", []) if f["name"] != name]
    data["fields"].append({"name": name, "regex": regex})
    save_temp(data)
    print(f"Field '{name}' added. ({len(data['fields'])} field(s) defined)")

def cmd_run(args):
    """Run extraction using stored text and fields. Results stored for save()."""
    data = load_temp()

    if not data.get("text"):
        print("ERROR: No text set. Use extract.text() first.", file=sys.stderr)
        sys.exit(1)
    if not data.get("fields"):
        print("ERROR: No fields defined. Use extract.field() first.", file=sys.stderr)
        sys.exit(1)

    chat_text = data["text"]
    fields    = data["fields"]

    users = sorted(set(re.findall(r"<([^>]+)>", chat_text)))
    if not users:
        print("ERROR: No <Username> tags found in text.", file=sys.stderr)
        sys.exit(1)

    headers = ["User"] + [f["name"] for f in fields]
    rows = []

    for user in users:
        user_parts = re.findall(
            rf"<{re.escape(user)}>(.*?)(?=<[^>]+>|$)",
            chat_text, re.DOTALL
        )
        combined = " ".join(user_parts).strip()

        row = [user]
        for field in fields:
            m = re.search(field["regex"], combined, re.IGNORECASE)
            row.append(m.group(1) if m and m.lastindex and m.lastindex >= 1 else "Unknown")
        rows.append(row)

    data["headers"] = headers
    data["rows"]    = rows
    save_temp(data)

    # Print table
    try:
        from tabulate import tabulate
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    except ImportError:
        col_w = [max(len(str(r[i])) for r in [headers] + rows) for i in range(len(headers))]
        def row_str(r):
            return " | ".join(str(r[i]).ljust(col_w[i]) for i in range(len(r)))
        print(row_str(headers))
        print("-+-".join("-" * w for w in col_w))
        for r in rows:
            print(row_str(r))

    print(f"\n{len(rows)} user(s) extracted.")

def cmd_save(args):
    """Save last run() results to CSV."""
    import csv
    data    = load_temp()
    headers = data.get("headers", [])
    rows    = data.get("rows", [])

    if not rows:
        print("ERROR: No results yet. Run extract.run() first.", file=sys.stderr)
        sys.exit(1)

    filename = args[0].strip() if args else "output.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"Saved {len(rows)} row(s) to {filename}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_clear(args):
    """Clear all stored data."""
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)
    print("Cleared.")

def cmd_fields(args):
    """List currently defined fields."""
    data   = load_temp()
    fields = data.get("fields", [])
    if not fields:
        print("No fields defined yet.")
        return
    print(f"{len(fields)} field(s):")
    for i, f in enumerate(fields):
        print(f"  [{i+1}] {f['name']}: {f['regex']}")

DISPATCH = {
    "text":   cmd_text,
    "field":  cmd_field,
    "run":    cmd_run,
    "save":   cmd_save,
    "clear":  cmd_clear,
    "fields": cmd_fields,
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
        print(f"ERROR: Unknown subcommand 'extract.{command}'", file=sys.stderr)
        sys.exit(1)