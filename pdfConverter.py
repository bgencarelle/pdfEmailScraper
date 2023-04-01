import os
import subprocess

def convert_pdf_to_ps(pdf_path, output_path):
    print("we're converting shit to PS!")
    subprocess.run(['pdftops', pdf_path, output_path])
    print("Now we're fucking done with PS!")

def convert_pdf_to_text(pdf_path, output_path):
    print("we're converting shit to TEXT!")
    subprocess.run(['pdftotext', pdf_path, output_path])
    print("Now we're fucking done with TEXT!")

def main(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, file_name)

            ps_output_path = os.path.join(output_folder, file_name.replace('.pdf', '.ps'))
            convert_pdf_to_ps(pdf_path, ps_output_path)

            txt_output_path = os.path.join(output_folder, file_name.replace('.pdf', '.txt'))
            convert_pdf_to_text(pdf_path, txt_output_path)

if __name__ == '__main__':
    input_folder = '/Users/main1/Library/CloudStorage/GoogleDrive-contact@bgencarelle.com/My Drive/anonKVFM/kustlerinnen/AndreasBecker/'
    output_folder = '/Users/main1/Desktop/'
    main(input_folder, output_folder)
