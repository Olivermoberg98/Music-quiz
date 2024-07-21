import subprocess
import sys
import os

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import PyPDF2
except ImportError:
    install_package('PyPDF2')
    import PyPDF2

# Helper function to get the PDF filenames from a folder
def get_pdf_files(folder):
    return [f for f in os.listdir(folder) if f.endswith('.pdf')]

# Merge PDFs from the two folders
def merge_pdfs(frontside_folder, backside_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Get lists of PDFs from both folders
    frontside_pdfs = sorted(get_pdf_files(frontside_folder))
    backside_pdfs = sorted(get_pdf_files(backside_folder))

    # Check if both folders have the same number of PDFs
    if len(frontside_pdfs) != len(backside_pdfs):
        raise ValueError("The number of PDFs in the frontside and backside folders must be the same.")

    # Merge PDFs from the two folders
    for front_pdf, back_pdf in zip(frontside_pdfs, backside_pdfs):
        front_pdf_path = os.path.join(frontside_folder, front_pdf)
        back_pdf_path = os.path.join(backside_folder, back_pdf)
        output_pdf_path = os.path.join(output_folder, f'merged_{front_pdf}')

        # Create a PdfFileWriter object
        pdf_writer = PyPDF2.PdfWriter()

        # Append the first PDF (frontside)
        try:
            with open(front_pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
        except Exception as e:
            print(f"Error reading {front_pdf_path}: {e}")
            continue

        # Append the second PDF (backside)
        try:
            with open(back_pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
        except Exception as e:
            print(f"Error reading {back_pdf_path}: {e}")
            continue

        # Write the combined PDF to the output folder
        try:
            with open(output_pdf_path, 'wb') as f:
                pdf_writer.write(f)
            print(f"Merged {front_pdf} and {back_pdf} into {output_pdf_path}")
        except Exception as e:
            print(f"Error writing {output_pdf_path}: {e}")

    merge_all_pdfs(output_folder, os.path.join(output_folder, 'final_merged.pdf'))

# Function to merge all PDFs in a folder into a single PDF
def merge_all_pdfs(folder, output_path):
    pdf_writer = PyPDF2.PdfWriter()

    # Get a list of all PDF files in the folder
    pdf_files = sorted(get_pdf_files(folder))

    # Append each PDF to the writer object
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(folder, pdf_file)
        try:
            with open(pdf_file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
        except Exception as e:
            print(f"Error reading {pdf_file_path}: {e}")
            continue

    # Write the combined PDF to the specified output path
    try:
        with open(output_path, 'wb') as f:
            pdf_writer.write(f)
        print(f"All PDFs in {folder} have been merged into {output_path}")
    except Exception as e:
        print(f"Error writing {output_path}: {e}")



#if __name__ == '__main__':
    #merge_pdfs(frontside_folder, backside_folder, output_folder)
