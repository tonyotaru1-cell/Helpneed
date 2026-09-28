"""Build the Puppy Panic lead-magnet ebook as HTML (and optionally PDF).

Usage:
    python build_ebook.py                 # writes output/Puppy_Panic_Survival_Guide.html
    python build_ebook.py --open          # ...and opens it in your browser
    python build_ebook.py --pdf           # ...and also writes a PDF (needs Playwright)

To change the ebook, edit the SETTINGS and PAGES sections below. You never
need to touch the HTML/CSS further down unless you want to restyle it.
"""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# SETTINGS - the things you will change most often
# ---------------------------------------------------------------------------

SETTINGS = {
    "brand": "PUPPY PANIC",
    "title": "The New Puppy Owner Survival Guide",
    "affiliate_url": "https://5065ekt-g52o1p0965oj1yv3wg.hop.clickbank.net/",
    "output_name": "Puppy_Panic_Survival_Guide",
    "images_dir": "images",  # drop cover.jpg, training.jpg etc. in here
    # Colours
    "accent": "#d97706",
    "accent_soft": "#fff7e6",
    "ink": "#1c2b39",
}

# ---------------------------------------------------------------------------
# PAGES - the ebook content, one dict per page, in order
#
# Block types you can use inside "blocks":
#   ("p", "text")                         paragraph
#   ("h3", "text")                        sub-heading
#   ("list", ["a", "b"])                  bullet list
#   ("checklist", ["a", "b"])             tick-box list (printable)
#   ("card", "text")                      highlighted tip box
#   ("image", "file.jpg", "prompt/alt")   photo; shows a placeholder with the
#                                         prompt text until the file exists
#   ("table", ["head", ...], [[row], ...])   fill-in worksheet table
#   ("cta", "heading", "text", "button")  affiliate call-to-action box
#   ("note", "text")                      small print
# ---------------------------------------------------------------------------

