import xml.etree.ElementTree as ET
import csv
import sys

def parse_music_notes(input_file, output_file):
    pitch_to_note = {
        "-7": "C", "-6": "C#", "-5": "D", "-4": "D#", "-3": "E", "-2": "F", "-1": "F#",
        "0": "G", "1": "G#", "2": "A", "3": "A#", "4": "B"
    }

    shape_to_unicode_codepoint = {
        "NOTEHEAD_BLACK": "U+266A",  # ♪
        "NOTEHEAD_VOID": "U+25CB",  # ○
        "NOTEHEAD_DOUBLEWHOLE": "U+1D15D",  # 𝅝
        "NOTEHEAD_HALF": "U+1D15E",  # 𝅗
        "NOTEHEAD_WHOLE": "U+1D15F",  # 𝅘
    }
    shape_to_duration = {
        "NOTEHEAD_BLACK": "Quarter Note",
        "NOTEHEAD_VOID": "Half Note",
        "NOTEHEAD_DOUBLEWHOLE": "Breve",
        "NOTEHEAD_HALF": "Half Note",
        "NOTEHEAD_WHOLE": "Whole Note",
    }

    tree = ET.parse(input_file)
    root = tree.getroot()

    notes_data = []
    for head in root.findall(".//head"):
        pitch = head.get("pitch")
        shape = head.get("shape")
        bounds = head.find("bounds").attrib if head.find("bounds") is not None else {}
        note_data = {
            "Note Name": pitch_to_note.get(pitch, "Unknown"),
            "Pitch (Numeric)": pitch,
            "Note Shape": shape,
            "Unicode": shape_to_unicode_codepoint.get(shape, "Unknown"),
            "Duration": shape_to_duration.get(shape, "Unknown"),
            "Glyph ID": head.get("glyph"),
            "Recognition Confidence": head.get("grade"),
            "X Position": bounds.get("x"),
            "Y Position": bounds.get("y"),
            "Width": bounds.get("w"),
            "Height": bounds.get("h"),
        }
        notes_data.append(note_data)

    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "Note Name", "Pitch (Numeric)", "Note Shape", "Unicode", "Duration",
                "Glyph ID", "Recognition Confidence", "X Position", "Y Position", "Width", "Height"
            ]
        )
        writer.writeheader()
        writer.writerows(notes_data)

    print(f"Die Daten wurden erfolgreich in '{output_file}' gespeichert.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Verwendung: python Skript.py <inputpath> <outputpath>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    parse_music_notes(input_path, output_path)


