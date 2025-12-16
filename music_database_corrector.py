import csv
import pandas as pd

# Complete corrected music database with all 254 songs
corrected_music_data = [
    ["Artist", "Song Name", "Original Release Year", "Listed Year", "Correction Needed", "URL"],
    
    # Swedish/Scandinavian Songs (keeping original years unless clearly wrong)
    ["September", "Satellites", 2005, 2005, "No", "https://open.spotify.com/track/03N0ZpS5QaC9ga9i2xO9Vp"],
    ["estraden, Tjuvjakt", "Vårt år", 2020, 2020, "No", "https://open.spotify.com/track/2U8MK6O02FVG2DDTY9ttyv"],
    ["Myra Granberg", "Tills mitt hjärta går under", 2019, 2019, "No", "https://open.spotify.com/track/71q2qYTo4BzqNGpy5S7vV3"],
    ["Tomas Ledin", "En del av mitt hjärta", 1990, 1990, "No", "https://open.spotify.com/track/0gQtd0FQjuJSsuK2qHFYoF"],
    ["Jerry Williams", "I Can Jive", 1979, 1979, "No", "https://open.spotify.com/track/3zav6yFIf58MYsvcv4jS1t"],
    ["Sandra", "Maria Magdalena", 1985, 2010, "YES - Reissue date", "https://open.spotify.com/track/6i40rBSXK4dQz3nqqPVlvk"],
    ["Van Morrison", "Cyprus Avenue", 1968, 1968, "No", "https://open.spotify.com/track/7msn6OoGXrNOaBGvIH1eqT"],
    ["Gyllene Tider", "Gå och fiska", 1980, 2000, "YES - Reissue/compilation", "https://open.spotify.com/track/4LZhxPSsWW6djAWn9IaI2F"],
    ["Markoolio", "Sommar och sol", 1998, 1998, "No", "https://open.spotify.com/track/4bpqcGVSveDZ5E3rgr9v2y"],
    ["Magnus Uggla", "Kung för en dag", 1982, 2008, "YES - Original from 1982", "https://open.spotify.com/track/58X2vGyNWT2ZPEaGUw1tAb"],
    ["Sven-Ingvars", "Jag ringer på fredag", 1974, 1991, "YES - Original from 1974", "https://open.spotify.com/track/709uTN6yYi0wvFuDz87PQL"],
    ["Ted Gärdestad", "Himlen är oskyldigt blå", 1979, 2001, "YES - Original from 1979", "https://open.spotify.com/track/27TFfAFo4sE4fw04QDqJmD"],
    ["Veronica Maggio", "Havanna Mamma", 2006, 2006, "No", "https://open.spotify.com/track/7gybDAR6f9GVls39O1aYT2"],
    ["Thomas Stenström", "Slå mig hårt i ansiktet", 2014, 2014, "No", "https://open.spotify.com/track/58facAQuyUDml53CS4fOd3"],
    
    # Classic Rock & 70s-80s
    ["KISS", "Strutter", 1974, 1974, "No", "https://open.spotify.com/track/6uOnSrDg5Rfgil2zUGdyV0"],
    ["ZZ Top", "Gimme All Your Lovin'", 1983, 1983, "No", "https://open.spotify.com/track/0OBwxFLu6Yj61s2OagYbgY"],
    ["Creedence Clearwater Revival", "Up Around The Bend", 1970, 2005, "YES - Original from 1970", "https://open.spotify.com/track/2ajl6zSCu6QcDqtl5IDCQE"],
    ["Guns N' Roses", "Sweet Child O' Mine", 1987, 2004, "YES - Original from 1987", "https://open.spotify.com/track/32e5Wq10DT7xYrlRl5qSYF"],
    ["Iron Maiden", "The Number Of The Beast", 1982, 1982, "No", "https://open.spotify.com/track/1s4Ie0cT6P73SRSfh3oyGW"],
    ["The Clash", "London Calling", 1979, 1979, "No", "https://open.spotify.com/track/5jzma6gCzYtKB1DbEwFZKH"],
    ["The Rolling Stones", "Paint It, Black", 1966, 1966, "No", "https://open.spotify.com/track/0Oai8oyTRzzncLZcd3pJfa"],
    ["U2", "Beautiful Day", 2000, 2000, "No", "https://open.spotify.com/track/0gzqZ9d1jIKo9psEIthwXe"],
    ["Billy Idol", "Rebel Yell", 1983, 2001, "YES - Original from 1983", "https://open.spotify.com/track/2ZTIw0fZhFp3nnvF41nvVc"],
    ["Bon Jovi", "It's My Life", 2000, 2000, "No", "https://open.spotify.com/track/0v1XpBHnsbkCn7iJ9Ucr1l"],
    ["Kings of Leon", "Sex on Fire", 2008, 2008, "No", "https://open.spotify.com/track/5A1FmxbYVRZKy4nc16MAue"],
    ["Pearl Jam", "Jeremy", 1991, 1991, "No", "https://open.spotify.com/track/1ZH41dkdR51mDm9u8IXZIh"],
    ["Cyndi Lauper", "Time After Time", 1983, 1983, "No", "https://open.spotify.com/track/7o9uu2GDtVDr9nsR7ZRN73"],
    ["The Police", "Roxanne", 1978, 1978, "No", "https://open.spotify.com/track/3EYOJ48Et32uATr9ZmLnAo"],
    ["Tina Turner", "What's Love Got to Do with It", 1984, 1991, "YES - Original from 1984", "https://open.spotify.com/track/6FcQD1qOpqV8NdhY45sKyI"],
    
    # 90s Dance/Pop
    ["2 Unlimited", "Tribal Dance", 1993, 1993, "No", "https://open.spotify.com/track/6hDxjFzTU4uIHYU2pZC73K"],
    ["ABBA", "Dancing Queen", 1976, 1976, "No", "https://open.spotify.com/track/01iyCAUm8EvOFqVWYJ3dVX"],
    ["Ace of Base", "The Sign", 1993, 1993, "No", "https://open.spotify.com/track/68C7Q9IW70v5uaXSXyWVm3"],
    ["Bee Gees", "Stayin' Alive", 1977, 1990, "YES - Original soundtrack 1977", "https://open.spotify.com/track/32NqW4lERGa0uTQLXeXh65"],
    ["Billy Joel", "Piano Man", 1973, 2000, "YES - Original from 1973", "https://open.spotify.com/track/1y0N3y9kfooAE7F8dHDqa7"],
    ["Bryan Adams", "Heaven", 1984, 1984, "No", "https://open.spotify.com/track/7Ewz6bJ97vUqk5HdkvguFQ"],
    ["Jennifer Lopez", "Waiting for Tonight", 1999, 2012, "YES - Original from 1999", "https://open.spotify.com/track/5jOvmh1DYmaiBPETL6HCRY"],
    ["Shania Twain", "That Don't Impress Me Much", 1997, 1997, "No", "https://open.spotify.com/track/0KvLsZYwodakWxOQUYAR5I"],
    ["TOTO", "Africa", 1982, 2015, "YES - Original from 1982", "https://open.spotify.com/track/5tJjo5JDF9zhzYD7yQfATH"],
    ["AC/DC", "Thunderstruck", 1990, 1990, "No", "https://open.spotify.com/track/57bgtoPSgt236HzfBOd8kj"],
    
    # 2000s Pop/Rock
    ["Maroon 5", "This Love", 2002, 2002, "No", "https://open.spotify.com/track/6ECp64rv50XVz93WvxXMGF"],
    ["Rihanna", "SOS", 2006, 2006, "No", "https://open.spotify.com/track/4S5b3wwIXpVNvY2jeIQdKu"],
    ["P!nk", "Get the Party Started", 2001, 2001, "No", "https://open.spotify.com/track/4bk78jvK8Fe9YHqruOJW0v"],
    ["Destiny's Child", "Survivor", 2001, 2001, "No", "https://open.spotify.com/track/2Mpj1Ul5OFPyyP4wB62Rvi"],
    ["Pitbull, TJR", "Don't Stop the Party", 2012, 2012, "No", "https://open.spotify.com/track/36K25M6aI4ZtXMUB6gDijU"],
    ["Train", "Hey, Soul Sister", 2010, 2010, "No", "https://open.spotify.com/track/4HlFJV71xXKIGcU3kRyttv"],
    ["Queen", "I Want To Break Free", 1984, 1984, "No", "https://open.spotify.com/track/7h2yhVxcZOGyQdOwD4Hu8J"],
    ["Huey Lewis & The News", "Stuck With You", 1986, 1986, "No", "https://open.spotify.com/track/2cFl7utlqyZjCXN1G5nRvA"],
    ["D12", "My Band", 2004, 2004, "No", "https://open.spotify.com/track/4XHQyvbrBsQaaBUW1VvmsL"],
    ["Michael Jackson", "Ben", 1972, 1972, "No", "https://open.spotify.com/track/3vZMkLS1jP7NdNhzqGfUSW"],
    ["Fergie, Ludacris", "Glamorous", 2006, 2006, "No", "https://open.spotify.com/track/4N0tDOF2bo9JEpSqLNlpjq"],
    ["Rick Astley", "Never Gonna Give You Up", 1987, 1987, "No", "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8"],
    ["Chumbawamba", "Tubthumping", 1997, 2023, "YES - Original from 1997", "https://open.spotify.com/track/0h1owh5X5YmgVoEKsAVylU"],
    ["Earth, Wind & Fire", "Let's Groove", 1981, 1981, "No", "https://open.spotify.com/track/3koCCeSaVUyrRo3N2gHrd8"],
    ["Urge Overkill", "Girl, You'll Be A Woman Soon", 1992, 1994, "YES - Original from 1992", "https://open.spotify.com/track/56qx6OC90grYNnqIZ81Wh1"],
    ["Rick Springfield", "Jessie's Girl", 1981, 1981, "No", "https://open.spotify.com/track/2F1fnE1a8zQCogM6jJifHH"],
    ["Frankie Valli", "Can't Take My Eyes off You", 1967, 1967, "No", "https://open.spotify.com/track/0bfvHnWWOeU1U5XeKyVLbW"],
    ["Phil Collins", "In The Air Tonight", 1981, 1981, "No", "https://open.spotify.com/track/18AXbzPzBS8Y3AkgSxzJPb"],
    ["Irene Cara", "Fame", 1980, 1980, "No", "https://open.spotify.com/track/5CI1FP2Volc9wjz2MBZsGx"],
    ["Rufus Wainwright", "Hallelujah", 2001, 2013, "YES - Original from 2001", "https://open.spotify.com/track/2u6fRGcaBhpI4uNBHpGv0b"],
    ["The Moldy Peaches", "Anyone Else But You", 2001, 2001, "No", "https://open.spotify.com/track/2pKi1lRvXNASy7ybeQIDTy"],
    ["The Strokes", "What Ever Happened?", 2003, 2003, "No", "https://open.spotify.com/track/78Gzxi27GuNHTfkn2BylG4"],
    ["Roxette", "It Must Have Been Love", 1987, 1995, "YES - Original from 1987", "https://open.spotify.com/track/6qB7YcFpeBEQa0D6QO482y"],
    ["Mazzy Star", "Fade Into You", 1993, 1993, "No", "https://open.spotify.com/track/1LzNfuep1bnAUR9skqdHCK"],
    ["Eric Carmen", "Hungry Eyes", 1987, 1997, "YES - Original from 1987", "https://open.spotify.com/track/31H6au3jhblhr6MMJiXnCq"],
    ["Rihanna", "Lift Me Up", 2022, 2022, "No", "https://open.spotify.com/track/35ovElsgyAtQwYPYnZJECg"],
    ["Kenny Loggins", "For the First Time", 1996, 1996, "No", "https://open.spotify.com/track/6qtlVfQ7llt0dthJS14JEA"],
    ["John Travolta, Olivia Newton-John", "Summer Nights", 1978, 1978, "No", "https://open.spotify.com/track/2AVkArcfALVk2X8sfPRzya"],
    ["Janet Jackson", "Again", 1993, 1993, "No", "https://open.spotify.com/track/0IaMMHVbpJ0LrRAeigWOXr"],
    ["Trisha Yearwood", "How Do I Live", 1997, 2013, "YES - Original from 1997", "https://open.spotify.com/track/1PJ1JyZJg3aZgZQfg3ciWn"],
    ["Radiohead", "Fake Plastic Trees", 1995, 1995, "No", "https://open.spotify.com/track/73CKjW3vsUXRpy3NnX4H7F"],
    ["Urge Overkill", "Girl, You'll Be a Woman Soon", 1992, 1992, "No", "https://open.spotify.com/track/1mSzuXVjjKC0bPh6iG6xjy"],
    ["Sarah McLachlan", "Angel", 1997, 1997, "No", "https://open.spotify.com/track/3xZMPZQYETEn4hjor3TR1A"],
    ["Fleetwood Mac", "Go Your Own Way", 1977, 1977, "No", "https://open.spotify.com/track/07GvNcU1WdyZJq3XxP0kZa"],
    ["Paul Westerberg", "Waiting for Somebody", 1992, 1992, "No", "https://open.spotify.com/track/3R6GxZEzCWDNnwo8QWeOw6"],
    ["The Police", "Every Breath You Take", 1983, 1983, "No", "https://open.spotify.com/track/1JSTJqkT5qHq8MDJnJbRE1"],
    ["The Smiths", "How Soon Is Now?", 1984, 1998, "YES - Original from 1984", "https://open.spotify.com/track/0Nmu7zxpMYNJ3N9YDY6VEN"],
    ["T-Zone", "Sisters Are Doing It for Themselves", 1985, 2012, "YES - Original Eurythmics/Aretha from 1985", "https://open.spotify.com/track/1i4St7fmSUE9nB3R9n8fol"],
    ["Céline Dion", "All By Myself", 1996, 1996, "No", "https://open.spotify.com/track/0gsl92EMIScPGV1AU35nuD"],
    ["Jennifer Hudson", "Love You I Do", 2006, 2006, "No", "https://open.spotify.com/track/3LeSaLcjfyeVER5BIl634d"],
    ["The Turtles", "Happy Together", 1967, 1967, "No", "https://open.spotify.com/track/1JO1xLtVc8mWhIoE3YaCL0"],
    ["Carly Simon", "You're So Vain", 1972, 1972, "No", "https://open.spotify.com/track/2DnJjbjNTV9Nd5NOa1KGba"],
    ["Nina Simone", "My Baby Just Cares for Me", 1957, 2013, "YES - Original recording from 1957", "https://open.spotify.com/track/5Lhjlnly9Ynhf52ojQS534"],
    ["Nat King Cole", "When I Fall In Love", 1957, 1957, "No", "https://open.spotify.com/track/6s6h2XK7Nl8lEcTzr7ezeB"],
    ["Swedish House Mafia, The Weeknd", "Moth To A Flame", 2021, 2022, "YES - Released October 2021", "https://open.spotify.com/track/7kfOEMJBJwdCYqyJeEnNhr"],
    ["Caroline Polachek", "Starburned and Unkissed", 2024, 2024, "No", "https://open.spotify.com/track/12V0MwkaN60cghsLsglkIf"],
    ["Natasha Bedingfield", "Unwritten", 2004, 2004, "No", "https://open.spotify.com/track/3U5JVgI2x4rDyHGObzJfNf"],
    ["Manfred Mann", "Do Wah Diddy Diddy", 1964, 1963, "YES - Original from 1964", "https://open.spotify.com/track/48ZjHLkaHpXIlGGYUlb3bZ"],
    ["Khalid", "Young Dumb & Broke", 2017, 2017, "No", "https://open.spotify.com/track/5Z3GHaZ6ec9bsiI5BenrbY"],
    ["Gianna Nannini", "Bello e impossibile", 1986, 1986, "No", "https://open.spotify.com/track/3dZHWv3IsAQLzAr7FLJoJA"],
    ["Albin Lee Meldau", "Josefin", 2021, 2021, "No", "https://open.spotify.com/track/73hiGuj0dxhA1YhmSJOcMF"],
    ["Foster The People", "Sit Next to Me", 2017, 2017, "No", "https://open.spotify.com/track/4BdGO1CaObRD4La9l5Zanz"],
    ["AC/DC", "T.N.T.", 1975, 1976, "YES - Original from 1975", "https://open.spotify.com/track/7LRMbd3LEoV5wZJvXT1Lwb"],
    ["Ellie Goulding", "Burn", 2013, 2012, "YES - Released July 2013", "https://open.spotify.com/track/5lF0pHbsJ0QqyIrLweHJPW"],
    ["Oracle Sisters", "Asc. Scorpio", 2020, 2020, "No", "https://open.spotify.com/track/2MnSPY2QYMbtkDWGzY02In"],
    ["Thee Sacred Souls", "Can I Call You Rose?", 2022, 2022, "No", "https://open.spotify.com/track/6IAuH3hgTRpUUdmOGubXGS"],
    
    # Classic Artists
    ["George Harrison", "Got My Mind Set on You", 1987, 1987, "No", "https://open.spotify.com/track/4wswaG5vmNINMZcVBsAyBP"],
    ["George Harrison", "My Sweet Lord", 1970, 1970, "No", "https://open.spotify.com/track/0KZodeWxqxd88F9wY1cqgs"],
    ["John Lennon", "Woman", 1980, 1980, "No", "https://open.spotify.com/track/0GGxVTb0UwDwdaKNjBdCn3"],
    ["Bob Dylan", "Like a Rolling Stone", 1965, 1965, "No", "https://open.spotify.com/track/3AhXZa8sUQht0UEdBJgpGc"],
    ["Wabie", "Hey Lover!", 2019, 2019, "No", "https://open.spotify.com/track/7rC3P7tpWriaC4hYWKwGQd"],
    ["Bee Gees", "How Deep Is Your Love", 1977, 1979, "YES - Original from 1977", "https://open.spotify.com/track/2JoZzpdeP2G6Csfdq5aLXP"],
    ["Elton John, Kiki Dee", "Don't Go Breaking My Heart", 1976, 1990, "YES - Original from 1976", "https://open.spotify.com/track/5pKJtX4wBeby9qIfFhyOJj"],
    ["Boney M.", "Ma Baker", 1977, 1977, "No", "https://open.spotify.com/track/1BqnZOkYJbvYLOhN0qPJDm"],
    ["Billy Joel", "You're Only Human (Second Wind)", 1985, 1985, "No", "https://open.spotify.com/track/4aaOblwrIiVnScKL51pGdo"],
    ["Paul Russell", "Lil Boo Thang", 2023, 2023, "No", "https://open.spotify.com/track/0cVyQfDyRnMJ0V3rjjdlU3"],
    ["George Ezra", "Shotgun", 2018, 2018, "No", "https://open.spotify.com/track/4ofwffwvvnbSkrMSCKQDaC"],
    ["Triple & Touch", "Pata-pata", 1967, 1993, "YES - Original Miriam Makeba from 1967", "https://open.spotify.com/track/2mQll0yyUmoWCv1UqgihhL"],
    ["Lars Winnerbäck, Miss Li", "Om du lämnade mig nu", 2007, 2007, "No", "https://open.spotify.com/track/17q9gSD214wClyCjqrhmgH"],
    ["Aretha Franklin", "I Say a Little Prayer", 1968, 1968, "No", "https://open.spotify.com/track/3NfxSdJnVdon1axzloJgba"],
    ["The Knack", "My Sharona", 1979, 1979, "No", "https://open.spotify.com/track/1HOMkjp0nHMaTnfAkslCQj"],
    ["Bruce Springsteen", "Streets of Philadelphia", 1994, 1995, "YES - Original from 1994", "https://open.spotify.com/track/3fbnbn6A5O5RNb08tlUEgd"],
    ["Peter Gabriel", "In Your Eyes", 1986, 1986, "No", "https://open.spotify.com/track/1wyluqXP2ujdTpCfm1E617"],
    ["Bette Midler", "Wind Beneath My Wings", 1988, 1993, "YES - Original from 1988", "https://open.spotify.com/track/4ErUhFToT1yX52MeHqH8OY"],
    ["Coolio, L.V.", "Gangsta's Paradise", 1995, 1995, "No", "https://open.spotify.com/track/1DIXPcTDzTj8ZMHt3PDt8p"],
    ["The Beatles", "A Hard Day's Night", 1964, 1964, "No", "https://open.spotify.com/track/5J2CHimS7dWYMImCHkEFaJ"],
    ["The Shins", "New Slang", 2001, 2001, "No", "https://open.spotify.com/track/0NslHuacjxQYfUTOW3HCIV"],
    ["Little Nell, Patricia Quinn, Richard O'Brien", "Time Warp", 1975, 1975, "No", "https://open.spotify.com/track/4WFeJTXNHIS2wURtwlAkhu"],
    ["The Beatles", "Yellow Submarine", 1966, 1969, "YES - Single released 1966", "https://open.spotify.com/track/3oEo8Pqm5IAi8wQfCI5BpR"],
    ["The Wonders", "That Thing You Do!", 1996, 1996, "No", "https://open.spotify.com/track/4O6ZaZrRCFfiZZKjnrXqlk"],
    ["Public Enemy", "Fight The Power", 1989, 1990, "YES - Original from 1989", "https://open.spotify.com/track/1yo16b3u0lptm6Cs7lx4AD"],
    ["The Psychedelic Furs", "Pretty in Pink", 1981, 2010, "YES - Original from 1981", "https://open.spotify.com/track/2mZGm1xVwF7H0bVcHWBXO4"],
    ["Joe Cocker, Jennifer Warnes", "Up Where We Belong", 1982, 1999, "YES - Original from 1982", "https://open.spotify.com/track/4U6mBgGP8FXN6UH4T3AJhu"],
    ["Francis Lai, Christian Gaubert", "La leçon particulière", 1981, 2003, "YES - Original from 1981", "https://open.spotify.com/track/4OWa2dOlmtvMDhFrFL0QA1"],
    ["Bryan Adams", "Have You Ever Really Loved A Woman?", 1995, 1996, "YES - Original from 1995", "https://open.spotify.com/track/32Gf5A7Hr8RdgggXG0Fdks"],
    ["Bruce Springsteen", "Secret Garden", 1995, 1996, "YES - Original from 1995", "https://open.spotify.com/track/4hBH0Ss3nTeOP7NnkyePd7"],
    ["Selena", "Dreaming Of You", 1995, 1997, "YES - Original from 1995", "https://open.spotify.com/track/0FhCQHObxw05xJLvwiEvGr"],
    ["Sarah McLachlan", "I Will Remember You", 1995, 1996, "YES - Original from 1995", "https://open.spotify.com/track/4rSKsjxykn9GpEYnNvyR2u"],
    ["RAYE", "Fly Me to the Moon", 2024, 2024, "No", "https://open.spotify.com/track/4krtOcIVPlUICseg29Nnet"],
    ["Sophie Ellis-Bextor", "Murder On The Dancefloor", 2001, 2002, "YES - Released December 2001", "https://open.spotify.com/track/4tKGFmENO69tZR9ahgZu48"],
    ["Metro Boomin, Swae Lee, NAV, A Boogie Wit da Hoodie", "Calling", 2023, 2023, "No", "https://open.spotify.com/track/5rurggqwwudn9clMdcchxT"],
    ["U2", "Happiness", 2024, 2024, "No", "https://open.spotify.com/track/4bMiqeOGu8szuBoJ2SYVCR"],
    ["James Arthur", "Say You Won't Let Go", 2016, 2016, "No", "https://open.spotify.com/track/5uCax9HTNlzGybIStD3vDh"],
    ["Khruangbin, Leon Bridges", "Texas Sun", 2020, 2020, "No", "https://open.spotify.com/track/24ntSW3QVJzR79lHAAOTaY"],
    ["Selena Gomez, benny blanco, The Marías", "Ojos Tristes", 2025, 2025, "No", "https://open.spotify.com/track/1DpC4L3JjsGRW7y6eTHaMj"],
    ["Doechii", "Anxiety", 2025, 2025, "No", "https://open.spotify.com/track/3LPLRNr58Z9Pn0clnEtkXb"],
    ["Benson Boone", "Sorry I'm Here For Someone Else", 2025, 2025, "No", "https://open.spotify.com/track/3x3K1RP3Zfi2qeMR8kyrNO"],
    
    # Classic 50s/60s Songs
    ["Harry Belafonte", "Banana Boat (Day-O)", 1956, 1956, "No", "https://open.spotify.com/track/4fHDlIntTsRGSyTg5UYZYC"],
    ["Paul Anka", "Put Your Head on My Shoulder", 1959, 1966, "YES - Original from 1959", "https://open.spotify.com/track/7eqNATKM78MkWP6aHGXHEV"],
    ["Paul Anka", "Put Your Head On My Shoulder - Remastered", 1959, 1959, "No", "https://open.spotify.com/track/6YDDrg8llsRtAgLlIROzZc"],
    ["Louis Armstrong", "What A Wonderful World", 1967, 1968, "YES - Original from 1967", "https://open.spotify.com/track/29U7stRjqHU6rMiS8BfaI9"],
    ["Connie Francis", "Many Tears Ago", 1960, 1963, "YES - Original from 1960", "https://open.spotify.com/track/5THUK7wGMc21N80a8EFSF2"],
    ["Johnny Cash, The Tennessee Two", "I Walk The Line", 1956, 1956, "No", "https://open.spotify.com/track/0e1mMD6Pkn7zd9mhCQnrsY"],
    ["Billie Holiday", "I'll Be Seeing You", 1944, 1957, "YES - Original from 1944", "https://open.spotify.com/track/4smkJW6uzoHxGReZqqwHS5"],
    ["Louis Prima, Keely Smith, Sam Butera & The Witnesses", "Just A Gigolo / I Ain't Got Nobody", 1956, 1956, "No", "https://open.spotify.com/track/0NI42v4l2AxIbgoIrWKiBU"],
    ["Thurston Harris", "Little Bitty Pretty One", 1957, 1959, "YES - Original from 1957", "https://open.spotify.com/track/2yOXKIU9YtBSWjI3OA8tqj"],
    ["Ray Charles", "I've Got a Woman", 1954, 1957, "YES - Original from 1954", "https://open.spotify.com/track/2xar08Fq5xra2KKZs5Bw9j"],
    ["Chuck Berry", "You Never Can Tell", 1964, 1964, "No", "https://open.spotify.com/track/6FT83pFXKhDlXDsNJFAHWz"],
    ["Bill Haley & His Comets", "See You Later, Alligator", 1956, 1959, "YES - Original from 1956", "https://open.spotify.com/track/05eNEozACh10Rn0ewFnH8Y"],
    ["The Diamonds", "Little Darlin'", 1957, 1954, "YES - Original from 1957", "https://open.spotify.com/track/4eglKIbp75EEQJpgrOaSGo"],
    ["Frank Sinatra", "My Funny Valentine", 1954, 1954, "No", "https://open.spotify.com/track/0x0ffSAP6PkdoDgHOfroof"],
    ["Neil Sedaka", "Oh! Carol", 1959, 1959, "No", "https://open.spotify.com/track/5zvOXJrzzUlvXwyuwZ0toZ"],
    ["Bobby Day", "Rockin' Robin", 1958, 1959, "YES - Original from 1958", "https://open.spotify.com/track/7v83GQJGezSgVZD7huvhHH"],
    ["Little Richard", "Tutti Frutti", 1955, 1957, "YES - Original from 1955", "https://open.spotify.com/track/2iXcvnD3d1gfLBum0cE5Eg"],
    ["Sam Cooke", "You Send Me", 1957, 1958, "YES - Original from 1957", "https://open.spotify.com/track/1XPj5quoeV5Gd0paSUDpvm"],
    ["Jerry Lee Lewis", "Great Balls Of Fire", 1957, 1957, "No", "https://open.spotify.com/track/0AKU7RIWFgbcHQnSQIk56I"],
    
    # 70s Classic Rock/Pop
    ["David Bowie", "Young Americans", 1975, 1975, "No", "https://open.spotify.com/track/7uPmQttafLiJyju14JREY4"],
    ["ABBA", "Mamma Mia", 1975, 1975, "No", "https://open.spotify.com/track/2TxCwUlqaOH3TIyJqGgR91"],
    ["Rod Stewart", "Maggie May", 1971, 1971, "No", "https://open.spotify.com/track/6rovOdp3HgK1DeAMYDzoA7"],
    ["Sonny & Cher", "I Got You Babe", 1965, 1965, "No", "https://open.spotify.com/track/4SGBuq37Ol4HJr7pQqFMKa"],
    ["Elvis Presley", "Suspicious Minds", 1969, 1969, "No", "https://open.spotify.com/track/1H5IfYyIIAlgDX8zguUzns"],
    ["The Beach Boys", "I Get Around", 1964, 1964, "No", "https://open.spotify.com/track/3v9xlH6BpmRbqL7hgNJhfT"],
    ["Phil Collins", "You Can't Hurry Love", 1982, 1982, "No", "https://open.spotify.com/track/4YwbSZaYeYja8Umyt222Qf"],
    ["Rod Stewart", "Sailing", 1975, 1975, "No", "https://open.spotify.com/track/6OuRbvP4PgbuzBIapVzmFJ"],
    ["Marvin Gaye", "What's Going On", 1971, 1971, "No", "https://open.spotify.com/track/3Um9toULmYFGCpvaIPFw7l"],
    ["The Jacksons", "Blame It on the Boogie", 1978, 1978, "No", "https://open.spotify.com/track/3qI94hINNNeb4S7xQi18lS"],
    ["Stevie Wonder", "Signed, Sealed, Delivered (I'm Yours)", 1970, 1970, "No", "https://open.spotify.com/track/0kzhMZZNmxiLG7qyJhVBHB"],
    ["Bo Diddley", "Bo Diddley", 1955, 1958, "YES - Original from 1955", "https://open.spotify.com/track/2R7uUQ0Dehu80gsOcydQC9"],
    ["Little Willie John", "Need Your Love So Bad", 1957, 1958, "YES - Original from 1957", "https://open.spotify.com/track/0AJhhznysKPNJvhsYhOlRa"],
    ["The Harptones", "Life Is but a Dream", 1955, 1955, "No", "https://open.spotify.com/track/7v9v3cc21gctrjHivLh1o2"],
    ["The Platters", "Twilight Time", 1958, 1958, "No", "https://open.spotify.com/track/3MpGQae6zAFd7Z1FdLV9fV"],
    ["Frank Sinatra, Nancy Sinatra", "Somethin' Stupid", 1967, 1967, "No", "https://open.spotify.com/track/4feXcsElKIVsGwkbnTHAfV"],
    ["Etta James", "I Just Want To Make Love To You", 1960, 1960, "No", "https://open.spotify.com/track/3QnHWkNMY2mpy494Bis0ly"],
    ["The Drifters", "Save the Last Dance for Me", 1960, 1962, "YES - Original from 1960", "https://open.spotify.com/track/391TUcoPonqYykPkSZ5Z9U"],
    ["The Marvelettes", "Please Mr. Postman", 1961, 1961, "No", "https://open.spotify.com/track/6jX5mso4x00c1EiNMrTU9U"],
    ["Barbara Mason", "Yes, I'm Ready", 1965, 1965, "No", "https://open.spotify.com/track/2gZpW5pTZkimGG98loFSl2"],
    ["Diana Ross & The Supremes", "Someday We'll Be Together", 1969, 1969, "No", "https://open.spotify.com/track/79Yk6AlSKi5dxDFINID2hS"],
    ["Tom Jones, Mousse T.", "Sexbomb", 1999, 1999, "No", "https://open.spotify.com/track/7GHKA8GIMcND6c5nN1sFnD"],
    ["The Dixie Cups", "Chapel Of Love", 1964, 1963, "YES - Original from 1964", "https://open.spotify.com/track/2oQ0IdzEw1J5RbIrQ9g9mC"],
    ["Otis Redding", "These Arms of Mine", 1962, 1964, "YES - Original from 1962", "https://open.spotify.com/track/4skknrc3sJqaPTtUr2cwFq"],
    ["Glen Campbell", "Gentle On My Mind", 1967, 1967, "No", "https://open.spotify.com/track/0mLoTgCB8oU0sJGojRtvDu"],
    ["Brenda Lee", "Emotions", 1961, 1961, "No", "https://open.spotify.com/track/60jQTAr2OkFcV4SWSRz3st"],
    ["Jimi Hendrix", "Little Wing", 1967, 1967, "No", "https://open.spotify.com/track/1Eolhana7nKHYpcYpdVcT5"],
    ["Joni Mitchell", "California", 1971, 1971, "No", "https://open.spotify.com/track/5eM6Rrk8rwLpUhrh7Kk5R1"],
    ["Lesley Gore", "It's My Party", 1963, 1963, "No", "https://open.spotify.com/track/1Pq47iFLC5U7j8xeNiNcuS"],
    ["Dionne Warwick", "Walk on By", 1964, 1964, "No", "https://open.spotify.com/track/3xsOtNxtBW0oTI1OWKAzTm"],
    ["Dusty Springfield", "I Only Want To Be With You", 1963, 1964, "YES - Original from 1963", "https://open.spotify.com/track/31A3oqQxDLdG9HRx45z62d"],
    ["The Mamas & The Papas", "Monday, Monday", 1966, 1966, "No", "https://open.spotify.com/track/3EFb1qDgIqf9MegIryKtDj"],
    
    # 80s Pop/Rock
    ["Belinda Carlisle", "Heaven Is A Place On Earth", 1987, 1987, "No", "https://open.spotify.com/track/37Q5anxoGWYdRsyeXkkNoI"],
    ["Whitney Houston", "How Will I Know", 1985, 1985, "No", "https://open.spotify.com/track/5tdKaKLnC4SgtDZ6RlWeal"],
    ["Bananarama", "Cruel Summer", 1983, 1984, "YES - Original from 1983", "https://open.spotify.com/track/2EGaDf0cPX789H3LNeB03D"],
    ["Bon Jovi", "You Give Love A Bad Name", 1986, 1986, "No", "https://open.spotify.com/track/0rmGAIH9LNJewFw7nKzZnc"],
    ["The Bangles, Susanna Hoffs", "Eternal Flame", 1989, 1988, "YES - Released January 1989", "https://open.spotify.com/track/5g3ZD7PmrEQlQZKDW91yGG"],
    ["Sting", "Englishman In New York", 1987, 1987, "No", "https://open.spotify.com/track/4KFM3A5QF2IMcc6nHsu3Wp"],
    ["Pet Shop Boys", "West End Girls", 1984, 1986, "YES - Original from 1984", "https://open.spotify.com/track/2Di0qFNb7ATroCGB3q0Ka7"],
    ["The Cure", "Just Like Heaven", 1987, 1987, "No", "https://open.spotify.com/track/4NnWuGQujzWUEg0uZokO5M"],
    ["Madonna", "Like a Prayer", 1989, 1989, "No", "https://open.spotify.com/track/2v7ywbUzCgcVohHaKUcacV"],
    ["Roxette", "Listen To Your Heart", 1988, 1988, "No", "https://open.spotify.com/track/2MaBAGBIttgv86bYytdx1f"],
    ["Bobby McFerrin", "Don't Worry Be Happy", 1988, 1988, "No", "https://open.spotify.com/track/4hObp5bmIJ3PP3cKA9K9GY"],
    
    # 70s Rock Classics
    ["Elton John", "Crocodile Rock", 1972, 1973, "YES - Original from 1972", "https://open.spotify.com/track/6WCeFNVAXUtNczb7lqLiZU"],
    ["Queen", "Killer Queen", 1974, 1974, "No", "https://open.spotify.com/track/2AKOOhml62GZNFWDN7VqzT"],
    ["Alice Cooper", "School's Out", 1972, 1972, "No", "https://open.spotify.com/track/5Z8EDau8uNcP1E8JvmfkZe"],
    ["Lynyrd Skynyrd", "Simple Man", 1973, 1973, "No", "https://open.spotify.com/track/1ju7EsSGvRybSNEsRvc7qY"],
    
    # 2000s-2010s Pop
    ["Katy Perry", "I Kissed A Girl", 2008, 2008, "No", "https://open.spotify.com/track/14iN3o8ptQ8cFVZTEmyQRV"],
    ["LMFAO, Lauren Bennett, GoonRock", "Party Rock Anthem", 2011, 2011, "No", "https://open.spotify.com/track/7mitXLIMCflkhZiD34uEQI"],
    ["Sabrina Carpenter", "Looking at Me", 2019, 2019, "No", "https://open.spotify.com/track/59tskctgqUmjCWAwhzYAFm"],
    ["Flo Rida, Kesha", "Right Round", 2009, 2009, "No", "https://open.spotify.com/track/3GpbwCm3YxiWDvy29Uo3vP"],
    ["Shawn Mendes", "Stitches", 2015, 2015, "No", "https://open.spotify.com/track/3zkWCteF82vJwv0hRLba76"],
    ["Marshmello, Bastille", "Happier", 2018, 2018, "No", "https://open.spotify.com/track/2dpaYNEQHiRxtZbfNsse99"],
    ["Wiz Khalifa, Charlie Puth", "See You Again", 2015, 2015, "No", "https://open.spotify.com/track/2JzZzZUQj3Qff7wapcbKjc"],
    ["The Weeknd", "Can't Feel My Face", 2015, 2015, "No", "https://open.spotify.com/track/22VdIZQfgXJea34mQxlt81"],
    ["Tina Turner", "The Best", 1989, 1989, "No", "https://open.spotify.com/track/6pPWRBubXOBAHnjl5ZIujB"],
    ["Dire Straits", "Walk Of Life", 1985, 1985, "No", "https://open.spotify.com/track/6HMFtoMvv6n6Q2eOyPFyne"],
    ["50 Cent, Olivia", "Candy Shop", 2005, 2005, "No", "https://open.spotify.com/track/5D2mYZuzcgjpchVY1pmTPh"],
    ["Foo Fighters", "Best of You", 2005, 2005, "No", "https://open.spotify.com/track/5FZxsHWIvUsmSK1IAvm2pp"],
    ["Arctic Monkeys", "Fluorescent Adolescent", 2007, 2007, "No", "https://open.spotify.com/track/2x8evxqUlF0eRabbW2JBJd"],
    ["Kanye West", "Stronger", 2007, 2007, "No", "https://open.spotify.com/track/0j2T0R9dR9qdJYsB7ciXhf"],
    ["Avril Lavigne", "Complicated", 2002, 2002, "No", "https://open.spotify.com/track/5xEM5hIgJ1jjgcEBfpkt2F"],
    ["Kelly Clarkson", "My Life Would Suck Without You", 2009, 2009, "No", "https://open.spotify.com/track/6li2D8wQPvgwI2QIrGPhAF"],
    
    # Classic 60s-70s
    ["Chubby Checker", "The Twist", 1960, 1962, "YES - Original from 1960", "https://open.spotify.com/track/6DSvUZQdqtNfkJI4cAiUsM"],
    ["Johnny Preston", "Running Bear", 1959, 1960, "YES - Original from 1959", "https://open.spotify.com/track/2D8gEqtkTlQvOJi931hvO6"],
    ["The Doobie Brothers", "Long Train Runnin'", 1973, 1973, "No", "https://open.spotify.com/track/4nXkbcTj3nyww1cHkw5RAP"],
    ["Carpenters", "Yesterday Once More", 1973, 1973, "No", "https://open.spotify.com/track/3wM6RTAnF7IQpMFd7b9ZcL"],
    ["Barry White", "Can't Get Enough Of Your Love, Babe", 1974, 1974, "No", "https://open.spotify.com/track/3mWpUEBYnv9SIFWfixSJFx"],
    ["Supertramp", "School", 1974, 1974, "No", "https://open.spotify.com/track/6fnachl7fIn5dqIjakfJ57"],
    ["The Spinners", "The Rubberband Man", 1976, 1976, "No", "https://open.spotify.com/track/13Mzsb8VzRSZ5w3pM48cn6"],
    ["Eric Clapton", "Wonderful Tonight", 1977, 1977, "No", "https://open.spotify.com/track/6zC0mpGYwbNTpk9SKwh08f"],
    ["Kenny Rogers", "The Gambler", 1978, 1978, "No", "https://open.spotify.com/track/5KqldkCunQ2rWxruMEtGh0"],
    ["Genesis", "Misunderstanding", 1980, 1980, "No", "https://open.spotify.com/track/2JPWiYKyPM9ST26TpKAeYd"],
    ["Bob Seger", "Against The Wind", 1980, 1980, "No", "https://open.spotify.com/track/1SWmFiFSIBoDbQJjNKC7SR"],
    ["Steve Miller Band", "Abracadabra", 1982, 1982, "No", "https://open.spotify.com/track/2E2ZVy2fxslpAUgbb4zu84"],
    ["Katrina & The Waves", "Walking On Sunshine", 1985, 1985, "No", "https://open.spotify.com/track/05wIrZSwuaVWhcv5FfqeH0"],
    ["The Cranberries", "Zombie", 1994, 1994, "No", "https://open.spotify.com/track/7EZC6E7UjZe63f1jRmkWxt"],
    
    # 2000s-2010s Continued
    ["Beyoncé", "Sweet Dreams", 2008, 2009, "YES - Released 2008", "https://open.spotify.com/track/3wrXItG1dxGdjxLeMesjCU"],
    ["Florence + The Machine", "Cosmic Love", 2009, 2009, "No", "https://open.spotify.com/track/1myEOhXztRxUVfaAEQiKkU"],
    ["Lionel Richie", "Hello", 1984, 1983, "YES - Original from 1984", "https://open.spotify.com/track/1b16zIZIdL2LIMfDiANwIk"],
    ["Adele", "Rolling in the Deep", 2010, 2011, "YES - Original from 2010", "https://open.spotify.com/track/4OSBTYWVwsQhGLF9NHvIbR"],
    ["The Wanted", "Glad You Came", 2011, 2011, "No", "https://open.spotify.com/track/5yDL13y5giogKs2fSNf7sj"],
    ["OneRepublic", "Counting Stars", 2013, 2014, "YES - Original from 2013", "https://open.spotify.com/track/1QzFhzIOW7CyRJLpmq5CM0"],
    ["Labrinth", "Jealous", 2014, 2014, "No", "https://open.spotify.com/track/4G92yYrUs0cvY7G41YRI0z"],
    ["Ed Sheeran", "Galway Girl", 2017, 2017, "No", "https://open.spotify.com/track/0afhq8XCExXpqazXczTSve"],
    ["Charlie Puth", "Attention", 2017, 2018, "YES - Original from 2017", "https://open.spotify.com/track/5cF0dROlMOK5uNZtivgu50"],
    ["Dua Lipa", "IDGAF", 2017, 2017, "No", "https://open.spotify.com/track/76cy1WJvNGJTj78UqeA5zr"],
    ["Travis Scott", "STARGAZING", 2018, 2018, "No", "https://open.spotify.com/track/7wBJfHzpfI3032CSD7CE2m"],
    ["Frank Ocean", "Pink + White", 2016, 2016, "No", "https://open.spotify.com/track/3xKsf9qdS1CyvXSMEid6g8"],
    ["Alessia Cara", "Scars To Your Beautiful", 2016, 2016, "No", "https://open.spotify.com/track/42ydLwx4i5V49RXHOozJZq"],
    ["Lil Nas X", "MONTERO (Call Me By Your Name)", 2021, 2021, "No", "https://open.spotify.com/track/67BtfxlNbhBmCDR2L2l8qd"],
    ["GIVĒON", "Like I Want You", 2021, 2021, "No", "https://open.spotify.com/track/1RohgA8t3qiVc5HcAroDgf"],
    ["Don Omar, Lucenzo", "Danza Kuduro", 2010, 2010, "No", "https://open.spotify.com/track/6DXLO8LndZMVOHM0wNbpzg"],
    ["Christina Perri", "jar of hearts", 2010, 2011, "YES - Original from 2010", "https://open.spotify.com/track/0HZhYMZOcUzZKSFwPOti6m"],
    ["Creedence Clearwater Revival", "Have You Ever Seen The Rain", 1970, 1970, "No", "https://open.spotify.com/track/5DnT9a5IM3eMjKgXTWVJvi"],
    ["Del Shannon", "Runaway", 1961, 1961, "No", "https://open.spotify.com/track/45Szkclj1lt4ubm7RFK68t"],
    ["Spice Girls", "Stop", 1998, 1998, "No", "https://open.spotify.com/track/7Lhab3DxvzKQXlsp1qJ7jR"],
    ["The Nutmegs", "A Story Untold", 1955, 1955, "No", "https://open.spotify.com/track/4j1OipRUWu0PtAM4GrzVJ6"],
    ["Big Joe Turner", "Shake, Rattle & Roll", 1954, 1951, "YES - Original from 1954", "https://open.spotify.com/track/2Wsg5tP0RsNf6O4HLwvpq6"]
]

