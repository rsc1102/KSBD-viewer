from pathlib import Path
from typing import List
from flask import Flask, abort, render_template

app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)

CHAPTER_DIR = Path(__file__).parent / "image_links"


def _slug_to_display_name(slug: str) -> str:
    return slug.replace("_", " ")


def _chapter_slugs() -> List[str]:
    """Return all chapter slugs based on available text files."""
    return sorted(path.stem for path in CHAPTER_DIR.glob("*.txt"))


@app.get("/")
def home() -> str:
    chapters = [
        (_slug_to_display_name(slug), slug)
        for slug in _chapter_slugs()
    ]
    return render_template("home.html", chapters=chapters)


@app.get("/<chapter_id>")
def chapter(chapter_id) -> str:
    chapter_slugs = _chapter_slugs()
    if chapter_id not in chapter_slugs:
        abort(404)

    current_index = chapter_slugs.index(chapter_id)
    prev_chapter = chapter_slugs[current_index - 1] if current_index > 0 else None
    next_chapter = (
        chapter_slugs[current_index + 1]
        if current_index < len(chapter_slugs) - 1
        else None
    )

    chapter_path = CHAPTER_DIR / f"{chapter_id}.txt"
    image_links = [
        line.strip()
        for line in chapter_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    return render_template(
        "chapter.html",
        chapter_name=_slug_to_display_name(chapter_id),
        prev_chapter=prev_chapter,
        next_chapter=next_chapter,
        image_links=image_links,
    )


if __name__ == "__main__":
    app.run(debug=True)
