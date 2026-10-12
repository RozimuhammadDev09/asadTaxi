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
# Asosiy yuk e'lonlari
"yuk bor", "yuk bor ekan", "yuk bor edi",
"yuk chiqdi", "yuk chiqibdi", "yuk tayyor",
"yuk jo'natish bor", "yuk jo'natiladi",
"yuk yuboriladi", "yuk yuborish bor",
"yuk tashlash kerak", "yuk jo'nataman",
"yuk jo'natmoqchiman", "yukim bor",
"yukimiz bor", "yuk borakan", "yuk borakan",
"yuk bor edi aka", "yuk bor kim bor",
"yuk bor mashina kerak", "yuk uchun mashina",
"yuk tashish kerak", "yukni olib borish kerak",
"yukni yetkazish kerak", "yuk yuborish kerak",
"yuk jo'natish kerak", "yuk chiqarish kerak",
"yuk beriladi", "yuk bor edi bugun",
"qo'shimcha yuk", "qoshimcha yuk",
"qo'shimcha yuk bor", "qoshimcha yuk bor",
"qo'shimcha yuk chiqdi", "qo'shimcha yuk bor ekan",
"qoshimcha yuk chiqdi", "ortiqcha yuk bor",
"ortiqcha yuk", "yuk bor ekan aka",

# Yuk so'zining xato yozilishlari
"yuk bor", "yukbor", "yuk bormi",
"yukla bor", "yuk borakan", "yuk borakan",
"yuk borakanmi", "yukla bor", "yuk bor edi",
"yuk jonatish", "yuk jonataman", "yuk jonatiladi",
"yuk yuborish", "yuk yubarish", "yuk yuberish",
"yuk tashash", "yuk tashlash", "yuk tashash kerak",
"yuk tashlab berish", "yuk borakan",
"qoshimcha yuk bor", "qoshimcha yuk borakan",
"qoshimcha yuk chiqdi", "qoshimcha yuk ketadi",
"qoshimcha yuk bor edi", "qoshimcha yuk borakan",

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
"1,0 tonna yuk", "1 yarim tonna yuk",
"1.5 tonna yuk", "1,5 tonna yuk",
"2 tonna yuk", "2tonna yuk", "2 ton yuk",
"2 tonna yuk bor", "2 ton yuk bor",
"3 tonna yuk", "3tonna yuk", "3 ton yuk",
"3 tonna yuk bor", "4 tonna yuk",
"4tonna yuk", "4 ton yuk", "4 tonna yuk bor",
"5 tonna yuk", "5tonna yuk", "5 ton yuk",
"5 tonna yuk bor", "6 tonna yuk",
"7 tonna yuk", "8 tonna yuk", "9 tonna yuk",
"10 tonna yuk", "10tonna yuk", "10 ton yuk",
"yarim tonna yuk", "yarim tonna yuk bor",
"0.5 tonna yuk", "0,5 tonna yuk",
"1 тонна юк", "1 тонна юк бор",
"2 тонна юк", "3 тонна юк", "4 тонна юк",
"5 тонна юк", "ярим тонна юк",

# Qo'shimcha yuk va vazn
"qo'shimcha 100 kg", "qo'shimcha 150 kg",
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
"Toshkentdan Farg'onaga yuk bor",
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
"Toshkentdan Farg'onaga yuk kerak emas",
"Toshkentdan yuk bor Farg'onaga",

# Kirillcha yo'nalish va yuk e'lonlari
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
"pochta yuk bor", "poshta yuk bor",
"jo'natma bor", "jo'natma yuborish kerak",
"yuk jo'natish bor", "yuk jo'natmoqchiman",
"yukim bor Toshkentga", "yukim bor Farg'onaga",
"Toshkentga yuboriladigan yuk bor",
"Farg'onaga yuboriladigan yuk bor",
"Toshkentga jo'natma bor",
"Farg'onaga jo'natma bor",
"Toshkentga yuk jo'nataman",
"Farg'onaga yuk jo'nataman",
"yuk bor Toshkentga", "yuk bor Farg'onaga",
"Toshkentga yuk chiqdi", "Farg'onaga yuk chiqdi",
"Toshkentga yuk bor ekan", "Farg'onaga yuk bor ekan"
]


KEYWORDS_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

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
        if not text or not KEYWORDS_RE.search(text):
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