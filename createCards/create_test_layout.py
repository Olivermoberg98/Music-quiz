import subprocess
import sys
import os
from PIL import Image, ImageDraw, ImageFont

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
SPACE_MM = 2  # Space between cards in millimeters

# Convert dimensions to pixels
A4_WIDTH = int(A4_WIDTH_MM * mm)
A4_HEIGHT = int(A4_HEIGHT_MM * mm)
CARD_WIDTH = mm_to_pixels(CARD_WIDTH_MM)
CARD_HEIGHT = mm_to_pixels(CARD_HEIGHT_MM)
SPACE = mm_to_pixels(SPACE_MM)

# Load font
def load_font(size):
    try:
        return ImageFont.truetype("FontsFree-Net-lucidity-condensed.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Wrap text to fit within a given width
def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        # Add a word to the current line and check its width
        test_line = f"{current_line} {word}".strip()
        width, _ = draw.textbbox((0, 0), test_line, font=font)[2:4]  # Get width from bounding box
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
            
    if current_line:
        lines.append(current_line)
        
    return lines

# Create a new image for a playing card
def create_card_image(song_name, release_year, artist, song_icon_path, artist_icon_path, card_number):
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), (255, 192, 203))  # Background color
    draw = ImageDraw.Draw(card)
    
    # Define font sizes
    font_size_artist = 55
    font_size_year = 140
    font_size_song = 55
    font_size_number = 12  # Font size for the card number
    font_artist = load_font(font_size_artist)
    font_year = load_font(font_size_year)
    font_song_name = load_font(font_size_song)
    font_number = load_font(font_size_number)

    # Load icons
    song_icon = Image.open(song_icon_path).convert("RGBA")
    artist_icon = Image.open(artist_icon_path).convert("RGBA")
    song_icon_size = 130
    artist_icon_size = 100
    song_icon = song_icon.resize((song_icon_size, song_icon_size))
    artist_icon = artist_icon.resize((artist_icon_size, artist_icon_size))
    
    # Define vertical positions for the text
    top_position = int(CARD_HEIGHT * 0.22)
    middle_position = int(CARD_HEIGHT * 0.5 - font_size_year / 2)
    bottom_position = int(CARD_HEIGHT * 0.8 - font_size_artist)
    
    # Wrap and draw Song Name
    song_lines = wrap_text(song_name, font_song_name, CARD_WIDTH - 70, draw)
    y_position = top_position
    for line in song_lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font_song_name)[2:4]
        draw.text(((CARD_WIDTH - text_width) // 2, y_position), line, font=font_song_name, fill=(245, 5, 85))
        y_position += text_height + 5  # 5px space between lines

    # Place the song icon
    card.paste(song_icon, ((CARD_WIDTH - song_icon_size) // 2, top_position - song_icon_size +10), song_icon)
    
    # Wrap and draw Release Year
    release_year_str = str(release_year)
    year_lines = wrap_text(release_year_str, font_year, CARD_WIDTH - 20, draw)
    y_position = middle_position
    for line in year_lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font_year)[2:4]
        draw.text(((CARD_WIDTH - text_width) // 2, y_position), line, font=font_year, fill=(245, 5, 85))
        y_position += text_height + 5
    
    # Wrap and draw Artist
    artist_lines = wrap_text(artist, font_artist, CARD_WIDTH - 70, draw)
    y_position = bottom_position
    for line in artist_lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font_artist)[2:4]
        draw.text(((CARD_WIDTH - text_width) // 2, y_position), line, font=font_artist, fill=(245, 5, 85))
        y_position += text_height + 5

    # Place the artist icon
    card.paste(artist_icon, ((CARD_WIDTH - artist_icon_size) // 2, bottom_position - artist_icon_size - 10), artist_icon)
    
    # Draw Card Number if provided
    if card_number is not None:
        number_text = str(card_number)
        number_width, number_height = draw.textbbox((0, 0), number_text, font=font_number)[2:4]
        number_x = CARD_WIDTH - number_width - 10  # 10 pixels from right edge
        number_y = CARD_HEIGHT - number_height - 10  # 10 pixels from bottom edge
        draw.text((number_x, number_y), number_text, font=font_number, fill='white')
    
    # Save the card image
    return card

# Generate and save a single card layout
def create_test_layout():
    # Sample data for testing
    song_name = "Här kommer alla känslorna"
    release_year = 1985
    artist = "London Symphony Orchestra"
    card_number = 1
    
    # Paths to icons
    song_icon_path = "song_icon.png"
    artist_icon_path = "artist_icon.png"

    # Create the card image
    card_image = create_card_image(song_name, release_year, artist, song_icon_path, artist_icon_path, card_number)
    
    # Save the image
    card_image_filename = 'test_card_layout.png'
    card_image.save(card_image_filename)
    print(f"Saved {card_image_filename}")

# Run the process
create_test_layout()
