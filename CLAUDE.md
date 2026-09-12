# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python3 build.py          # regenerate index.html from questions.md + template.html (no dependencies)
python3 -m http.server    # serve the repo, then open http://localhost:8000
```

There is no test suite, linter, or package manifest — the only build step is `build.py`, and
the only runtime dependency is a browser. Verify changes by loading the page and using it.

## The one thing to get right

`index.html` is **generated output that is also committed**. Never edit it by hand — any
change there is silently destroyed by the next `python3 build.py` (and by CI on every push).

- Markup, CSS, and behaviour live in `template.html`.
- Question content lives in `questions.md`.
- Run `python3 build.py` before committing, so the committed `index.html` matches its sources.
  It is committed deliberately, so the site also works when the file is opened directly.

## Architecture

### The build is a three-placeholder string substitution

`build.py` parses `questions.md` into categories, then replaces exactly three placeholders in
`template.html`:

| Placeholder | Becomes |
| --- | --- |
| `{{TOTAL_QUESTION_COUNT}}` | the number in the title and the `<title>`/meta tags |
| `{{CATEGORY_CHECKBOXES}}` | the `<button class="category" data-slug=…>` rows |
| `{{QUESTION_DATA_JSON}}` | the `ALL_QUESTIONS` array the page's JS reads |

Adding a placeholder means touching both files. `data-slug` is the join key between the
checkbox markup and the `category` field of each question — `slugify()` produces it from the
category heading (diacritics stripped: `Dětství a kořeny` → `detstvi-a-koreny`).

### `questions.md` format

A `#` heading opens a category. Every blank-line-separated block below it is one question: the
first line is the question, the remaining lines are the paragraphs shown underneath it.
Categories with no questions are dropped from the build entirely, so an empty heading is a
harmless placeholder.

### Question ids are positional, and links depend on them

`number_the_questions()` numbers questions `1..N` in file order across all categories, and the
browsing address is built from that number. Shared links no longer depend on it — they carry
the question itself — but a number still changes meaning when questions are inserted or
reordered, so append rather than insert and preserve the file-order numbering.

### The whole site is one file, and the router is the URL hash

`template.html` inlines all CSS and JS; the deploy workflow copies only `index.html` into the
published artifact. Introducing a separate `.css`, `.js`, or image file therefore requires
updating `.github/workflows/deploy.yml` too — otherwise it 404s in production while working
locally. The only external requests are Google Fonts.

There are two kinds of address. Browsing writes `#q=12&c=vztahy,hlouposti` — the question
number plus the chosen categories. The share button writes `#s=<base64>`, which holds the
question's text, notes and category name rather than a pointer into the list, so it survives
any reordering of `questions.md` and needs nothing from the page it opens on.

`renderCurrentLocation()` is the single entry point: it reads the hash, and shows the intro
(`#` empty, or an `#s=` payload that does not decode), a pool built from the category slugs,
or a decoded shared question. The screens are `<main>` elements toggled with the `hidden`
property.

The proposal form is the exception, and deliberately so: it is a third `<main>`, opened from
the reader bar's `+` and closed straight back to the question underneath, **without touching
the hash** — a half-written question is nothing to land on, share or reload into. So
`renderCurrentLocation()` hides it unconditionally, which keeps the router the only thing that
decides which screen is up, and the `keydown` handler gives the arrow keys to the form's
textareas while it is open.

A shared question becomes a one-item `currentPool`, which is what reduces the bottom bar to a
single dot and disables both arrows; it carries `isASharedQuestion` so that
`showQuestionAtPosition()` keeps rewriting the `#s=` address instead of a number, and the
category buttons are left alone because it belongs to no category on this page. A `#q=` link
pointing at a question outside its own `c=` selection widens the pool to every question rather
than failing.

The base64 is URL-safe and unpadded, and the payload goes through `TextEncoder` before `btoa`
because the questions are Czech.

### The proposal form sends through a relay

