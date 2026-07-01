"""Turn detected musical events into a standard MIDI file."""

from typing import Iterable

from .notes import MusicalEvent


def write_midi(
    events: Iterable[MusicalEvent],
    output_path,
    tempo: int = 100,
    beat_duration: float = 1.0,
    volume: int = 90,
    instrument: int = 0,
) -> None:
    """Write detected events out as a single-track .mid file.

    Each event (note or chord) occupies one `beat_duration`-length slot in
    sequence, so a chord's notes sound together and the progression plays
    back in the order it was found in the document. The resulting file can
    be imported into GarageBand (File > Import) or any other DAW and
    dropped onto a software instrument track.
    """
    from midiutil import MIDIFile

    events = list(events)
    track = 0
    channel = 0
    time = 0.0

    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)
    midi.addProgramChange(track, channel, time, instrument)

    for event in events:
        for pitch in event.pitches:
            midi.addNote(track, channel, pitch, time, beat_duration, volume)
        time += beat_duration

    with open(output_path, "wb") as midi_file:
        midi.writeFile(midi_file)
