import re
import asyncio
from telethon import TelegramClient, events

# =================== TELEGRAM API ===================
api_id = 31975448
api_hash = '15378c6dc7237a5d32836e6495117a0c'

# =================== TELEGRAM CLIENT ===================
client = TelegramClient(
    "taxi_session",          # session nomi
    api_id,
    api_hash,
    device_model="PC 64bit",
    system_version="Windows 10",
    app_version="Telegram 9.12.1"
)

# =================== SKIP CHAT ID ===================
SKIP_CHAT_IDS = [
    -1003766812597
]

# =================== TARGET CHAT ID ===================
TARGET_CHAT_IDS = [
    -1003766812597
]

# =================== KALIT SO'ZLAR ===================
KEYWORDS = [
    "qoshimcha yuk bor", "qoshimcha yuk borakan",
    "qoshimcha yuk chiqdi", "qoshimcha yuk ketadi",
    "qoshimcha yuk bor edi", "qoshimcha yuk borakan",
    "qoshimcha yuk bor ekan", "qoshimcha yuk bor ekan edi",
    "qo'shimcha yuk bor ekan aka", "qo'shimcha yuk bor ekan aka",
    "qo'shimcha yukla bor", "qo'shimcha yuk bor edi aka", "qo'shimcha yuk bor ekan edi",
    "qowimcha yuk bor ekan edi", "qo'shimcha yuk bor ekan edi",
    "quwimca yuk bor ekan edi", "qo'shimcha yuk bor ekan edi",
    "yuk bor 500kg", "yuk bor 500 kg", "yuk bor 500 kilo", "yuk bor 500 kilogramm",
    "yuk bor 500 kg bor", "yuk bor 500kg bor", "1 tona yuk bor", "1 tonna yuk bor", "1 ton yuk bor", "1 ton yuk bor ekan",  
    "1 tonna yuk bor ekan", "1 tonna yuk bor edi", "1 ton yuk bor edi", "1 ton yuk bor ekan edi", "1 tonna yuk bor ekan edi",   
    "200 kg qoshimcha yuk bor", "200 kg qo'shimcha yuk bor", "200 kg qo'shimcha yuk bor ekan", "200 kg qo'shimcha yuk bor edi", "200 kg qo'shimcha yuk bor ekan edi",   
    "qushimcha yuk", "qushimcha yuk bor", "qushimcha yuk bor ekan", "qushimcha yuk bor edi", "qushimcha yuk bor ekan edi",  
    "200 kg yuk bor", "200 kg yuk bor ekan", "200 kg yuk bor edi", "200 kg yuk bor ekan edi",   
    "100 kg yuk bor", "100 kg yuk bor ekan", "100 kg yuk bor edi", "100 kg yuk bor ekan edi"

    # 100–900 kg
    "100 kg yuk", "100kg yuk", "100 kilo yuk",
    "100 kilogramm yuk", "100 kg yuk bor",
    "100kg yuk bor", "100 kilolik yuk",
    "150 kg yuk", "150kg yuk", "150 kilo yuk",
    "150 kilogramm yuk", "150 kg yuk bor",
    "150kg yuk bor", "150 kilolik yuk",
    "200 kg yuk", "200kg yuk", "200 kilo yuk",
    "200 kilogramm yuk", "200 kg yuk bor",
    "200kg yuk bor", "200 kilolik yuk",
    "250 kg yuk", "250kg yuk", "250 kilo yuk",
    "250 kilogramm yuk", "250 kg yuk bor",
    "250kg yuk bor", "250 kilolik yuk",
    "300 kg yuk", "300kg yuk", "300 kilo yuk",
    "300 kilogramm yuk", "300 kg yuk bor",
    "300kg yuk bor", "300 kilolik yuk",
    "350 kg yuk", "350kg yuk", "350 kilo yuk",
    "350 kilogramm yuk", "350 kg yuk bor",
    "350kg yuk bor", "350 kilolik yuk",
    "400 kg yuk", "400kg yuk", "400 kilo yuk",
    "400 kilogramm yuk", "400 kg yuk bor",
    "400kg yuk bor", "400 kilolik yuk",
    "450 kg yuk", "450kg yuk", "450 kilo yuk",
    "450 kilogramm yuk", "450 kg yuk bor",
    "450kg yuk bor", "450 kilolik yuk",
    "500 kg yuk", "500kg yuk", "500 kilo yuk",
    "500 kilogramm yuk", "500 kg yuk bor",
    "500kg yuk bor", "500 kilolik yuk",
    "550 kg yuk", "550kg yuk", "550 kilo yuk",
    "550 kilogramm yuk", "550 kg yuk bor",
    "550kg yuk bor", "550 kilolik yuk",
    "600 kg yuk", "600kg yuk", "600 kilo yuk",
    "600 kilogramm yuk", "600 kg yuk bor",
    "600kg yuk bor", "600 kilolik yuk",
    "650 kg yuk", "650kg yuk", "650 kilo yuk",
    "650 kilogramm yuk", "650 kg yuk bor",
    "650kg yuk bor", "650 kilolik yuk",
    "700 kg yuk", "700kg yuk", "700 kilo yuk",
    "700 kilogramm yuk", "700 kg yuk bor",
    "700kg yuk bor", "700 kilolik yuk",
    "750 kg yuk", "750kg yuk", "750 kilo yuk",
    "750 kilogramm yuk", "750 kg yuk bor",
    "750kg yuk bor", "750 kilolik yuk",
    "800 kg yuk", "800kg yuk", "800 kilo yuk",
    "800 kilogramm yuk", "800 kg yuk bor",
    "800kg yuk bor", "800 kilolik yuk",
    "850 kg yuk", "850kg yuk", "850 kilo yuk",
    "850 kilogramm yuk", "850 kg yuk bor",
    "850kg yuk bor", "850 kilolik yuk",
    "900 kg yuk", "900kg yuk", "900 kilo yuk",
    "900 kilogramm yuk", "900 kg yuk bor",
    "900kg yuk bor", "900 kilolik yuk",
    "950 kg yuk", "950kg yuk", "950 kilo yuk",
    "950 kilogramm yuk", "950 kg yuk bor",
    "950kg yuk bor", "950 kilolik yuk",

    # Vazn oldin yoziladigan variantlar
    "100 kg qo'shimcha yuk", "150 kg qo'shimcha yuk",
    "200 kg qo'shimcha yuk", "250 kg qo'shimcha yuk",
    "300 kg qo'shimcha yuk", "350 kg qo'shimcha yuk",
    "400 kg qo'shimcha yuk", "450 kg qo'shimcha yuk",
    "500 kg qo'shimcha yuk", "550 kg qo'shimcha yuk",
    "600 kg qo'shimcha yuk", "650 kg qo'shimcha yuk",
    "700 kg qo'shimcha yuk", "750 kg qo'shimcha yuk",
    "800 kg qo'shimcha yuk", "850 kg qo'shimcha yuk",
    "900 kg qo'shimcha yuk", "950 kg qo'shimcha yuk",

    # Tonna bilan yozilgan yuklar
    "1 tonna yuk", "1tonna yuk", "1 ton yuk",
    "1 tonna yuk bor", "1tonna yuk bor",
    "1 ton yuk bor", "bir tonna yuk",
    "bir tonna yuk bor", "1.0 tonna yuk",
    "1,0 tonna yuk",
    "yarim tonna yuk", "yarim tonna yuk bor",
    "0.5 tonna yuk", "0,5 tonna yuk",
    "1 тонна юк", "1 тонна юк бор", "qo'shimcha 100 kg", "qo'shimcha 150 kg",
    "qo'shimcha 200 kg", "qo'shimcha 250 kg",
    "qo'shimcha 300 kg", "qo'shimcha 350 kg",
    "qo'shimcha 400 kg", "qo'shimcha 450 kg",
    "qo'shimcha 500 kg", "qo'shimcha 550 kg",
    "qo'shimcha 600 kg", "qo'shimcha 650 kg",
    "qo'shimcha 700 kg", "qo'shimcha 750 kg",
    "qo'shimcha 800 kg", "qo'shimcha 850 kg",
    "qo'shimcha 900 kg", "qo'shimcha 950 kg",
    "qo'shimcha 1 tonna", "qoshimcha 1 tonna",
    "qo'shimcha yuk 100 kg", "qo'shimcha yuk 150 kg",
    "qo'shimcha yuk 200 kg", "qo'shimcha yuk 250 kg",
    "qo'shimcha yuk 300 kg", "qo'shimcha yuk 400 kg",
    "qo'shimcha yuk 500 kg", "qo'shimcha yuk 600 kg",
    "qo'shimcha yuk 700 kg", "qo'shimcha yuk 800 kg",
    "qo'shimcha yuk 900 kg", "qo'shimcha yuk 1 tonna",

    # Farg'ona → Toshkent
    "Farg'onadan Toshkentga yuk bor",
    "Fargonadan Toshkentga yuk bor",
    "Farg'onadan Toshkentga yuk",
    "Fargonadan Toshkentga yuk",
    "Farg'onadan Toshkentga qo'shimcha yuk",
    "Farg'onadan Toshkentga 100 kg",
    "Farg'onadan Toshkentga 150 kg",
    "Farg'onadan Toshkentga 200 kg",
    "Farg'onadan Toshkentga 250 kg",
    "Farg'onadan Toshkentga 300 kg",
    "Farg'onadan Toshkentga 400 kg",
    "Farg'onadan Toshkentga 500 kg",
    "Farg'onadan Toshkentga 600 kg",
    "Farg'onadan Toshkentga 700 kg",
    "Farg'onadan Toshkentga 800 kg",
    "Farg'onadan Toshkentga 900 kg",
    "Farg'onadan Toshkentga 1 tonna",
    "Farg'ona Toshkent yuk bor",
    "Farg'ona Toshkentga yuk bor",
    "Farg'onaga yuk bor Toshkentdan",
    "Farg'onadan yuk bor Toshkentga",

    # Toshkent → Farg'ona
    "Toshkentdan Farg'onaga qushimcha yuk bor",
    "Toshkentdan Fargonaga yuk bor",
    "Toshkentdan Farg'onaga yuk",
    "Toshkentdan Fargonaga yuk",
    "Toshkentdan Farg'onaga qo'shimcha yuk",
    "Toshkentdan Farg'onaga 100 kg",
    "Toshkentdan Farg'onaga 150 kg",
    "Toshkentdan Farg'onaga 200 kg",
    "Toshkentdan Farg'onaga 250 kg",
    "Toshkentdan Farg'onaga 300 kg",
    "Toshkentdan Farg'onaga 400 kg",
    "Toshkentdan Farg'onaga 500 kg",
    "Toshkentdan Farg'onaga 600 kg",
    "Toshkentdan Farg'onaga 700 kg",
    "Toshkentdan Farg'onaga 800 kg",
    "Toshkentdan Farg'onaga 900 kg",
    "Toshkentdan Farg'onaga 1 tonna",
    "Toshkent Farg'ona yuk bor",
    "Toshkentdan Farg'onaga ",
    "Toshkentdan yuk bor Farg'onaga",
    "Фарғонадан Тошкентга юк бор",
    "Тошкентдан Фарғонага юк бор",
    "Фарғонадан Тошкентга 100 кг",
    "Фарғонадан Тошкентга 150 кг",
    "Фарғонадан Тошкентга 200 кг",
    "Фарғонадан Тошкентга 250 кг",
    "Фарғонадан Тошкентга 300 кг",
    "Фарғонадан Тошкентга 400 кг",
    "Фарғонадан Тошкентга 500 кг",
    "Фарғонадан Тошкентга 600 кг",
    "Фарғонадан Тошкентга 700 кг",
    "Фарғонадан Тошкентга 800 кг",
    "Фарғонадан Тошкентга 900 кг",
    "Фарғонадан Тошкентга 1 тонна",
    "Тошкентдан Фарғонага 100 кг",
    "Тошкентдан Фарғонага 150 кг",
    "Тошкентдан Фарғонага 200 кг",
    "Тошкентдан Фарғонага 250 кг",
    "Тошкентдан Фарғонага 300 кг",
    "Тошкентдан Фарғонага 400 кг",
    "Тошкентдан Фарғонага 500 кг",
    "Тошкентдан Фарғонага 600 кг",
    "Тошкентдан Фарғонага 700 кг",
    "Тошкентдан Фарғонага 800 кг",
    "Тошкентдан Фарғонага 900 кг",
    "Тошкентдан Фарғонага 1 тонна",
    "қўшимча юк 100 кг", "қўшимча юк 150 кг",
    "қўшимча юк 200 кг", "қўшимча юк 250 кг",
    "қўшимча юк 300 кг", "қўшимча юк 400 кг",
    "қўшимча юк 500 кг", "қўшимча юк 600 кг",
    "қўшимча юк 700 кг", "қўшимча юк 800 кг",
    "қўшимча юк 900 кг", "қўшимча юк 1 тонна",
    "100 кг юк бор", "150 кг юк бор",
    "200 кг юк бор", "250 кг юк бор",
    "300 кг юк бор", "400 кг юк бор",
    "500 кг юк бор", "600 кг юк бор",
    "700 кг юк бор", "800 кг юк бор",
    "900 кг юк бор", "1 тонна юк бор",

    # Boshqa yuk e'lonlari
    "pochta bor", "poshta bor",
    "yuk bor Toshkentga", "yuk bor Farg'onaga",
    "Toshkentga yuk chiqdi", "Farg'onaga yuk chiqdi",
    "Toshkentga yuk bor ekan", "Farg'onaga yuk bor ekan", "Qoshimcha yuk",
    "karobka", "karobkalar", "karobkalar", "qop", "2 qop", "3 qop", "4 qop", "5 qop", "6 qop", "7 qop", "8 qop", "9 qop", "10 qop", 
    "11 qop", "12 qop", "13 qop", "14 qop", "15 qop", "16 qop", "17 qop", "18 qop", "19 qop", "20 qop", 
    "Toshkentdan Rishtonga 2 qop yuk bor", "Toshkentdan Rishtonga 3 qop yuk bor", "Toshkentdan Rishtonga 4 qop yuk bor",    
    "rishtondan toshkentga 2 qop yuk bor", "rishtondan toshkentga 3 qop yuk bor", "rishtondan toshkentga 4 qop yuk bor",    
    "farg'onadan toshkentga 2 qop yuk bor", "farg'onadan toshkentga 3 qop yuk bor", "farg'onadan toshkentga 4 qop yuk bor",
    "fargonadan qoqonga qop yuk bor", "fargonadan qoqonga 2 qop yuk bor", "fargonadan qoqonga 3 qop yuk bor", "fargonadan qoqonga 4 qop yuk bor",   
    "qo'qondan farg'onaga 2 qop yuk bor", "qo'qondan farg'onaga 3 qop yuk bor", "qo'qondan farg'onaga 4 qop yuk bor",   
    "toshkentdan farg'onaga 2 qop yuk bor", "toshkentdan farg'onaga 3 qop yuk bor", "toshkentdan farg'onaga 4 qop yuk bor", 
    "toshkentdan qoqonga 2 qop yuk bor", "toshkentdan qoqonga 3 qop yuk bor", "toshkentdan qoqonga 4 qop yuk bor",
    "fargonaga 2 qop yuk bor", "fargonaga 3 qop yuk bor", "fargonaga 4 qop yuk bor",    
    "qoqonga 2 qop yuk bor", "qoqonga 3 qop yuk bor", "qoqonga 4 qop yuk bor",
    "farg'onadan toshkentga 2 qop yuk bor", "farg'onadan toshkentga 3 qop yuk bor", "farg'onadan toshkentga 4 qop yuk bor",
    "karopkarlar bor", "karopkalar bor", "karobkalar bor", "qoplar bor", "2 qoplar bor", "3 qoplar bor", "4 qoplar bor", "5 qoplar bor", "6 qoplar bor", "7 qoplar bor", "8 qoplar bor", "9 qoplar bor", "10 qoplar bor",
    "karopka bor", "qoshimcha yuk bor", "qo'shimcha yuk bor", "qo'shimcha yuklar bor", "qoshimcha yuklar bor", "qo'shimcha yuk chiqdi", "qo'shimcha yuk chiqibdi", "qo'shimcha yuk chiqibdi aka", "qo'shimcha yuk chiqibdi edi", "qo'shimcha yuk chiqibdi ekan", "qo'shimcha yuk chiqibdi ekan edi",
    "qo'shimcha yuk chiqibdi edi aka", "qo'shimcha yuk chiqibdi edi ekan", "qo'shimcha yuk chiqibdi edi ekan edi",
    # Yangi kalit so'zlar (KEYWORDS ro'yxatining oxiriga qo'shing)
    "Toshkentga pochta bor", "Farg'onaga pochta bor",
    "Toshkentga jo'natma bor", "Farg'onaga jo'natma bor",
    "Yuk jo'natish kerak", "Pochta yuborish kerak",
    "Qo'shimcha yuk olib ketiladi", "Qo'shimcha yuk bor", "Qo'shimcha yuk kerak",
    "Labo kerak", "Labo bilan yuk tashish", "Labo yuk bor", "Yuk ko'p, Labo kerak",
    "100 kg qo'shimcha yuk", "200 kg qo'shimcha yuk", "300 kg qo'shimcha yuk",
    "500 kg qo'shimcha yuk", "700 kg qo'shimcha yuk",
    "1 tonnagacha yuk bor",
    "Farg'onadan Toshkentga yuk bor", "Toshkentdan Farg'onaga yuk bor",
    "Toshkent Farg'ona qo'shimcha yuk", "Farg'ona Toshkent qo'shimcha yuk",
    "Farg'onadan Toshkentga qo'shimcha yuk", "Toshkentdan Farg'onaga qo'shimcha yuk"
]


