# Card Writing Rules

The file format is trivial. Card *quality* is the hard part and the reason this
skill exists. A deck of bad cards is worse than no deck — it burns review time
daily and trains recall of the wrong things.

## The core principle: one card, one fact

A card should have exactly one correct answer that can be produced in a few
seconds. If answering requires recalling several independent things, the card
will fail intermittently for different reasons, and the scheduling algorithm
cannot help — it only knows "wrong."

**Bad** — four facts welded together:
> Front: What are the derivative rules?
> Back: Power rule, product rule, quotient rule, chain rule...

**Good** — four cards, each independently schedulable:
> Front: What is the product rule?
> Back: \(\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)\)

## Anti-patterns to reject

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| **Enumeration** — "List all seven..." | All-or-nothing; fails on the one you forget | One card per item, or ask for the count separately |
| **Yes/no question** | 50% correct by guessing | Ask *why* or *when* instead |
| **Ambiguous front** — "Integration by parts?" | Unclear what's being asked; the user answers a different question each time | Make the question specific: "What is the integration by parts *formula*?" |
| **Answer leaks in the question** | Recognition, not recall | Remove the giveaway wording |
| **Copy-pasted paragraph** | Nothing testable; the user reads and clicks through | Extract the single claim that matters |
| **Unresolved pronoun/context** — "What does it converge to?" | Meaningless six months later out of deck order | Every card stands alone |

## Reversibility

Only make a card reversed when **both directions are useful and unambiguous**.

- `abash` ↔ `to humiliate or embarrass` — reversible. Both directions are real
  recall tasks, and the mapping is one-to-one.
- `What is a regular language?` ↔ `A language recognized by some DFA` — **not**
  reversible. The reverse direction has many valid question phrasings, so the
  user will "fail" cards they actually know.

## Formulas and notation

State the formula, then decode it if the notation is dense. This mirrors the
user's own habit:

> Front: What does \[\delta^*(q_i,w)=Q_j\] mean?
>
> Back: This is an extended transition function.<br><br>Or in plain English:
> start in state \(q_i\), read the whole string \(w\), and tell me every state
> the automaton could be in afterward.

For drill-style pattern cards (the `Basic+` type), front is the input and back
is the worked result, with no prose:

> Front: \(y=\sin(x)(x^2)\)
> Back: \(y'=(\cos x)(x^2)+(\sin x)(2x)\)

Build these in graduated sets — constant, linear, polynomial, then composite —
so the pattern is visible across cards rather than explained on one.

## How many cards

Coverage is not the goal; retention is. From a dense textbook section, 10–25
cards is usually right. Signs you have overshot:

- Cards testing trivia the user would never need to produce from memory
- Several cards that are rephrasings of each other
- Cards whose answer is "it depends" or a judgment call

When the source genuinely contains more than the requested count, prioritize:
**definitions and formulas the user must produce cold** > **conditions and
edge cases** ("converges for p>1") > **worked patterns** > **historical or
contextual detail** (usually skip entirely).

## Before writing the file

Re-read each card and ask: *could I answer this in five seconds, and is there
exactly one right answer?* Cut or split every card that fails.
