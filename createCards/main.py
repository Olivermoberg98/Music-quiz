import os
import get_spotify_track_data
import create_qrcodes
import generate_cards_frontside
import generate_cards_backside
import merge_PDFs

def main():
    playlist_url = 'https://open.spotify.com/playlist/4TJgT7TE9WbJHdk12kEJvt?si=a647bdd0697541fa'

    category = 'mixed'
    version = 'v0'

    # Base directory
    base_dir = f'{category}_{version}'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Subdirectories
    output_excel = os.path.join(base_dir, f'hitster_data_{category}_{version}.xlsx')
    qrcode_output_folder = os.path.join(base_dir, f'qrcode_images_hitster_{category}_{version}')
    frontside_output_folder = os.path.join(base_dir, f'frontside_images_hitster_{category}_{version}')
    backside_output_folder = os.path.join(base_dir, f'backside_images_hitster_{category}_{version}')
    merged_output_folder = os.path.join(base_dir, f'Merged_hitster_{category}_PDFs_{version}')

    # Create subdirectories if they don't exist
    os.makedirs(qrcode_output_folder, exist_ok=True)
    os.makedirs(frontside_output_folder, exist_ok=True)
    os.makedirs(backside_output_folder, exist_ok=True)
    os.makedirs(merged_output_folder, exist_ok=True)

    # Step 1: Fetch and save Spotify data
    get_spotify_track_data.fetch_and_save_spotify_data(playlist_url, output_excel)

    # Step 2: Create QR codes
    create_qrcodes.create_qr_images(output_excel, qrcode_output_folder)

    # Step 3: Generate frontside images for the cards
    generate_cards_frontside.generate_frontside_images(frontside_output_folder, output_excel)

    # Step 4: Generate frontside images for the cards
    generate_cards_backside.generate_backside_images(qrcode_output_folder, backside_output_folder)

    # Step 5: Merge PDFs
    merge_PDFs.merge_pdfs(frontside_output_folder, backside_output_folder,merged_output_folder)

if __name__ == '__main__':
    main()