# =================== LOTIN → KIRILL (faqat bot ishga tushganda 1 marta) ===================
# Apostrof turlari: Telegramda o' g' ni har xil belgi bilan yozishadi (' ’ ʻ ʼ ` ´)
APOSTROPHES = str.maketrans({
    "\u2019": "'", "\u2018": "'", "\u02bb": "'", "\u02bc": "'", "`": "'", "\u00b4": "'",
})

def normalize(text):
    """Barcha apostrof turlarini oddiy ' ga almashtiradi."""
    return text.translate(APOSTROPHES)

def uzbek_lotin_kirill(matn):
    matn = normalize(matn).lower()

    # O'zbek tilidagi harf birikmalari
    almashtirishlar = [
        ("o'", "ў"),
        ("g'", "ғ"),
        ("sh", "ш"),
        ("ch", "ч"),
        ("yo", "ё"),
        ("yu", "ю"),
        ("ya", "я"),
        ("ye", "е"),
        ("ts", "ц"),
    ]

    for eski, yangi in almashtirishlar:
        matn = matn.replace(eski, yangi)

    harflar = {
        "a": "а", "b": "б", "d": "д", "e": "е",
        "f": "ф", "g": "г", "h": "ҳ", "i": "и",
        "j": "ж", "k": "к", "l": "л", "m": "м",
        "n": "н", "o": "о", "p": "п", "q": "қ",
        "r": "р", "s": "с", "t": "т", "u": "у",
        "v": "в", "w": "в", "x": "х", "y": "й", "z": "з",
    }

    return "".join(harflar.get(h, h) for h in matn)

