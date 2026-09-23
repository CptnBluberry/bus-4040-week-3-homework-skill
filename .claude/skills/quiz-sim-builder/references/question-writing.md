# Writing Quiz Questions

Generating a quiz is easy. Generating one that teaches something on the way
through is the hard part, and it comes down to the wrong answers.

## No trick questions

The point of a self-test is to find gaps, not to catch the student out. A
question is a trick if a person who understands the material could still get it
wrong — because the wording was ambiguous, because it hinged on a word like
"always" buried mid-sentence, or because it tested recall of a number nobody
would be expected to memorize.

If a question would feel unfair on a real exam, cut it.

## Distractors are the whole game

A multiple-choice question is only as good as its wrong answers. Each distractor
should be something a student with a partial understanding might actually pick.

**Weak** — three of the four are obviously filler:
> Who created Git?
> A) Linus Torvalds  B) A robot  C) Nobody  D) The government

**Strong** — every option is plausible if you half-remember the material:
> Git was created in 2005 for what purpose?
> A) Linux kernel development, after the project lost access to its
>    proprietary tool
> B) To give GitHub a version control system to sell
> C) To replace centralized systems at a single large company
> D) To let one user at a time track changes to individual files

Options B, C, and D each echo something real from the material — GitHub, the
centralized era, the 1970s single-user tools — so picking correctly requires
actually knowing the answer.

Rules for distractors:

- **Draw them from the same material.** The best wrong answer is a true fact
  that answers a *different* question.
- **Match length and grammar to the correct answer.** A correct option that is
  noticeably longer or more detailed is a giveaway, and it is the most common
  tell in AI-generated quizzes.
- **Never use "all of the above" or "none of the above."** They test
  test-taking skill rather than knowledge.
- **Keep them mutually exclusive.** If two options could both be defended, the
  question is broken.

## True/false questions

A true/false question is worth including only when the false version is a
believable misconception. "Git was created in 1823" is not a question, it is a
formality.

Good false statements invert something the material specifically corrects:

> In a centralized version control system, every developer holds a full copy
> of the entire history.  → **False.** That describes Git. Centralized systems
> required everyone to depend on one central server.

Aim for a roughly even split of true and false answers. A student who notices
that most statements are true will start guessing "true."

## Spread the correct answer around

Track which index is correct across the whole set. If half the answers sit at
option A, the quiz is guessable without reading. The validator warns when any
one position holds more than 40% of the correct answers.

## Explanations

Every question carries an explanation shown after answering. It should do two
things:

1. State why the correct answer is correct, in one or two sentences.
2. Where a distractor reflects a common confusion, name it.

> **Correct.** Parameters are the numbers tuned inside the model during
> training; tokens are the chunks of text going in and out. They get mixed up
> because both are quoted in large numbers, but you pay per token, not per
> parameter.

Write explanations to be readable by someone who just got the question wrong
and is mildly annoyed. No lecturing, no "as we discussed."

## What to pull questions from

Prioritize in this order:

1. **Definitions and distinctions the material spends time on** — harness vs.
   model, open weight vs. closed, parameters vs. tokens. If the source
   contrasts two things explicitly, that contrast is a question.
2. **Process steps in order** — the branch/add/commit/push/PR sequence.
3. **Concrete facts with a reason attached** — why `Add README` matters when
   creating a repo (it creates the initial commit that maps the repo to `main`).
4. **Numbers that carry meaning** — grading weights, a token being roughly 3/4
   of a word.

Skip entirely: scheduling details, the instructor's personal asides, anything
that reads as a one-off remark rather than course content.

## Before building the file

Read the set start to finish and cut anything that is a near-duplicate of
another question. Twenty questions that each test a distinct idea beat twenty
that circle the same three ideas.
