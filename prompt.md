Write a website in CSS + HTML: A modern look, light pink background, black text. Should be a single index.html file, able to operate in one of two modes:
a) An intro page. This is the one loaded when one first loads the page. It should have a centered text:
N  | shades
----------
of | Ivča
The lines show the layout, each of the lines should fade in + move into view from different direction: N from left, shades from top, of from bottom, Ivca from right. Keep the animations with slightly different starting times to create a dynamic effect.

Below this, there should a list of several options, with toggle-able boxes. Each category adds certain questions to the list
[ ] Category 1
[ ] Category 2
... etc.

Below categories, add a button, without border, just italic text with a nice font. It should move and turn gray when hovered:
Start >

b) The questions page. The goal is to present a single question.

Above the question, show the < arrow, pressable, for returning to the menu. On the right show a share button.

The question should be present in the middle, in modern, italic font, gray on the pink background. On the top you should use a share icon, allowing sharing a link to this question. Below the question, you should show a simple navigation menu:

< ....5....10....15... etc. > where each dot is clickable and stands for a question. The arrows are clickable to move by one. 


Finally, create a github pages workflow that creates the contents of the above mentioned webpage:
We will have a .md file, containing all the questions and their categories, as

# Category
Question 1 aaaaa
First paragraph
Second

Q2 Some header
First paragraph is very nice too

# Category 2
Q3 aaa
etc.

You should write a script that parses the markdown file (questions.md) and generates the desired index.html. (Ideally using an index.html already written elsewhere + some placeholders that can be replaced). Wrap everything as a github pages repo, the website should be automatically deployed on each new push.

# Code Style

Write code as **executable prose**: every line should be immediately understandable as natural language. Use domain-specific nouns and verbs, descriptive names, and small intention-revealing functions. Prefer `send_order_confirmation(order)` over generic `handle()` or `process()`, and `customer_has_active_subscription` over cryptic conditions. Structure control flow so it reads naturally from top to bottom, using intermediate variables when they clarify reasoning. Avoid clever one-liners, unnecessary abstractions, abbreviations, dense expressions, and premature DRY when they make the code harder to understand. Abstract implementation details behind meaningful operations. Optimize for **semantic clarity rather than brevity**: extra lines are good if they make the program read like a clear explanation of what it does.



# Frontend workflow

When building or modifying UI:
- Prioritize distinctive, intentional visual design over generic templates.
- Run the application and inspect the actual rendered page.
- Use browser tools to screenshot and evaluate the result.
- Iterate on visual problems rather than stopping after the first implementation.
- Check both desktop and mobile layouts.
- Use current library documentation when unsure about an API.
- Pay particular attention to typography, spacing, alignment, hierarchy, and responsive behavior.