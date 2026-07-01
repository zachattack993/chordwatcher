package com.musictextscanner;

import java.io.File;
import java.io.FileWriter;
import java.util.List;

public class MusicXmlGenerator {
    public static void export(List<MusicEvent> events, int tempo, File outputFile) throws Exception {
        try (FileWriter writer = new FileWriter(outputFile)) {
            writer.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n");
            writer.write("<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 3.1 Partwise//EN\" ");
            writer.write("\"http://www.musicxml.org/dtds/partwise.dtd\">\n");
            writer.write("<score-partwise version=\"3.1\">\n");
            writer.write("  <part-list>\n");
            writer.write("    <score-part id=\"P1\"><part-name>Music Text Scanner</part-name></score-part>\n");
            writer.write("  </part-list>\n");
            writer.write("  <part id=\"P1\">\n");
            writer.write("    <measure number=\"1\">\n");
            writer.write("      <attributes><divisions>1</divisions><key><fifths>0</fifths></key><time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef></attributes>\n");
            writer.write("      <direction placement=\"above\"><direction-type><metronome><beat-unit>quarter</beat-unit><per-minute>" + tempo + "</per-minute></metronome></direction-type><sound tempo=\"" + tempo + "\"/></direction>\n");

            int beatCount = 0;
            int measure = 1;
            for (MusicEvent event : events) {
                if (beatCount >= 4) {
                    writer.write("    </measure>\n");
                    writer.write("    <measure number=\"" + (++measure) + "\">\n");
                    beatCount = 0;
                }
                boolean first = true;
                for (int midi : event.getMidiNotes()) {
                    NoteParts p = toNoteParts(midi);
                    writer.write("      <note>\n");
                    if (!first) writer.write("        <chord/>\n");
                    writer.write("        <pitch><step>" + p.step + "</step>");
                    if (p.alter != 0) writer.write("<alter>" + p.alter + "</alter>");
                    writer.write("<octave>" + p.octave + "</octave></pitch>\n");
                    writer.write("        <duration>1</duration><type>quarter</type>\n");
                    writer.write("      </note>\n");
                    first = false;
                }
                beatCount++;
            }

            writer.write("    </measure>\n");
            writer.write("  </part>\n");
            writer.write("</score-partwise>\n");
        }
    }

    private static NoteParts toNoteParts(int midi) {
        int pc = midi % 12;
        int octave = (midi / 12) - 1;
        return switch (pc) {
            case 0 -> new NoteParts("C", 0, octave);
            case 1 -> new NoteParts("C", 1, octave);
            case 2 -> new NoteParts("D", 0, octave);
            case 3 -> new NoteParts("D", 1, octave);
            case 4 -> new NoteParts("E", 0, octave);
            case 5 -> new NoteParts("F", 0, octave);
            case 6 -> new NoteParts("F", 1, octave);
            case 7 -> new NoteParts("G", 0, octave);
            case 8 -> new NoteParts("G", 1, octave);
            case 9 -> new NoteParts("A", 0, octave);
            case 10 -> new NoteParts("A", 1, octave);
            case 11 -> new NoteParts("B", 0, octave);
            default -> new NoteParts("C", 0, octave);
        };
    }

    private record NoteParts(String step, int alter, int octave) {}
}
