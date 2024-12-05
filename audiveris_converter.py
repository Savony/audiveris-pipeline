import os
import shutil
import subprocess
import zipfile
import csv

def process_files(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print(f"Eingabeordner '{input_folder}' existiert nicht.")
        return
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    current_dir = os.path.dirname(__file__)  # Pfad des aktuellen Skripts

    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)
        if not os.path.isfile(input_file_path):
            continue
        
        file_name, _ = os.path.splitext(file_name)
        output_file_path = os.path.join(output_folder, f"{file_name}")
        try:
            print(f"Verarbeite: {file_name}")
            subprocess.run(
                ["python", os.path.join(current_dir, "PDF2OMR.py"), input_file_path, output_file_path],
                check=True
            )
            print(f"Erfolgreich verarbeitet: {file_name}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Verarbeiten von {file_name}: {e}")


def clean_and_unpack(output_folder):
    if not os.path.exists(output_folder):
        print(f"Ausgabeordner '{output_folder}' existiert nicht.")
        return

    for root, dirs, files in os.walk(output_folder):
        if 'XML_Sheets' in dirs:
            dirs.remove('XML_Sheets')
        if 'CSV' in dirs:
            dirs.remove('CSV')

        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.endswith(".mxl"):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            elif file_name.endswith(".omr"):
                try:
                    folder_name = os.path.splitext(file_name)[0]
                    extract_path = os.path.join(root, folder_name)

                    if not os.path.exists(extract_path):
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            os.makedirs(extract_path, exist_ok=True) 
                            zip_ref.extractall(extract_path)
                            print(f"Entpackt: {file_path} nach {extract_path}")
                        
                        for sub_root, sub_dirs, sub_files in os.walk(extract_path):
                            for sub_file in sub_files:
                                if sub_file.endswith(".xml"):
                                    src_file_path = os.path.join(sub_root, sub_file)
                                    dest_file_path = os.path.join(root, sub_file)
                                    try:
                                        shutil.move(src_file_path, dest_file_path)
                                        print(f"Moved: {src_file_path} to {dest_file_path}")
                                    except Exception as e:
                                        print(f"Failed to move {src_file_path}: {e}")

                        shutil.rmtree(extract_path)
                    else:
                        print(f"Folder '{extract_path}' already exists, skipping extraction.")
                except zipfile.BadZipFile as e:
                    print(f"Failed to extract {file_path}: {e}")
            else:
                print(f"Skipped: {file_path}")

def process_extracted_files(folder):
    current_dir = os.path.dirname(__file__)  # Pfad des aktuellen Skripts

    for subdir, dirs, files in os.walk(folder):
        if subdir == folder:
            continue

        if subdir.endswith('XML_Sheets') or subdir.endswith('CSV'):
            continue  

        xml_sheets_folder = os.path.join(subdir, "XML_Sheets")
        csv_analysis_folder = os.path.join(subdir, "CSV")

        if os.path.exists(xml_sheets_folder) or os.path.exists(csv_analysis_folder):
            print(f"Skipped processing in {subdir} (folders already exist)")
            
            for file_name in files:
                if file_name.endswith(".xml"):
                    xml_file_path = os.path.join(subdir, file_name)
                    try:
                        os.remove(xml_file_path)
                        print(f"Deleted: {xml_file_path}")
                    except Exception as e:
                        print(f"Failed to delete {xml_file_path}: {e}")
            continue

        if not os.path.exists(xml_sheets_folder):
            os.makedirs(xml_sheets_folder)
            print(f"Created folder: {xml_sheets_folder}")

        if not os.path.exists(csv_analysis_folder):
            os.makedirs(csv_analysis_folder)
            print(f"Created folder: {csv_analysis_folder}")

        for file_name in files:
            if file_name.endswith(".xml"):
                xml_file_path = os.path.join(subdir, file_name)
                xml_dest_path = os.path.join(xml_sheets_folder, file_name)
                csv_file_name = f"{os.path.splitext(file_name)[0]}.csv"
                csv_file_path = os.path.join(csv_analysis_folder, csv_file_name)

                try:
                    shutil.move(xml_file_path, xml_dest_path)
                    print(f"Moved: {xml_file_path} to {xml_dest_path}")
                except Exception as e:
                    print(f"Failed to move {xml_file_path}: {e}")

                try:
                    print(f"Processing XML: {file_name}")
                    subprocess.run(
                        ["python", os.path.join(current_dir, "XML2CSV.py"), xml_dest_path, csv_file_path],
                        check=True
                    )
                    print(f"Successfully processed: {file_name} to {csv_file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {file_name}: {e}")


def csv_cleanup(output_folder):
    for root, dirs, files in os.walk(output_folder):
        if 'CSV' in dirs:
            csv_folder = os.path.join(root, 'CSV')  
            print(f"Cleaning CSV files in: {csv_folder}")

            for file_name in os.listdir(csv_folder):
                if file_name.endswith(".csv"):
                    file_path = os.path.join(csv_folder, file_name)

                    try:
                        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                            csv_reader = csv.reader(file)
                            rows = list(csv_reader)  
                            
                            
                            if len(rows) <= 1:  
                                os.remove(file_path)  
                                print(f"Deleted empty CSV file: {file_path}")
                            else:
                                data_found = False
                                for row in rows[1:]:  
                                    if any(row):  
                                        data_found = True
                                        break
                                if not data_found:
                                    os.remove(file_path)  
                                    print(f"Deleted CSV with no data: {file_path}")
                    except Exception as e:
                        print(f"Failed to read or process {file_path}: {e}")


if __name__ == "__main__":
    input_folder = "/home/jan/Notenblätter/"  # Eingabeordner
    output_folder = "/home/jan/Notenblätter_analyse/"  # Ausgabeordner
    
    process_files(input_folder, output_folder)
    
    clean_and_unpack(output_folder)

    process_extracted_files(output_folder)

    csv_cleanup(output_folder)
