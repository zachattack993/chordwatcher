package com.musictextscanner;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class NoteParser {
    private static final Map<String, Integer> ROOTS = Map.ofEntries(
            Map.entry("C", 60), Map.entry("C#", 61), Map.entry("DB", 61),
            Map.entry("D", 62), Map.entry("D#", 63), Map.entry("EB", 63),
            Map.entry("E", 64),
            Map.entry("F", 65), Map.entry("F#", 66), Map.entry("GB", 66),
            Map.entry("G", 67), Map.entry("G#", 68), Map.entry("AB", 68),
            Map.entry("A", 69), Map.entry("A#", 70), Map.entry("BB", 70),
            Map.entry("B", 71)
    );

    private static final Pattern TOKEN_PATTERN = Pattern.compile(
            "\\b([A-Ga-g](?:#|b)?(?:maj7|maj|min|m|dim|aug|sus2|sus4|7)?)\\b"
    );

    public static List<MusicEvent> parse(String text) {
        List<MusicEvent> events = new ArrayList<>();
        Matcher matcher = TOKEN_PATTERN.matcher(text);

        while (matcher.find()) {
            String original = matcher.group(1);
            MusicEvent event = parseToken(original);
            if (event != null) {
                events.add(event);
            }
        }
        return events;
    }

    private static MusicEvent parseToken(String original) {
        String normalized = original.substring(0, 1).toUpperCase(Locale.ROOT) + original.substring(1);
        String root = normalized.substring(0, 1).toUpperCase(Locale.ROOT);
        int index = 1;

        if (normalized.length() > 1 && (normalized.charAt(1) == '#' || normalized.charAt(1) == 'b')) {
            root = normalized.substring(0, 2).toUpperCase(Locale.ROOT);
            index = 2;
        }

        Integer base = ROOTS.get(root);
        if (base == null) return null;

        String quality = normalized.substring(index).toLowerCase(Locale.ROOT);
        List<Integer> notes;

        if (quality.equals("m") || quality.equals("min")) {
            notes = List.of(base, base + 3, base + 7);
        } else if (quality.equals("7")) {
            notes = List.of(base, base + 4, base + 7, base + 10);
        } else if (quality.equals("maj7") || quality.equals("maj")) {
            notes = List.of(base, base + 4, base + 7, base + 11);
        } else if (quality.equals("dim")) {
            notes = List.of(base, base + 3, base + 6);
        } else if (quality.equals("aug")) {
            notes = List.of(base, base + 4, base + 8);
        } else if (quality.equals("sus2")) {
            notes = List.of(base, base + 2, base + 7);
        } else if (quality.equals("sus4")) {
            notes = List.of(base, base + 5, base + 7);
        } else {
            notes = List.of(base);
        }

        return new MusicEvent(original, notes, 1);
    }
}
