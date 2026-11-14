# CertiGen build guide

This kit gives you the project's skeleton: function names, rules for what each one must do, sample data, a sample certificate design, a font, and tests. **You write the code inside each function.** That is what makes CertiGen your project, and it's what you'll be asked about in interviews.

Work through the steps in order. Each one is small, roughly one evening. Check every step with its tests, then commit. Searching the docs and Stack Overflow is normal. If you get help from a person or an AI, ask them to explain the idea, then type the code yourself. You should be able to explain every line.

| Step | Function | Main thing you learn | Rough time |
|---|---|---|---|
| 0 | Setup | Python environment, Git, GitHub | 1 hour |
| 1 | `load_names` | pandas: reading CSV and Excel, cleaning text | 1–2 hours |
| 2 | `safe_filename` | Regular expressions, sets, loops | 1 hour |
| 3 | `fit_font_size` | Pillow fonts, measuring text | 1 hour |
| 4 | `render_certificate` | Drawing text on an image | 1–2 hours |
| 5 | `make_certificate` | Saving PDFs, creating folders | 30 minutes |
| 6 | `generate_all` | Putting it together, ZIP files | 1 hour |
| 7 | Demo-ready | README, screenshots, a demo video | 2 hours |

---

## Step 0: Setup

The starter kit is already on GitHub at **github.com/tejasvinisharma/certigen**, so this step is about getting it onto your laptop.

1. Check Python with `python --version` (3.10 or newer). Install VS Code and Git if you don't have them.
2. Get the code. In a terminal, go to the folder where you keep projects and run:
   ```bash
   git clone https://github.com/tejasvinisharma/certigen.git
   cd certigen
   ```
   Then open the `certigen` folder in VS Code.
