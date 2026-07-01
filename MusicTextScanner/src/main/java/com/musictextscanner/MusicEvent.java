package com.musictextscanner;

import java.util.List;

public class MusicEvent {
    private final String symbol;
    private final List<Integer> midiNotes;
    private final int beats;

    public MusicEvent(String symbol, List<Integer> midiNotes, int beats) {
        this.symbol = symbol;
        this.midiNotes = midiNotes;
        this.beats = beats;
    }

    public String getSymbol() {
        return symbol;
    }

    public List<Integer> getMidiNotes() {
        return midiNotes;
    }

    public int getBeats() {
        return beats;
    }
}