PAGES = [
    {
        "kind": "cover",
        "title": "The New Puppy Owner<br>Survival Guide",
        "subtitle": "A complete beginner handbook for raising a happier, "
                    "calmer and better-trained dog.",
        "image": ("cover.jpg", "Happy owner cuddling a golden retriever puppy "
                               "on a sofa, warm natural light"),
        "tagline": "15+ essential lessons every new puppy owner should know",
    },
    {"kind": "toc"},
    {
        "title": "Welcome To Puppy Parenthood 🐾",
        "blocks": [
            ("p", "Congratulations on welcoming a new puppy into your life. The first "
                  "weeks are important because your puppy is learning about your home, "
                  "your routine and your expectations."),
            ("p", "Many puppy behaviours that frustrate owners are normal parts of "
                  "development. With patience, consistency and the right guidance, you "
                  "can build a strong relationship with your dog."),
            ("card", "<b>The Puppy Panic Promise:</b><br>Help owners understand their "
                     "dogs, create better habits and enjoy the journey."),
        ],
    },
    {
        "title": "Preparing Your Home",
        "blocks": [
            ("checklist", ["Safe sleeping area", "Food and water bowls", "Chew toys",
                           "Training treats", "Leash and collar",
                           "Remove dangerous objects (cables, shoes, cleaning products)"]),
            ("h3", "Remember"),
            ("p", "Your puppy learns from the environment you create."),
        ],
    },
    {
        "title": "Understanding Puppy Behaviour",
        "blocks": [
            ("h3", "Why Puppies Bite"),
            ("p", "Puppies bite because they explore, play and experience teething. The "
                  "goal is not punishment. The goal is teaching better choices."),
            ("h3", "Why Puppies Chew"),
            ("p", "Chewing is natural. Provide safe alternatives and reward good decisions."),
            ("image", "behaviour.jpg", "Puppy chewing a rope toy on a wooden floor"),
        ],
    },
    {
        "title": "Puppy Training Foundations",
        "blocks": [
            ("h3", "First Commands"),
            ("list", ["Sit", "Stay", "Come", "Leave It", "Name Recognition"]),
            ("card", "Short daily training sessions are more effective than long "
                     "frustrating sessions."),
            ("image", "training.jpg", "Owner teaching a puppy to sit with a treat, "
                                      "garden background"),
        ],
    },
    {
        "title": "Your Puppy's First 30 Days",
        "blocks": [
            ("h3", "Week 1"),
            ("p", "Build trust, introduce routines and teach your puppy their name."),
            ("h3", "Week 2"),
            ("p", "Begin basic commands and create consistent habits."),
            ("h3", "Week 3-4"),
            ("p", "Increase training, confidence and independence."),
        ],
    },
    {
        "title": "Solving Common Problems",
        "blocks": [
            ("h3", "Puppy Crying At Night"),
            ("list", ["Create a bedtime routine", "Provide comfort",
                      "Allow toilet breaks"]),
            ("h3", "Puppy Jumping"),
            ("p", "Reward calm greetings instead of excited behaviour."),
        ],
    },
    {
        "title": "Brain Training For Dogs 🧠",
        "blocks": [
            ("p", "Dogs need mental exercise as well as physical exercise. Brain games "
                  "can encourage focus, confidence and problem solving."),
            ("list", ["Puzzle activities", "Scent games", "Learning challenges",
                      "Training games"]),
            ("image", "brain-games.jpg", "Puppy sniffing out treats in a snuffle mat"),
        ],
    },
    {
        "title": "Bonus: 7-Day Puppy Training Challenge",
        "blocks": [
            ("p", "Five to ten minutes a day. Tick each day off as you go."),
            ("table", ["Day", "Focus", "Done"], [
                ["1", "Name game: say their name, reward eye contact", ""],
                ["2", "Sit: lure with a treat, reward the moment they sit", ""],
                ["3", "Handling: gently touch paws and ears, reward calm", ""],
                ["4", "Come: short recalls indoors, big rewards", ""],
                ["5", "Leave it: reward looking away from a treat in your hand", ""],
                ["6", "Settle: reward lying calmly on their bed", ""],
                ["7", "Review: practise every skill in a new room", ""],
            ]),
        ],
    },
    {
        "title": "Bonus: Daily Puppy Schedule",
        "blocks": [
            ("p", "Fill in your own times. Consistency is what matters most."),
            ("table", ["Time", "Activity", "Notes"], [
                ["", "Wake up + toilet break", ""],
                ["", "Breakfast", ""],
                ["", "Short training session", ""],
                ["", "Nap", ""],
                ["", "Play + toilet break", ""],
                ["", "Dinner", ""],
                ["", "Calm evening wind-down", ""],
                ["", "Last toilet break + bed", ""],
            ]),
        ],
    },
    {
        "title": "My Puppy Profile",
        "blocks": [
            ("table", [], [["Name", ""], ["Breed", ""], ["Age", ""],
                           ["Favourite Treat", ""], ["Vet Phone Number", ""],
                           ["Training Goal", ""]]),
        ],
    },
    {
        "title": "My Puppy Progress Tracker",
        "blocks": [
            ("table", ["Skill", "Week 1", "Week 2", "Week 3", "Week 4"], [
                [skill, "", "", "", ""]
                for skill in ["Sit", "Come", "Stay", "Leave It", "Name", "Loose Lead"]
            ]),
        ],
    },
    {
        "title": "Continue Your Training Journey",
        "blocks": [
            ("p", "For owners who want a structured approach with progressive "
                  "exercises, explore Brain Training For Dogs."),
            ("cta", "🧠 Explore Brain Training For Dogs",
                    "A guided training system for developing focus, engagement and "
                    "learning.",
                    "Start Training Your Dog"),
            ("note", "Disclosure: Puppy Panic may earn a commission if you purchase "
                     "through this link at no extra cost to you."),
        ],
    },
    {
        "kind": "cover",
        "title": "Your Puppy Journey Starts Today 🐾",
        "subtitle": "Every great dog begins with patience, consistency and love.",
    },
]

# ---------------------------------------------------------------------------
# Rendering - no need to edit below here for content changes
# ---------------------------------------------------------------------------