def prepare_keywords(words):
    """
    1) har bir so'zning kirillcha variantini qo'shadi
    2) takrorlarni olib tashlaydi
    3) boshqa kalit so'z ichiga kirib ketgan uzun so'zlarni olib tashlaydi
       (masalan "qo'shimcha yuk" bo'lsa, "qo'shimcha yuk bor" kerak emas, chunki
       u allaqachon topiladi). Natija o'zgarmaydi, lekin qidiruv ancha tez bo'ladi.
    """
    all_words = set()
    for w in words:
        if not w.strip():
            continue
        all_words.add(normalize(w).lower())
        all_words.add(uzbek_lotin_kirill(w))

    kept = []
    for w in sorted(all_words, key=len):
        if not any(k in w for k in kept):
            kept.append(w)
    return kept

def build_regex(words):
    if not words:
        return None
    return re.compile("|".join(re.escape(k) for k in words), re.IGNORECASE)

_asl_soni = len(KEYWORDS)
KEYWORDS = prepare_keywords(KEYWORDS)
KEYWORDS_RE = build_regex(KEYWORDS)
print(f"Kalit so'zlar: {_asl_soni} ta yozilgan -> {len(KEYWORDS)} ta ishlaydi (lotin + kirill)")

# =================== REJECTED KALIT SO'ZLAR ===================
# Xabarda oddiy kalit so'z topilsa ham, quyidagilardan biri bo'lsa xabar YUBORILMAYDI.
# Kalit so'zlarni shu ro'yxatga o'zingiz qo'shing, masalan:
# "kerak emas", "bekor", "yuk yo'q"
REJECTED_KEYWORDS = [
    "fura kerak", "isizu", "kamaz", "Nukusdan", "Surxandaryodan", "Nukusga",
    "surxandaryo", "surxondaryo", "surxandaryoga", "surxandaryoga", "surxandaryodan", "surxondaryodan",
    "surxandaryoga", "surxondaryoga", "surxandaryodan", "olaman", "odam bor", "odam kerak", "yuk yo'q", "yuk kerak emas", "yuk kerakmas", "yuk kerakmas ekan", "yuk kerak emas ekan",
    "yuk kerakmas edi", "yuk kerak emas edi", "yuk kerak",
    "olamiz", "olamiz ekan", "olamiz edi", "olamiz ekan edi", "olamiz edi ekan", "olamiz kerak", "olamiz kerak emas", "olamiz kerakmas", "olamiz kerakmas ekan", "olamiz kerak emas ekan",
    "olamiz kerakmas edi", "olamiz kerak emas edi", "olamiz kerak", "olamiz kerakmas ekan edi", "olamiz kerak emas ekan edi",
    "isuzi bor", "isuzi kerak", "isuzi kerakmas", "isuzi kerakmas ekan", "isuzi kerak emas ekan",
    "isuzi kerakmas edi", "isuzi kerak emas edi", "isuzi kerak", "isuzi kerakmas ekan edi", "isuzi kerak emas ekan edi",
    "kamaz bor", "kamaz kerak", "kamaz kerakmas", "kamaz kerakmas ekan", "kamaz kerak emas ekan",
    "kamaz kerakmas edi", "kamaz kerak emas edi", "kamaz kerak", "tentli yuk", "tentli yuk bor", "tentli yuk kerak", "tentli yuk kerakmas", "tentli yuk kerakmas ekan", "tentli yuk kerak emas ekan",
    "tentli yuk kerakmas edi", "tentli yuk kerak emas edi", "tentli yuk kerak", "tentli yuk kerakmas ekan edi", "tentli yuk kerak emas ekan edi",
    "фура керак", "исузи", "камаз", "Нукусдан", "Нукусга",
    "Сурхандариё", "Сурхондарё", "Сурхондарёга", "Сурхондарёдан",
    "оламан", "одам бор", "одам керак", "юк йўқ", "юк керак эмас", "юк керакмас",
    "юк керакмас экан", "юк керак эмас экан", "юк керакмас эди", "юк керак эмас эди", "юк керак",
    "оламиз", "оламиз экан", "оламиз эди", "оламиз экан эди", "оламиз эди экан",
    "оламиз керак", "оламиз керак эмас", "оламиз керакмас", "оламиз керакмас экан", "оламиз керак эмас экан",
    "оламиз керакмас эди", "оламиз керак эмас эди", "оламиз керакмас экан эди", "оламиз керак эмас экан эди",
    "исузи бор", "исузи керак", "исузи керакмас", "исузи керакмас экан", "исузи керак эмас экан",
    "исузи керакмас эди", "исузи керак эмас эди", "исузи керакмас экан эди", "исузи керак эмас экан эди",
    "камаз бор", "камаз керак", "камаз керакмас", "камаз керакмас экан", "камаз керак эмас экан",
    "камаз керакмас эди", "камаз керак эмас эди", "тентли юк", "тентли юк бор", "тентли юк керак",
    "тентли юк керакмас", "тентли юк керакмас экан", "тентли юк керак эмас экан",
    "тентли юк керакмас эди", "тентли юк керак эмас эди", "тентли юк керакмас экан эди", "тентли юк керак эмас экан эди"
]

