import subprocess
import sys
import os
import math

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
    from reportlab.lib.units import mm
except ImportError:
    install_package('reportlab')
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm


# Define DPI (dots per inch)
DPI = 300

# Conversion functions
def mm_to_pixels(mm):
    return int(mm * DPI / 25.4)

# Dimensions in millimeters
CARD_WIDTH_MM, CARD_HEIGHT_MM = 63.5, 88.9  # Typical playing card size
A4_WIDTH_MM, A4_HEIGHT_MM = 210, 297  # A4 size
SPACE_MM = 1  # Space between cards in millimeters

# Convert dimensions to points
A4_WIDTH = int(A4_WIDTH_MM * mm)
A4_HEIGHT = int(A4_HEIGHT_MM * mm)
CARD_WIDTH = mm_to_pixels(CARD_WIDTH_MM)
CARD_HEIGHT = mm_to_pixels(CARD_HEIGHT_MM)
SPACE = mm_to_pixels(SPACE_MM)
CARD_WIDTH_POINTS = int(CARD_WIDTH_MM * mm)
CARD_HEIGHT_POINTS = int(CARD_HEIGHT_MM * mm)
SPACE_POINTS = math.floor(SPACE_MM * mm)


# Load font
def load_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()
    
# Create a rounded rectangle mask
def create_rounded_rectangle_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill=255)
    return mask

# Create a new image for a playing card
def create_card_image(qr_image_filename, card_number):
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), (255, 192, 203))
    draw = ImageDraw.Draw(card)

    font_size_number = 12  # Font size for the card number
    font_number = load_font(font_size_number)

    # Function to calculate text width and height
    def get_text_size(text, font):
        return draw.textlength(text, font=font), draw.textbbox((0, 0), text, font=font)[3]

    # Define dimensions for the square where the QR code will go
    qr_size = int(min(CARD_WIDTH, CARD_HEIGHT) * 0.6)
    qr_position = (int((CARD_WIDTH - qr_size) // 2), int((CARD_HEIGHT - qr_size) // 2))

    # Draw the QR code image on the card with rounded edges
    try:
        qr_image = Image.open(qr_image_filename).convert("RGBA")
        qr_image = qr_image.resize((qr_size, qr_size))

        # Create a mask with rounded edges
        radius = 20  # Radius for rounded corners
        mask = create_rounded_rectangle_mask((qr_size, qr_size), radius)

        # Create a new image for the QR code with rounded edges
        qr_image_with_rounded_corners = Image.new("RGBA", (qr_size, qr_size))
        qr_image_with_rounded_corners.paste(qr_image, (0, 0), mask)

        # Paste the rounded QR code onto the card
        card.paste(qr_image_with_rounded_corners, qr_position, qr_image_with_rounded_corners)
    except FileNotFoundError:
        print(f"QR code image file {qr_image_filename} not found. QR code will not be added.")


        # Draw card number if provided
    if (card_number - 1) % 9 == 0:
        number_text = str(card_number)
        number_width, number_height = get_text_size(number_text, font_number)
        number_x = CARD_WIDTH - number_width - 10  # 10 pixels from right edge
        number_y = CARD_HEIGHT - number_height - 10  # 10 pixels from bottom edge
        draw.text((number_x, number_y), number_text, font=font_number, fill='white')

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
    cards_per_page = int((A4_WIDTH + SPACE_POINTS) / (CARD_WIDTH_POINTS + SPACE_POINTS)) * int((A4_HEIGHT + SPACE_POINTS) / (CARD_HEIGHT_POINTS + SPACE_POINTS))
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
        num_cols = int((A4_WIDTH + SPACE_POINTS) / (CARD_WIDTH_POINTS + SPACE_POINTS))
        num_rows = int((A4_HEIGHT + SPACE_POINTS) / (CARD_HEIGHT_POINTS + SPACE_POINTS))

        # Place cards in rows and columns on this page, starting from top-right
        for idx, qr_image_file in enumerate(cards_to_print):
            # Calculate row and column for right-to-left placement
            row = idx // num_cols
            col = idx % int(A4_WIDTH / (CARD_WIDTH_POINTS + SPACE_POINTS))
            
            # Calculate x and y coordinates for card placement
            x = int(A4_WIDTH - (col + 1) * CARD_WIDTH_POINTS - col*SPACE_POINTS)
            y = int(A4_HEIGHT - (row + 1) * CARD_HEIGHT_POINTS  - row*SPACE_POINTS)

            # Calculate card number for display
            card_number = start_idx + idx + 1
            
            # Create card image with QR code
            card_image = create_card_image(os.path.join(qr_image_folder, qr_image_file), card_number)
            
            # Draw the card image onto the canvas
            c.drawInlineImage(card_image, x, y, width=CARD_WIDTH_POINTS, height=CARD_HEIGHT_POINTS)

        # Save the PDF for this page
        c.save()
        print(f"Saved {output_pdf_filename}")

# Create a playing card image with QR code from a folder
def generate_backside_images(qr_image_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    arrange_cards_on_a4(output_folder, qr_image_folder)

#if __name__ == '__main__':
#    generate_backside_images('qrcode_images_hitster_svenska_latar_v0', 'A4_backside_hitster_svenska_latar_v0')