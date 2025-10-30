from pathlib import Path
from flask import Flask
import os

app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)


@app.get("/")
def home() -> str:
    data = {}
    chapters = os.listdir(str(Path(__file__).parent / "image_links"))
    chapters.sort()
    data["chapters"] = [
        (x.replace(".txt", "").replace("_", " "), x.replace(".txt", ""))
        for x in chapters
    ]
    return app.jinja_env.get_template(
        "home.html",
    ).render(data)


@app.get("/<chapter_id>")
def chapter(chapter_id) -> str:
    data = {}

    chapter_name = chapter_id.replace("_", " ")
    data["chapter_name"] = chapter_name

    chapter_number = int(chapter_id.split("_")[-1])
    prev_chapter = (
        f"Chapter_{'0' if chapter_number - 1 < 10 else ''}{chapter_number - 1}"
        if chapter_number > 1
        else None
    )
    next_chapter = (
        f"Chapter_{'0' if chapter_number + 1 < 10 else ''}{chapter_number + 1}"
        if chapter_number < 45
        else None
    )
    data["prev_chapter"] = prev_chapter
    data["next_chapter"] = next_chapter

    with open(
        os.path.join(str(Path(__file__).parent / "image_links"), chapter_id + ".txt"),
        "r",
    ) as file:
        image_links = file.readlines()

    data["image_links"] = image_links

    return app.jinja_env.get_template(
        "chapter.html",
    ).render(data)


if __name__ == "__main__":
    app.run(debug=True)
