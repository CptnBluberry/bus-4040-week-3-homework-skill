# BUS 4040 - Week 3

---

## Slide 1 - Welcome

Welcome to the third week of BUS 4040 - AI for Business Applications

- This week is a high level introduction to modern AI and the tools you will use in this class
- Goal for today is to bring the concepts and tools we have discussed into a cohesive working environment.
- These tools will be your workbench and the foundation for the remainder of this course.

## Slide 2 - AI in General
- AI research started in the 1950's
  - The AI we are using today surfaced around 2011
  - There has been explosive progress since 2023
- AI takes text in and produces text out (input / output)
  - You give it words, and it uses math to predict the next word
- That's all you need to know to successfully use AI
- A given AI "model" is trained by reviewing data in a sophisticated "Guess, Check, and Tune" cycle.
- Different models are different sizes and different training, so they offer different functionality at different speed, cost, and output quality


## Slide 3 - AI Models

- A "model" is a single trained AI.
- A company usually ships a family of them, small to large (i.e., cheap to expensive)
- The pattern is common: a family name, a size tier, a version number, and a price tag

- **Anthropic** makes **Claude**
  - Four model tiers, largest to smallest: Fable, Opus, Sonnet, Haiku
  - Current versions are Fable 5.1, Opus 5, Sonnet 5, and Haiku 4.5
  - Fable is the top end model for the hardest problems, and it is priced accordingly
  - Opus is a solid step up in capability from Sonnet, at roughly twice the cost
  - Sonnet is the cost effective everyday workhorse
  - Haiku is fast, cheap, and less capable, good for simple high volume work

- **OpenAI** makes **ChatGPT**, built on the **GPT** models
  - ChatGPT is the product, GPT is the model underneath, the two names get used interchangeably
  - Older versions were plain numbers, GPT-3.5, GPT-4, GPT-5
  - They now name tiers like Claude does: GPT-5.6 ships as Sol, Terra, and Luna, largest to smallest
  - GPT-6 Astra is the current top model

- **Google** makes **Gemini** and **Gemma**
  - Gemini is the large commercial model, sold through Google and built into Search and Workspace
  - Gemma is the small open model you can download and run yourself

- **Alibaba** makes **Qwen**
  - Chinese, open weight, strong at coding and at languages other than English
  - Popular for running privately because you can host it on your own hardware

- **Meta** (Facebook) makes **Llama**
  - The model that made open weight AI mainstream
  - Free to download and widely used as the starting point for custom business models

- **Europe** is building sovereign models so that public data does not have to leave the region
  - Mistral in France is the best known
  - **Germany** recently released **SOOFI-S**, pronounced like "Sophie", short for Sovereign Open-Source Foundation Models
    - Built by a German consortium coordinated by the German AI Association, funded by the German government and the EU
    - Open source, and it publishes its full training data list (about 27 trillion tokens) so the data can be audited
    - Aimed at European industry and government that do not want to depend on foreign tech providers

- **Open weight vs closed**
  - Closed models (Claude, GPT, Gemini) run on the vendor's servers, you rent access
  - Open weight models (Llama, Qwen, Gemma) can be downloaded and run on your own hardware
  - The business tradeoff is control and privacy against convenience and top end quality

- Bottom line for business: there is no single best model, there is a best fit for the job, the budget, and the privacy requirement


## Slide 4 - Parameters & Tokens

- **Parameters** are the numbers inside a model that get tuned during training
  - More parameters generally means more capability, considerably higher hardware requirements and cost to maintain speed
  - Sizes are quoted in billions, for example a 7B model versus a 70B model
  - You do not pick models by parameter count, you pick by result, speed, and price
- **Tokens** are chunks of text, roughly 3/4 of an English word on average
  - AI does not read whole words, it reads a token
  - Short common words are one token, longer or unusual words get split into several tokens
- Why does this matter?
  - You pay per token, input and output
  - Every model has a limit on how many tokens it can consider at once (the context window)
  - Long documents, long chat history, big data pastes all burn tokens
  - Every turn resends the whole conversation, so a long chat costs more per message than a short one
  - Large context windows can cause AI sessions to drift off track


## Slide 5 - Harnesses vs. Models

- A **harness** is the program you use to interact with an AI model. The **model** is the AI behind the harness
  - The harness is the music player, the model is the music
  - Example harnesses: the Claude app, Claude Code, Codex, Forge Code, Ollama
- Not a big deal for this class, but the same model may behave differently when accessed by different harnesses
  - Using a model directly is not a common business process
- The harness is where the usability features live
  - The harness manages the chat interface and the context memory
  - **Skills**, reusable instructions for a repeated task
  - **Agents**, a model turned loose to work through several steps on its own
  - **Slash commands**, typed shortcuts like `/clear` that control the tool

- The Claude harness in particular
  - `CLAUDE.md` is a standing instruction file Claude reads every session
    - Global applies to all your work
    - Project applies to one folder
  - Slash commands are helpful
    - `/clear` starts a fresh conversation
    - `/memory` edits what Claude remembers
    - `/compact` shrinks the data in the context (can reduce cost and drift)
    - `/agents` manages agents
  - Ask Claude to write results to a file if you want to pick up later

- Every harness presents the functionality differently (kind of like how Windows has different commands than a Mac, or iOS vs. Android)

## Slide 6 - The Models You Will Use

- In this class you have access to two AI systems
  - Claude
  - U of I Mindrouter
- Both systems have a graphical user interface (GUI), a command line interface (CLI), and connect to VS Code
- The CLI is a bit more complicated and much more powerful
  - You do not need the CLI for this class
  - You should know it exists and roughly what it provides
- VS Code is a good balance, yet the GUI will work fine.

## Slide 7 - Accessing U of I Mindrouter

- Mindrouter has more setup than Claude
- Reference: week-3-cline-mindrouter-setup.md

## Slide 8 - VS Code, GUI, CLI, Oh My!
- VS Code will be the default interface for in class illustration
- All interfaces are acceptable, use whatever you are comfortable with