3. Create a virtual environment and install the libraries:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate            # Windows
   # source .venv/bin/activate       # Mac / Linux
   pip install -r requirements.txt
   ```
4. Run the tests: `python -m pytest`. You should see **16 failed**. That's correct, because nothing is written yet. Each failure says `NotImplementedError: Step N`.
5. Saving your work to GitHub, after every step:
   ```bash
   git add .
   git commit -m "Describe what you did"
   git push
   ```
   The first `git push` asks you to sign in to GitHub. Follow the prompt in the terminal or browser.
6. **LinkedIn:** publish **Post 1** (draft at the end of this guide) on the day you start Step 1.

---

## Step 1: `load_names`

**Goal:** read a CSV or Excel file and return a clean list of names.

**Read first:** [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html), [pandas.read_excel](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html), [pandas.isna](https://pandas.pydata.org/docs/reference/api/pandas.isna.html)

**Hints**
- `Path(path).suffix.lower()` gives `".csv"` or `".xlsx"`. Pick `pd.read_csv` or `pd.read_excel` based on it, and raise `ValueError` for anything else.
- Find the column by looping over `df.columns` and comparing `str(col).strip().lower()` with `"name"`.
- `" ".join(text.split())` removes spaces at both ends **and** squeezes the spaces in between.
- An empty Excel cell comes back as `NaN`, and `str(NaN)` is the text `"nan"`. Check `pd.isna(value)` before you clean a value, or you'll print certificates for a person called "nan".

**Check:** `python -m pytest -k step1` → 5 passed
**Commit:** `git commit -am "Read and clean names from CSV and Excel"` then `git push`

---

## Step 2: `safe_filename`

**Goal:** `"Riya Verma"` → `"Riya_Verma"`, and the second Riya Verma → `"Riya_Verma_2"`.

**Read first:** [re.sub](https://docs.python.org/3/library/re.html#re.sub)

**Hints**
- The pattern `[^A-Za-z0-9]+` matches one or more characters that are *not* letters or digits.
- `"__A_B__".strip("_")` → `"A_B"`.
- If the result is empty, use `"certificate"`.
- Use a `while` loop: while the name is in `used`, try `base_2`, `base_3` and so on. Then `used.add(...)` before returning.

**Check:** `python -m pytest -k step2` → 3 passed
**Commit:** `"Make safe, unique file names"`

---

## Step 3: `fit_font_size`

**Goal:** find the biggest font size at which a name fits the space.

**Read first:** [ImageFont.truetype and getlength](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html)

**Hints**
- `font = ImageFont.truetype(str(font_path), size)` loads the font at one size. `font.getlength(name)` gives the width in pixels.
- Start at `start_size` and go down by 2 while the name is wider than `max_width`. Stop at `min_size`.
- Try it in the terminal first:
  ```python
  from PIL import ImageFont
  f = ImageFont.truetype("fonts/Poppins-Medium.ttf", 190)
  f.getlength("Kabir Singh")
  ```

**Check:** `python -m pytest -k step3` → 3 passed
**Commit:** `"Shrink long names to fit"`

**LinkedIn:** the repo now has working commits, so add the CertiGen **project entry** (section 7.1 of the implementation package). Keep "Status: in progress" and tick "I am currently working on this project".

---

## Step 4: `render_certificate`

**Goal:** write the name on the template, centred, in navy.

**Read first:** [ImageDraw.text](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html), [Text anchors](https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html)

**Hints**
- `Image.open(template_path).convert("RGB")`: PDFs can't hold transparency, so convert first.
- `draw = ImageDraw.Draw(image)`, then `draw.text((x, y), name, font=font, fill=color, anchor="mm")`.
- In `anchor="mm"`, the first `m` centres the text horizontally and the second centres it vertically, so `(x, y)` becomes the middle of the text. For the centre of the page, use `x = image.width / 2` and `y = config["name_center_y"]`.
- Look at your result before running the tests: `render_certificate("Your Name", ...).show()`.

**Check:** `python -m pytest -k step4` → 3 passed
**Commit:** `"Draw names on the certificate template"`

---

## Step 5: `make_certificate`

**Goal:** save one certificate as an A4 PDF.

**Read first:** [Pillow PDF saving](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#pdf-saving)

**Hints**
- `Path(out_path).parent.mkdir(parents=True, exist_ok=True)` creates the folder if needed.
- `image.save(out_path, "PDF", resolution=300)`. A 3508 × 2480 px image at 300 dpi is exactly A4.

**Check:** `python -m pytest -k step5` → 1 passed
**Commit:** `"Save certificates as PDF"`

---

## Step 6: `generate_all`

**Goal:** a PDF for every name, and one ZIP containing them all.

**Read first:** [zipfile.ZipFile](https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile)

**Hints**
- Make one `used = set()` before the loop and pass it to every `safe_filename` call.
- Keep a list of the PDF paths you made.
- `with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:` then `zf.write(pdf, arcname=pdf.name)`. `arcname` keeps folder paths out of the ZIP.

**Check:** `python -m pytest` → **16 passed**
**Run it:** `python certigen.py sample_data/names.csv`, then open a few PDFs in `output/certificates/`.
**Commit:** `"Generate all certificates and ZIP them"`

**LinkedIn:** publish **Post 2** (draft below) with a screenshot of one certificate and the terminal line that shows how many it made and how fast.

---

## Step 7: Make it demo-ready

1. **Speed test:** make a CSV of 100 made-up names and run it. Write down the time the tool prints; that's your real number for posts and the README.
2. **README:** tick the features that work, add a screenshot of 2 certificates, and fill in "What I learned" with 3–5 honest points.
3. **Demo video (60 seconds):** show the spreadsheet → run the command → open the ZIP → open 2 PDFs. A free screen recorder is fine.
4. Then, per the implementation package: post 3 (the demo), add the demo to Featured, and mark the LinkedIn project as completed once the README and video are live.

---

## Stretch goals (pick any, after Step 7)

- **Two-line names.** Try `Venkata Lakshmi Narasimha Bhattacharya Raghunathan` from the sample data: it hits the smallest font size and still runs wider than `name_max_width`. Split long names onto two lines instead. This is a good "problem I found and fixed" story.
- **Event date:** add a `--date` option and draw it in a second position.
- **Your own design:** make a 3508 × 2480 px design in Canva, export it as PNG, and measure where the name goes. Update `CONFIG`.
- **Web page:** a small Streamlit app where someone uploads a CSV and downloads the ZIP.

## Real names and privacy

- Keep real attendee lists out of the public repo. Put them in a `private_data/` folder, which `.gitignore` already skips.
- Get the organiser's permission before posting certificates that show real people's names.

## Be ready to explain

Once you've finished, you should be able to answer these without looking:

1. How does your code handle an empty cell in Excel? Why does `str()` on it cause trouble?
2. What happens when two people have the same name?
3. How do you decide the font size, and what happens when a name is too long even at the smallest size?
4. Why convert the image to RGB before saving the PDF?
5. What does `anchor="mm"` do?
6. How long does it take for 100 names, and which part is slowest? (Time each part with `time.perf_counter()` to find out.)

---

## LinkedIn post drafts

Before posting, change anything that isn't true for you. Use at most 3 hashtags.

### Post 1: publish the day you push the first commit

> Most certificates for college events and coaching batches are still typed out one name at a time. It's slow, and it's easy to misspell someone's name.
>
> So my first Python project is CertiGen: a tool that reads a spreadsheet of names and makes one ready-to-print PDF certificate per person, bundled into a single ZIP.
>
> The plan:
> 1. Read names from a CSV or Excel file and clean them up
> 2. Shrink long names so they still fit the design
> 3. Write each name on the certificate
> 4. Save one PDF per person, then zip them all
>
> I'm building it one step at a time, with tests that check each part, and I'll share what works and what breaks.
>
> If you've made certificates for an event, what was the most annoying part?
>
> #Python #BuildInPublic #LearningInPublic

### Post 2: publish when all 16 tests pass

Fill in every [bracket] with your real details.

> CertiGen made its first [N] certificates today, in [X] seconds.
>
> What works:
> • Reads names from CSV or Excel, even with messy spaces and blank rows
> • Shrinks long names so they fit the design
> • Gives repeated names their own files (Riya_Verma.pdf, Riya_Verma_2.pdf)
> • Saves one A4 PDF per person and zips them
>
> What broke first: [one real thing that went wrong while you built it, and how you fixed it]
>
> What doesn't work yet: very long names hit the smallest font size and still run too wide. Next I'm splitting them onto two lines.
>
> Code: [GitHub link]. Feedback on my approach is welcome.
>
> #Python #pandas #BuildInPublic
