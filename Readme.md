# Voraussetzungen

Linux mit installiertem Flatpak Audiveris und Python 3.12.X
**Freigabe der gewünschten Eingabe- / Ausgabeordner an Flatpak Sandbox!**

## Skript

Anpassen der Ein und Ausgabeordner im Skript selbst.
Die beiden Dateien PDF2OMR und XML2CSV müssen sich im selben unterordner wie audiveris_converter befinden.

## Features

- Automatisierte Verarbeitung der PDF aus dem Eingabeordner durch Audiveris.
- Anhand der Dateien im Ausgabeverzeichnis wird erkannt ob die PDF bereits bearbeitet wurde und entsprechend übersprungen.
- Entpacken der erzeugten XML Dateien und Cleanup nicht weiter benötigter Dateien.
- Interpretation der von Audiveris erzeugten Dateien in Form einer CSV.
- Entfernung leerer CSV Dateien.

## Ausgabe
Als Ausgabe gibt es im Zielordner jeweils einen Unterordner der den Namen der PDF trägt und sowohl die OMR als auch Logs von Audiveris enthält. Im XML_Sheets Ordner befinden sich die aus der OMR extrahierten XML Datein. Im CSV Ordner befinden sich die entsprechenden Interpretationen der Daten.
