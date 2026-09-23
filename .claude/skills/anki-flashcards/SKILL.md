---
name: anki-flashcards
description: Turns source material into an Anki-importable flashcard deck. Use when the user asks to make flashcards, Anki cards, a study deck, or to convert lecture notes, a textbook section, a problem set, or documentation into cards for spaced repetition.
---

# Anki Flashcards

Converts source material into a tab-separated file that imports directly into
Anki, written to match this user's existing collection conventions.

## Workflow

1. **Get the source.** A file path, pasted text, or a named topic. If the user
   names a topic with no material, ask whether to generate from your own
   knowledge or wait for their notes — do not silently invent content they
   intend to supply.

2. **Confirm scope before writing.** State the target deck name and your
   estimated card count, then proceed. Do not stop and wait unless the source is
   ambiguous. Twenty good cards beat sixty mediocre ones; if the source supports
   far more cards than requested, cover the highest-yield material first and say
   what you left out.

3. **Choose the note type** — see the table in "Note types" below.

4. **Extract candidate facts.** One atomic, testable fact per card. Read
   `references/card-writing.md` before writing the first card. Its rules are the
   substance of this skill; skipping it produces generic cards the user will
   delete.

5. **Write the file** to `<topic>-cards.txt` in the working directory, using the
   exact format in `references/import-format.md`.

6. **Validate — always, no exceptions:**
   ```
   python .claude/skills/anki-flashcards/scripts/validate_deck.py <file>
   ```
   Fix every error and re-run until it passes. Never hand the user a file that
   has not passed the validator.

7. **Report**: card count, deck name, note type, file path, and the import steps
   (File > Import, verify the deck/notetype line, Import).

## Note types

| Situation | Note type | Fields |
|---|---|---|
| Default — concept, rule, procedure, definition | `Basic` | Front, Back |
| Term ↔ meaning where recall must run both ways (vocabulary) | `Basic (and reversed card)+` | Front, Back |
| Worked pattern drill (`\(y=x^2\)` → `\(y'=2x\)`) | `Basic+` | Front, Back |

Default to `Basic`. Use the reversed type **only** for vocabulary-style pairs —
it doubles the review load, and reversing a conceptual question produces
nonsense ("*What is the derivative of a constant?*" reversed asks the user to
recall a question from an answer).

This collection contains **no cloze and no image-occlusion notes**. Do not
produce cloze deletions unless the user explicitly asks; if the material seems
to call for it, offer, then wait.

## House style

These come from 2,011 notes in the user's actual collection. They are what make
generated cards match hand-written ones.

- **Math is MathJax, always delimited.** Inline `\(x^2\)`, display `\[\int_1^\infty\]`.
  Bare LaTeX with no delimiter renders as raw source — this is the single most
  common defect in the existing collection, and the validator rejects it.
- **Line breaks are `<br>`.** The file is one card per line, so a literal
  newline inside a field breaks the import. Lists use `<ul>/<ol>` with `<li>`.
- **Restate dense notation in plain language.** After formal notation, the user
  writes `Or in plain English:` followed by a sentence. Follow this whenever a
  card carries notation a reader must decode — it is their strongest habit.
- **Give the mnemonic when a real one exists** (LIATE for choosing `u`). Do not
  invent forced ones.
- **Generalize in a parenthetical** where a pattern extends:
  `(same pattern for cos, divide by a)`.
- **No tags.** The user organizes purely by deck. Do not add a tags column
  unless asked.

## Deck naming

Top-level deck per course or topic, matching existing names where one fits
(`Specifically Calc II`, `Theory of Computation`, `Calc II Memorize`). For a
batch over ~100 cards, split into `::` subdecks of 30 with zero-padded numbering,
mirroring `GRE Vocab Master List::01: Set 1`.

## References

- `references/card-writing.md` — card quality rules. **Read before writing cards.**
- `references/import-format.md` — file format, header directives, escaping.
- `assets/example-deck.txt` — a known-good validated file to model output on.
