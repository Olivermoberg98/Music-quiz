import json
import csv
import os
from dataclasses import dataclass
from typing import List, Optional
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    SPOTIPY_AVAILABLE = True
except ImportError:
    SPOTIPY_AVAILABLE = False
    print("⚠️  Spotipy not installed. Run 'pip install spotipy' to enable Spotify integration.")

@dataclass
class Song:
    country: str
    artist: str
    title: str
    year: int
    language: str
    
    def __str__(self):
        return f"{self.country}: {self.artist} - {self.title} ({self.year})"

# World Music Playlist - One Song Per Country (195 Countries)
world_playlist = [
    # A
    Song("Afghanistan", "Ahmad Zahir", "Kamar Bareek-e-Man", 1970, "Dari"),
    Song("Albania", "Vaçe Zela", "Kënga ime", 1962, "Albanian"),
    Song("Algeria", "Cheb Khaled", "Didi", 1992, "Arabic"),
    Song("Andorra", "Marta Roure", "La teva decisió", 2017, "Catalan"),
    Song("Angola", "Bonga", "Mona Ki Ngi Xica", 1972, "Portuguese"),
    Song("Antigua and Barbuda", "Burning Flames", "Workey Workey", 1995, "English"),
    Song("Argentina", "Carlos Gardel", "Por una Cabeza", 1935, "Spanish"),
    Song("Armenia", "Aram Khachaturian", "Sabre Dance", 1942, "Instrumental"),
    Song("Australia", "Men at Work", "Down Under", 1981, "English"),
    Song("Austria", "Falco", "Rock Me Amadeus", 1985, "German/English"),
    Song("Azerbaijan", "Rashid Behbudov", "Gül açdı", 1958, "Azerbaijani"),
    
    # B
    Song("Bahamas", "Baha Men", "Who Let the Dogs Out", 2000, "English"),
    Song("Bahrain", "Khaled Al Sheikh", "Ya Msafer", 1980, "Arabic"),
    Song("Bangladesh", "Runa Laila", "Chokher Bali", 1974, "Bengali"),
    Song("Barbados", "Rihanna", "Umbrella", 2007, "English"),
    Song("Belarus", "Pesnyary", "Vologda", 1975, "Russian"),
    Song("Belgium", "Jacques Brel", "Ne me quitte pas", 1959, "French"),
    Song("Belize", "Shyne", "Bad Boyz", 2000, "English"),
    Song("Benin", "Angélique Kidjo", "Agolo", 1994, "Fon"),
    Song("Bhutan", "Shera Lhendup", "Druk Tsendhen", 1953, "Dzongkha"),
    Song("Bolivia", "Los Kjarkas", "Llorando se fue", 1982, "Spanish"),
    Song("Bosnia and Herzegovina", "Goran Bregović", "Mesečina", 1987, "Serbian"),
    Song("Botswana", "Franco & Afro Musica", "Pelo", 1995, "Setswana"),
    Song("Brazil", "Antônio Carlos Jobim", "The Girl from Ipanema", 1964, "Portuguese"),
    Song("Brunei", "Anita Sarawak", "Gemilang", 1985, "Malay"),
    Song("Bulgaria", "Lili Ivanova", "Vetăr", 1974, "Bulgarian"),
    Song("Burkina Faso", "Amadou & Mariam", "Senegal Fast Food", 2004, "French"),
    Song("Burundi", "Jean-Pierre Nimbona", "Burundi Bwacu", 1962, "Kirundi"),
    
    # C
    Song("Cambodia", "Sinn Sisamouth", "Champa Battambang", 1965, "Khmer"),
    Song("Cameroon", "Manu Dibango", "Soul Makossa", 1972, "French/Duala"),
    Song("Canada", "Leonard Cohen", "Hallelujah", 1984, "English"),
    Song("Cape Verde", "Cesária Évora", "Sodade", 1992, "Cape Verdean Creole"),
    Song("Central African Republic", "Zokela", "Sango", 1980, "Sango"),
    Song("Chad", "Clément Masdongar", "N'Djamena", 1975, "French"),
    Song("Chile", "Violeta Parra", "Gracias a la Vida", 1966, "Spanish"),
    Song("China", "Teresa Teng", "Yue Liang Dai Biao Wo De Xin", 1977, "Mandarin"),
    Song("Colombia", "Shakira", "Hips Don't Lie", 2006, "English/Spanish"),
    Song("Comoros", "Maalesh", "Hadiya", 1985, "Comorian"),
    Song("Congo (Brazzaville)", "Papa Wemba", "Maria Valencia", 1988, "French/Lingala"),
    Song("Congo (Kinshasa)", "Franco Luambo", "Mario", 1985, "Lingala"),
    Song("Costa Rica", "Éditus", "Delirios", 1999, "Spanish"),
    Song("Croatia", "Oliver Dragojević", "Cesarica", 1967, "Croatian"),
    Song("Cuba", "Compay Segundo", "Chan Chan", 1997, "Spanish"),
    Song("Cyprus", "Anna Vissi", "Autostop", 1981, "Greek"),
    Song("Czech Republic", "Karel Gott", "Biene Maja", 1976, "Czech"),
    
    # D
    Song("Denmark", "Aqua", "Barbie Girl", 1997, "English"),
    Song("Djibouti", "Groupe RTD", "Djibouti", 1977, "French"),
    Song("Dominica", "Exile One", "Hit Me With Music", 1975, "English"),
    Song("Dominican Republic", "Juan Luis Guerra", "Burbujas de Amor", 1990, "Spanish"),
    
    # E
    Song("East Timor", "Ego Lemos", "Balibo", 2009, "Tetum"),
    Song("Ecuador", "Julio Jaramillo", "Nuestro Juramento", 1957, "Spanish"),
    Song("Egypt", "Umm Kulthum", "Alf Leila wa Leila", 1969, "Arabic"),
    Song("El Salvador", "Álvaro Torres", "Hazme Olvidarla", 1991, "Spanish"),
    Song("Equatorial Guinea", "Malabo Strit Band", "África", 1980, "Spanish"),
    Song("Eritrea", "Bereket Mengisteab", "Hawey", 1991, "Tigrinya"),
    Song("Estonia", "Ruja", "Ei ole üksi ükski maa", 1981, "Estonian"),
    Song("Eswatini", "Busi Mhlongo", "Yehlisan uMoya", 1991, "Swazi"),
    Song("Ethiopia", "Mahmoud Ahmed", "Ere Mela Mela", 1975, "Amharic"),
    
    # F
    Song("Fiji", "Black Rose", "Domo", 1995, "Fijian"),
    Song("Finland", "Sibelius", "Finlandia", 1899, "Instrumental"),
    Song("France", "Édith Piaf", "La Vie en Rose", 1947, "French"),
    
    # G
    Song("Gabon", "Pierre Akendengué", "Réveil", 1974, "French"),
    Song("Gambia", "Jaliba Kuyateh", "Foday Musa Suso", 1988, "Mandinka"),
    Song("Georgia", "Hamlet Gonashvili", "Chela", 1970, "Georgian"),
    Song("Germany", "Nena", "99 Luftballons", 1983, "German"),
    Song("Ghana", "Nana Ampadu", "Ebi Te Yie", 1967, "Twi"),
    Song("Greece", "Mikis Theodorakis", "Zorba the Greek", 1964, "Greek"),
    Song("Grenada", "Mighty Sparrow", "Carnival", 1956, "English"),
    Song("Guatemala", "Paco Pérez", "Luna de Xelajú", 1944, "Spanish"),
    Song("Guinea", "Bembeya Jazz", "Regard", 1971, "French"),
    Song("Guinea-Bissau", "Dulce Pontes", "Lágrima", 1991, "Portuguese"),
    Song("Guyana", "Eddy Grant", "Electric Avenue", 1983, "English"),
    
    # H
    Song("Haiti", "Tabou Combo", "New York City", 1975, "French Creole"),
    Song("Honduras", "Polache", "Sopa de Caracol", 1991, "Spanish"),
    Song("Hungary", "Márta Sebestyén", "Szívemben", 1989, "Hungarian"),
    
    # I
    Song("Iceland", "Björk", "Human Behaviour", 1993, "English"),
    Song("India", "Lata Mangeshkar", "Lag Jaa Gale", 1964, "Hindi"),
    Song("Indonesia", "Rhoma Irama", "Begadang", 1973, "Indonesian"),
    Song("Iran", "Googoosh", "Gharibeh Ashena", 1975, "Persian"),
    Song("Iraq", "Nazem Al-Ghazali", "Fog el Nakhal", 1955, "Arabic"),
    Song("Ireland", "U2", "Sunday Bloody Sunday", 1983, "English"),
    Song("Israel", "Ofra Haza", "Im Nin'Alu", 1984, "Hebrew"),
    Song("Italy", "Domenico Modugno", "Volare", 1958, "Italian"),
    Song("Ivory Coast", "Alpha Blondy", "Brigadier Sabari", 1982, "French"),
    
    # J
    Song("Jamaica", "Bob Marley", "No Woman No Cry", 1974, "English"),
    Song("Japan", "Sukiyaki", "Ue o Muite Arukō", 1961, "Japanese"),
    Song("Jordan", "Mohammed Abdel Wahab", "Ya Msafer", 1960, "Arabic"),
    
    # K
    Song("Kazakhstan", "Rosa Rymbayeva", "Amanat", 1978, "Kazakh"),
    Song("Kenya", "Them Mushrooms", "Jambo Bwana", 1982, "Swahili"),
    Song("Kiribati", "Kiribati String Band", "Teirake", 1980, "Gilbertese"),
    Song("Kuwait", "Nawal Al Kuwaitia", "Mathkoursh", 1984, "Arabic"),
    Song("Kyrgyzstan", "Gulnara Nazaralieva", "Kyrgyzstan", 1991, "Kyrgyz"),
    
    # L
    Song("Laos", "Sayan Sanya", "Lam Saravane", 1975, "Lao"),
    Song("Latvia", "Prāta Vētra", "Ziema", 2000, "Latvian"),
    Song("Lebanon", "Fairuz", "Li Beirut", 1984, "Arabic"),
    Song("Lesotho", "Tau ea Matseka", "Lesotho Fatše La Bo-Ntat'a Rona", 1967, "Sesotho"),
    Song("Liberia", "Miatta Fahnbulleh", "Liberia", 1960, "English"),
    Song("Libya", "Ahmed Fakroun", "Soleil", 1988, "Arabic"),
    Song("Liechtenstein", "Marco Fritsche", "Liechtensteiner Polka", 1962, "German"),
    Song("Lithuania", "Antis", "Zombiai", 1989, "Lithuanian"),
    Song("Luxembourg", "Vicky Leandros", "Après toi", 1972, "French"),
    
    # M
    Song("Madagascar", "Mahaleo", "Mila Ho Avy", 1975, "Malagasy"),
    Song("Malawi", "Daniel Kachamba", "Panado", 1980, "Chichewa"),
    Song("Malaysia", "Siti Nurhaliza", "Isabella", 1999, "Malay"),
    Song("Maldives", "Naifaru Seena", "Maldives", 1985, "Dhivehi"),
    Song("Mali", "Salif Keita", "Soro", 1987, "Bambara"),
    Song("Malta", "Ira Losco", "7th Wonder", 2016, "English"),
    Song("Marshall Islands", "Jebro", "Yokwe", 1990, "Marshallese"),
    Song("Mauritania", "Dimi Mint Abba", "Habibi", 1980, "Arabic"),
    Song("Mauritius", "Kaya", "Seggae Music", 1990, "Creole"),
    Song("Mexico", "Pedro Infante", "Cielito Lindo", 1947, "Spanish"),
    Song("Micronesia", "Saimon Peter", "Pohnpei", 1995, "Pohnpeian"),
    Song("Moldova", "Zdob și Zdub", "Hora din Moldova", 2005, "Romanian"),
    Song("Monaco", "Céline Dion", "Ne partez pas sans moi", 1988, "French"),
    Song("Mongolia", "Baatarjav", "Mongol Ulsyn Töriin Duulal", 1961, "Mongolian"),
    Song("Montenegro", "Zdravko Čolić", "Ti Si Mi U Krvi", 1976, "Montenegrin"),
    Song("Morocco", "Nass El Ghiwane", "Ya Sah", 1970, "Arabic"),
    Song("Mozambique", "Marrabenta Star", "Xitende", 1980, "Portuguese"),
    Song("Myanmar", "Sai Htee Saing", "Thingyan", 1970, "Burmese"),
    
    # N
    Song("Namibia", "Jackson Kaujeua", "Namibia", 1990, "English"),
    Song("Nauru", "Nauru String Band", "Nauru Bwiema", 1968, "Nauruan"),
    Song("Nepal", "Narayan Gopal", "Euta Manche", 1974, "Nepali"),
    Song("Netherlands", "Golden Earring", "Radar Love", 1973, "English"),
    Song("New Zealand", "Crowded House", "Don't Dream It's Over", 1986, "English"),
    Song("Nicaragua", "Carlos Mejía Godoy", "Nicaragua, Nicaragüita", 1980, "Spanish"),
    Song("Niger", "Mamar Kassey", "Yaral Sa Doom", 1999, "Hausa"),
    Song("Nigeria", "Fela Kuti", "Zombie", 1976, "English/Yoruba"),
    Song("North Korea", "Pochonbo Electronic Ensemble", "Arirang", 1989, "Korean"),
    Song("North Macedonia", "Toše Proeski", "Čija Si", 2003, "Macedonian"),
    Song("Norway", "a-ha", "Take On Me", 1985, "English"),
    
    # O
    Song("Oman", "Salim Rashid Suri", "Ya Msafer", 1975, "Arabic"),
    
    # P
    Song("Pakistan", "Nusrat Fateh Ali Khan", "Allah Hoo", 1992, "Urdu"),
    Song("Palau", "Yano", "Mechesil Belau", 1980, "Palauan"),
    Song("Panama", "Rubén Blades", "Pedro Navaja", 1978, "Spanish"),
    Song("Papua New Guinea", "Telek", "Serious Tam", 1997, "Tok Pisin"),
    Song("Paraguay", "José Asunción Flores", "India", 1928, "Spanish"),
    Song("Peru", "Chabuca Granda", "La Flor de la Canela", 1950, "Spanish"),
    Song("Philippines", "Freddie Aguilar", "Anak", 1978, "Tagalog"),
    Song("Poland", "Czesław Niemen", "Dziwny Jest Ten Świat", 1967, "Polish"),
    Song("Portugal", "Amália Rodrigues", "Lágrima", 1955, "Portuguese"),
    
    # Q
    Song("Qatar", "Mohammed Abdel Wahab", "Qatar", 1971, "Arabic"),
    
    # R
    Song("Romania", "Maria Tănase", "Ciocârlia", 1950, "Romanian"),
    Song("Russia", "Kalinka", "Kalinka", 1860, "Russian"),
    Song("Rwanda", "Intore", "Rwanda Nziza", 1962, "Kinyarwanda"),
    
    # S
    Song("Saint Kitts and Nevis", "Small Axe", "Sugar Mas", 1985, "English"),
    Song("Saint Lucia", "Tru Tones", "Creole", 1990, "English/Creole"),
    Song("Saint Vincent and the Grenadines", "Becket", "Vincy", 1979, "English"),
    Song("Samoa", "Five Stars", "Samoa", 1985, "Samoan"),
    Song("San Marino", "Little Tony", "Cuore Matto", 1967, "Italian"),
    Song("São Tomé and Príncipe", "Africa Negra", "Muadiê", 1985, "Portuguese"),
    Song("Saudi Arabia", "Mohammed Abdo", "Al Amaken", 1981, "Arabic"),
    Song("Senegal", "Youssou N'Dour", "7 Seconds", 1994, "French/English"),
    Song("Serbia", "Đorđe Balašević", "Priča o Vasi Ladačkom", 1983, "Serbian"),
    Song("Seychelles", "Patrick Victor", "Seychelles", 1976, "Creole"),
    Song("Sierra Leone", "Ebenezer Calendar", "Gbagba", 1980, "Krio"),
    Song("Singapore", "Dick Lee", "Fried Rice Paradise", 1989, "English"),
    Song("Slovakia", "Elán", "Amnestia", 1990, "Slovak"),
    Song("Slovenia", "Laibach", "Opus Dei", 1987, "Slovenian"),
    Song("Solomon Islands", "Narasirato", "Aelan Mama", 1988, "English"),
    Song("Somalia", "Maryam Mursal", "Somali", 1991, "Somali"),
    Song("South Africa", "Miriam Makeba", "Pata Pata", 1967, "Xhosa"),
    Song("South Korea", "Cho Yong-pil", "Return to Busan Port", 1976, "Korean"),
    Song("South Sudan", "Emmanuel Jal", "Gua", 2005, "English"),
    Song("Spain", "Paco de Lucía", "Entre Dos Aguas", 1973, "Instrumental"),
    Song("Sri Lanka", "W.D. Amaradeva", "Sasara Wasana Thuru", 1967, "Sinhala"),
    Song("Sudan", "Mohammed Wardi", "Ya Ard-i", 1972, "Arabic"),
    Song("Suriname", "Lieve Hugo", "Kon Tiki", 1961, "Dutch"),
    Song("Sweden", "ABBA", "Dancing Queen", 1976, "English"),
    Song("Switzerland", "DJ BoBo", "Chihuahua", 2002, "English"),
    Song("Syria", "Fairuz", "Habaytak Bissayf", 1960, "Arabic"),
    
    # T
    Song("Taiwan", "Teresa Teng", "Tian Mi Mi", 1979, "Mandarin"),
    Song("Tajikistan", "Barno Iskhakova", "Tajikistan", 1991, "Tajik"),
    Song("Tanzania", "Remmy Ongala", "Mambo", 1992, "Swahili"),
    Song("Thailand", "Carabao", "Made in Thailand", 1984, "Thai"),
    Song("Togo", "Bella Bellow", "Rockia", 1973, "French"),
    Song("Tonga", "Taumalolo", "Tonga", 1970, "Tongan"),
    Song("Trinidad and Tobago", "Lord Kitchener", "London Is the Place for Me", 1948, "English"),
    Song("Tunisia", "Anouar Brahem", "Le Pas du Chat Noir", 2002, "Instrumental"),
    Song("Turkey", "Sezen Aksu", "Şarkı Söylemek Lazım", 1987, "Turkish"),
    Song("Turkmenistan", "Ashir Orazow", "Turkmenistan", 1991, "Turkmen"),
    Song("Tuvalu", "Tuvalu String Band", "Tuvalu", 1978, "Tuvaluan"),
    
    # U
    Song("Uganda", "Philly Lutaaya", "Born in Africa", 1987, "English"),
    Song("Ukraine", "Okean Elzy", "Vesna", 2000, "Ukrainian"),
    Song("United Arab Emirates", "Hussain Al Jassmi", "Boshret Kheir", 2012, "Arabic"),
    Song("United Kingdom", "The Beatles", "Hey Jude", 1968, "English"),
    Song("United States", "Elvis Presley", "Hound Dog", 1956, "English"),
    Song("Uruguay", "Alfredo Zitarrosa", "Milonga para una Niña", 1965, "Spanish"),
    Song("Uzbekistan", "Yulduz Usmanova", "Uzbekistan", 1991, "Uzbek"),
    
    # V
    Song("Vanuatu", "Vanessa Quai", "Vanuatu", 1980, "Bislama"),
    Song("Vatican City", "Sistine Chapel Choir", "Ave Maria", 1950, "Latin"),
    Song("Venezuela", "Simón Díaz", "Caballo Viejo", 1978, "Spanish"),
    Song("Vietnam", "Trịnh Công Sơn", "Diễm Xưa", 1967, "Vietnamese"),
    
    # Y
    Song("Yemen", "Ahmed Fathi", "Yemen", 1990, "Arabic"),
    
    # Z
    Song("Zambia", "Amayenge", "Bana", 1987, "English"),
    Song("Zimbabwe", "Oliver Mtukudzi", "Todii", 1999, "Shona")
]

