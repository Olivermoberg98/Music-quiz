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

try:
    import pandas as pd
except ImportError:
    install_package('pandas')
    import pandas as pd


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
def create_card_image(song_name, release_year, artist):
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), (36, 36, 36))
    draw = ImageDraw.Draw(card)
    
    # Define box dimensions and positions
    box_height = int(CARD_HEIGHT * 0.1)  # Smaller height
    box_width = int(CARD_WIDTH * 0.9)    # Slightly smaller width
    box_margin = 20
    font_size_artist = 20
    font_size_year = 40
    font_size_song = 20
    font_artist = load_font(font_size_artist)
    font_year = load_font(font_size_year)
    font_song_name = load_font(font_size_song)
    
    # Define vertical positions of the boxes
    top_position = int(CARD_HEIGHT * 0.2)
    middle_position = int(CARD_HEIGHT * 0.5 - box_height / 2)
    bottom_position = int(CARD_HEIGHT * 0.8 - box_height)
    
    # Function to calculate text width and height
    def get_text_size(text, font):
        return draw.textlength(text, font=font), draw.textbbox((0, 0), text, font=font)[3]

    # Draw three boxes with rounded edges
    def draw_rounded_rectangle(x, y, width, height, radius, fill):
        draw.rectangle([x + radius, y, x + width - radius, y + height], fill=fill)
        draw.rectangle([x, y + radius, x + width, y + height - radius], fill=fill)
        draw.ellipse([x, y, x + 2 * radius, y + 2 * radius], fill=fill)
        draw.ellipse([x + width - 2 * radius, y, x + width, y + 2 * radius], fill=fill)
        draw.ellipse([x, y + height - 2 * radius, x + 2 * radius, y + height], fill=fill)
        draw.ellipse([x + width - 2 * radius, y + height - 2 * radius, x + width, y + height], fill=fill)
    
    # Draw first box (Song Name)
    box_x = (CARD_WIDTH - box_width) // 2
    draw_rounded_rectangle(box_x, top_position, box_width, box_height, radius=10, fill=(255, 255, 255))
    text_width, text_height = get_text_size(song_name, font_song_name)
    draw.text((box_x + (box_width - text_width) // 2, top_position + (box_height - text_height) // 2), song_name, font=font_song_name, fill='black')

    # Draw second box (Release Year)
    release_year_str = str(release_year)  # Convert to string
    draw_rounded_rectangle(box_x, middle_position, box_width, box_height, radius=10, fill=(255, 255, 255))
    text_width, text_height = get_text_size(release_year_str, font_year)
    draw.text((box_x + (box_width - text_width) // 2, middle_position + (box_height - text_height) // 2), release_year_str, font=font_year, fill='black')

    # Draw third box (Artist)
    draw_rounded_rectangle(box_x, bottom_position, box_width, box_height, radius=10, fill=(255, 255, 255))
    text_width, text_height = get_text_size(artist, font_artist)
    draw.text((box_x + (box_width - text_width) // 2, bottom_position + (box_height - text_height) // 2), artist, font=font_artist, fill='black')
    
    # Save the card image
    return card



# Arrange cards on A4 sheets with spacing and multiple pages
def arrange_cards_on_a4(output_folder, data_file):
    # Read the data from Excel file
    df = pd.read_excel(data_file)

    # Determine the number of pages needed
    num_cards = len(df)
    cards_per_page = int((A4_WIDTH + SPACE) / (CARD_WIDTH + SPACE)) * int((A4_HEIGHT + SPACE) / (CARD_HEIGHT + SPACE))
    num_pages = (num_cards + cards_per_page - 1) // cards_per_page

    # Generate each page
    for page_num in range(num_pages):
        output_pdf_filename = os.path.join(output_folder, f'playing_cards_page_{page_num + 1}.pdf')
        c = canvas.Canvas(output_pdf_filename, pagesize=(A4_WIDTH, A4_HEIGHT))

        # Calculate the range of cards for this page
        start_idx = page_num * cards_per_page
        end_idx = min(start_idx + cards_per_page, num_cards)
        df_page = df.iloc[start_idx:end_idx]

        # Place cards in rows and columns on this page
        for i, row in enumerate(df_page.iterrows()):
            _, data = row
            song_name = data['Song Name']
            release_year = data['Album Release Year']
            artist = data['Artist']
            
            # Create the card image
            card_image = create_card_image(song_name, release_year, artist)
            
            col = i % int(A4_WIDTH / (CARD_WIDTH + SPACE))
            row = i // int(A4_WIDTH / (CARD_WIDTH + SPACE))
            x = int(col * (CARD_WIDTH + SPACE))
            y = int(A4_HEIGHT - (row + 1) * (CARD_HEIGHT + SPACE))
            
            # Draw the card image onto the canvas
            card_image = card_image.convert("RGB")
            c.drawInlineImage(card_image, x, y, width=CARD_WIDTH, height=CARD_HEIGHT)

        c.save()
        print(f"Saved {output_pdf_filename}")

# Create a playing card image from the data
def create_card_front_side():
    output_folder = 'A4_frontside_hitster_v0'
    os.makedirs(output_folder, exist_ok=True)
    data_file = 'Hitster_data_v0.xlsx'
    arrange_cards_on_a4(output_folder, data_file)

# Run the process
create_card_front_side()

print("PDF created successfully.")