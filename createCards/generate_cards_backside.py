import subprocess
import sys
import os

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required packages are installed
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    install_package('Pillow')
    from PIL import Image, ImageDraw, ImageFont

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
except ImportError:
    install_package('reportlab')
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4


# Define DPI (dots per inch)
DPI = 300

# Conversion functions
def mm_to_pixels(mm):
    return int(mm * DPI / 25.4)

# Dimensions in millimeters
CARD_WIDTH_MM, CARD_HEIGHT_MM = 63.5, 88.9  # Typical playing card size
A4_WIDTH_MM, A4_HEIGHT_MM = 210, 297  # A4 size
SPACE_MM = 2  # Space between cards in millimeters

# Convert dimensions to pixels
CARD_WIDTH = mm_to_pixels(CARD_WIDTH_MM)
CARD_HEIGHT = mm_to_pixels(CARD_HEIGHT_MM)
A4_WIDTH = mm_to_pixels(A4_WIDTH_MM)
A4_HEIGHT = mm_to_pixels(A4_HEIGHT_MM)
SPACE = mm_to_pixels(SPACE_MM)

# Load font
def load_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Create a new image for a playing card
def create_card_image(qr_image_filename, card_number):
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), (36, 36, 36))
    draw = ImageDraw.Draw(card)

    font_size_number = 12  # Font size for the card number
    font_number = load_font(font_size_number)

    # Function to calculate text width and height
    def get_text_size(text, font):
        return draw.textlength(text, font=font), draw.textbbox((0, 0), text, font=font)[3]

    # Define dimensions for the square where the QR code will go
    qr_size = int(min(CARD_WIDTH, CARD_HEIGHT) * 0.6)  # Convert to integer
    qr_position = (int((CARD_WIDTH - qr_size) // 2), int((CARD_HEIGHT - qr_size) // 2))  # Convert to integer

    # Draw the QR code image on the card
    try:
        qr_image = Image.open(qr_image_filename)
        qr_image = qr_image.resize((qr_size, qr_size))  # Resize the QR image to fit
        card.paste(qr_image, qr_position)
    except FileNotFoundError:
        print(f"QR code image file {qr_image_filename} not found. QR code will not be added.")

        # Draw card number if provided
    if (card_number - 1) % 9 == 0:
        number_text = str(card_number)
        number_width, number_height = get_text_size(number_text, font_number)
        number_x = CARD_WIDTH - number_width - 10  # 10 pixels from right edge
        number_y = CARD_HEIGHT - number_height - 10  # 10 pixels from bottom edge
        draw.text((number_x, number_y), number_text, font=font_number, fill='black')

    # Save the card image
    return card

# Arrange cards on A4 sheets with spacing and multiple pages
def arrange_cards_on_a4(output_folder, qr_image_folder):
    # Load QR code image files
    qr_image_files = [f for f in os.listdir(qr_image_folder) if os.path.isfile(os.path.join(qr_image_folder, f))]
    if not qr_image_files:
        print("No QR code images found in the folder.")
        return

    # Determine the number of pages needed
    num_cards = len(qr_image_files)
    cards_per_page = int((A4_WIDTH + SPACE) / (CARD_WIDTH + SPACE)) * int((A4_HEIGHT + SPACE) / (CARD_HEIGHT + SPACE))
    num_pages = (num_cards + cards_per_page - 1) // cards_per_page

    # Generate each page
    for page_num in range(num_pages):
        output_pdf_filename = os.path.join(output_folder, f'playing_cards_page_{page_num + 1}.pdf')
        c = canvas.Canvas(output_pdf_filename, pagesize=(A4_WIDTH, A4_HEIGHT))

        # Calculate the range of cards for this page
        start_idx = page_num * cards_per_page
        end_idx = min(start_idx + cards_per_page, num_cards)
        cards_to_print = qr_image_files[start_idx:end_idx]

        # Determine the number of cards per row and column
        num_cols = int((A4_WIDTH + SPACE) / (CARD_WIDTH + SPACE))
        num_rows = int((A4_HEIGHT + SPACE) / (CARD_HEIGHT + SPACE))

        # Place cards in rows and columns on this page, starting from top-right
        for idx, qr_image_file in enumerate(cards_to_print):
            # Calculate row and column for right-to-left placement
            row = idx // num_cols
            col = idx % int(A4_WIDTH / (CARD_WIDTH + SPACE))
            
            # Calculate x and y coordinates for card placement
            
            x = int(A4_WIDTH - (col + 1) * CARD_WIDTH - col*SPACE)
            y = int(A4_HEIGHT - (row + 1) * CARD_HEIGHT  - row*SPACE)

            # Calculate card number for display
            card_number = start_idx + idx + 1
            
            # Create card image with QR code
            card_image = create_card_image(os.path.join(qr_image_folder, qr_image_file), card_number)
            
            # Draw the card image onto the canvas
            c.drawInlineImage(card_image, x, y, width=CARD_WIDTH, height=CARD_HEIGHT)

        # Save the PDF for this page
        c.save()
        print(f"Saved {output_pdf_filename}")

# Create a playing card image with QR code from a folder
def create_card_with_qr_image(qr_image_folder='qrcode_images_hitster_svenska_latar_v0'):
    output_folder = 'A4_backside_hitster_svenska_latar_v0'
    os.makedirs(output_folder, exist_ok=True)
    arrange_cards_on_a4(output_folder, qr_image_folder)

# Run the process
create_card_with_qr_image()

print("PDF created successfully.")