CSS = """
@page { size: A4; margin: 0; }
:root { --accent: %(accent)s; --accent-soft: %(accent_soft)s; --ink: %(ink)s; }
* { box-sizing: border-box; }
body {
  margin: 0; background: #e9ecef; color: #333;
  font-family: "Segoe UI", Arial, Helvetica, sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.book { max-width: 210mm; margin: auto; }
.page {
  background: #fff; width: 100%%; min-height: 297mm; margin: 25px auto;
  padding: 22mm 20mm 26mm; position: relative; overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,.08);
}
.page::before {  /* gold accent bar */
  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 8px;
  background: var(--accent);
}
.cover {
  background: linear-gradient(135deg, var(--accent-soft), #fff);
  text-align: center; display: flex; flex-direction: column; justify-content: center;
}
.brand { color: var(--accent); font-size: 20px; letter-spacing: 3px; font-weight: bold; }
h1 { font-size: 46px; line-height: 1.15; color: var(--ink); margin: 20px 0; }
h2 {
  color: var(--ink); font-size: 30px; margin-top: 0;
  border-bottom: 3px solid var(--accent); padding-bottom: 10px;
}
h3 { color: var(--accent); margin-bottom: 4px; }
p, li { font-size: 17px; line-height: 1.7; }
.subtitle { font-size: 22px; }
.figure {
  margin: 25px 0; border-radius: 20px; overflow: hidden; height: 260px;
  background: #f1f5f9; display: flex; align-items: center; justify-content: center;
}
.figure img { width: 100%%; height: 100%%; object-fit: cover; }
.placeholder {
  border: 2px dashed #cbd5e1; color: #64748b; padding: 20px; text-align: center;
  font-size: 14px;
}
.placeholder b { display: block; color: #475569; margin-bottom: 6px; }
.card {
  background: var(--accent-soft); border-left: 6px solid var(--accent);
  padding: 20px; margin: 20px 0; border-radius: 12px; font-size: 17px; line-height: 1.7;
}
.checklist { list-style: none; padding: 20px; background: #f8fafc; border-radius: 15px; }
.checklist li::before {
  content: ""; display: inline-block; width: 16px; height: 16px; margin-right: 12px;
  border: 2px solid var(--accent); border-radius: 4px; vertical-align: -2px;
}
.toc ol { padding-left: 0; list-style: none; counter-reset: toc; }
.toc li {
  counter-increment: toc; display: flex; gap: 12px; padding: 10px 0;
  border-bottom: 1px dotted #cbd5e1;
}
.toc li::before { content: counter(toc, decimal-leading-zero); color: var(--accent); font-weight: bold; }
.toc a { color: inherit; text-decoration: none; }
.cta {
  background: var(--ink); color: #fff; padding: 35px; border-radius: 20px;
  text-align: center; margin: 25px 0;
}
.cta h3 { color: #fff; }
.cta a {
  display: inline-block; background: var(--accent); color: #fff; padding: 15px 30px;
  border-radius: 30px; text-decoration: none; margin-top: 10px; font-weight: bold;
}
.note { font-size: 13px; color: #666; }
table { width: 100%%; border-collapse: collapse; margin: 15px 0; }
td, th { border: 1px solid #ddd; padding: 14px 12px; font-size: 16px; text-align: left; }
th { background: var(--accent-soft); color: var(--ink); }
.form td:first-child { width: 35%%; font-weight: bold; background: #f8fafc; }
td:empty::after { content: "\\00a0"; }
.footer {
  position: absolute; bottom: 12mm; left: 20mm; right: 20mm;
  display: flex; justify-content: space-between; color: #999; font-size: 12px;
}
@media print {
  body { background: #fff; }
  .page { margin: 0; box-shadow: none; height: 297mm; page-break-after: always; break-after: page; }
}
@media (max-width: 600px) {
  .page { padding: 30px 18px 60px; min-height: auto; margin: 10px auto; }
  .footer { left: 18px; right: 18px; bottom: 15px; }
  h1 { font-size: 34px; } h2 { font-size: 24px; } p, li { font-size: 16px; }
}
"""

esc = html.escape  # used for text that should never contain HTML


