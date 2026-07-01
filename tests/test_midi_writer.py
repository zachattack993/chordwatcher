import tempfile
import unittest
from pathlib import Path

from chordwatcher.midi_writer import write_midi
from chordwatcher.notes import scan_text_for_events


class TestWriteMidi(unittest.TestCase):
    def test_writes_a_valid_midi_file(self):
        events = scan_text_for_events("C  G  Am  F\n")
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "out.mid"
            write_midi(events, output_path)

            self.assertTrue(output_path.exists())
            data = output_path.read_bytes()
            self.assertGreater(len(data), 0)
            self.assertEqual(data[:4], b"MThd")  # standard MIDI file header

    def test_no_events_still_writes_a_header_only_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "empty.mid"
            write_midi([], output_path)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
