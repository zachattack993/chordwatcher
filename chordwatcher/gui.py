"""Minimal desktop GUI for ChordWatcher, built on tkinter (Python's stdlib GUI toolkit)."""

from pathlib import Path


def launch_gui() -> None:
    # Imported lazily so importing this module doesn't require tkinter unless
    # the GUI is actually launched (headless environments can still use the CLI).
    import tkinter as tk
    from tkinter import filedialog, messagebox

    from .midi_writer import write_midi
    from .notes import scan_text_for_events
    from .scanner import extract_text

    root = tk.Tk()
    root.title("ChordWatcher")
    root.geometry("420x220")
    root.resizable(False, False)

    status_var = tk.StringVar(value="Select a document to scan for music notes.")
    selected_path = {"value": None}

    def pick_file() -> None:
        path = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[("Supported documents", "*.txt *.docx *.pdf"), ("All files", "*.*")],
        )
        if path:
            selected_path["value"] = path
            status_var.set(f"Selected: {Path(path).name}")

    def scan_and_export() -> None:
        path = selected_path["value"]
        if not path:
            messagebox.showwarning("ChordWatcher", "Please select a file first.")
            return

        try:
            text = extract_text(Path(path))
            events = scan_text_for_events(text)
        except (ValueError, RuntimeError) as exc:
            messagebox.showerror("ChordWatcher", str(exc))
            return

        if not events:
            messagebox.showinfo(
                "ChordWatcher", "No musical notes or chords were found in that document."
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Save MIDI file",
            defaultextension=".mid",
            initialfile=Path(path).stem + ".mid",
            filetypes=[("MIDI file", "*.mid")],
        )
        if not output_path:
            return

        write_midi(events, output_path)
        status_var.set(f"Wrote {len(events)} note(s)/chord(s) to {Path(output_path).name}")
        messagebox.showinfo(
            "ChordWatcher",
            f"Found {len(events)} note(s)/chord(s).\n\n"
            f"Saved to {output_path}\n\n"
            "Import this file into GarageBand via File > Import, then drag it onto a "
            "software instrument track.",
        )

    tk.Label(root, text="ChordWatcher", font=("Helvetica", 18, "bold")).pack(pady=(16, 4))
    tk.Label(root, textvariable=status_var, wraplength=380, justify="center").pack(pady=4)
    tk.Button(root, text="Choose Document...", command=pick_file, width=24).pack(pady=8)
    tk.Button(root, text="Scan && Export MIDI", command=scan_and_export, width=24).pack(pady=8)

    root.mainloop()
