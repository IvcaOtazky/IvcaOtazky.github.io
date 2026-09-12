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

Questions are numbered in file order. Nothing shared depends on that number —
a shared link carries the question itself — but the numbering is what the
address bar shows while browsing, so keep adding questions at the end.

## Building locally

```bash
python3 build.py          # regenerates index.html (no dependencies)
python3 -m http.server    # then open http://localhost:8000
```

## Proposing a question

The `+` beside the share icon opens a form: category (one of the existing ones, or a new one),
the question, an optional note, a name, and an optional email. `Send` posts it to a relay that
mails it on from its own address, so nothing opens on the sender's device.

This needs an access key from <https://web3forms.com> (free, no account — they mail you a key)
pasted into `PROPOSAL_RELAY_ACCESS_KEY` in `template.html`. Until then, and whenever the relay
cannot be reached, the form offers a pre-formatted mail draft instead.

## Deployment

Push to `main`. The workflow runs `build.py` and publishes the result.
One-time setup in the repository: **Settings → Pages → Source → GitHub Actions**.

## Sharing a question

While browsing, the address bar carries the current question and the chosen
categories, e.g. `#q=12&c=vztahy,hlouposti`.

The share button builds a different link: `#s=<base64>`, holding the question's
own text, its notes and its category name. Such a link opens that one question
and nothing else — the bar below it shows a single dot — and it keeps working
however `questions.md` is later reordered. The button uses the native share
sheet on phones and falls back to copying the link to the clipboard on desktop.
