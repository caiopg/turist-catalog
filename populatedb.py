from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import DB_PATH, Base, Country, Attraction, User

''' populatedb is used to populate the db with some information related to
countries and their attraction points.
'''

engine = create_engine(DB_PATH)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create the admin user. All countries and attractions created here will be
# associated with him.
admin = User(
    name='Bilbo Baggins',
    email="bilbo.baggins@precious.com")

session.add(admin)

# Create Brazil.
brazil = Country(
    user=admin,
    name="Brazil",
    description="Brazil, officially the Federative Republic of Brazil, "
                "is the largest country in both South America and Latin "
                "America. At 8.5 million square kilometers (3.2 million "
                "square miles) and with over 208 million people, Brazil is "
                "the world's fifth-largest country by area and the "
                "sixth-most populous. The capital is Brasília, and the "
                "most-populated city is São Paulo. It is the largest country "
                "to have Portuguese as an official language and the only one "
                "in the Americas. Bounded by the Atlantic Ocean on the east, "
                "Brazil has a coastline of 7,491 kilometers (4,655 mi). It "
                "borders all other South American countries except Ecuador "
                "and Chile and covers 47.3% of the continent's land area. "
                "Its Amazon River basin includes a vast tropical forest, "
                "home to diverse wildlife, a variety of ecological systems, "
                "and extensive natural resources spanning numerous protected "
                "habitats. This unique environmental heritage makes Brazil "
                "one of 17 megadiverse countries, and is the subject of "
                "significant global interest and debate regarding "
                "deforestation and environmental protection.")

session.add(brazil)

# Create Sugar Loaf and associate with Brazil.
sugar_loaf = Attraction(
    user=admin,
    name="Sugar Loaf Mountain",
    city="Rio de Janeiro",
    description="Sugarloaf Mountain is a peak situated in Rio de Janeiro, "
                "Brazil, at the mouth of Guanabara Bay on a peninsula that "
                "juts out into the Atlantic Ocean. Rising 396 m (1,299 ft) "
                "above the harbor, its name is said to refer to its "
                "resemblance to the traditional shape of concentrated "
                "refined loaf sugar. It is known worldwide for its cableway "
                "and panoramic views of the city.",
    country=brazil)

session.add(sugar_loaf)

# Create Christ The Redeemer and associate with Brazil.
christ_redeemer = Attraction(
    user=admin,
    name="Christ the Redeemer",
    city="Rio de Janeiro",
    description="Christ the Redeemer is an Art Deco statue of Jesus Christ "
                "in Rio de Janeiro, Brazil, created by French sculptor Paul "
                "Landowski and built by the Brazilian engineer Heitor da "
                "Silva Costa, in collaboration with the French engineer "
                "Albert Caquot. Romanian sculptor Gheorghe Leonida fashioned "
                "the face. Constructed between 1922 and 1931, the statue is "
                "30 metres (98 ft) tall, excluding its 8-metre (26 ft) "
                "pedestal. The arms stretch 28 metres (92 ft) wide. ",
    country=brazil)

session.add(christ_redeemer)

# Create Ibirapuera Park and associate with Brazil.
ibirapuera = Attraction(
    user=admin,
    name="Ibirapuera Park",
    city="São Paulo",
    description="Ibirapuera Park (Portuguese: Parque Ibirapuera) is a major "
                "urban park in São Paulo, Brazil. It has a large area for "
                "leisure, jogging and walking, as well a vivid cultural "
                "scene with museums and a music hall. Its importance to São "
                "Paulo is often comparable to that of Central Park to New "
                "York City, Golden Gate Park to San Francisco, or Ueno Park "
                "to Tokyo. Ibirapuera is one of Latin America's largest city "
                "parks, together with Chapultepec Park in Mexico City and "
                "Simón Bolívar Park in Bogota.",
    country=brazil)

session.add(ibirapuera)

# Create France.
france = Country(
    user=admin,
    name="France",
    description="France, officially the French Republic (French: République "
                "française, pronounced [ʁepyblik fʁɑ̃sɛz]), is a country "
                "whose territory consists of metropolitan France in western "
                "Europe, as well as several overseas regions and "
                "territories. The metropolitan area of France extends from "
                "the Mediterranean Sea to the English Channel and the North "
                "Sea, and from the Rhine to the Atlantic Ocean. The overseas "
                "territories include French Guiana in South America and "
                "several islands in the Atlantic, Pacific and Indian oceans. "
                "The country's 18 integral regions (five of which are "
                "situated overseas) span a combined area of 643,801 square "
                "kilometres (248,573 sq mi) which, as of October 2017, "
                "has a population of 67.15 million people. France is a "
                "unitary semi-presidential republic with its capital in "
                "Paris, the country's largest city and main cultural and "
                "commercial centre. Other major urban centres include "
                "Marseille, Lyon, Lille, Nice, Toulouse and Bordeaux.")

