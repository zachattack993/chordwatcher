package com.musictextscanner;

import javax.sound.midi.*;
import java.io.File;
import java.util.List;

public class MidiGenerator {
    public static void export(List<MusicEvent> events, int tempo, int instrument, File outputFile) throws Exception {
        Sequence sequence = new Sequence(Sequence.PPQ, 480);
        Track track = sequence.createTrack();

        addTempo(track, tempo);
        addInstrument(track, instrument);

        long tick = 0;
        for (MusicEvent event : events) {
            long duration = event.getBeats() * 480L;
            for (int note : event.getMidiNotes()) {
                addNote(track, note, tick, duration, 90);
            }
            tick += duration;
        }

        MidiSystem.write(sequence, 1, outputFile);
    }

    private static void addTempo(Track track, int bpm) throws Exception {
        int mpq = 60000000 / bpm;
        MetaMessage msg = new MetaMessage();
        byte[] data = {(byte) (mpq >> 16), (byte) (mpq >> 8), (byte) mpq};
        msg.setMessage(0x51, data, 3);
        track.add(new MidiEvent(msg, 0));
    }

    private static void addInstrument(Track track, int instrument) throws Exception {
        ShortMessage msg = new ShortMessage();
        msg.setMessage(ShortMessage.PROGRAM_CHANGE, 0, instrument, 0);
        track.add(new MidiEvent(msg, 0));
    }

    private static void addNote(Track track, int note, long start, long duration, int velocity) throws Exception {
        ShortMessage on = new ShortMessage();
        on.setMessage(ShortMessage.NOTE_ON, 0, note, velocity);
        track.add(new MidiEvent(on, start));

        ShortMessage off = new ShortMessage();
        off.setMessage(ShortMessage.NOTE_OFF, 0, note, 0);
        track.add(new MidiEvent(off, start + duration));
    }
}
