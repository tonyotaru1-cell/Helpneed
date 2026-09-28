# Puppy Panic ebook builder

Generates the *New Puppy Owner Survival Guide* lead magnet as a print-ready A4 HTML file (and optionally a PDF).

## Quick start

```bash
python build_ebook.py --open      # build and open in your browser
python build_ebook.py --pdf       # also export a PDF
```

Output goes to `output/Puppy_Panic_Survival_Guide.html` (and `.pdf`).

## Editing

Everything you normally change is at the top of `build_ebook.py`:

- **`SETTINGS`** – brand name, affiliate link, colours, output file name.
- **`PAGES`** – the ebook content, one entry per page. Add, remove or reorder pages freely;
  the table of contents and page numbers update automatically.

Swap the affiliate link for one build without editing the file:

```bash
python build_ebook.py --affiliate-url "https://your-link.example"
```

## Photos

Each image slot shows a dashed placeholder with the file name it wants and a suggested
prompt (handy for Google Flow or any image generator). Save the picture into `images/`
with that name, e.g. `images/cover.jpg`, rebuild, and it is embedded in the HTML.

## PDF export

`--pdf` uses Playwright:

```bash
pip install playwright
playwright install chromium
```

No Playwright? Open the HTML in Chrome → Print → Save as PDF, paper size A4, margins
*None*, and tick **Background graphics**.