_rej_asl_soni = len(REJECTED_KEYWORDS)
REJECTED_KEYWORDS = prepare_keywords(REJECTED_KEYWORDS)
REJECTED_RE = build_regex(REJECTED_KEYWORDS)  # ro'yxat bo'sh bo'lsa None
print(f"Rejected so'zlar: {_rej_asl_soni} ta yozilgan -> {len(REJECTED_KEYWORDS)} ta ishlaydi (lotin + kirill)")

def is_rejected(text):
    """Xabarda rejected kalit so'z bo'lsa True qaytaradi."""
    return bool(REJECTED_RE and REJECTED_RE.search(text))

# =================== TELEFON REGEX ===================
PHONE_RE = re.compile(r'(\+?998[\d\-\s\(\)]{9,15}|9\d{8})')

def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('998') and len(digits) >= 12:
        return '+' + digits[:12]
    if len(digits) == 9:
        return '+998' + digits
    return None

# =================== HANDLER ===================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if not (event.is_group or event.is_channel):
            return

        chat_id = event.chat_id
        if chat_id in SKIP_CHAT_IDS:
            return

        text = event.raw_text
        if not text:
            return
        check_text = normalize(text)  # faqat tekshirish uchun, yuboriladigan matn o'zgarmaydi

        # 1-qadam: oddiy kalit so'zlar tekshiriladi
        if not KEYWORDS_RE.search(check_text):
            return

        # 2-qadam: rejected kalit so'zlar tekshiriladi, bo'lsa xabar yuborilmaydi
        if is_rejected(check_text):
            print("🚫 Rejected kalit so'z topildi, xabar yuborilmadi")
            return

        chat, sender = await asyncio.gather(
            event.get_chat(),
            event.get_sender()
        )

        group_name = getattr(chat, 'title', 'Nomaʼlum guruh')

        username = getattr(sender, 'username', None)
        owner_display = f"@{username}" if username else "БЕРКИТИЛГАН"

        sender_id = getattr(sender, 'id', None)
        sender_hash = getattr(sender, 'access_hash', None)

        if username:
            # Username orqali profilga o'tish eng ishonchli usul, hech qachon uzilib qolmaydi
            profile_link = f"<a href='https://t.me/{username}'>ПРОФИЛГА ЎТИШ</a>"
        elif sender_id and sender_hash:
            # access_hash mavjud bo'lsa tg://user link ham ishonchli ishlaydi
            profile_link = f"<a href='tg://user?id={sender_id}&hash={sender_hash}'>ПРОФИЛГА ЎТИШ</a>"
        elif sender_id:
            profile_link = f"<a href='tg://user?id={sender_id}'>ПРОФИЛГА ЎТИШ</a>"
        else:
            profile_link = "БЕРКИТИЛГАН"

        phone = normalize_phone(sender.phone) if sender.phone else None
        if not phone:
            for m in PHONE_RE.finditer(text):
                phone = normalize_phone(m.group(0))
                if phone:
                    break

        phone_display = phone if phone else "БЕРКИТИЛГАН"

        message_text = (
            f"🚨 <b>ЯНГИ ЗАКАЗ</b>\n"
            f"________________\n\n"
            f"{text}\n"
            f"________________\n\n"
            f"📍 <b>ГУРУҲ : </b> {group_name}\n"
            f"👤 <b>КЛЕНТ ЛИЧКАСИ : </b> {owner_display}\n"
            f"📞 <b>КЛЕНТ НОМЕРИ : </b> {phone_display}\n\n"
            f"👉🏻 <b></b> {profile_link}"
        )

        for target_id in TARGET_CHAT_IDS:
            await client.send_message(
                target_id,
                message_text,
                parse_mode='html'
            )
            print(f"📨 Yuborildi → {target_id}")

    except Exception as e:
        print("❌ Xatolik:", e)

# =================== START ===================
print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()