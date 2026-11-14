"""
Checks for each build step. Run one step at a time:

    python -m pytest -k step1

or everything:

    python -m pytest

A test that fails with NotImplementedError just means you haven't written
that step yet.
"""

import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import certigen  # noqa: E402

TEMPLATE = ROOT / "templates" / "certificate_template.png"
FONT = ROOT / "fonts" / "Poppins-Medium.ttf"


# ---------------------------------------------------------------- Step 1 --
def test_step1_reads_csv_and_cleans_names(tmp_path):
    f = tmp_path / "names.csv"
    f.write_text(" Name \n  Riya   Verma  \nAman Gill\n   \nKabir Singh\n", encoding="utf-8")
    assert certigen.load_names(f) == ["Riya Verma", "Aman Gill", "Kabir Singh"]


def test_step1_reads_excel_and_skips_empty_cells(tmp_path):
    f = tmp_path / "names.xlsx"
    pd.DataFrame({"NAME": ["Priya Sharma", None, "  Ishaan  Gupta ", "Priya Sharma"]}).to_excel(f, index=False)
    assert certigen.load_names(f) == ["Priya Sharma", "Ishaan Gupta", "Priya Sharma"]


def test_step1_finds_name_column_among_others(tmp_path):
    f = tmp_path / "names.csv"
    f.write_text("roll_no,name,branch\n101,Neha Joshi,CSE\n102,Aarav Mehta,ECE\n", encoding="utf-8")
    assert certigen.load_names(f) == ["Neha Joshi", "Aarav Mehta"]


def test_step1_missing_name_column_raises(tmp_path):
    f = tmp_path / "names.csv"
    f.write_text("student\nRiya Verma\n", encoding="utf-8")
    with pytest.raises(ValueError, match="name"):
        certigen.load_names(f)


def test_step1_unsupported_file_type_raises(tmp_path):
    f = tmp_path / "names.txt"
    f.write_text("name\nRiya Verma\n", encoding="utf-8")
    with pytest.raises(ValueError):
        certigen.load_names(f)


# ---------------------------------------------------------------- Step 2 --
def test_step2_simple_names():
    assert certigen.safe_filename("Riya Verma", set()) == "Riya_Verma"
    assert certigen.safe_filename(" A/B: C? ", set()) == "A_B_C"
    assert certigen.safe_filename("O'Brien", set()) == "O_Brien"


def test_step2_nothing_left_uses_default():
    assert certigen.safe_filename("***", set()) == "certificate"


def test_step2_repeated_names_get_numbers():
    used = set()
    assert certigen.safe_filename("Riya Verma", used) == "Riya_Verma"
    assert certigen.safe_filename("Riya Verma", used) == "Riya_Verma_2"
    assert certigen.safe_filename("Riya  Verma", used) == "Riya_Verma_3"
    assert used == {"Riya_Verma", "Riya_Verma_2", "Riya_Verma_3"}


# ---------------------------------------------------------------- Step 3 --
def _width(name, size):
    return ImageFont.truetype(str(FONT), size).getlength(name)


def test_step3_short_name_keeps_start_size():
    size = certigen.fit_font_size("Kabir Singh", FONT, 2400, 190, 90)
    assert isinstance(size, int)
    assert size == 190


def test_step3_long_name_shrinks_to_fit():
    name = "Ananya Krishnamurthy Subramaniam"
    size = certigen.fit_font_size(name, FONT, 2400, 190, 90)
    assert 90 <= size < 190
    assert _width(name, size) <= 2400 * 1.02          # it fits
    assert _width(name, size + 2) > 2400 * 0.98       # and it isn't much smaller than needed


def test_step3_never_below_min_size():
    name = "An extremely long name " * 6
    assert certigen.fit_font_size(name, FONT, 2400, 190, 90) == 90


# ---------------------------------------------------------------- Step 4 --
def _dark_box(image, top, bottom):
    """Bounding box (left, top, right, bottom) of navy-ish pixels between two rows."""
    band = np.asarray(image.convert("RGB"))[top:bottom]
    dark = (band[:, :, 0] < 110) & (band[:, :, 1] < 110) & (band[:, :, 2] < 140)
    ys, xs = np.nonzero(dark)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max(), ys.max()


def test_step4_returns_rgb_image_of_template_size():
    image = certigen.render_certificate("Kabir Singh", TEMPLATE, FONT)
    template = Image.open(TEMPLATE)
    assert isinstance(image, Image.Image)
    assert image.mode == "RGB"
    assert image.size == template.size


def test_step4_name_is_drawn_centred_in_the_name_area():
    image = certigen.render_certificate("Kabir Singh", TEMPLATE, FONT)
    cy = certigen.CONFIG["name_center_y"]
    box = _dark_box(image, cy - 170, cy + 170)
    assert box is not None, "No dark text found in the name area"
    left, top, right, bottom = box
    centre_x = (left + right) / 2
    assert abs(centre_x - image.width / 2) < image.width * 0.03, "Name is not centred"
    centre_y = cy - 170 + (top + bottom) / 2
    assert abs(centre_y - cy) < 60, "Name is not at name_center_y"


def test_step4_template_file_is_not_changed():
    before = Image.open(TEMPLATE).tobytes()
    certigen.render_certificate("Kabir Singh", TEMPLATE, FONT)
    assert Image.open(TEMPLATE).tobytes() == before


# ---------------------------------------------------------------- Step 5 --
def test_step5_saves_a_pdf(tmp_path):
    out = tmp_path / "nested" / "Kabir_Singh.pdf"
    result = certigen.make_certificate("Kabir Singh", TEMPLATE, FONT, out)
    assert Path(result) == out
    assert out.exists()
    assert out.read_bytes()[:5] == b"%PDF-"


# ---------------------------------------------------------------- Step 6 --
def test_step6_makes_one_pdf_per_name_and_a_zip(tmp_path):
    names = tmp_path / "names.csv"
    names.write_text("Name\nRiya Verma\nAman Gill\nRiya Verma\n", encoding="utf-8")
    zip_path = certigen.generate_all(names, TEMPLATE, FONT, tmp_path / "out")

    assert Path(zip_path) == tmp_path / "out" / "certificates.zip"
    with zipfile.ZipFile(zip_path) as zf:
        assert sorted(zf.namelist()) == ["Aman_Gill.pdf", "Riya_Verma.pdf", "Riya_Verma_2.pdf"]
        for member in zf.namelist():
            assert zf.read(member)[:5] == b"%PDF-"
    assert (tmp_path / "out" / "certificates" / "Aman_Gill.pdf").exists()
