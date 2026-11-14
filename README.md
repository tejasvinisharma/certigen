# CertiGen: bulk certificate generator

**Status: in progress.** A self-initiated learning project.

Coaching institutes, schools and college clubs often make participation certificates one by one in Canva or Word. It's slow, and names get misspelt. CertiGen reads a spreadsheet of names, writes each name on a certificate design, and saves one ready-to-print PDF per person, bundled into a single ZIP.

## Features

Tick each box only when it actually works.

- [ ] Read names from a CSV or Excel file
- [ ] Clean up extra spaces and skip blank rows
- [ ] Give every person a safe, unique file name (`Riya_Verma.pdf`, `Riya_Verma_2.pdf`)
- [ ] Shrink long names so they fit the design
- [ ] Write each name on the certificate template, centred
- [ ] Save one A4 PDF per person and bundle them into a ZIP
- [ ] Planned: split very long names onto two lines
- [ ] Planned: add the event date
- [ ] Planned: a simple web page with Streamlit

## Demo

<!-- Add a screenshot of 2 finished certificates and a link to a 60-second demo video here. -->
Coming soon.

## How to run it

You need Python 3.10 or newer.

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# Mac / Linux:  source .venv/bin/activate
pip install -r requirements.txt

python certigen.py sample_data/names.csv
```

The PDFs go to `output/certificates/` and the ZIP to `output/certificates.zip`.

Options:

| Option | What it does | Default |
|---|---|---|
| `--template` | Certificate design (PNG or JPG) | `templates/certificate_template.png` |
| `--font` | TTF font for the names | `fonts/Poppins-Medium.ttf` |
| `--out` | Output folder | `output` |

To use your own design, change the numbers in `CONFIG` at the top of `certigen.py` to match it.

## Tests

```bash
python -m pytest
```

## Project structure

```
certigen.py                     the tool
tests/test_certigen.py          checks for each part
sample_data/names.csv           made-up names for testing
templates/certificate_template.png   sample A4 design (3508 x 2480 px)
fonts/Poppins-Medium.ttf        font for the names (SIL Open Font License)
```

## Tech

Python, pandas, Pillow, pytest

## What I learned

<!-- Fill this in as you go: 3-5 honest bullet points, including something that broke. -->

## Credits

- The project structure, tests, sample data and sample template came from a starter kit I was given. The code in `certigen.py` is my own.
- Poppins font: Copyright 2020 The Poppins Project Authors, licensed under the SIL Open Font License 1.1 (see `fonts/OFL.txt`).
- All names in `sample_data/` are made up.
