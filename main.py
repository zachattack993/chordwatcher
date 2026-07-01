#!/usr/bin/env python3
"""Entry point for the ChordWatcher app.

Run with no arguments to launch the desktop GUI (requires tkinter). Run with
a file path argument to use it as a command-line tool instead, e.g.:

    python3 main.py song.txt -o song.mid
"""

import sys


def main() -> None:
    if len(sys.argv) > 1:
        from chordwatcher.cli import main as cli_main

        sys.exit(cli_main(sys.argv[1:]))

    try:
        from chordwatcher.gui import launch_gui
    except ImportError:
        print("No file argument given, and the GUI isn't available (tkinter not installed).")
        print("Usage: python3 main.py <file.txt|.docx|.pdf> [-o output.mid]")
        sys.exit(1)

    launch_gui()


if __name__ == "__main__":
    main()
