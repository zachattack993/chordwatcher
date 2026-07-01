import unittest

from chordwatcher.notes import (
    note_letter_to_semitone,
    note_to_midi,
    chord_to_midi_pitches,
    scan_text_for_events,
)


class TestSemitones(unittest.TestCase):
    def test_natural_notes(self):
        self.assertEqual(note_letter_to_semitone("C"), 0)
        self.assertEqual(note_letter_to_semitone("A"), 9)
        self.assertEqual(note_letter_to_semitone("B"), 11)

    def test_accidentals(self):
        self.assertEqual(note_letter_to_semitone("C", "#"), 1)
        self.assertEqual(note_letter_to_semitone("D", "b"), 1)
        self.assertEqual(note_letter_to_semitone("B", "#"), 0)  # wraps to C


class TestNoteToMidi(unittest.TestCase):
    def test_middle_c(self):
        self.assertEqual(note_to_midi("C", None, 4), 60)

    def test_octave_math(self):
        self.assertEqual(note_to_midi("A", None, 4), 69)
        self.assertEqual(note_to_midi("C", "#", 4), 61)


class TestChordIntervals(unittest.TestCase):
    def test_c_major(self):
        # C major triad, root at octave 3 -> C3=48, E3=52, G3=55
        self.assertEqual(chord_to_midi_pitches(0, ""), [48, 52, 55])

    def test_a_minor(self):
        self.assertEqual(chord_to_midi_pitches(9, "m"), [57, 60, 64])

    def test_g7(self):
        self.assertEqual(chord_to_midi_pitches(7, "7"), [55, 59, 62, 65])


class TestScanTextForEvents(unittest.TestCase):
    def test_chord_line_detection(self):
        text = "C  G  Am  F\nHello world, this is just a lyric line.\n"
        events = scan_text_for_events(text)
        self.assertEqual(len(events), 4)
        self.assertEqual([e.token for e in events], ["C", "G", "Am", "F"])
        self.assertEqual(events[0].kind, "chord")
        self.assertEqual(events[0].pitches, [48, 52, 55])

    def test_explicit_notes_with_octave(self):
        text = "Play these notes in order: C4 E4 G4 then C5."
        events = scan_text_for_events(text)
        self.assertEqual([e.token for e in events], ["C4", "E4", "G4", "C5"])
        self.assertEqual(events[0].pitches, [60])
        self.assertEqual(events[3].pitches, [72])

    def test_ordinary_prose_yields_nothing(self):
        text = "This is a normal sentence with no music notation in it at all."
        events = scan_text_for_events(text)
        self.assertEqual(events, [])

    def test_seventh_and_slash_chords(self):
        text = "Dm7  G7  Cmaj7  D/F#"
        events = scan_text_for_events(text)
        self.assertEqual([e.token for e in events], ["Dm7", "G7", "Cmaj7", "D/F#"])


if __name__ == "__main__":
    unittest.main()