session.add(france)

# Create Eiffel Tower and associate it with France.
eiffel_tower = Attraction(
    user=admin,
    name="Eiffel Tower",
    city="Paris",
    description="The Eiffel Tower is a wrought iron lattice tower on the "
                "Champ de Mars in Paris, France. It is named after the "
                "engineer Gustave Eiffel, whose company designed and built "
                "the tower. Constructed from 1887–89 as the entrance to the "
                "1889 World's Fair, it was initially criticized by some of "
                "France's leading artists and intellectuals for its design, "
                "but it has become a global cultural icon of France and one "
                "of the most recognisable structures in the world. The "
                "Eiffel Tower is the most-visited paid monument in the "
                "world; 6.91 million people ascended it in 2015.",
    country=france)

session.add(eiffel_tower)

# Create Louvre and associate it with France.
louvre = Attraction(
    user=admin,
    name="Louvre",
    city="Paris",
    description="The Louvre, is the world's largest art museum and a "
                "historic monument in Paris, France. A central landmark of "
                "the city, it is located on the Right Bank of the Seine in "
                "the city's 1st arrondissement (district or ward). "
                "Approximately 38,000 objects from prehistory to the 21st "
                "century are exhibited over an area of 72,735 square metres "
                "(782,910 square feet).[3] In 2016, the Louvre was the "
                "world's most visited art museum, receiving 7.3 million "
                "visitors.",
    country=france)

session.add(louvre)

# Create the U.S.A.
usa = Country(
    user=admin,
    name="United States of America",
    description="The United States of America (USA), commonly known as the "
                "United States (U.S.) or America, is a federal republic "
                "composed of 50 states, a federal district, five major "
                "self-governing territories, and various possessions. At 3.8 "
                "million square miles (9.8 million km2) and with over 325 "
                "million people, the United States is the world's third- or "
                "fourth-largest country by total area and the third-most "
                "populous. The capital is Washington, D.C., and the largest "
                "city by population is New York City. Forty-eight states and "
                "the capital's federal district are contiguous and located "
                "in North America between Canada and Mexico. The state of "
                "Alaska is in the northwest corner of North America, "
                "bordered by Canada to the east and across the Bering Strait "
                "from Russia to the west. The state of Hawaii is an "
                "archipelago in the mid-Pacific Ocean. The U.S. territories "
                "are scattered about the Pacific Ocean and the Caribbean "
                "Sea, stretching across nine official time zones. The "
                "extremely diverse geography, climate, and wildlife of the "
                "United States make it one of the world's 17 megadiverse "
                "countries.")

session.add(usa)

# Create the Statue of Liberty and associate it with the U.S.A.
statue_liberty = Attraction(
    user=admin,
    name="Statue of Liberty",
    city="New York City",
    description="The Statue of Liberty (Liberty Enlightening the World; "
                "French: La Liberté éclairant le monde) is a colossal "
                "neoclassical sculpture on Liberty Island in New York Harbor "
                "in New York City, in the United States. The copper statue, "
                "a gift from the people of France to the people of the "
                "United States, was designed by French sculptor Frédéric "
                "Auguste Bartholdi and built by Gustave Eiffel. The statue "
                "was dedicated on October 28, 1886.",
    country=usa)

session.add(statue_liberty)

# Create the Golden Gate Bridge and associate it with the U.S.A.
golden_gate_bridge = Attraction(
    user=admin,
    name="Golden Gate Bridge",
    city="San Francisco",
    description="The Golden Gate Bridge is a suspension bridge spanning the "
                "Golden Gate, the one-mile-wide (1.6 km) strait connecting "
                "San Francisco Bay and the Pacific Ocean. The structure "
                "links the American city of San Francisco, California – the "
                "northern tip of the San Francisco Peninsula – to Marin "
                "County, carrying both U.S. Route 101 and California State "
                "Route 1 across the strait. The bridge is one of the most "
                "internationally recognized symbols of San Francisco, "
                "California, and the United States. It has been declared one "
                "of the Wonders of the Modern World by the American Society "
                "of Civil Engineers.",
    country=usa)

session.add(golden_gate_bridge)

# Create Greece.
greece = Country(
    user=admin,
    name="Greece",
    description="Greece is located at the crossroads of Europe, Asia, "
                "and Africa. Situated on the southern tip of the Balkan "
                "peninsula, it shares land borders with Albania to the "
                "northwest, the Republic of Macedonia and Bulgaria to the "
                "north, and Turkey to the northeast. The Aegean Sea lies to "
                "the east of the mainland, the Ionian Sea to the west, "
                "the Cretan Sea and the Mediterranean Sea to the south. "
                "Greece has the longest coastline on the Mediterranean Basin "
                "and the 11th longest coastline in the world at 13,676 km ("
                "8,498 mi) in length, featuring a large number of islands, "
                "of which 227 are inhabited. Eighty percent of Greece is "
                "mountainous, with Mount Olympus being the highest peak at "
                "2,918 metres (9,573 ft). The country consists of nine "
                "geographic regions: Macedonia, Central Greece, "
                "the Peloponnese, Thessaly, Epirus, the Aegean Islands ("
                "including the Dodecanese and Cyclades), Thrace, Crete, "
                "and the Ionian Islands.")

