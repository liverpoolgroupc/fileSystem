from typing import List, Dict

# Major countries (official full names, at least 50)
COUNTRY_CATALOG: List[str] = [
    # North America
    "United States", "Canada", "Mexico",
    # Sourth America
    "Brazil", "Argentina", "Chile", "Colombia", "Peru", "Venezuela",
    "Uruguay", "Paraguay", "Ecuador",
    # Europe
    "United Kingdom", "Ireland", "France", "Germany", "Spain", "Portugal",
    "Italy", "Netherlands", "Belgium", "Luxembourg", "Switzerland", "Austria",
    "Monaco", "Liechtenstein",
    # Europe
    "Norway", "Sweden", "Finland", "Denmark", "Iceland",
    "Poland", "Czechia", "Hungary", "Romania", "Bulgaria", "Slovakia",
    "Slovenia", "Croatia", "Greece", "Türkiye", "Ukraine",
    # Middle East
    "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Oman", "Bahrain", "Israel",
    # Africa
    "Egypt", "South Africa", "Nigeria", "Kenya", "Morocco", "Algeria", "Tunisia", "Ethiopia", "Tanzania",
    # Asia
    "China", "Japan", "South Korea", "Hong Kong", "Macao", "Taiwan",
    "India", "Pakistan", "Bangladesh", "Sri Lanka",
    "Singapore", "Malaysia", "Thailand", "Vietnam", "Philippines", "Indonesia",
    "Cambodia", "Laos", "Myanmar", "Mongolia", "Nepal",
    # Oceania
    "Australia", "New Zealand",
]