A static file cannot send mail, so `Send` POSTs the message to Web3Forms, which sends it on
from its own servers — nothing opens on the proposer's device and no address of theirs travels
unless they typed one. `PROPOSAL_RELAY_ACCESS_KEY` is empty until someone pastes in the key
mailed by <https://web3forms.com>; it is **not a secret** (it can only send to the one inbox it
was issued for, and this file is published), so it belongs in `template.html` like any other
constant.

When the relay cannot be reached — no key yet, offline, a bad day — the form stays put and
offers a `mailto:` draft as a **link**. It must be a link: the browser refuses to open mail on
the click that started the request, because awaiting the network outlives the user gesture.
Setting `location.href` there fails with *"Not allowed to launch … a user gesture is required"*.

A row is marked `is-open` by a click **and** by having any text in it, so a value arriving from
browser autofill is not left sitting at `opacity: 0`.

Every row is `Label ›` plus one slot holding both the parenthesised comment and the writing
line: the comment is absolutely positioned so it can fade out from under the words instead of
shoving them sideways, and the input is always present at `opacity: 0` so opening a row never
shuffles the rows below it. The question and the note are auto-growing `<textarea>`s (newlines
allowed); everything else is an `<input>`, which is what keeps it to one line. The form's own
copy is English, matching `Start ›` and the title — `aria-label`s stay Czech like the rest.

Because routing is hash-based there is no server-side routing and no 404 page to maintain.

### The title cross is measured in JavaScript

`N | shades / of | Ivča` is a 3×3 grid whose middle row and column are 1px tracks — the cross
is those two tracks, so its position is decided entirely by how wide the outer columns are.
`fitTitleColumnsToTheWords()` pins those columns to measured pixel widths so the cross *glides*
when the cycling word changes length instead of snapping. It must be re-run whenever the words
can change size: on the word cycle, on resize, and on `document.fonts.ready` (the title is set
in a webfont and sized in viewport units). Re-measuring passes `withoutAnimating` to suppress
the transition; only an actual word change should animate.

Editing `WORDS_FOR_QUESTIONS` is safe, but removing the `#of-word` / `#ivca-word` / `#shades-word`
ids breaks the measurement.

## Deployment

Push to `main`. `.github/workflows/deploy.yml` runs `build.py` and publishes via GitHub Actions
to <https://ivcaotazky.github.io/>. Pages source is already set to GitHub Actions — no manual
configuration is needed. `.nojekyll` is present but redundant on this path.

## Conventions

UI copy and `questions.md` are in Czech; code, comments, and commit messages are in English.

The intro/reader split, the directional entrance animations, and the borderless italic
`Start >` button all come from the original design brief, whose two standing rules are kept
verbatim at the end of this file. The existing code already follows them — match it, including
the comment density that explains *why* a piece of layout or timing works.


# Frontend workflow

When building or modifying UI:
- Prioritize distinctive, intentional visual design over generic templates.
- Run the application and inspect the actual rendered page.
- Use browser tools to screenshot and evaluate the result.
- Iterate on visual problems rather than stopping after the first implementation.
- Check both desktop and mobile layouts.
- Use current library documentation when unsure about an API.
- Pay particular attention to typography, spacing, alignment, hierarchy, and responsive behavior.

# Code Style

Write code as **executable prose**: every line should be immediately understandable as natural language. Use domain-specific nouns and verbs, descriptive names, and small intention-revealing functions. Prefer `send_order_confirmation(order)` over generic `handle()` or `process()`, and `customer_has_active_subscription` over cryptic conditions. Structure control flow so it reads naturally from top to bottom, using intermediate variables when they clarify reasoning. Avoid clever one-liners, unnecessary abstractions, abbreviations, dense expressions, and premature DRY when they make the code harder to understand. Abstract implementation details behind meaningful operations. Optimize for **semantic clarity rather than brevity**: extra lines are good if they make the program read like a clear explanation of what it does.