def slug(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")


def image_html(filename: str, prompt: str, images_dir: Path) -> str:
    """Embed the image if it exists, otherwise show a labelled placeholder."""
    path = images_dir / filename
    if path.is_file():
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode()
        return (f'<div class="figure"><img src="data:{mime};base64,{data}" '
                f'alt="{esc(prompt)}"></div>')
    return (f'<div class="figure placeholder"><div><b>📷 Add {esc(images_dir.name)}/'
            f'{esc(filename)}</b>Prompt: {esc(prompt)}</div></div>')


def block_html(block: tuple, cfg: dict, images_dir: Path) -> str:
    kind, *args = block
    if kind == "p":
        return f"<p>{args[0]}</p>"
    if kind == "h3":
        return f"<h3>{args[0]}</h3>"
    if kind in ("list", "checklist"):
        cls = ' class="checklist"' if kind == "checklist" else ""
        items = "".join(f"<li>{item}</li>" for item in args[0])
        return f"<ul{cls}>{items}</ul>"
    if kind == "card":
        return f'<div class="card">{args[0]}</div>'
    if kind == "note":
        return f'<p class="note">{args[0]}</p>'
    if kind == "image":
        return image_html(args[0], args[1], images_dir)
    if kind == "table":
        head, rows = args
        thead = "<tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>" if head else ""
        body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
        cls = "" if head else ' class="form"'  # no header = label/answer form
        return f"<table{cls}>{thead}{body}</table>"
    if kind == "cta":
        heading, text, button = args
        return (f'<div class="cta"><h3>{heading}</h3><p>{text}</p>'
                f'<a href="{esc(cfg["affiliate_url"])}" target="_blank" '
                f'rel="sponsored noopener">{button}</a></div>')
    raise ValueError(f"Unknown block type: {kind!r}")


def build_html(cfg: dict, pages: list[dict], images_dir: Path) -> str:
    chapters = [p for p in pages if p.get("kind", "chapter") == "chapter"]
    sections = []
    for number, page in enumerate(pages, start=1):
        kind = page.get("kind", "chapter")
        footer = (f'<div class="footer"><span>{esc(cfg["brand"])}</span>'
                  f"<span>{number}</span></div>")
        if kind == "cover":
            image = image_html(*page["image"], images_dir) if page.get("image") else ""
            tagline = f'<p>{page["tagline"]}</p>' if page.get("tagline") else ""
            sections.append(
                f'<section class="page cover"><div class="brand">{esc(cfg["brand"])}</div>'
                f'<h1>{page["title"]}</h1><p class="subtitle">{page["subtitle"]}</p>'
                f"{image}{tagline}</section>")
        elif kind == "toc":
            items = "".join(f'<li><a href="#{slug(c["title"])}">{c["title"]}</a></li>'
                            for c in chapters)
            sections.append(f'<section class="page toc"><h2>Inside This Guide</h2>'
                            f"<ol>{items}</ol>{footer}</section>")
        else:
            body = "\n".join(block_html(b, cfg, images_dir) for b in page["blocks"])
            sections.append(f'<section class="page" id="{slug(page["title"])}">'
                            f'<h2>{page["title"]}</h2>{body}{footer}</section>')

    title = f'{cfg["brand"].title()} - {cfg["title"]}'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{CSS % cfg}</style>
</head>
<body>
<div class="book">
{chr(10).join(sections)}
</div>
</body>
</html>
"""


def write_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit(
            "PDF export needs Playwright:\n"
            "    pip install playwright && playwright install chromium\n"
            "Or open the HTML in Chrome and use Print > Save as PDF "
            "(tick 'Background graphics').")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.pdf(path=str(pdf_path), format="A4", print_background=True,
                 prefer_css_page_size=True)
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=HERE / "output",
                        help="output folder (default: ./output)")
    parser.add_argument("--open", action="store_true", help="open the HTML in your browser")
    parser.add_argument("--pdf", action="store_true", help="also export a PDF")
    parser.add_argument("--affiliate-url", help="override the affiliate link")
    args = parser.parse_args()

    cfg = dict(SETTINGS)
    if args.affiliate_url:
        cfg["affiliate_url"] = args.affiliate_url
    images_dir = HERE / cfg["images_dir"]

    args.out.mkdir(parents=True, exist_ok=True)
    html_path = args.out / f'{cfg["output_name"]}.html'
    html_path.write_text(build_html(cfg, PAGES, images_dir), encoding="utf-8")
    print(f"HTML: {html_path}")

    missing = [b[1] for p in PAGES for b in p.get("blocks", []) if b[0] == "image"]
    missing += [p["image"][0] for p in PAGES if p.get("image")]
    missing = [m for m in missing if not (images_dir / m).is_file()]
    if missing:
        print(f"Placeholders shown for missing images in {images_dir.name}/: "
              + ", ".join(missing))

    if args.pdf:
        pdf_path = html_path.with_suffix(".pdf")
        write_pdf(html_path, pdf_path)
        print(f"PDF:  {pdf_path}")
    if args.open:
        webbrowser.open(html_path.as_uri())


if __name__ == "__main__":
    main()
