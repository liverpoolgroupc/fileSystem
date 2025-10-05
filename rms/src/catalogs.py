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
<<<<<<< HEAD
    # 大洋洲
    "Australia", "New Zealand",
]

# “国家 -> 主要城市”映射（可继续扩充）
=======
    # Oceania
    "Australia", "New Zealand",
]

# Country → Major Cities mapping (extensible)
>>>>>>> 3e9480169e251baa2428df129cc69d33e104ebe8
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

<<<<<<< HEAD
# 供航班 Start/EndCity 使用的“全局热门城市清单”
CITY_CATALOG: List[str] = sorted({c for lst in COUNTRY_TO_CITIES.values() for c in lst})
=======
# Global Popular Cities List
CITY_CATALOG: List[str] = sorted(
    {c for lst in COUNTRY_TO_CITIES.values() for c in lst})
>>>>>>> 3e9480169e251baa2428df129cc69d33e104ebe8
