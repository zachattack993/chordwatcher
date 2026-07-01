import tempfile
import unittest
from pathlib import Path

from chordwatcher.scanner import extract_text


class TestExtractText(unittest.TestCase):
    def test_txt_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "song.txt"
            path.write_text("C  G  Am  F\n", encoding="utf-8")
            self.assertEqual(extract_text(path), "C  G  Am  F\n")

    def test_docx_file(self):
        docx = pytest_import_docx()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "song.docx"
            document = docx.Document()
            document.add_paragraph("C  G  Am  F")
            document.save(str(path))
            text = extract_text(path)
            self.assertIn("C  G  Am  F", text)

    def test_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "song.xyz"
            path.write_text("nothing", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_text(path)

    def test_legacy_doc_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "song.doc"
            path.write_text("nothing", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_text(path)


def pytest_import_docx():
    try:
        import docx

        return docx
    except ImportError:
        raise unittest.SkipTest("python-docx not installed")


if __name__ == "__main__":
    unittest.main()
