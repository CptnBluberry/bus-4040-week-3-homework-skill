#!/usr/bin/env python3
"""Validate an Anki tab-separated import file before importing it.

Catches the defects that actually occur in this collection: LaTeX with missing
math delimiters, double-escaped HTML entities, wrong field counts, and
duplicate fronts.

Usage:
    python validate_deck.py <file.txt>

Exit codes:  0 = passed (warnings allowed)   1 = errors found   2 = bad usage
"""

import re
import sys
import unicodedata
from collections import Counter

REQUIRED_HEADERS = ("separator", "html", "notetype", "deck")

# Field count per note type. All types used in this collection take two fields.
FIELD_COUNTS = {
    "Basic": 2,
    "Basic+": 2,
    "Basic (and reversed card)": 2,
    "Basic (and reversed card)+": 2,
    "Basic (type in the answer)": 2,
    "Cloze": 2,
}

BS = chr(92)  # backslash, kept out of literals so the intent stays readable

# Common math commands. Finding one of these outside a delimited math region
# means it will render as raw source text.
MATH_COMMANDS = (
    "frac sum int lim sqrt mathbb mathcal cdot times pm mp infty alpha beta "
    "gamma delta theta lambda sigma omega partial nabla forall exists in "
    "subset cup cap neq leq geq approx equiv rightarrow leftarrow Rightarrow "
    "ln log sin cos tan arctan arcsin arccos binom begin end left right"
).split()

INLINE_MATH = re.compile(re.escape(BS + "(") + r".*?" + re.escape(BS + ")"), re.S)
DISPLAY_MATH = re.compile(re.escape(BS + "[") + r".*?" + re.escape(BS + "]"), re.S)
LATEX_TOKEN = re.compile(re.escape(BS) + r"([a-zA-Z]+)")
DOUBLE_ESCAPED = re.compile(r"&amp;(#x?[0-9a-fA-F]+|[a-zA-Z]+);")
DOLLAR_MATH = re.compile(r"\$[^$]+\$")
HTML_TAG = re.compile(r"<[^>]+>")

MAX_FIELD_CHARS = 700  # beyond this a card is usually doing too much


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, line_no, msg):
        self.errors.append((line_no, msg))

    def warn(self, line_no, msg):
        self.warnings.append((line_no, msg))


def strip_math(text):
    """Remove delimited math regions so what remains should be plain content."""
    return DISPLAY_MATH.sub(" ", INLINE_MATH.sub(" ", text))


def check_math(field, line_no, where, rep):
    opens_p = field.count(BS + "(")
    closes_p = field.count(BS + ")")
    opens_b = field.count(BS + "[")
    closes_b = field.count(BS + "]")

    if opens_p != closes_p:
        rep.error(line_no, f"{where}: {opens_p} '{BS}(' vs {closes_p} '{BS})' "
                           "- unbalanced inline math delimiters")
    if opens_b != closes_b:
        rep.error(line_no, f"{where}: {opens_b} '{BS}[' vs {closes_b} '{BS}]' "
                           "- unbalanced display math delimiters")

    # LaTeX commands sitting outside any delimited region render as source text.
    leftover = strip_math(field)
    stray = {m.group(1) for m in LATEX_TOKEN.finditer(leftover)
             if m.group(1) in MATH_COMMANDS}
    if stray:
        listed = ", ".join(BS + s for s in sorted(stray))
        rep.error(line_no, f"{where}: LaTeX outside math delimiters ({listed}) "
                           f"- wrap it in {BS}( ... {BS}) or {BS}[ ... {BS}]")

    if DOLLAR_MATH.search(strip_math(field)):
        rep.warn(line_no, f"{where}: '$...$' found - Anki does not render this "
                          f"by default, use {BS}( ... {BS})")


