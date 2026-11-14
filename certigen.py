"""
CertiGen: bulk certificate generator.

Reads a spreadsheet of names, puts each name on a certificate template,
saves one PDF per person, and bundles all the PDFs into a ZIP file.

How to work on this file
------------------------
Follow BUILD_GUIDE.md one step at a time. Each function below says which
step it belongs to. Replace its `raise NotImplementedError(...)` line with
your own code, then check that step with:

    python -m pytest -k step1        (or step2, step3 ...)

When every step passes, run the whole tool:

    python certigen.py sample_data/names.csv
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

# You will need these imports as you go. They are here so you know which
# libraries the project uses.
import pandas as pd  # noqa: F401  (Step 1)
from PIL import Image, ImageDraw, ImageFont  # noqa: F401  (Steps 3-5)

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = PROJECT_DIR / "templates" / "certificate_template.png"
DEFAULT_FONT = PROJECT_DIR / "fonts" / "Poppins-Medium.ttf"

# Layout settings for templates/certificate_template.png (3508 x 2480 px,
# A4 landscape at 300 dpi). If you switch to your own template, measure your
# design and change these numbers to match it.
CONFIG = {
    "name_center_y": 1320,   # vertical centre of the name, in pixels from the top
    "name_max_width": 2400,  # the name must fit inside this width, in pixels
    "name_start_size": 190,  # font size to try first
    "name_min_size": 90,     # never go smaller than this
    "name_color": "#1F2A44", # navy
}


# ---------------------------------------------------------------------------
# Step 1
# ---------------------------------------------------------------------------
def load_names(path: str | Path) -> list[str]:
    """Read names from a .csv or .xlsx file and return them as a clean list.

    Rules:
    - The file must have a column called "name". Match it in any letter case
      and ignore spaces around the header, so "Name", " NAME " and "name"
      all work. If there is no such column, raise ValueError with a message
      that mentions the "name" column.
    - Files that end in anything other than .csv or .xlsx raise ValueError.
    - Clean every name: remove spaces at the start and end, and squeeze
      repeated spaces inside the name down to one ("  Riya   Verma " ->
      "Riya Verma").
    - Skip empty cells and cells that only contain spaces. Watch out: pandas
      reads an empty Excel cell as NaN, not as "".
    - Keep the original order. Keep repeated names: two different people can
      share a name.
    """
    raise NotImplementedError("Step 1: write load_names(). See BUILD_GUIDE.md")


# ---------------------------------------------------------------------------
# Step 2
# ---------------------------------------------------------------------------
def safe_filename(name: str, used: set[str]) -> str:
    """Turn a person's name into a safe, unique file name (without .pdf).

    Rules:
    - Replace every run of characters that are not A-Z, a-z or 0-9 with a
      single underscore, then remove underscores from the start and end.
      "Riya Verma" -> "Riya_Verma", " A/B: C? " -> "A_B_C".
    - If nothing is left (for example "***"), use "certificate".
    - `used` holds the file names already taken. If the result is already in
      `used`, add _2, _3 and so on until it is free:
      "Riya_Verma", then "Riya_Verma_2", then "Riya_Verma_3".
    - Add the name you return to `used` before returning it.
    """
    raise NotImplementedError("Step 2: write safe_filename(). See BUILD_GUIDE.md")


# ---------------------------------------------------------------------------
# Step 3
# ---------------------------------------------------------------------------
def fit_font_size(
    name: str,
    font_path: str | Path,
    max_width: int,
    start_size: int,
    min_size: int,
) -> int:
    """Return the biggest font size (an int) at which `name` fits in `max_width`.

    Rules:
    - Start at `start_size`. If the name is too wide, try smaller sizes,
      going down 2 points at a time.
    - Stop at the first size where the text width is <= max_width.
    - Never return less than `min_size`, even if the name still does not
      fit at that size.
    - Measure the text width with Pillow (ImageFont.truetype, then
      font.getlength(name)).
    """
    raise NotImplementedError("Step 3: write fit_font_size(). See BUILD_GUIDE.md")


# ---------------------------------------------------------------------------
# Step 4
# ---------------------------------------------------------------------------
def render_certificate(
    name: str,
    template_path: str | Path,
    font_path: str | Path,
    config: dict = CONFIG,
) -> Image.Image:
    """Open the template, write the name on it, and return the image.

    Rules:
    - Open the template and convert it to "RGB" mode (PDFs can't be saved
      with transparency).
    - Choose the font size with fit_font_size(), using the numbers in
      `config`.
    - Draw the name centred horizontally on the page, with its centre at
      config["name_center_y"], in config["name_color"].
      Hint: ImageDraw.text(..., anchor="mm") centres text on a point.
    - Return the image. Don't save it here.
    """
    raise NotImplementedError("Step 4: write render_certificate(). See BUILD_GUIDE.md")


# ---------------------------------------------------------------------------
# Step 5
# ---------------------------------------------------------------------------
def make_certificate(
    name: str,
    template_path: str | Path,
    font_path: str | Path,
    out_path: str | Path,
    config: dict = CONFIG,
) -> Path:
    """Render one certificate and save it as a PDF at `out_path`.

    Rules:
    - Use render_certificate() to get the image.
    - Create the folder for `out_path` if it doesn't exist yet.
    - Save as PDF with resolution=300, so it prints at A4 size.
    - Return `out_path` as a Path.
    """
    raise NotImplementedError("Step 5: write make_certificate(). See BUILD_GUIDE.md")


# ---------------------------------------------------------------------------
# Step 6
# ---------------------------------------------------------------------------
def generate_all(
    names_path: str | Path,
    template_path: str | Path,
    font_path: str | Path,
    out_dir: str | Path,
    config: dict = CONFIG,
) -> Path:
    """Make one PDF per name, then put all the PDFs in one ZIP file.

    Rules:
    - Read the names with load_names().
    - Save each PDF in out_dir/"certificates", named with safe_filename()
      plus ".pdf". Use one `used` set for the whole run, so repeated names
      get _2, _3 and so on.
    - Create out_dir/"certificates.zip" containing every PDF. Inside the ZIP,
      store just the file names ("Riya_Verma.pdf"), not the full folder path.
    - Return the path of the ZIP file.
    """
    raise NotImplementedError("Step 6: write generate_all(). See BUILD_GUIDE.md")


# ---------------------------------------------------------------------------
# Command line (already written for you)
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Make one PDF certificate per name in a spreadsheet."
    )
    parser.add_argument("names", help="CSV or Excel file with a 'name' column")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE, help="certificate template image")
    parser.add_argument("--font", default=DEFAULT_FONT, help="TTF font for the names")
    parser.add_argument("--out", default="output", help="folder for the PDFs and ZIP")
    args = parser.parse_args()

    started = time.perf_counter()
    zip_path = generate_all(args.names, args.template, args.font, args.out)
    seconds = time.perf_counter() - started

    import zipfile

    with zipfile.ZipFile(zip_path) as zf:
        count = len(zf.namelist())
    print(f"Made {count} certificates in {seconds:.1f} seconds -> {zip_path}")


if __name__ == "__main__":
    main()
