package com.musictextscanner;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TempoDetector {
    private static final Pattern[] TEMPO_PATTERNS = new Pattern[] {
            Pattern.compile("(?i)\\btempo\\s*[:=]?\\s*(\\d{2,3})\\b"),
            Pattern.compile("(?i)\\b(\\d{2,3})\\s*bpm\\b")
    };

    public static int detect(String text) {
        for (Pattern pattern : TEMPO_PATTERNS) {
            Matcher matcher = pattern.matcher(text);
            if (matcher.find()) {
                int bpm = Integer.parseInt(matcher.group(1));
                if (bpm >= 40 && bpm <= 240) {
                    return bpm;
                }
            }
        }
        return 120;
    }
}
