# BUS 4040 - Week 2

---

## Slide 1 - Welcome 

Welcome to the second week of BUS 4040 - AI for Business Applications


## Slide 2 - A Professor's Dilemma
- There's a reason the cart is in front of the horse
![Cart Before the Horse](week-2-cart-before-horse.jpg)


## Slide 3 - A short History of Version Control
A short history of version control

- 1970s into the 1980s 
  - Early tools tracked changes to individual files on a single machine, one user at a time.
- 1990s into the 2000s
  - Centralized systems versioned entire projects
  - These systems required everyone to depend on one central server to commit, branch, or view history.
- In 2005
  - Linus Torvalds created Git for Linux kernel development after the project lost access to its proprietary tool.
  - Linus released a free, fast, and decentralized code versioning framework.
  - Every developer holds a full copy of the entire history.
  - There's no single bottleneck or single point of failure.

Why does Git matter today?

- It is the near-universal standard, underneath GitHub, GitLab, and almost every software team.
- It is the safety net for moving fast with AI-generated code: every change is reviewable, traceable, and reversible.
- You can always see what changed, undo it, and have someone check it before it reaches a customer.


## Slide 4 - Git and GitHub Overview

- You have a GitHub account
- You can create a repo from the Web GUI
  - Go to the GitHub web page
  - Select your account avatar in the upper right corner
  - Select **Repositories**
  - Select **New** on the right side of the screen
    - The **Owner** should default to your account name
    - The **Name** can be whatever you want
    - Ensure you set **Add README** to **On**
      - This is important because creating the **README** creates an initial commit that maps the repo to the **main** branch.
- Now you can `clone` the repo and build a test webpage
  - To clone a repo, select the repo and copy the URL
  - For example:
    ```bash
    git clone https://github.com/professor-carlyle/example_repo
    ```
- Configure your AI client to work in the new local directory



Let's build a micro-SPEC for an AI to create a basic webpage for a small hotel chain
- The hotel is called "Cheap & Clean Rooms by the Garden"
- The hotel is run by a hip young couple who like birds and flowers, and grow food
- The daily rate is $50 and if you stay for two nights it's $75
- They like blue and sunset colors
- They have a fresh garden and often serve a quality affordable breakfast 
- We want the web page to be simple and attractive
- Add a cool faded watermark, if that works for the design
- Create the page as a single index.html file



AI will build a much more detailed plan
- We will feed the plan back into AI
- The output will be an `index.html` file

1. Create and switch to a new branch
    ```bash
    git checkout -b add-hotel-landing-page
    ```
2. Stage the file(s)
   ```bash
   git add index.html
   # Alternatively use the -A option to add all changed files
   git add -A
   ```
3. Commit
   ```bash
   git commit -m "Add landing page for Cheap & Clean Rooms by the Garden"
   ```

4. Push the branch and set upstream
   ```bash
   git push -u origin add-hotel-landing-page
   ```

5. Create the PR
   ```bash
   gh pr create --base main \
   --head add-hotel-landing-page \
   --title "Add hotel landing page" \
   --body "Simple single-page site for the hotel chain."
   ```
6. Optional: Open the PR in the browser
   ```bash
   gh pr view --web
   ```
7. Return to the GitHub GUI and review the PR (Pull Request)
8. Merge the PR


## Slide 5 - Pictures are Better
> Git is like a Marvel movie multiverse code management system 
> - `git` & `gh` allow you to navigate the code multiverse
> - `main` is the original reality
> - `clone` copies the repo from GitHub to your local computer
> - `checkout` a `branch` to create a new timeline (copy) of `main`
> - `add` stages the files that will be added to the `branch`
> - `commit` updates changes (staged files) to your local branch
> - `push` updates the remote branch (i.e., the branch is pushed to GitHub)
> - `pr` creates a Pull Request to merge the `branch` into `main`

![Pictures are Better](week-2-pictures-are-better.jpg)


## Slide 6 - Configuring (Git) GitHub

**General Warning**
> Please be thoughtful about what you download. I use my computer for personal activities and AI software is the wild west. Avoid granting unfamiliar software access to private folders, and be wary of anything that scans your network or sends you notifications. I say 'no' and 'deny' by default. fwiw, a colleague of mine was hacked recently when he downloaded a voice to text LLM from a site that masqueraded as a trusted software vendor.

- Good old-fashioned Google searching is good.
- Cross reference with Claude, Gemini, or ChatGPT.
- When in doubt, slow down and do your homework. It will save you time.

> The **week-2-connecting-to-github.md** file contains further instructions
