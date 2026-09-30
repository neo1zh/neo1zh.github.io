# Zihao Zhao — editorial research site

The new homepage is a static site with no runtime or package dependencies. `.nojekyll` makes GitHub Pages serve it directly. The inherited AcademicPages source and older assets are preserved; they are no longer used to render the homepage. `/about/`, `/publications/`, `/cv/`, and `/resume/` redirect to their current destinations.

## Edit and build

- `templates/editorial.html`: homepage biography, background, and layout.
- `_data/research.json`: publication data shared by the homepage and LaTeX CV.
- `assets/editorial/style.css`: responsive light/dark design.
- `templates/cv.tex`: CV sections and formatting.
- `assets/Zihao-Zhao-CV.tex`: generated, standalone source that can be uploaded to Overleaf and compiled with pdfLaTeX.
- `assets/Zihao-Zhao-CV.pdf`: downloadable CV, compiled from that exact source.

Run from the repository root:

```sh
python3 scripts/build.py
mkdir -p tmp/latex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=tmp/latex assets/Zihao-Zhao-CV.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=tmp/latex assets/Zihao-Zhao-CV.tex
cp tmp/latex/Zihao-Zhao-CV.pdf assets/Zihao-Zhao-CV.pdf
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000`. All content is readable without JavaScript. JavaScript enhances publication filtering and remembers a light/dark preference locally.

## Add the new portrait

Save the approved photo to `images/portrait.jpg`, set `portrait` to `/images/portrait.jpg` in `_data/research.json`, and rebuild. A 4:5 head-and-shoulders crop at roughly 880 × 1100 pixels works well. The current monogram is explicitly a placeholder.

## Content provenance and remaining editorial choices

Publication statuses, dates, affiliations, awards, and experience come from the supplied CV. The three research questions are editorial framing based on paper titles, not claims about measured results. Author truncation matches the supplied CV; expand lists when complete citation data is available. The Rutgers entry says “doctoral studies”; no degree completion or transfer reason is inferred.

The previous homepage's research internships are not carried forward as current positions because the supplied CV does not provide updated dates or descriptions. Add specific research contributions and code links when available. No fabricated metrics, skills, internship availability, or paper abstracts have been added.

## Publish

This local branch does not change the live website. After review, merge the generated files, PDF, and `.nojekyll` into the branch configured in GitHub Pages (the existing repository uses `master`). If the Pages source is “Deploy from a branch,” keep its root directory. If an external workflow overrides the Pages source, point it to these static files. No secrets or environment variables are needed.
