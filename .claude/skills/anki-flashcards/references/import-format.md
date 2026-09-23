# Anki Import Format

Anki imports plain text. Tab-separated, one note per line, UTF-8, with
configuration supplied as `#` header lines. No `.apkg` tooling is needed.

## File shape

```
#separator:tab
#html:true
#notetype:Basic
#deck:Specifically Calc II
What is the power rule?	\(\frac{d}{dx}[x^n] = nx^{n-1}\)
What is the product rule?	\(\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)\)
```

## Header directives

| Directive | Value | Notes |
|---|---|---|
| `#separator:tab` | `tab` | Always use tab. Commas collide with card content constantly. |
| `#html:true` | `true` | Required — without it, `<br>` displays as literal text. |
| `#notetype:Basic` | note type name | Must match the name in the collection **exactly**, including `+` suffixes like `Basic (and reversed card)+`. |
| `#deck:Name` | deck name | Created on import if absent. `::` makes subdecks. |
| `#tags:` | space-separated | Omit — this collection uses no tags. |

Header lines must come first, before any note. One deck and one note type per
file: if a batch needs two note types, write two files.

## Field rules

Fields are separated by a single tab. `Basic`, `Basic+`, and
`Basic (and reversed card)+` all take exactly **two** fields, so every note line
has exactly **one** tab.

Hard constraints:

- **No literal tab inside a field** — it splits the field. Use `&nbsp;` or a space.
- **No literal newline inside a field** — it splits the note. Use `<br>`.
- **Neither field may be empty** — Anki rejects a note with an empty first field.

## HTML

With `#html:true`, field content is rendered as HTML. The tags used in this
collection: `<br>`, `<div>`, `<strong>`, `<b>`, `<sub>`, `<sup>`, `<code>`,
`<blockquote>`, `<ul>/<ol>` with `<li>`, and `<table>` with inline
`style="border: 1px solid black; padding: 4px;"` on cells.

### Escaping — the trap

Write `&` as `&amp;` and `<` as `&lt;` **only** when you mean a literal
character rather than markup. Do not escape an entity that is already an entity.

- Want an apostrophe in `f'(x)`? Write the character `'` directly.
- `&#x27;` also works.
- `&amp;#x27;` is **wrong** — it renders as the visible text `&#x27;`.

Five notes in the existing collection have this exact defect. The validator
flags it.

## MathJax

Anki renders MathJax natively. **Delimiters are mandatory.**

| Purpose | Delimiter | Example |
|---|---|---|
| Inline | `\(` … `\)` | `\(x^2 + 1\)` |
| Display (own line, centered) | `\[` … `\]` | `\[\int_1^\infty \frac{1}{x^p}dx\]` |

Bare LaTeX without delimiters renders as raw source text. Twelve notes in the
existing collection have LaTeX commands with a missing or malformed opening
delimiter — the most common real defect in the collection. Every `\(` needs a
matching `\)`, and every `\[` a matching `\]`.

Do **not** use `$...$` or `$$...$$`; Anki does not recognize them by default.

Dollar signs, percent signs, and underscores outside math mode are fine in HTML
and need no escaping.

## Importing

File > Import, select the file. Anki reads the headers and shows the deck and
note type — verify that line matches what the file declares, then Import.
Duplicate detection is on the first field: re-importing an updated file updates
existing notes rather than duplicating them, which makes iteration safe.