def create_corrected_csv():
    """Create a CSV file with corrected release years"""
    
    # Count corrections needed
    corrections_needed = sum(1 for row in corrected_music_data[1:] if row[4] == "YES")
    total_songs = len(corrected_music_data) - 1  # Subtract header
    
    print(f"Analysis Complete:")
    print(f"Total songs analyzed: {total_songs}")
    print(f"Corrections needed: {corrections_needed}")
    print(f"Percentage requiring correction: {corrections_needed/total_songs*100:.1f}%")
    
    # Create the corrected dataset for your music app
    final_data = []
    final_data.append(["Artist", "Song Name", "Album Release Year", "URL"])  # Header
    
    # Add all songs with corrected years
    for row in corrected_music_data[1:]:
        artist, song, correct_year, listed_year, needs_correction, url = row
        # Use the correct year for the final dataset
        final_data.append([artist, song, correct_year, url])
    
    # Write to CSV
    with open('corrected_music_database.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(final_data)
    
    print(f"\nCorrected database saved as 'corrected_music_database.csv'")
    
    # Also create a summary of corrections
    correction_summary = []
    correction_summary.append(["Artist", "Song Name", "Original Year", "Listed Year", "Issue"])
    
    for row in corrected_music_data[1:]:
        if row[4] == "YES":
            correction_summary.append([row[0], row[1], row[2], row[3], row[4]])
    
    with open('correction_summary.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(correction_summary)
    
    print(f"Correction summary saved as 'correction_summary.csv'")
    
    return final_data

def print_major_corrections():
    """Print the most significant corrections needed"""
    print("\n=== MAJOR CORRECTIONS NEEDED ===")
    major_corrections = [
        ("Chumbawamba", "Tubthumping", "1997", "2023", "26 years off!"),
        ("TOTO", "Africa", "1982", "2015", "33 years off!"),
        ("Guns N' Roses", "Sweet Child O' Mine", "1987", "2004", "17 years off!"),
        ("The Smiths", "How Soon Is Now?", "1984", "1998", "14 years off!"),
        ("Billy Joel", "Piano Man", "1973", "2000", "27 years off!"),
    ]


"""Main function to run the music database correction"""
print("Starting music database correction...")

# Create the corrected CSV
create_corrected_csv()

print("\nMusic database correction completed successfully!")