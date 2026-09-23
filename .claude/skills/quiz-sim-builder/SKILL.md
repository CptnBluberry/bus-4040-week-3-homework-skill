---
name: quiz-sim-builder
description: Builds a self-contained single-file HTML quiz simulator from course material such as weekly narrative markdown files, lecture notes, or readings. Use when the user asks for a quiz, quiz simulator, practice test, self-test, or study quiz generated from their own documents.
---

# Quiz Simulator Builder

Turns course material into one `index.html` file that runs by double-clicking it
— no server, no build step, no internet, no external libraries.

## The grounding rule

**Use only facts stated in the source files.** Do not add outside knowledge,
even when you are confident it is correct and related. If the material is
unclear or contradicts itself, skip that point rather than guessing.

This is the rule that makes the quiz worth taking: a student reviewing for an
exam needs to be tested on what the course actually said, not on what is
generally true about the subject. A question the instructor never taught is
worse than no question.

Do not introduce vocabulary the source material does not use. If the narrative
says "harness," do not write a question about "orchestration layers."

## Workflow

1. **Identify the sources.** Ask for the folder or files if not given. List them
   back before generating, so the user can catch a missing week.

2. **Extract candidate facts**, tracking which source file each came from. The
   provenance label is a required field on every question, so capture it while
   reading, not afterward from memory.

3. **Write the questions.** Read `references/question-writing.md` first — it
   covers distractor quality, the traps to avoid, and how to balance coverage
   across sources. This is the part that determines whether the quiz is useful.

4. **Build the file** from `assets/quiz-template.html`. Replace only the JSON
   inside the `<script type="application/json" id="quiz-data">` block. Do not
   restructure the surrounding HTML, CSS, or JavaScript — the template is
   already tested and the validator assumes its shape. Schema is documented in
   `references/output-spec.md`.

5. **Validate — always:**
   ```
   python .claude/skills/quiz-sim-builder/scripts/validate_quiz.py index.html --expect 20
   ```
   Fix every error and re-run until it passes. Never hand over a file that has
   not passed.

6. **Report**: question count, the multiple-choice / true-false split, coverage
   per source, the file path, and that it opens by double-clicking.

## Defaults

Unless the user says otherwise:

| Setting | Default |
|---|---|
| Question count | 20 |
| Mix | Both multiple-choice and true/false, roughly 70/30 |
| Multiple-choice options | 4 |
| Order | Shuffled fresh on every run, including option order |
| Feedback | Immediate, with an explanation and the source label |
| End of quiz | Score, per-source breakdown, retry-missed-only |

Spread questions across sources roughly evenly by content volume. A quiz where
16 of 20 questions come from one week teaches the student that the other weeks
do not matter.

## Constraints on the output file

These are hard requirements, not preferences:

- **One file.** No separate CSS or JS, no images that live elsewhere.
- **Nothing external.** No `<script src>`, no `<link rel="stylesheet">`, no
  CDN, no web fonts, no `fetch`. It must work with the network off.
- **Opens from the filesystem.** It will be run as `file:///...`, so anything
  requiring an HTTP origin is unavailable — that rules out ES modules,
  `fetch()` on local files, and most of the storage APIs. The template already
  respects this.
- **Plain language.** The audience is a business student, not a programmer.

## References

- `references/question-writing.md` — question quality. **Read before writing.**
- `references/output-spec.md` — the JSON schema and how the template consumes it.
- `assets/quiz-template.html` — the tested shell. Copy, then swap the JSON.