session.add(greece)

# Create the Parthenon and associate it with Greece.
parthenon = Attraction(
    user=admin,
    name="Parthenon",
    city="Athens",
    description="The Parthenon is a former temple, on the Athenian "
                "Acropolis, Greece, dedicated to the goddess Athena, "
                "whom the people of Athens considered their patron. "
                "Construction began in 447 BC when the Athenian Empire was "
                "at the peak of its power. It was completed in 438 BC "
                "although decoration of the building continued until 432 BC. "
                "It is the most important surviving building of Classical "
                "Greece, generally considered the zenith of the Doric order. "
                "Its decorative sculptures are considered some of the high "
                "points of Greek art. The Parthenon is regarded as an "
                "enduring symbol of Ancient Greece, Athenian democracy and "
                "western civilization, and one of the world's greatest "
                "cultural monuments.",
    country=greece)

session.add(parthenon)

# Create Germany.
germany = Country(
    user=admin,
    name="Germany",
    description="Germany, officially the Federal Republic of Germany is a "
                "federal parliamentary republic in central-western Europe. "
                "It includes 16 constituent states, covers an area of 357,"
                "021 square kilometres (137,847 sq mi), and has a largely "
                "temperate seasonal climate. With about 82 million "
                "inhabitants, Germany is the most populous member state of "
                "the European Union. After the United States, it is the "
                "second most popular immigration destination in the world. "
                "Germany's capital and largest metropolis is Berlin, "
                "while its largest conurbation is the Ruhr, with its main "
                "centres of Dortmund and Essen. The country's other major "
                "cities are Hamburg, Munich, Cologne, Frankfurt, Stuttgart, "
                "Düsseldorf, Leipzig, Bremen, Dresden, Hannover and "
                "Nuremberg.")

session.add(germany)

# Create the Berlin Wall and associate it with Germany.
berlin_wall = Attraction(
    user=admin,
    name="Berlin Wall",
    city="Berlin",
    description="The Berlin Wall (German: Berliner Mauer) was a guarded "
                "concrete barrier that physically and ideologically divided "
                "Berlin from 1961 to 1989. Constructed by the German "
                "Democratic Republic (GDR, East Germany), starting on 13 "
                "August 1961, the Wall cut off (by land) West Berlin from "
                "virtually all of surrounding East Germany and East Berlin "
                "until government officials opened it in November 1989. Its "
                "demolition officially began on 13 June 1990 and finished in "
                "1992. The barrier included guard towers placed along large "
                "concrete walls, accompanied by a wide area (later known as "
                "the 'death strip') that contained anti-vehicle trenches, "
                "'fakir beds' and other defenses.",
    country=germany)

session.add(berlin_wall)

# Create the Brandenburg Gate and associate it with Germany.
brandenburg_gate = Attraction(
    user=admin,
    name="Brandenburg Gate",
    city="Berlin",
    description="The Brandenburg Gate (German: Brandenburger Tor) is an "
                "18th-century neoclassical monument in Berlin, built on the "
                "orders of Prussian king Frederick William II after the ("
                "temporarily) successful restoration of order during the "
                "early Batavian Revolution.[1] One of the best-known "
                "landmarks of Germany, it was built on the site of a former "
                "city gate that marked the start of the road from Berlin to "
                "the town of Brandenburg an der Havel, which used to be "
                "capital of the Margraviate of Brandenburg.",
    country=germany)

session.add(brandenburg_gate)

# Create India.
india = Country(
    user=admin,
    name="India",
    description="India, officially the Republic of India (Bhārat Gaṇarājya),"
                "[e] is a country in South Asia. It is the seventh-largest "
                "country by area, the second-most populous country (with "
                "over 1.2 billion people), and the most populous democracy "
                "in the world. It is bounded by the Indian Ocean on the "
                "south, the Arabian Sea on the southwest, and the Bay of "
                "Bengal on the southeast. It shares land borders with "
                "Pakistan to the west;[f] China, Nepal, and Bhutan to the "
                "northeast; and Myanmar (Burma) and Bangladesh to the east. "
                "In the Indian Ocean, India is in the vicinity of Sri Lanka "
                "and the Maldives. India's Andaman and Nicobar Islands share "
                "a maritime border with Thailand and Indonesia.")

session.add(india)

