"""Music theory helpers: find note/chord tokens in text and convert them to MIDI pitches."""

import re
from dataclasses import dataclass
from typing import List

# Semitone offset of each natural note from C.
NOTE_SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

# Semitone intervals (from the root) for each chord quality, longest symbol first
# so the anchored regex below prefers the most specific match on backtracking.
CHORD_INTERVALS = {
    "maj9": (0, 4, 7, 11, 14),
    "maj7": (0, 4, 7, 11),
    "maj": (0, 4, 7),
    "min9": (0, 3, 7, 10, 14),
    "min7": (0, 3, 7, 10),
    "min": (0, 3, 7),
    "m13": (0, 3, 7, 10, 14, 21),
    "m11": (0, 3, 7, 10, 14, 17),
    "m9": (0, 3, 7, 10, 14),
    "m7": (0, 3, 7, 10),
    "m6": (0, 3, 7, 9),
    "m": (0, 3, 7),
    "dim7": (0, 3, 6, 9),
    "dim": (0, 3, 6),
    "aug": (0, 4, 8),
    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),
    "add9": (0, 4, 7, 14),
    "13": (0, 4, 7, 10, 14, 21),
    "11": (0, 4, 7, 10, 14, 17),
    "9": (0, 4, 7, 10, 14),
    "7": (0, 4, 7, 10),
    "6": (0, 4, 7, 9),
    "": (0, 4, 7),  # bare letter (e.g. "C") means a major triad
}

_QUALITY_ALTERNATION = "|".join(q for q in CHORD_INTERVALS if q)

# A whole "word" that looks like a chord symbol, e.g. C, Am, G7, F#m7, Bb, D/F#.
CHORD_TOKEN_RE = re.compile(
    r"^(?P<letter>[A-G])"
    r"(?P<acc>#{1,2}|b{1,2})?"
    rf"(?P<quality>{_QUALITY_ALTERNATION})?"
    r"(?:/(?P<bass_letter>[A-G])(?P<bass_acc>#{1,2}|b{1,2})?)?$"
)

# An explicit note name with an octave number, e.g. C4, F#3, Bb2. Unambiguous,
# so it is searched for anywhere in the text (not just on chord-like lines).
NOTE_OCTAVE_RE = re.compile(r"\b(?P<letter>[A-G])(?P<acc>#{1,2}|b{1,2})?(?P<octave>-?[0-8])\b")

# Fraction of whitespace-separated tokens on a line that must look like chord
# symbols before that line is treated as a chord line (as opposed to lyrics/prose).
CHORD_LINE_THRESHOLD = 0.6

_STRIP_CHARS = ".,;:()[]|"


@dataclass
class MusicalEvent:
    """A single detected note or chord, expressed as MIDI pitch numbers."""

    pitches: List[int]
    token: str
    kind: str  # "note" or "chord"


def note_letter_to_semitone(letter: str, accidental: str = None) -> int:
    semitone = NOTE_SEMITONES[letter.upper()]
    if accidental:
        if accidental[0] == "#":
            semitone += len(accidental)
        elif accidental[0] == "b":
            semitone -= len(accidental)
    return semitone % 12


def chord_to_midi_pitches(semitone: int, quality: str, base_octave: int = 3) -> List[int]:
    root_midi = (base_octave + 1) * 12 + semitone
    intervals = CHORD_INTERVALS.get(quality or "", CHORD_INTERVALS[""])
    return [_clamp_midi(root_midi + interval) for interval in intervals]


def note_to_midi(letter: str, accidental: str, octave: int) -> int:
    semitone = note_letter_to_semitone(letter, accidental)
    return _clamp_midi((octave + 1) * 12 + semitone)


def _clamp_midi(pitch: int) -> int:
    return max(0, min(127, pitch))


def _event_from_chord_match(match: "re.Match") -> MusicalEvent:
    letter = match.group("letter")
    acc = match.group("acc")
    quality = match.group("quality") or ""
    semitone = note_letter_to_semitone(letter, acc)
    pitches = chord_to_midi_pitches(semitone, quality)
    return MusicalEvent(pitches=pitches, token=match.group(0), kind="chord")


def _event_from_note_match(match: "re.Match") -> MusicalEvent:
    letter = match.group("letter")
    acc = match.group("acc")
    octave = int(match.group("octave"))
    pitch = note_to_midi(letter, acc, octave)
    return MusicalEvent(pitches=[pitch], token=match.group(0), kind="note")


def scan_text_for_events(text: str) -> List[MusicalEvent]:
    """Scan raw document text for chord charts and explicit note names.

    Lines that are mostly made up of chord-looking tokens (e.g. "C  G  Am  F")
    are treated as chord lines and every chord token on them is captured.
    Everywhere else, only explicit note names with an octave number
    (e.g. "C4", "F#3") are captured, since a bare letter is too ambiguous
    with ordinary words to safely detect outside of a chord line.
    """
    events: List[MusicalEvent] = []
    for line in text.splitlines():
        tokens = line.split()
        if not tokens:
            continue

        matches = [CHORD_TOKEN_RE.match(tok.strip(_STRIP_CHARS)) for tok in tokens]
        hit_count = sum(1 for m in matches if m)

        if hit_count / len(tokens) >= CHORD_LINE_THRESHOLD:
            for m in matches:
                if m:
                    events.append(_event_from_chord_match(m))
        else:
            for m in NOTE_OCTAVE_RE.finditer(line):
                events.append(_event_from_note_match(m))

    return events
