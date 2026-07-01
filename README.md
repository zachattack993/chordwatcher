# chordwatcher

music scanner that puts notes from documents into a midi

ChordWatcher scans `.txt`, `.docx`, and `.pdf` documents for chord charts
(e.g. `C  G  Am  F`) and explicit note names (e.g. `C4 E4 G4`), then exports
what it finds as a standard `.mid` file. Import that file into GarageBand
(File > Import) or any other DAW and drop it onto a software instrument
track to hear it played back.

## Install

```
pip install -r requirements.txt
```

The `pdf2image`/`pytesseract` entries are only needed to OCR scanned PDFs
that have no extractable text; they also require the system tools `poppler`
and `tesseract-ocr` to be installed.

## Usage

**GUI** (requires Python's `tkinter`, which ships with most Python installs):

```
python3 main.py
```

Pick a document, then choose where to save the resulting `.mid` file.

**Command line:**

```
python3 main.py song.txt -o song.mid
# or directly:
python3 -m chordwatcher.cli song.docx --tempo 120
```

## How detection works

- A line where most whitespace-separated tokens look like chord symbols
  (`C`, `Am`, `G7`, `F#m7`, `D/F#`, ...) is treated as a chord line, and
  every chord on it is captured as a major/minor/seventh/etc. triad.
- Elsewhere, only explicit note names with an octave number (`C4`, `Bb2`,
  `F#5`) are captured, since a bare letter is too easy to confuse with an
  ordinary word outside of a chord chart.

## Building a standalone executable

```
pip install pyinstaller
pyinstaller --onefile --windowed --name ChordWatcher main.py
```

This produces a double-clickable executable in `dist/` (`ChordWatcher.exe`
on Windows, `ChordWatcher` on macOS/Linux) that launches the GUI without
needing Python installed separately.

## Tests

```
python3 -m unittest discover tests
```
