import csv
import os
import subprocess
import re


def find_pdfs(folder_path):
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


def convert_pdf_to_text(pdf_path, output_path):
    subprocess.run(['pdftotext', '-enc', 'UTF-8', pdf_path, output_path])


def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as file:
        text = file.read()
    return text


def find_sender_name_and_email(text):
    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    name_email_pattern = r'([\w\s\-\.\(\)]+)?\s*<(' + email_pattern + r')'

    message_pattern = r'message(?:\n|\s)'
    message_match = re.search(message_pattern, text)

    if message_match:
        text_after_message = text[message_match.end():]
        name_email_match = re.search(name_email_pattern, text_after_message)
        if name_email_match:
            name = name_email_match.group(1).strip() if name_email_match.group(1) else None
            email = name_email_match.group(2).strip() if name_email_match else None
            return name, email

    return None, None


def write_pairs_to_csv(pairs, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Count', 'Folder', 'Name', 'Email', 'Filename'])
        for i, pair in enumerate(pairs, start=1):
            csv_writer.writerow([i] + list(pair))


import re

def main(folder_path, output_file):
    pdf_files = find_pdfs(folder_path)
    all_pairs = []
    for pdf_file in pdf_files:
        txt_file = pdf_file.replace('.pdf', '.txt')
        convert_pdf_to_text(pdf_file, txt_file)
        text = extract_text_from_txt(txt_file)
        name, email = find_sender_name_and_email(text)
        relative_path = os.path.relpath(pdf_file, folder_path)
        folder_name = os.path.dirname(relative_path)
        folder_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', folder_name)  # Add a space between capitalized words
        filename = os.path.basename(pdf_file)
        if folder_name and (name and email):
            # Add the folder name before the name field
            all_pairs.append((folder_name, name, email, filename))
    # Sort the pairs by the name
    sorted_pairs = sorted(all_pairs, key=lambda x: x[1])
    write_pairs_to_csv(sorted_pairs, output_file)




if __name__ == '__main__':
    # Prompt user for input folder
    input_folder_path = input("Enter the path to the input folder: ")

    # Check if input path is a valid directory
    while not os.path.isdir(input_folder_path):
        print("Error: Input path is not a valid directory.")
        input_folder_path = input("Enter the path to the input folder: ")

    # Assume input folder is also the output folder
    output_file = 'output.csv'
    output_folder_path = input_folder_path

    # Call main function with input and output folder paths
    main(input_folder_path, os.path.join(output_folder_path, output_file))
