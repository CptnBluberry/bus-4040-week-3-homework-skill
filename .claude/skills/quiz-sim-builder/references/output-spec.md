# Output Spec

## How the template works

`assets/quiz-template.html` is a complete, tested quiz application. The question
data lives in exactly one place:

```html
<script type="application/json" id="quiz-data">
{ ... }
</script>
```

The page reads it at startup with
`JSON.parse(document.getElementById('quiz-data').textContent)`.

**Build a quiz by replacing the contents of that block and nothing else.** The
surrounding HTML, CSS, and JavaScript are already correct; editing them
invalidates the validator's assumptions and is how a working template turns
into a broken one-off.

A `<script type="application/json">` block is used rather than a JavaScript
array on purpose: the browser never executes it, unescaped apostrophes and
quotes in question text cannot break the page, and the validator can parse the
data with a strict JSON parser instead of guessing at JavaScript syntax.

## Schema

```json
{
  "title": "BUS 4040 — Weeks 1-3 Practice Quiz",
  "questions": [
    {
      "id": "w2-git-origin",
      "source": "Week 2",
      "type": "mc",
      "prompt": "Git was created in 2005 for what purpose?",
      "options": [
        "Linux kernel development, after the project lost access to its proprietary tool",
        "To give GitHub a version control system to sell",
        "To replace centralized systems at a single large company",
        "To let one user at a time track changes to individual files"
      ],
      "answer": 0,
      "explanation": "Linus Torvalds wrote Git for Linux kernel development after the project lost access to its proprietary tool, and released it free, fast, and decentralized."
    }
  ]
}
```

### Top level

| Field | Type | Notes |
|---|---|---|
| `title` | string | Shown in the page header and the browser tab. |
| `questions` | array | One entry per question. Order does not matter — the page shuffles. |

### Question object

| Field | Type | Rules |
|---|---|---|
| `id` | string | Unique, kebab-case. Prefix with the source (`w1-`, `w2-`) for readability. |
| `source` | string | Where the answer comes from, e.g. `"Week 2"`. Shown with the feedback so the student knows what to review. Required, never empty. |
| `type` | string | `"mc"` or `"tf"`. |
| `prompt` | string | The question. Plain text; no HTML. |
| `options` | array of strings | `mc`: 3–5 entries, 4 preferred. `tf`: exactly `["True", "False"]`. |
| `answer` | integer | Zero-based index into `options`. |
| `explanation` | string | Why the answer is right. Shown after the student responds. Required, never empty. |

## Behavior the template already implements

You do not need to write any of this — it is in the template:

- Questions shuffled on every run; multiple-choice options shuffled too, with
  the correct index tracked through the shuffle. True/false keeps True first.
- One question on screen at a time, with a progress counter.
- Immediate feedback on selection, with the explanation and source label.
- Keyboard support: `1`–`5` select an option, `Enter` advances.
- Final screen with score, percentage, and a per-source breakdown of misses.
- **Retry missed only** — requizzes just the wrong ones, reshuffled.
- Runs entirely from `file://`. No network, no storage APIs, no libraries.

## Validation

```
python scripts/validate_quiz.py index.html --expect 20
```

Errors (exit 1):

- Missing or unparseable `quiz-data` block
- Any external reference — `<script src>`, `<link rel=stylesheet>`, `@import`,
  an `http://` or `https://` URL in markup
- Schema violations: missing field, bad `type`, `answer` out of range, empty
  `source` or `explanation`, wrong option count, malformed true/false options
- Duplicate `id` or duplicate `prompt`

Warnings (exit 0, but fix if easy):

- Question count differs from `--expect`
- One answer position holds more than 40% of the correct answers
- A correct option is much longer than its distractors
- A source contributes no questions, or more than half of them
- `all of the above` / `none of the above` in any option
