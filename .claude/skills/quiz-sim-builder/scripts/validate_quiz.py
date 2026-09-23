#!/usr/bin/env python3
"""Validate a generated single-file quiz simulator before handing it over.

Checks that the file is genuinely self-contained (no external references, so it
works offline from file://) and that the embedded question data is well formed.

Usage:
    python validate_quiz.py <index.html> [--expect 20]

Exit codes:  0 = passed (warnings allowed)   1 = errors found   2 = bad usage
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict

QUIZ_DATA = re.compile(
    r'<script[^>]*id=["\']quiz-data["\'][^>]*>(.*?)</script>',
    re.S | re.I,
)

# Patterns that would make the page depend on something outside itself.
EXTERNAL_PATTERNS = [
    (re.compile(r'<script[^>]+\bsrc\s*=', re.I), "external <script src=...>"),
    (re.compile(r'<link[^>]+stylesheet', re.I), "external stylesheet <link>"),
    (re.compile(r'@import\b', re.I), "CSS @import"),
    (re.compile(r'https?://', re.I), "absolute http(s) URL"),
    (re.compile(r'\bfetch\s*\(', re.I), "fetch() call"),
    (re.compile(r'<iframe\b', re.I), "<iframe>"),
    (re.compile(r'\btype\s*=\s*["\']module["\']', re.I),
     'type="module" (blocked by CORS on file://)'),
]

REQUIRED_FIELDS = ("id", "source", "type", "prompt", "options", "answer", "explanation")
VALID_TYPES = ("mc", "tf")
BANNED_OPTION_TEXT = ("all of the above", "none of the above")

POSITION_BIAS_LIMIT = 0.40   # no single answer index should exceed this share
SOURCE_DOMINANCE_LIMIT = 0.50


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append((where, msg))

    def warn(self, where, msg):
        self.warnings.append((where, msg))


def check_self_contained(html, rep):
    """Scan markup for external dependencies, ignoring the question data."""
    stripped = QUIZ_DATA.sub("", html)  # question text may legitimately cite a URL
    for pattern, label in EXTERNAL_PATTERNS:
        match = pattern.search(stripped)
        if match:
            line = stripped[:match.start()].count("\n") + 1
            rep.error(f"line {line}", f"not self-contained: {label}")


def check_question(q, pos, rep):
    where = f"question {pos}"

    missing = [f for f in REQUIRED_FIELDS if f not in q]
    if missing:
        rep.error(where, f"missing field(s): {', '.join(missing)}")
        return
    where = f"question {pos} ({q['id']})"

    for field in ("id", "source", "prompt", "explanation"):
        if not isinstance(q[field], str) or not q[field].strip():
            rep.error(where, f"'{field}' must be a non-empty string")

    qtype = q["type"]
    if qtype not in VALID_TYPES:
        rep.error(where, f"type '{qtype}' is not one of {VALID_TYPES}")
        return

    options = q["options"]
    if not isinstance(options, list) or not all(isinstance(o, str) for o in options):
        rep.error(where, "'options' must be a list of strings")
        return

    if qtype == "tf":
        if options != ["True", "False"]:
            rep.error(where, f"true/false options must be exactly "
                             f'["True", "False"], got {options}')
    elif not 3 <= len(options) <= 5:
        rep.error(where, f"multiple choice needs 3-5 options, got {len(options)}")

    answer = q["answer"]
    if not isinstance(answer, int) or isinstance(answer, bool):
        rep.error(where, f"'answer' must be an integer index, got {answer!r}")
    elif not 0 <= answer < len(options):
        rep.error(where, f"'answer' is {answer}, out of range for "
                         f"{len(options)} option(s)")

    if len(set(o.strip().lower() for o in options)) != len(options):
        rep.error(where, "duplicate option text")

    for opt in options:
        if opt.strip().lower() in BANNED_OPTION_TEXT:
            rep.warn(where, f"option '{opt}' tests test-taking skill, not knowledge")

    # A correct answer noticeably longer than every distractor is a giveaway.
    if qtype == "mc" and isinstance(answer, int) and 0 <= answer < len(options):
        right = options[answer]
        others = [o for i, o in enumerate(options) if i != answer]
        if others:
            avg = sum(len(o) for o in others) / len(others)
            if len(right) > max(len(o) for o in others) and len(right) > avg * 1.5:
                rep.warn(where, f"correct option is {len(right)} chars vs "
                                f"{avg:.0f} avg for distractors - length gives it away")


def check_set(questions, expect, rep):
    ids = Counter(q.get("id") for q in questions if isinstance(q.get("id"), str))
    for qid, n in ids.items():
        if n > 1:
            rep.error("set", f"duplicate id '{qid}' appears {n} times")

    prompts = Counter(
        " ".join(q["prompt"].lower().split())
        for q in questions if isinstance(q.get("prompt"), str)
    )
    for text, n in prompts.items():
        if n > 1:
            rep.error("set", f"duplicate prompt appears {n} times: "
                             f"'{text[:60]}{'...' if len(text) > 60 else ''}'")

    total = len(questions)
    if expect is not None and total != expect:
        rep.warn("set", f"{total} questions, expected {expect}")

    types = Counter(q.get("type") for q in questions)
    if types.get("mc", 0) == 0 or types.get("tf", 0) == 0:
        rep.warn("set", f"expected a mix of both types, got "
                        f"{types.get('mc', 0)} mc / {types.get('tf', 0)} tf")

    mc = [q for q in questions if q.get("type") == "mc"
          and isinstance(q.get("answer"), int)]
    if len(mc) >= 5:
        positions = Counter(q["answer"] for q in mc)
        top, count = positions.most_common(1)[0]
        share = count / len(mc)
        if share > POSITION_BIAS_LIMIT:
            rep.warn("set", f"{share:.0%} of multiple-choice answers sit at "
                            f"position {top + 1} - spread them out")

    tf = [q for q in questions if q.get("type") == "tf"
          and isinstance(q.get("answer"), int)]
    if len(tf) >= 4:
        trues = sum(1 for q in tf if q["answer"] == 0)
        share = trues / len(tf)
        if share > 0.75 or share < 0.25:
            rep.warn("set", f"{trues} of {len(tf)} true/false answers are "
                            f"'True' - unbalanced, students will guess")

    by_source = defaultdict(int)
    for q in questions:
        if isinstance(q.get("source"), str) and q["source"].strip():
            by_source[q["source"]] += 1
    if by_source and total:
        biggest, n = max(by_source.items(), key=lambda kv: kv[1])
        if len(by_source) > 1 and n / total > SOURCE_DOMINANCE_LIMIT:
            rep.warn("set", f"'{biggest}' supplies {n}/{total} questions - "
                            "coverage is lopsided")
    return by_source


def validate(path, expect):
    rep = Report()
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    check_self_contained(html, rep)

    block = QUIZ_DATA.search(html)
    if not block:
        rep.error("file", 'no <script type="application/json" id="quiz-data"> block')
        return rep, [], {}

    try:
        data = json.loads(block.group(1))
    except json.JSONDecodeError as exc:
        rep.error("quiz-data", f"invalid JSON: {exc}")
        return rep, [], {}

    if not isinstance(data, dict):
        rep.error("quiz-data", "top level must be an object")
        return rep, [], {}
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        rep.error("quiz-data", "'title' must be a non-empty string")

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        rep.error("quiz-data", "'questions' must be a non-empty array")
        return rep, [], {}

    for pos, q in enumerate(questions, start=1):
        if not isinstance(q, dict):
            rep.error(f"question {pos}", "must be an object")
            continue
        check_question(q, pos, rep)

    by_source = check_set(questions, expect, rep)
    return rep, questions, by_source


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--expect", type=int, default=None,
                    help="expected question count (warns on mismatch)")
    args = ap.parse_args()

    try:
        rep, questions, by_source = validate(args.path, args.expect)
    except FileNotFoundError:
        print(f"ERROR: no such file: {args.path}")
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: file is not valid UTF-8: {exc}")
        return 2

    for where, msg in rep.errors:
        print(f"ERROR   {where}: {msg}")
    for where, msg in rep.warnings:
        print(f"WARN    {where}: {msg}")

    types = Counter(q.get("type") for q in questions if isinstance(q, dict))
    print()
    print(args.path)
    print(f"  questions : {len(questions)} "
          f"({types.get('mc', 0)} multiple choice, {types.get('tf', 0)} true/false)")
    for src in sorted(by_source):
        print(f"      {src:<12} {by_source[src]}")
    print(f"  errors    : {len(rep.errors)}")
    print(f"  warnings  : {len(rep.warnings)}")

    if rep.errors:
        print("\nFAILED - fix the errors above before shipping.")
        return 1
    print("\nPASSED - self-contained and well formed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
