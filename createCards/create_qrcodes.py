import os
import subprocess
import sys

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required packages are installed
try:
    import pandas as pd
except ImportError:
    install_package('pandas')
    import pandas as pd

try:
    import qrcode
except ImportError:
    install_package('qrcode')
    import qrcode

try:
    import openpyxl  # openpyxl is needed for pandas to read .xlsx files
except ImportError:
    install_package('openpyxl')
    import openpyxl

# Function to generate QR codes
def generate_qr_codes(excel_file, url_column, output_folder):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over the URLs in the specified column
    for index, url in enumerate(df[url_column]):
        # Create a QR code for the URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image of the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Format the filename with leading zeros
        filename = f'qrcode_{index + 1:03d}.png'
        file_path = os.path.join(output_folder, filename)

        # Save the image
        img.save(file_path)
        print(f'Saved {file_path}')

def create_qr_images(excel_file, output_folder):
    generate_qr_codes(excel_file, 'URL', output_folder)

#if __name__ == '__main__':
#    create_qr_images('Hitster_data_svenska_latar_v0.xlsx', 'qrcode_images_hitster_svenska_latar_v0')
