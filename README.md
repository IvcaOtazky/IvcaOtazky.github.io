# N shades of Ivča

A single-page site with two modes: an intro that lets you pick question
categories, and a reader that shows one question at a time.

## How it fits together

| File | Role |
| --- | --- |
| `questions.md` | All the content. **This is the only file you normally edit.** |
| `template.html` | The whole site — markup, styling, behaviour — with three placeholders. |
| `build.py` | Reads `questions.md`, fills the placeholders, writes `index.html`. |
| `index.html` | Generated. Committed so the site also works when opened directly. |
| `.github/workflows/deploy.yml` | Rebuilds and deploys to GitHub Pages on every push to `main`. |

## Writing questions

A heading opens a category. Every blank-line-separated block below it is one
question: the first line is the question, the remaining lines are the
paragraphs shown underneath it.

```markdown
# Dětství a kořeny
Jaká je tvoje nejstarší vzpomínka?
Nemusí to být nic velkého — stačí vůně, místo, jeden obrázek.
Kolik ti v ní asi bylo a kdo v ní ještě je?

Po kom jsi zdědila nejvíc?
Může to být povaha, ruce, smích i něco, co bys radši vrátila.

# Vztahy
Kdy jsi naposledy někomu odpustila?
```

Questions are numbered in file order, and a shared link points at that number —
so adding questions at the end never breaks links that are already out there.

## Building locally

```bash
python3 build.py          # regenerates index.html (no dependencies)
python3 -m http.server    # then open http://localhost:8000
```

## Deployment

Push to `main`. The workflow runs `build.py` and publishes the result.
One-time setup in the repository: **Settings → Pages → Source → GitHub Actions**.

## Sharing a question

The address bar carries the current question and the chosen categories, e.g.
`#q=12&c=vztahy,hlouposti`. The share button uses the native share sheet on
phones and falls back to copying the link to the clipboard on desktop.
