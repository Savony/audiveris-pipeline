import subprocess
import os
import sys

def run_audiveris(pdf_file, output_dir=None):
    print(f"PDF-Datei: {pdf_file}")
    print(f"Ausgabeverzeichnis: {output_dir}")

    if not os.path.exists(pdf_file):
        print(f"Die Datei '{pdf_file}' wurde nicht gefunden!")
        return

    if not os.path.isfile(pdf_file):
        print(f"'{pdf_file}' ist keine gültige Datei!")
        return

    if output_dir is None:
        output_dir = os.path.dirname(pdf_file)

    pdf_basename = os.path.splitext(os.path.basename(pdf_file))[0]
    output_file = os.path.join(output_dir, pdf_basename + ".omr")

    if os.path.exists(output_file):
        print(f"Die Ausgabedatei '{output_file}' existiert bereits. Konvertierung übersprungen.")
        return

    audiveris_command = [
        "flatpak", "run", "org.audiveris.audiveris", 
        "-batch", "-export", "-output", output_dir, pdf_file
    ]
    print(f"Befehl: {' '.join(audiveris_command)}")

    try:
        print(f"Konvertiere '{pdf_file}' ...")
        subprocess.run(audiveris_command, check=True)
        print(f"Konvertierung abgeschlossen! Die Ausgabedateien befinden sich im Ordner: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Ausführung von Audiveris: {e}")
    except Exception as e:
        print(f"Unbekannter Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("PDF-Datei als Argument angeben.")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    run_audiveris(pdf_file, output_dir)