def check_field(field, line_no, where, rep):
    if not field.strip():
        rep.error(line_no, f"{where}: field is empty")
        return

    for m in DOUBLE_ESCAPED.finditer(field):
        rep.error(line_no, f"{where}: double-escaped entity '{m.group(0)}' "
                           f"- renders as literal text, write '&{m.group(1)};'")

    if "\t" in field:
        rep.error(line_no, f"{where}: contains a literal tab")

    check_math(field, line_no, where, rep)

    if len(field) > MAX_FIELD_CHARS:
        rep.warn(line_no, f"{where}: {len(field)} chars - likely too much for "
                          "one card, consider splitting")

    for ch in field:
        if unicodedata.category(ch) == "Cc" and ch not in "\t\n":
            rep.warn(line_no, f"{where}: control character U+{ord(ch):04X}")


def plain_text(field):
    """Normalize a field for duplicate comparison."""
    text = HTML_TAG.sub("", field).replace("&nbsp;", " ")
    return " ".join(text.split()).lower()


def validate(path):
    rep = Report()
    with open(path, encoding="utf-8") as fh:
        raw_lines = fh.read().split("\n")

    headers = {}
    notes = []           # (line_no, [fields])
    seen_note = False

    for idx, raw in enumerate(raw_lines, start=1):
        line = raw.rstrip("\r")
        if not line.strip():
            continue

        if line.startswith("#"):
            if seen_note:
                rep.error(idx, "header directive appears after notes have "
                               "started - headers must come first")
            key, _, value = line[1:].partition(":")
            headers[key.strip().lower()] = value.strip()
            continue

        seen_note = True
        notes.append((idx, line.split("\t")))

    # --- headers -----------------------------------------------------------
    for key in REQUIRED_HEADERS:
        if key not in headers:
            rep.error(0, f"missing required header '#{key}:'")

    if headers.get("separator", "").lower() not in ("tab", ""):
        rep.error(0, f"#separator is '{headers['separator']}' - use 'tab'")
    if headers.get("html", "").lower() not in ("true", ""):
        rep.error(0, "#html is not 'true' - HTML tags will render as literal text")

    notetype = headers.get("notetype", "")
    if notetype and notetype not in FIELD_COUNTS:
        rep.warn(0, f"unrecognized note type '{notetype}' - verify it exists in "
                    "the collection and that the name matches exactly")
    expected = FIELD_COUNTS.get(notetype, 2)

    if "tags" in headers:
        rep.warn(0, "#tags declared - this collection uses no tags")

    # --- notes -------------------------------------------------------------
    if not notes:
        rep.error(0, "file contains no notes")

    for line_no, fields in notes:
        if len(fields) != expected:
            rep.error(line_no, f"{len(fields)} field(s), expected {expected} "
                               f"for '{notetype}' ({expected - 1} tab(s) per line)")
            continue
        for pos, field in enumerate(fields):
            label = "Front" if pos == 0 else "Back" if pos == 1 else f"Field {pos+1}"
            check_field(field, line_no, label, rep)

    fronts = Counter(plain_text(f[0]) for _, f in notes if f and f[0].strip())
    for text, count in fronts.items():
        if count > 1:
            preview = text[:60] + ("..." if len(text) > 60 else "")
            rep.error(0, f"duplicate front appears {count} times: '{preview}'")

    return rep, len(notes), headers


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    path = sys.argv[1]
    try:
        rep, count, headers = validate(path)
    except FileNotFoundError:
        print(f"ERROR: no such file: {path}")
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: file is not valid UTF-8: {exc}")
        return 2

    for line_no, msg in rep.errors:
        where = f"line {line_no}" if line_no else "header"
        print(f"ERROR   {where}: {msg}")
    for line_no, msg in rep.warnings:
        where = f"line {line_no}" if line_no else "header"
        print(f"WARN    {where}: {msg}")

    print()
    print(f"{path}")
    print(f"  notes     : {count}")
    print(f"  note type : {headers.get('notetype', '?')}")
    print(f"  deck      : {headers.get('deck', '?')}")
    print(f"  errors    : {len(rep.errors)}")
    print(f"  warnings  : {len(rep.warnings)}")

    if rep.errors:
        print("\nFAILED - fix the errors above before importing.")
        return 1
    print("\nPASSED - safe to import.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