def print_playlist():
    """Print the complete playlist"""
    print("🌍 WORLD MUSIC PLAYLIST - ONE SONG FROM EACH COUNTRY 🌍")
    print("=" * 70)
    
    for i, song in enumerate(world_playlist, 1):
        print(f"{i:3d}. {song}")
    
    print(f"\nTotal Songs: {len(world_playlist)}")

def export_to_csv(filename="world_music_playlist.csv"):
    """Export playlist to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['#', 'Country', 'Artist', 'Title', 'Year', 'Language'])
        
        for i, song in enumerate(world_playlist, 1):
            writer.writerow([i, song.country, song.artist, song.title, song.year, song.language])
    
    print(f"Playlist exported to {filename}")

def export_to_json(filename="world_music_playlist.json"):
    """Export playlist to JSON file"""
    playlist_data = []
    for i, song in enumerate(world_playlist, 1):
        playlist_data.append({
            'number': i,
            'country': song.country,
            'artist': song.artist,
            'title': song.title,
            'year': song.year,
            'language': song.language
        })
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(playlist_data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Playlist exported to {filename}")

def search_by_country(country_name):
    """Search for a song by country name"""
    matches = [song for song in world_playlist if country_name.lower() in song.country.lower()]
    
    if matches:
        print(f"\nFound {len(matches)} result(s) for '{country_name}':")
        for song in matches:
            print(f"  {song}")
    else:
        print(f"No songs found for '{country_name}'")

def search_by_decade(decade):
    """Search for songs by decade (e.g., 1960, 1970, etc.)"""
    matches = [song for song in world_playlist if decade <= song.year < decade + 10]
    
    if matches:
        print(f"\nFound {len(matches)} song(s) from the {decade}s:")
        for song in sorted(matches, key=lambda x: x.year):
            print(f"  {song}")
    else:
        print(f"No songs found from the {decade}s")

def get_statistics():
    """Get statistics about the playlist"""
    decades = {}
    languages = {}
    
    for song in world_playlist:
        # Count by decade
        decade = (song.year // 10) * 10
        decades[decade] = decades.get(decade, 0) + 1
        
        # Count by language
        languages[song.language] = languages.get(song.language, 0) + 1
    
    print("\n📊 PLAYLIST STATISTICS 📊")
    print("=" * 40)
    
    print("\nSongs by Decade:")
    for decade in sorted(decades.keys()):
        print(f"  {decade}s: {decades[decade]} songs")
    
    print(f"\nSongs by Language (Top 10):")
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    for lang, count in sorted_languages[:10]:
        print(f"  {lang}: {count} songs")
    
    print(f"\nTotal Languages: {len(languages)}")
    print(f"Total Countries: {len(world_playlist)}")

def create_spotify_playlist_format():
    """Create a format suitable for Spotify playlist creation"""
    print("\n🎵 SPOTIFY PLAYLIST FORMAT 🎵")
    print("=" * 50)
    print("Copy and paste these search terms into Spotify:\n")
    
    for i, song in enumerate(world_playlist, 1):
        search_term = f'"{song.title}" "{song.artist}"'
        print(f"{i:3d}. {search_term}")

def setup_spotify_credentials():
    """
    Setup instructions for Spotify API credentials
    """
    print("\n🎵 SPOTIFY API SETUP INSTRUCTIONS 🎵")
    print("=" * 50)
    print("To create playlists programmatically, you need to:")
    print("1. Go to https://developer.spotify.com/dashboard")
    print("2. Click on your existing app (or create a new one)")
    print("3. Click 'Edit Settings'")
    print("4. In 'Redirect URIs', ADD this URL:")
    print("   http://localhost:8888/callback")
    print("   (Keep your existing musikquiz://callback if you want)")
    print("5. Click 'Save'")
    print("6. Get your Client ID and Client Secret from the app page")
    print("7. Set environment variables:")
    print("   SPOTIPY_CLIENT_ID=your_client_id")
    print("   SPOTIPY_CLIENT_SECRET=your_client_secret")
    print("   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback")
    print("\n📝 Alternative: Create a .env file with:")
    print("   SPOTIPY_CLIENT_ID=your_client_id_here")
    print("   SPOTIPY_CLIENT_SECRET=your_client_secret_here")
    print("   SPOTIPY_REDIRECT_URI=http://localhost:8888/callback")
    print("\n⚠️  Important: You need the localhost redirect URI for this script!")
    print("   Your musikquiz://callback is for mobile apps, not Python scripts.")
    print("=" * 50)

def create_spotify_playlist(playlist_name="World Music - 195 Countries", 
                          description="One iconic song from each country in the world", 
                          public=True):
    """
    Create an actual Spotify playlist with the world music collection
    """
    if not SPOTIPY_AVAILABLE:
        print("❌ Spotipy library not installed. Run: pip install spotipy")
        return None
    
    # Check for credentials
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')
    
    if not client_id or not client_secret:
        print("❌ Spotify credentials not found!")
        setup_spotify_credentials()
        return None
    
    try:
        # Set up authentication
        scope = "playlist-modify-public playlist-modify-private"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        ))
        
        # Get current user
        user = sp.current_user()
        user_id = user['id']
        print(f"✅ Authenticated as: {user['display_name']}")
        
        # Create playlist
        playlist = sp.user_playlist_create(
            user_id, 
            playlist_name, 
            public=public, 
            description=description
        )
        
        print(f"✅ Created playlist: {playlist['name']}")
        print(f"🔗 Playlist URL: {playlist['external_urls']['spotify']}")
        
        # Search for and add tracks
        track_uris = []
        not_found = []
        
        print("\n🔍 Searching for tracks...")
        for i, song in enumerate(world_playlist, 1):
            # Try multiple search queries
            search_queries = [
                f'"{song.title}" "{song.artist}"',
                f'{song.title} {song.artist}',
                f'track:"{song.title}" artist:"{song.artist}"',
                f'{song.title}'  # Last resort
            ]
            
            track_uri = None
            for query in search_queries:
                results = sp.search(q=query, type='track', limit=10)
                
                if results['tracks']['items']:
                    # Find best match
                    for track in results['tracks']['items']:
                        if (song.artist.lower() in track['artists'][0]['name'].lower() or
                            track['artists'][0]['name'].lower() in song.artist.lower()):
                            track_uri = track['uri']
                            break
                    
                    if not track_uri:
                        # Take first result if no exact artist match
                        track_uri = results['tracks']['items'][0]['uri']
                    break
            
            if track_uri:
                track_uris.append(track_uri)
                print(f"✅ {i:3d}. Found: {song.country} - {song.title}")
            else:
                not_found.append(song)
                print(f"❌ {i:3d}. Not found: {song.country} - {song.title}")
        
        # Add tracks to playlist in batches (Spotify limit: 100 tracks per request)
        if track_uris:
            batch_size = 100
            for i in range(0, len(track_uris), batch_size):
                batch = track_uris[i:i + batch_size]
                sp.playlist_add_items(playlist['id'], batch)
            
            print(f"\n✅ Added {len(track_uris)} tracks to playlist!")
        
        # Report not found tracks
        if not_found:
            print(f"\n⚠️  {len(not_found)} tracks not found:")
            for song in not_found:
                print(f"   - {song.country}: {song.artist} - {song.title}")
            
            # Save not found tracks to file
            with open('not_found_tracks.txt', 'w', encoding='utf-8') as f:
                f.write("Tracks not found on Spotify:\n")
                f.write("=" * 40 + "\n")
                for song in not_found:
                    f.write(f"{song.country}: {song.artist} - {song.title} ({song.year})\n")
            print("   📄 Saved to 'not_found_tracks.txt'")
        
        return playlist
        
    except Exception as e:
        print(f"❌ Error creating playlist: {e}")
        return None

def search_and_preview_spotify_matches(limit=10):
    """
    Search for tracks on Spotify and preview matches without creating playlist
    """
    if not SPOTIPY_AVAILABLE:
        print("❌ Spotipy library not installed. Run: pip install spotipy")
        return
    
    # Check for credentials
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')
    
    if not client_id or not client_secret:
        print("❌ Spotify credentials not found!")
        setup_spotify_credentials()
        return
    
    try:
        # Set up authentication (no special scopes needed for search)
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-library-read"
        ))
        
        print(f"\n🔍 SPOTIFY SEARCH PREVIEW (First {limit} songs)")
        print("=" * 60)
        
        for i, song in enumerate(world_playlist[:limit], 1):
            query = f'"{song.title}" "{song.artist}"'
            results = sp.search(q=query, type='track', limit=3)
            
            print(f"\n{i:2d}. {song.country}: {song.artist} - {song.title}")
            
            if results['tracks']['items']:
                print("   Spotify matches:")
                for j, track in enumerate(results['tracks']['items'], 1):
                    artists = ', '.join([artist['name'] for artist in track['artists']])
                    print(f"     {j}. {artists} - {track['name']}")
                    print(f"        Album: {track['album']['name']} ({track['album']['release_date'][:4]})")
            else:
                print("   ❌ No matches found")
                
    except Exception as e:
        print(f"❌ Error searching Spotify: {e}")

def create_manual_playlist_instructions():
    """
    Create step-by-step instructions for manual playlist creation
    """
    print("\n📋 MANUAL PLAYLIST CREATION GUIDE 📋")
    print("=" * 50)
    print("If you prefer to create the playlist manually:")
    print("\n1. Open Spotify and create a new playlist")
    print("2. Use the search terms below to find each song")
    print("3. Add each song to your playlist")
    print("\nTip: Some songs might not be available in your region")
    print("or under different artist names. Try variations!")
    print("\n" + "=" * 50)
    
    create_spotify_playlist_format()

def main_menu():
    """Interactive menu for different script options"""
    print("\n🌍 WORLD MUSIC PLAYLIST GENERATOR 🌍")
    print("=" * 50)
    print("Choose an option:")
    print("1. View complete playlist")
    print("2. Export to CSV/JSON files")
    print("3. Show statistics")
    print("4. Search by country")
    print("5. Search by decade")
    print("6. Setup Spotify credentials")
    print("7. Create Spotify playlist (automatic)")
    print("8. Preview Spotify search results")
    print("9. Get manual playlist instructions")
    print("0. Exit")
    print("=" * 50)
    
    while True:
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == "1":
            print_playlist()
        elif choice == "2":
            export_to_csv()
            export_to_json()
        elif choice == "3":
            get_statistics()
        elif choice == "4":
            country = input("Enter country name: ").strip()
            search_by_country(country)
        elif choice == "5":
            try:
                decade = int(input("Enter decade (e.g., 1980): ").strip())
                search_by_decade(decade)
            except ValueError:
                print("Please enter a valid decade number")
        elif choice == "6":
            setup_spotify_credentials()
        elif choice == "7":
            create_spotify_playlist()
        elif choice == "8":
            try:
                limit = int(input("How many songs to preview? (default 10): ").strip() or "10")
                search_and_preview_spotify_matches(limit)
            except ValueError:
                search_and_preview_spotify_matches(10)
        elif choice == "9":
            create_manual_playlist_instructions()
        elif choice == "0":
            print("Goodbye! 🎵")
            break
        else:
            print("Invalid choice. Please enter a number between 0-9.")

# Main execution
if __name__ == "__main__":
    import sys
    
    # Check if specific function requested via command line
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "playlist":
            print_playlist()
        elif command == "export":
            export_to_csv()
            export_to_json()
        elif command == "stats":
            get_statistics()
        elif command == "spotify-setup":
            setup_spotify_credentials()
        elif command == "spotify-create":
            create_spotify_playlist()
        elif command == "spotify-preview":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            search_and_preview_spotify_matches(limit)
        elif command == "manual":
            create_manual_playlist_instructions()
        elif command == "menu":
            main_menu()
        else:
            print("Available commands:")
            print("  playlist        - Show complete playlist")
            print("  export          - Export to CSV/JSON")
            print("  stats           - Show statistics")
            print("  spotify-setup   - Show Spotify setup instructions")
            print("  spotify-create  - Create Spotify playlist")
            print("  spotify-preview - Preview Spotify search results")
            print("  manual          - Manual playlist instructions")
            print("  menu            - Interactive menu")
    else:
        # Default behavior - show overview and menu
        print("🌍 WORLD MUSIC PLAYLIST - 195 COUNTRIES 🌍")
        print("=" * 50)
        print(f"Total Songs: {len(world_playlist)}")
        print("From 1928 to 2017 • 50+ Languages • All Continents")
        print("\nThis script contains one iconic song from each country.")
        print("You can view the playlist, export it, or create a Spotify playlist.")
        
        # Quick setup check
        if SPOTIPY_AVAILABLE:
            client_id = os.getenv('SPOTIPY_CLIENT_ID')
            if client_id:
                print("\n✅ Spotify integration ready!")
                print("   Run with 'spotify-create' to make playlist")
            else:
                print("\n⚠️  Spotify credentials not configured")
                print("   Run with 'spotify-setup' for instructions")
        else:
            print("\n⚠️  Spotify integration not available")
            print("   Run: pip install spotipy")
        
        print("\nRun with 'menu' for interactive options")
        print("or use these quick commands:")
        print("  python script.py playlist")
        print("  python script.py spotify-create")
        print("  python script.py menu")