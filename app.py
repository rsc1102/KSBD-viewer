import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List
from flask import Flask, abort, render_template

app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)

IMAGE_LINKS_FILE = Path(__file__).parent / "image_links.json"


def _slug_to_display_name(slug: str) -> str:
    return slug.replace("_", " ")


@lru_cache(maxsize=1024)
def _image_links_map() -> Dict[str, List[str]]:
    with IMAGE_LINKS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    cleaned: Dict[str, List[str]] = {}
    for slug, links in data.items():
        cleaned_links: List[str] = []
        for link in links:
            text = str(link).strip()
            if text:
                cleaned_links.append(text)
        cleaned[str(slug)] = cleaned_links
    return cleaned


def _chapter_slugs() -> List[str]:
    """Return all chapter slugs based on available JSON entries."""
    return sorted(_image_links_map().keys())


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
    image_links_map = _image_links_map()
    if chapter_id not in chapter_slugs:
        abort(404)

    current_index = chapter_slugs.index(chapter_id)
    prev_chapter = chapter_slugs[current_index - 1] if current_index > 0 else None
    next_chapter = (
        chapter_slugs[current_index + 1]
        if current_index < len(chapter_slugs) - 1
        else None
    )

    image_links = image_links_map.get(chapter_id, [])

    return render_template(
        "chapter.html",
        chapter_name=_slug_to_display_name(chapter_id),
        prev_chapter=prev_chapter,
        next_chapter=next_chapter,
        image_links=image_links,
    )


if __name__ == "__main__":
    app.run(debug=True)
