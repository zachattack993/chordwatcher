package com.musictextscanner;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.io.File;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class MusicTextScannerApp extends JFrame {
    private final JTextArea previewArea = new JTextArea();
    private final JLabel statusLabel = new JLabel("Drag a PDF, DOCX, or TXT file into the window.");
    private final JComboBox<String> instrumentBox = new JComboBox<>();
    private final JSpinner tempoSpinner = new JSpinner(new SpinnerNumberModel(120, 40, 240, 1));
    private List<MusicEvent> currentEvents = List.of();
    private int currentTempo = 120;

    private static final Map<String, Integer> INSTRUMENTS = new LinkedHashMap<>();
    static {
        INSTRUMENTS.put("Piano", 0);
        INSTRUMENTS.put("Acoustic Guitar", 24);
        INSTRUMENTS.put("Electric Guitar", 27);
        INSTRUMENTS.put("Violin", 40);
        INSTRUMENTS.put("Strings", 48);
        INSTRUMENTS.put("Trumpet", 56);
        INSTRUMENTS.put("Flute", 73);
        INSTRUMENTS.put("Synth Lead", 80);
    }

    public MusicTextScannerApp() {
        super("Music Text Scanner");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(850, 600);
        setLocationRelativeTo(null);

        INSTRUMENTS.keySet().forEach(instrumentBox::addItem);
        previewArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
        previewArea.setEditable(false);

        JButton openButton = new JButton("Open File");
        JButton exportMidiButton = new JButton("Export .MID");
        JButton exportXmlButton = new JButton("Export MusicXML");

        openButton.addActionListener(e -> chooseFile());
        exportMidiButton.addActionListener(e -> exportMidi());
        exportXmlButton.addActionListener(e -> exportMusicXml());

        JPanel top = new JPanel(new FlowLayout(FlowLayout.LEFT));
        top.add(openButton);
        top.add(new JLabel("Instrument:"));
        top.add(instrumentBox);
        top.add(new JLabel("Tempo:"));
        top.add(tempoSpinner);
        top.add(exportMidiButton);
        top.add(exportXmlButton);

        add(top, BorderLayout.NORTH);
        add(new JScrollPane(previewArea), BorderLayout.CENTER);
        add(statusLabel, BorderLayout.SOUTH);

        setTransferHandler(new TransferHandler() {
            @Override
            public boolean canImport(TransferSupport support) {
                return support.isDataFlavorSupported(DataFlavor.javaFileListFlavor);
            }

            @Override
            public boolean importData(TransferSupport support) {
                try {
                    List<File> files = (List<File>) support.getTransferable().getTransferData(DataFlavor.javaFileListFlavor);
                    if (!files.isEmpty()) loadFile(files.get(0));
                    return true;
                } catch (Exception ex) {
                    showError(ex);
                    return false;
                }
            }
        });
    }

    private void chooseFile() {
        JFileChooser chooser = new JFileChooser();
        chooser.setFileFilter(new FileNameExtensionFilter("PDF, DOCX, TXT", "pdf", "docx", "txt"));
        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            loadFile(chooser.getSelectedFile());
        }
    }

    private void loadFile(File file) {
        try {
            String text = FileTextReader.read(file);
            currentTempo = TempoDetector.detect(text);
            tempoSpinner.setValue(currentTempo);
            currentEvents = NoteParser.parse(text);

            StringBuilder preview = new StringBuilder();
            preview.append("Loaded: ").append(file.getName()).append("\n");
            preview.append("Detected tempo: ").append(currentTempo).append(" BPM\n");
            preview.append("Detected notes/chords: ").append(currentEvents.size()).append("\n\n");
            preview.append("Original Text Preview:\n");
            preview.append(text.length() > 5000 ? text.substring(0, 5000) + "\n..." : text);

            previewArea.setText(preview.toString());
            statusLabel.setText("Ready to export. Detected " + currentEvents.size() + " note/chord items.");
        } catch (Exception ex) {
            showError(ex);
        }
    }

    private void exportMidi() {
        if (currentEvents.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No notes were detected yet.");
            return;
        }
        JFileChooser chooser = new JFileChooser();
        chooser.setSelectedFile(new File("song.mid"));
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                int instrument = INSTRUMENTS.get((String) instrumentBox.getSelectedItem());
                int tempo = (Integer) tempoSpinner.getValue();
                MidiGenerator.export(currentEvents, tempo, instrument, chooser.getSelectedFile());
                statusLabel.setText("MIDI exported: " + chooser.getSelectedFile().getAbsolutePath());
            } catch (Exception ex) {
                showError(ex);
            }
        }
    }

    private void exportMusicXml() {
        if (currentEvents.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No notes were detected yet.");
            return;
        }
        JFileChooser chooser = new JFileChooser();
        chooser.setSelectedFile(new File("song.musicxml"));
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                int tempo = (Integer) tempoSpinner.getValue();
                MusicXmlGenerator.export(currentEvents, tempo, chooser.getSelectedFile());
                statusLabel.setText("MusicXML exported: " + chooser.getSelectedFile().getAbsolutePath());
            } catch (Exception ex) {
                showError(ex);
            }
        }
    }

    private void showError(Exception ex) {
        ex.printStackTrace();
        JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        statusLabel.setText("Error: " + ex.getMessage());
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MusicTextScannerApp().setVisible(true));
    }
}