# Create the Taj Mahal and associate it with India.
taj_mahal = Attraction(
    user=admin,
    name="Taj Mahal",
    city="Agra",
    description="The Taj Mahal is an ivory-white marble mausoleum on the "
                "south bank of the Yamuna river in the Indian city of Agra. "
                "It was commissioned in 1632 by the Mughal emperor, "
                "Shah Jahan (reigned from 1628 to 1658), to house the tomb "
                "of his favourite wife, Mumtaz Mahal. The tomb is the "
                "centrepiece of a 17-hectare (42-acre)[5] complex, "
                "which includes a mosque and a guest house, and is set in "
                "formal gardens bounded on three sides by a crenellated "
                "wall.",
    country=india)

session.add(taj_mahal)

# Create England.
england = Country(
    user=admin,
    name="England",
    description="England is a country that is part of the United Kingdom. It "
                "shares land borders with Scotland to the north and Wales to "
                "the west. The Irish Sea lies northwest of England and the "
                "Celtic Sea lies to the southwest. England is separated from "
                "continental Europe by the North Sea to the east and the "
                "English Channel to the south. The country covers "
                "five-eighths of the island of Great Britain (which lies in "
                "the North Atlantic) in its centre and south, and includes "
                "over 100 smaller named islands such as the Isles of Scilly "
                "and the Isle of Wight.")

session.add(england)

# Create the Big Ben and associate it with England.
big_ben = Attraction(
    user=admin,
    name="Big Ben",
    city="London",
    description="Big Ben is the nickname for the Great Bell of the clock at "
                "the north end of the Palace of Westminster in London and is "
                "usually extended to refer to both the clock and the clock "
                "tower. The tower is officially Elizabeth Tower, renamed to "
                "celebrate the Diamond Jubilee of Elizabeth II in 2012; "
                "before that, it was known simply as the Clock Tower.",
    country=england)

session.add(big_ben)

# Create Italy.
italy = Country(
    user=admin,
    name="Italy",
    description="Italy, officially the Italian Republic (Italian: Repubblica "
                "italiana), is a unitary parliamentary republic in Europe. "
                "Located in the heart of the Mediterranean Sea, Italy shares "
                "open land borders with France, Switzerland, Austria, "
                "Slovenia, San Marino and Vatican City. Italy covers an area "
                "of 301,338 km2 (116,347 sq mi) and has a largely temperate "
                "seasonal and Mediterranean climate. With around 61 million "
                "inhabitants it is the fourth most populous EU member state.")

session.add(italy)

# Create the Coliseum and associate it with Italy.
coliseum = Attraction(
    user=admin,
    name="Coliseum",
    city="Rome",
    description="The Colosseum or Coliseum, also known as the Flavian "
                "Amphitheatre, is an oval amphitheatre in the centre of the "
                "city of Rome, Italy. Built of travertine, tuff, "
                "and brick-faced concrete, it is the largest amphitheatre "
                "ever built. The Colosseum is situated just east of the "
                "Roman Forum. Construction began under the emperor Vespasian "
                "in AD 72, and was completed in AD 80 under his successor "
                "and heir Titus. Further modifications were made during the "
                "reign of Domitian (81–96). These three emperors are known "
                "as the Flavian dynasty, and the amphitheatre was named in "
                "Latin for its association with their family name (Flavius)",
    country=italy)

session.add(coliseum)

# Create Japan.
japan = Country(
    user=admin,
    name="Japan",
    description="Japan is a sovereign island nation in East Asia. Located in "
                "the Pacific Ocean, it lies off the eastern coast of the "
                "Asian mainland and stretches from the Sea of Okhotsk in the "
                "north to the East China Sea and China in the southwest. The "
                "kanji, or Sino-Japanese characters, that make up Japan's "
                "name mean 'sun origin', and it is often called the 'Land of "
                "the Rising Sun'. Japan is a stratovolcanic archipelago "
                "consisting of about 6,852 islands. The four largest are "
                "Honshu, Hokkaido, Kyushu and Shikoku, which make up about "
                "ninety-seven percent of Japan's land area and often are "
                "referred to as home islands. The country is divided into 47 "
                "prefectures in eight regions, with Hokkaido being the "
                "northernmost prefecture and Okinawa being the southernmost "
                "one.")

session.add(japan)

# Create Tokyo Tower and associate it with Japan.
tokyo_tower = Attraction(
    user=admin,
    name="Tokyo Tower",
    city="Tokyo",
    description="Tokyo Tower is a communications and observation tower in "
                "the Shiba-koen district of Minato, Tokyo, Japan. At 332.9 "
                "metres (1,092 ft), it is the second-tallest structure in "
                "Japan. The structure is an Eiffel Tower-inspired lattice "
                "tower that is painted white and international orange to "
                "comply with air safety regulations.",
    country=japan)

session.add(tokyo_tower)

session.commit()
