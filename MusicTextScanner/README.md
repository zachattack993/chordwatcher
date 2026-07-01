# Music Text Scanner

A Java desktop app that reads PDF, DOCX, or TXT files containing music notes/chords written in letter form and exports them as MIDI or MusicXML.

Example input:

```text
Tempo: 120 BPM
C D E F G A B
Am F C G
G7 Cmaj7 Dm
```

## Features

- Drag-and-drop file import
- Opens PDF, DOCX, and TXT files
- Detects tempo markings such as `Tempo: 120` or `120 BPM`
- Lets the user choose an instrument
- Exports `.mid` for GarageBand, Ableton, FL Studio, Logic, etc.
- Exports `.musicxml` for notation software like MuseScore, Finale, or Sibelius

## Requirements

- Java 17 or newer
- Maven 3.8 or newer

## Build executable JAR

```bash
mvn clean package
```

The runnable file will be created here:

```text
target/MusicTextScanner-1.0.0.jar
```

## Run

```bash
java -jar target/MusicTextScanner-1.0.0.jar
```

## Notes Supported

Basic notes:

```text
C D E F G A B C# Db Eb F# Gb Ab Bb
```

Basic chords:

```text
Am Dm Em G7 Cmaj7 Fsus4 Bdim Caug
```

This is a starter version. It can be expanded later to support note lengths, octaves, rests, multiple tracks, lyrics, and advanced chord types.
