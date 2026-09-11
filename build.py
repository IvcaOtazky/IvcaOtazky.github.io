#!/usr/bin/env python3
"""Turn questions.md + template.html into the deployable index.html.

The markdown file is written like this:

    # Category name
    The question itself
    A note that belongs to the question
    Another note

    The next question in the same category
    Its only note

    # Another category
    ...

In other words: a heading opens a category, and every blank-line-separated
block below it is one question whose first line is the question and whose
remaining lines are the paragraphs shown underneath it.
"""

from dataclasses import dataclass, field
from html import escape
from pathlib import Path
import json
import re
import sys
import unicodedata

PROJECT_DIRECTORY = Path(__file__).parent
QUESTIONS_MARKDOWN_FILE = PROJECT_DIRECTORY / "questions.md"
TEMPLATE_FILE = PROJECT_DIRECTORY / "template.html"
GENERATED_PAGE_FILE = PROJECT_DIRECTORY / "index.html"


@dataclass
class Question:
    identifier: str
    text: str
    notes: list[str]
    category_name: str
    category_slug: str


@dataclass
class Category:
    name: str
    slug: str
    questions: list[Question] = field(default_factory=list)


def slugify(name: str) -> str:
    """Make a URL-friendly slug: 'Dětství a kořeny' -> 'detstvi-a-koreny'."""
    without_diacritics = unicodedata.normalize("NFKD", name)
    ascii_only = without_diacritics.encode("ascii", "ignore").decode("ascii")
    hyphenated = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    return hyphenated or "category"


def parse_questions_markdown(markdown_text: str) -> list[Category]:
    categories: list[Category] = []
    current_category: Category | None = None
    current_block: list[str] = []

    def finish_current_block() -> None:
        """A finished block becomes one question of the current category."""
        nonlocal current_block
        if not current_block:
            return
        if current_category is None:
            raise ValueError(f"Question {current_block[0]!r} appears before any '# Category' heading.")

        question_text, *note_paragraphs = current_block
        current_category.questions.append(
            Question(
                identifier="",  # filled in by number_the_questions once every question is known
                text=question_text,
                notes=note_paragraphs,
                category_name=current_category.name,
                category_slug=current_category.slug,
            )
        )
        current_block = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()

        line_opens_a_category = line.startswith("#")
        line_ends_a_block = line == ""

        if line_opens_a_category:
            finish_current_block()
            category_name = line.lstrip("#").strip()
            current_category = Category(name=category_name, slug=slugify(category_name))
            categories.append(current_category)
        elif line_ends_a_block:
            finish_current_block()
        else:
            current_block.append(line)

    finish_current_block()

    number_the_questions(categories)
    return [category for category in categories if category.questions]


def number_the_questions(categories: list[Category]) -> None:
    """Give every question a stable id, so shared links keep working."""
    running_number = 1
    for category in categories:
        for question in category.questions:
            question.identifier = str(running_number)
            running_number += 1


def render_category_checkboxes(categories: list[Category]) -> str:
    checkbox_rows = []
    for category in categories:
        question_count = len(category.questions)
        checkbox_rows.append(
            f'    <button class="category" role="checkbox" aria-checked="true" data-slug="{escape(category.slug)}">'
            f'<span class="category-box">[×]</span>'
            f'<span class="category-name">{escape(category.name)}</span>'
            f'<span class="category-count">{question_count}</span>'
            f"</button>"
        )
    return "\n".join(checkbox_rows)


def render_question_data(categories: list[Category]) -> str:
    questions_for_the_browser = [
        {
            "id": question.identifier,
            "text": question.text,
            "notes": question.notes,
            "category": question.category_slug,
            "categoryName": question.category_name,
        }
        for category in categories
        for question in category.questions
    ]
    return json.dumps(questions_for_the_browser, ensure_ascii=False, indent=0)


def build_site() -> None:
    if not QUESTIONS_MARKDOWN_FILE.exists():
        sys.exit(f"Missing {QUESTIONS_MARKDOWN_FILE.name} — there is nothing to build.")

    categories = parse_questions_markdown(QUESTIONS_MARKDOWN_FILE.read_text(encoding="utf-8"))
    if not categories:
        sys.exit(f"{QUESTIONS_MARKDOWN_FILE.name} contains no questions.")

    total_question_count = sum(len(category.questions) for category in categories)

    page = TEMPLATE_FILE.read_text(encoding="utf-8")
    page = page.replace("{{CATEGORY_CHECKBOXES}}", render_category_checkboxes(categories))
    page = page.replace("{{QUESTION_DATA_JSON}}", render_question_data(categories))
    page = page.replace("{{TOTAL_QUESTION_COUNT}}", str(total_question_count))

    GENERATED_PAGE_FILE.write_text(page, encoding="utf-8")

    print(f"Built {GENERATED_PAGE_FILE.name}: {total_question_count} questions in {len(categories)} categories.")
    for category in categories:
        print(f"  {category.name} ({category.slug}): {len(category.questions)}")


if __name__ == "__main__":
    build_site()
