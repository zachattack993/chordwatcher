"""Command-line interface: scan a document and export a MIDI file."""

import argparse
import sys
from pathlib import Path

from .midi_writer import write_midi
from .notes import scan_text_for_events
from .scanner import extract_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chordwatcher",
        description=(
            "Scan a .txt, .docx, or .pdf document for musical notes/chords and "
            "export them as a MIDI file you can import into GarageBand or any DAW."
        ),
    )
    parser.add_argument("input", help="Path to the document to scan")
    parser.add_argument(
        "-o", "--output", help="Output .mid path (default: same name as input, with .mid)"
    )
    parser.add_argument("--tempo", type=int, default=100, help="Tempo in BPM (default: 100)")
    parser.add_argument(
        "--beat-duration",
        type=float,
        default=1.0,
        dest="beat_duration",
        help="Length of each detected note/chord, in beats (default: 1.0)",
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".mid")

    try:
        text = extract_text(input_path)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    events = scan_text_for_events(text)
    if not events:
        print(f"No musical notes or chords were found in {input_path}")
        return 1

    write_midi(events, output_path, tempo=args.tempo, beat_duration=args.beat_duration)

    print(f"Found {len(events)} note(s)/chord(s). Wrote MIDI file to {output_path}")
    print(
        "Import this file into GarageBand via File > Import, then drag it onto a "
        "software instrument track."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
