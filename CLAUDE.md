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

`number_the_questions()` numbers questions `1..N` in file order across all categories, and a
shared link points at that number. **Appending questions is always safe; inserting or
reordering silently repoints every link already out there.** This is the reason for the
file-order numbering — preserve it.

### The whole site is one file, and the router is the URL hash

`template.html` inlines all CSS and JS; the deploy workflow copies only `index.html` into the
published artifact. Introducing a separate `.css`, `.js`, or image file therefore requires
updating `.github/workflows/deploy.yml` too — otherwise it 404s in production while working
locally. The only external requests are Google Fonts.

Addresses look like `#q=12&c=vztahy,hlouposti` — the question plus the chosen categories.
`renderCurrentLocation()` is the single entry point: it reads the hash, and either shows the
intro (`#` empty) or builds the question pool from the category slugs. The two screens are two
`<main>` elements toggled with the `hidden` property. A shared link pointing at a question
outside its own `c=` selection widens the pool to every question rather than failing.

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