# Country → Major Cities mapping (extensible)
COUNTRY_TO_CITIES: Dict[str, List[str]] = {
    "United States": ["New York", "Los Angeles", "San Francisco", "Seattle", "Chicago", "Boston", "Houston", "Miami"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Ottawa"],
    "Mexico": ["Mexico City", "Guadalajara", "Monterrey"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília"],
    "Argentina": ["Buenos Aires", "Cordoba", "Rosario"],
    "Chile": ["Santiago", "Valparaiso"],
    "Colombia": ["Bogotá", "Medellín", "Cali"],
    "Peru": ["Lima", "Cusco"],
    "Venezuela": ["Caracas", "Maracaibo"],
    "Uruguay": ["Montevideo"],
    "Paraguay": ["Asunción"],
    "Ecuador": ["Quito", "Guayaquil"],

    "United Kingdom": ["London", "Manchester", "Birmingham", "Edinburgh"],
    "Ireland": ["Dublin", "Cork"],
    "France": ["Paris", "Lyon", "Marseille"],
    "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville"],
    "Portugal": ["Lisbon", "Porto"],
    "Italy": ["Rome", "Milan", "Florence", "Naples"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht"],
    "Belgium": ["Brussels", "Antwerp"],
    "Luxembourg": ["Luxembourg City"],
    "Switzerland": ["Zurich", "Geneva", "Basel"],
    "Austria": ["Vienna", "Salzburg"],
    "Monaco": ["Monaco"],
    "Liechtenstein": ["Vaduz"],

    "Norway": ["Oslo", "Bergen"],
    "Sweden": ["Stockholm", "Gothenburg"],
    "Finland": ["Helsinki", "Tampere"],
    "Denmark": ["Copenhagen", "Aarhus"],
    "Iceland": ["Reykjavik"],
    "Poland": ["Warsaw", "Krakow", "Gdansk"],
    "Czechia": ["Prague", "Brno"],
    "Hungary": ["Budapest", "Debrecen"],
    "Romania": ["Bucharest", "Cluj-Napoca"],
    "Bulgaria": ["Sofia", "Plovdiv"],
    "Slovakia": ["Bratislava", "Košice"],
    "Slovenia": ["Ljubljana", "Maribor"],
    "Croatia": ["Zagreb", "Split"],
    "Greece": ["Athens", "Thessaloniki"],
    "Türkiye": ["Istanbul", "Ankara", "Izmir"],
    "Ukraine": ["Kyiv", "Lviv"],

    "United Arab Emirates": ["Dubai", "Abu Dhabi"],
    "Saudi Arabia": ["Riyadh", "Jeddah", "Dammam"],
    "Qatar": ["Doha"],
    "Kuwait": ["Kuwait City"],
    "Oman": ["Muscat"],
    "Bahrain": ["Manama"],
    "Israel": ["Tel Aviv", "Jerusalem", "Haifa"],

    "Egypt": ["Cairo", "Alexandria", "Giza"],
    "South Africa": ["Johannesburg", "Cape Town", "Durban"],
    "Nigeria": ["Lagos", "Abuja"],
    "Kenya": ["Nairobi", "Mombasa"],
    "Morocco": ["Casablanca", "Rabat", "Marrakesh"],
    "Algeria": ["Algiers", "Oran"],
    "Tunisia": ["Tunis", "Sfax"],
    "Ethiopia": ["Addis Ababa", "Dire Dawa"],
    "Tanzania": ["Dar es Salaam", "Arusha"],

    "China": ["Beijing", "Shanghai", "Shenzhen", "Guangzhou", "Chengdu", "Hangzhou", "Wuhan"],
    "Japan": ["Tokyo", "Osaka", "Nagoya", "Fukuoka", "Sapporo"],
    "South Korea": ["Seoul", "Busan", "Incheon"],
    "Hong Kong": ["Hong Kong"],
    "Macao": ["Macao"],
    "Taiwan": ["Taipei", "Taichung", "Kaohsiung"],
    "India": ["New Delhi", "Mumbai", "Bengaluru", "Chennai"],
    "Pakistan": ["Karachi", "Lahore", "Islamabad"],
    "Bangladesh": ["Dhaka", "Chittagong"],
    "Sri Lanka": ["Colombo", "Kandy"],
    "Singapore": ["Singapore"],
    "Malaysia": ["Kuala Lumpur", "Penang", "Johor Bahru"],
    "Thailand": ["Bangkok", "Chiang Mai", "Phuket"],
    "Vietnam": ["Hanoi", "Ho Chi Minh City", "Da Nang"],
    "Philippines": ["Manila", "Cebu", "Davao"],
    "Indonesia": ["Jakarta", "Surabaya", "Bali"],
    "Cambodia": ["Phnom Penh", "Siem Reap"],
    "Laos": ["Vientiane", "Luang Prabang"],
    "Myanmar": ["Yangon", "Mandalay"],
    "Mongolia": ["Ulaanbaatar"],
    "Nepal": ["Kathmandu", "Pokhara"],

    "Australia": ["Sydney", "Melbourne", "Brisbane"],
    "New Zealand": ["Auckland", "Wellington", "Christchurch"],
}

# catalogs.py

# -----------------------------
# Country → States/Provinces
# -----------------------------
COUNTRY_TO_STATES: Dict[str, List[str]] = {
    # North America
    "United States": [
        "New York", "California", "Washington", "Illinois", "Massachusetts", "Texas", "Florida"
    ],
    "Canada": ["Ontario", "British Columbia", "Quebec"],
    "Mexico": ["Mexico City (CDMX)", "Jalisco", "Nuevo León"],

    # South America
    "Brazil": ["São Paulo", "Rio de Janeiro", "Distrito Federal"],
    "Argentina": ["Buenos Aires", "Córdoba", "Santa Fe"],
    "Chile": ["Región Metropolitana de Santiago", "Valparaíso Region"],
    "Colombia": ["Bogotá Capital District", "Antioquia", "Valle del Cauca"],
    "Peru": ["Lima Province", "Cusco"],
    "Venezuela": ["Capital District", "Zulia"],
    "Uruguay": ["Montevideo Department"],
    "Paraguay": ["Asunción (Capital District)"],
    "Ecuador": ["Pichincha", "Guayas"],

    # Western Europe
    "United Kingdom": ["England", "Scotland"],
    "Ireland": ["County Dublin", "County Cork"],
    "France": ["Île-de-France", "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur"],
    "Germany": ["Berlin", "Bavaria", "Hesse", "Hamburg"],
    "Spain": ["Community of Madrid", "Catalonia", "Valencian Community", "Andalusia"],
    "Portugal": ["Lisbon District", "Porto District"],
    "Italy": ["Lazio", "Lombardy", "Tuscany", "Campania"],
    "Netherlands": ["North Holland", "South Holland", "Utrecht"],
    "Belgium": ["Brussels-Capital Region", "Antwerp"],
    "Luxembourg": ["Luxembourg"],
    "Switzerland": ["Zürich", "Geneva", "Basel-Stadt"],
    "Austria": ["Vienna", "Salzburg"],
    "Monaco": ["Monaco"],
    "Liechtenstein": ["Vaduz"],

    # Central/Eastern/Northern Europe
    "Norway": ["Oslo", "Vestland"],
    "Sweden": ["Stockholm County", "Västra Götaland County"],
    "Finland": ["Uusimaa", "Pirkanmaa"],
    "Denmark": ["Capital Region of Denmark", "Central Denmark Region"],
    "Iceland": ["Capital Region"],
    "Poland": ["Masovian", "Lesser Poland", "Pomeranian"],
    "Czechia": ["Prague", "South Moravian"],
    "Hungary": ["Budapest", "Hajdú-Bihar"],
    "Romania": ["Bucharest", "Cluj"],
    "Bulgaria": ["Sofia City Province", "Plovdiv Province"],
    "Slovakia": ["Bratislava Region", "Košice Region"],
    "Slovenia": ["Central Slovenia", "Drava"],
    "Croatia": ["City of Zagreb", "Split-Dalmatia"],
    "Greece": ["Attica", "Central Macedonia"],
    "Türkiye": ["Istanbul", "Ankara", "Izmir"],
    "Ukraine": ["Kyiv City", "Lviv Oblast"],

    # Middle East
    "United Arab Emirates": ["Dubai", "Abu Dhabi"],
    "Saudi Arabia": ["Riyadh Province", "Makkah Province", "Eastern Province"],
    "Qatar": ["Doha"],
    "Kuwait": ["Al Asimah (Capital)"],
    "Oman": ["Muscat"],
    "Bahrain": ["Capital Governorate"],
    "Israel": ["Tel Aviv District", "Jerusalem District", "Haifa District"],

    # Africa
    "Egypt": ["Cairo Governorate", "Alexandria Governorate", "Giza Governorate"],
    "South Africa": ["Gauteng", "Western Cape", "KwaZulu-Natal"],
    "Nigeria": ["Lagos", "Federal Capital Territory"],
    "Kenya": ["Nairobi County", "Mombasa County"],
    "Morocco": ["Casablanca-Settat", "Rabat-Salé-Kénitra", "Marrakech-Safi"],
    "Algeria": ["Algiers Province", "Oran Province"],
    "Tunisia": ["Tunis Governorate", "Sfax Governorate"],
    "Ethiopia": ["Addis Ababa", "Dire Dawa"],
    "Tanzania": ["Dar es Salaam Region", "Arusha Region"],

    # Asia
    "China": ["Beijing", "Shanghai", "Guangdong", "Sichuan", "Zhejiang", "Hubei"],
    "Japan": ["Tokyo", "Osaka", "Aichi", "Fukuoka", "Hokkaido"],
    "South Korea": ["Seoul", "Busan", "Incheon"],
    "Hong Kong": ["Hong Kong"],
    "Macao": ["Macao"],
    "Taiwan": ["Taipei City", "Taichung City", "Kaohsiung City"],
    "India": ["Delhi (NCT)", "Maharashtra", "Karnataka", "Tamil Nadu"],
    "Pakistan": ["Sindh", "Punjab", "Islamabad Capital Territory"],
    "Bangladesh": ["Dhaka Division", "Chittagong Division"],
    "Sri Lanka": ["Western Province", "Central Province"],
    "Singapore": ["Singapore"],
    "Malaysia": ["Kuala Lumpur Federal Territory", "Penang", "Johor"],
    "Thailand": ["Bangkok", "Chiang Mai", "Phuket"],
    "Vietnam": ["Hanoi", "Ho Chi Minh City", "Da Nang"],
    "Philippines": ["Metro Manila (NCR)", "Cebu Province", "Davao Region"],
    "Indonesia": ["Jakarta (DKI)", "East Java", "Bali Province"],
    "Cambodia": ["Phnom Penh", "Siem Reap Province"],
    "Laos": ["Vientiane Prefecture", "Luang Prabang Province"],
    "Myanmar": ["Yangon Region", "Mandalay Region"],
    "Mongolia": ["Ulaanbaatar"],
    "Nepal": ["Bagmati Province", "Gandaki Province"],

    # Oceania
    "Australia": ["New South Wales", "Victoria", "Queensland"],
    "New Zealand": ["Auckland Region", "Wellington Region", "Canterbury Region"],
}

# -----------------------------
# City → State/Province (per country)
# -----------------------------
CITY_TO_STATE: Dict[str, Dict[str, str]] = {
    "United States": {
        "New York": "New York",
        "Los Angeles": "California",
        "San Francisco": "California",
        "Seattle": "Washington",
        "Chicago": "Illinois",
        "Boston": "Massachusetts",
        "Houston": "Texas",
        "Miami": "Florida",
    },
    "Canada": {
        "Toronto": "Ontario",
        "Vancouver": "British Columbia",
        "Montreal": "Quebec",
        "Ottawa": "Ontario",
    },
    "Mexico": {
        "Mexico City": "Mexico City (CDMX)",
        "Guadalajara": "Jalisco",
        "Monterrey": "Nuevo León",
    },

    "Brazil": {
        "São Paulo": "São Paulo",
        "Rio de Janeiro": "Rio de Janeiro",
        "Brasília": "Distrito Federal",
    },
    "Argentina": {
        "Buenos Aires": "Buenos Aires",
        "Cordoba": "Córdoba",
        "Rosario": "Santa Fe",
    },
    "Chile": {
        "Santiago": "Región Metropolitana de Santiago",
        "Valparaiso": "Valparaíso Region",
    },
    "Colombia": {
        "Bogotá": "Bogotá Capital District",
        "Medellín": "Antioquia",
        "Cali": "Valle del Cauca",
    },
    "Peru": {
        "Lima": "Lima Province",
        "Cusco": "Cusco",
    },
    "Venezuela": {
        "Caracas": "Capital District",
        "Maracaibo": "Zulia",
    },
    "Uruguay": {
        "Montevideo": "Montevideo Department",
    },
    "Paraguay": {
        "Asunción": "Asunción (Capital District)",
    },
    "Ecuador": {
        "Quito": "Pichincha",
        "Guayaquil": "Guayas",
    },

    "United Kingdom": {
        "London": "England",
        "Manchester": "England",
        "Birmingham": "England",
        "Edinburgh": "Scotland",
    },
    "Ireland": {
        "Dublin": "County Dublin",
        "Cork": "County Cork",
    },
    "France": {
        "Paris": "Île-de-France",
        "Lyon": "Auvergne-Rhône-Alpes",
        "Marseille": "Provence-Alpes-Côte d'Azur",
    },
    "Germany": {
        "Berlin": "Berlin",
        "Munich": "Bavaria",
        "Frankfurt": "Hesse",
        "Hamburg": "Hamburg",
    },
    "Spain": {
        "Madrid": "Community of Madrid",
        "Barcelona": "Catalonia",
        "Valencia": "Valencian Community",
        "Seville": "Andalusia",
    },
    "Portugal": {
        "Lisbon": "Lisbon District",
        "Porto": "Porto District",
    },
    "Italy": {
        "Rome": "Lazio",
        "Milan": "Lombardy",
        "Florence": "Tuscany",
        "Naples": "Campania",
    },
    "Netherlands": {
        "Amsterdam": "North Holland",
        "Rotterdam": "South Holland",
        "Utrecht": "Utrecht",
    },
    "Belgium": {
        "Brussels": "Brussels-Capital Region",
        "Antwerp": "Antwerp",
    },
    "Luxembourg": {
        "Luxembourg City": "Luxembourg",
    },
    "Switzerland": {
        "Zurich": "Zürich",
        "Geneva": "Geneva",
        "Basel": "Basel-Stadt",
    },
    "Austria": {
        "Vienna": "Vienna",
        "Salzburg": "Salzburg",
    },
    "Monaco": {"Monaco": "Monaco"},
    "Liechtenstein": {"Vaduz": "Vaduz"},

    "Norway": {"Oslo": "Oslo", "Bergen": "Vestland"},
    "Sweden": {"Stockholm": "Stockholm County", "Gothenburg": "Västra Götaland County"},
    "Finland": {"Helsinki": "Uusimaa", "Tampere": "Pirkanmaa"},
    "Denmark": {"Copenhagen": "Capital Region of Denmark", "Aarhus": "Central Denmark Region"},
    "Iceland": {"Reykjavik": "Capital Region"},
    "Poland": {"Warsaw": "Masovian", "Krakow": "Lesser Poland", "Gdansk": "Pomeranian"},
    "Czechia": {"Prague": "Prague", "Brno": "South Moravian"},
    "Hungary": {"Budapest": "Budapest", "Debrecen": "Hajdú-Bihar"},
    "Romania": {"Bucharest": "Bucharest", "Cluj-Napoca": "Cluj"},
    "Bulgaria": {"Sofia": "Sofia City Province", "Plovdiv": "Plovdiv Province"},
    "Slovakia": {"Bratislava": "Bratislava Region", "Košice": "Košice Region"},
    "Slovenia": {"Ljubljana": "Central Slovenia", "Maribor": "Drava"},
    "Croatia": {"Zagreb": "City of Zagreb", "Split": "Split-Dalmatia"},
    "Greece": {"Athens": "Attica", "Thessaloniki": "Central Macedonia"},
    "Türkiye": {"Istanbul": "Istanbul", "Ankara": "Ankara", "Izmir": "Izmir"},
    "Ukraine": {"Kyiv": "Kyiv City", "Lviv": "Lviv Oblast"},

    "United Arab Emirates": {"Dubai": "Dubai", "Abu Dhabi": "Abu Dhabi"},
    "Saudi Arabia": {"Riyadh": "Riyadh Province", "Jeddah": "Makkah Province", "Dammam": "Eastern Province"},
    "Qatar": {"Doha": "Doha"},
    "Kuwait": {"Kuwait City": "Al Asimah (Capital)"},
    "Oman": {"Muscat": "Muscat"},
    "Bahrain": {"Manama": "Capital Governorate"},
    "Israel": {"Tel Aviv": "Tel Aviv District", "Jerusalem": "Jerusalem District", "Haifa": "Haifa District"},

    "Egypt": {"Cairo": "Cairo Governorate", "Alexandria": "Alexandria Governorate", "Giza": "Giza Governorate"},
    "South Africa": {"Johannesburg": "Gauteng", "Cape Town": "Western Cape", "Durban": "KwaZulu-Natal"},
    "Nigeria": {"Lagos": "Lagos", "Abuja": "Federal Capital Territory"},
    "Kenya": {"Nairobi": "Nairobi County", "Mombasa": "Mombasa County"},
    "Morocco": {"Casablanca": "Casablanca-Settat", "Rabat": "Rabat-Salé-Kénitra", "Marrakesh": "Marrakech-Safi"},
    "Algeria": {"Algiers": "Algiers Province", "Oran": "Oran Province"},
    "Tunisia": {"Tunis": "Tunis Governorate", "Sfax": "Sfax Governorate"},
    "Ethiopia": {"Addis Ababa": "Addis Ababa", "Dire Dawa": "Dire Dawa"},
    "Tanzania": {"Dar es Salaam": "Dar es Salaam Region", "Arusha": "Arusha Region"},

    "China": {
        "Beijing": "Beijing",
        "Shanghai": "Shanghai",
        "Shenzhen": "Guangdong",
        "Guangzhou": "Guangdong",
        "Chengdu": "Sichuan",
        "Hangzhou": "Zhejiang",
        "Wuhan": "Hubei",
    },
    "Japan": {
        "Tokyo": "Tokyo",
        "Osaka": "Osaka",
        "Nagoya": "Aichi",
        "Fukuoka": "Fukuoka",
        "Sapporo": "Hokkaido",
    },
    "South Korea": {
        "Seoul": "Seoul",
        "Busan": "Busan",
        "Incheon": "Incheon",
    },
    "Hong Kong": {"Hong Kong": "Hong Kong"},
    "Macao": {"Macao": "Macao"},
    "Taiwan": {"Taipei": "Taipei City", "Taichung": "Taichung City", "Kaohsiung": "Kaohsiung City"},
    "India": {
        "New Delhi": "Delhi (NCT)",
        "Mumbai": "Maharashtra",
        "Bengaluru": "Karnataka",
        "Chennai": "Tamil Nadu",
    },
    "Pakistan": {
        "Karachi": "Sindh",
        "Lahore": "Punjab",
        "Islamabad": "Islamabad Capital Territory",
    },
    "Bangladesh": {"Dhaka": "Dhaka Division", "Chittagong": "Chittagong Division"},
    "Sri Lanka": {"Colombo": "Western Province", "Kandy": "Central Province"},
    "Singapore": {"Singapore": "Singapore"},
    "Malaysia": {"Kuala Lumpur": "Kuala Lumpur Federal Territory", "Penang": "Penang", "Johor Bahru": "Johor"},
    "Thailand": {"Bangkok": "Bangkok", "Chiang Mai": "Chiang Mai", "Phuket": "Phuket"},
    "Vietnam": {"Hanoi": "Hanoi", "Ho Chi Minh City": "Ho Chi Minh City", "Da Nang": "Da Nang"},
    "Philippines": {"Manila": "Metro Manila (NCR)", "Cebu": "Cebu Province", "Davao": "Davao Region"},
    "Indonesia": {"Jakarta": "Jakarta (DKI)", "Surabaya": "East Java", "Bali": "Bali Province"},
    "Cambodia": {"Phnom Penh": "Phnom Penh", "Siem Reap": "Siem Reap Province"},
    "Laos": {"Vientiane": "Vientiane Prefecture", "Luang Prabang": "Luang Prabang Province"},
    "Myanmar": {"Yangon": "Yangon Region", "Mandalay": "Mandalay Region"},
    "Mongolia": {"Ulaanbaatar": "Ulaanbaatar"},
    "Nepal": {"Kathmandu": "Bagmati Province", "Pokhara": "Gandaki Province"},

    "Australia": {"Sydney": "New South Wales", "Melbourne": "Victoria", "Brisbane": "Queensland"},
    "New Zealand": {"Auckland": "Auckland Region", "Wellington": "Wellington Region", "Christchurch": "Canterbury Region"},
}


# Global Popular Cities List
CITY_CATALOG: List[str] = sorted(
    {c for lst in COUNTRY_TO_CITIES.values() for c in lst})
