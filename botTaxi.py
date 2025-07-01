import hashlib
import re
from telethon import TelegramClient, events

# Telethon API ma'lumotlari
api_id = 22731419
api_hash = '2e2a9ce500a5bd08bae56f6ac2cc4890'

client = TelegramClient('taxi_session', api_id, api_hash)

# 🚨 Kalit so‘zlar: lotin + kirill yozuvda, noto‘g‘ri imlolarni ham o‘z ichiga oladi
keywords = [
    # Lotin yozuvli
    "odam bor", "yo'lovchi bor", "yolovchi bor", "yulovchi bor",
    "odam ketadi", "odam ketyapti", "odam ketyapman",
    "yo‘lovchi ketadi", "yo‘lovchi ketyapti", "yo‘lovchi ketyapman",
    "boraman", "ketaman", "boramiz", "ketamiz", "bormoqchimiz", "ketmoqchimiz",
    "2ta odam", "3ta odam", "4ta odam", "2ta kishi", "3 kishi", "4 kishi",
    "1ta odam", "1ta kishi", "odamlar bor", "odam bilan ketamiz",
    "toshkentga", "rishtonga",
    "mashina kerak", "moshina kerak", "avto kerak", "taksi kerak",
    "taxi kerak", "avtomobil kerak", "mashina yo‘q", "mashina yoq",
    "mashina izlayapman", "mashina topish kerak",
    "komplekt", "kamplekt", "komplect", "komplek", "komplekta", "komplekda", "komplek bor", "komplek kerak",
    "1ta", "2ta", "3ta", "4ta", "1 ta", "2 ta", "3 ta", "4 ta",
    "1 kishi", "2 kishi", "3 kishi", "4 kishi",

    # Kirill yozuvli (rus harflarida yozilgan o‘zbekcha)
    "одам бор", "йўловчи бор", "ёлловчи бор", "юловчи бор",
    "одам кетади", "одам кетяпти", "одам кетяпман",
    "йўловчи кетади", "йўловчи кетяпти", "йўловчи кетяпман",
    "бораман", "кетаман", "борамиз", "кетамиз", "бормоқчимиз", "кетмоқчимиз",
    "2та одам", "3та одам", "4та одам", "2та киши", "3 киши", "4 киши",
    "1та одам", "1та киши", "одамлар бор", "одам билан кетамиз",
    "тошкентга", "риштонга",
    "машина керак", "мошина керак", "авто керак", "такси керак",
    "автомобил керак", "машина йўқ", "машина йок",
    "машина излаяпман", "машина топиш керак",
    "комплект", "камплект", "комплек", "комплекта", "комплекда", "комплек бор", "комплек керак",
    "1та", "2та", "3та", "4та", "1 та", "2 та", "3 та", "4 та",
    "1 киши", "2 киши", "3 киши", "4 киши"
]

# Natijalarni yuboradigan kanal
target_chat = '@rozimuhammadTaxi'

# Takroriy yuborilmasligi uchun hashlar
seen_messages = set()

def get_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# Xabarni filtrlovchi funksiya
def is_keyword_found(text):
    text = text.lower()
    for keyword in keywords:
        if re.search(re.escape(keyword), text):
            return True
    return False

# Yangi xabarlar uchun event
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if event.is_private:
            return

        text = event.raw_text
        if not text:
            return

        if not is_keyword_found(text):
            return

        text_hash = get_md5(text)
        if text_hash in seen_messages:
            return
        seen_messages.add(text_hash)

        chat = await event.get_chat()

        if hasattr(chat, 'username') and chat.username:
            chat_link = f"https://t.me/{chat.username}/{event.message.id}"
            chat_name = chat.title or chat.username
            source_line = f"{chat_name} ({chat_link})"
        else:
            if hasattr(event.sender, 'username') and event.sender.username:
                source_line = f"@{event.sender.username} (Link yo‘q)"
            else:
                source_line = "Shaxsiy yoki yopiq guruh (username yo‘q)"

        message_to_send = (
            f"🚖 <b>Xabar topildi!</b>\n\n"
            f"📄 <b>Matn:</b>\n{text}\n\n"
            f"📍 <b>Qayerdan:</b>\n{source_line}\n\n"
            f"🤝 <i>Hamkorlik va do‘stlik yo‘lidamiz. Siz bilan birgamiz!</i>"
        )

        await client.send_message(target_chat, message_to_send, parse_mode='html')
        print("✅ Yuborildi:", text[:50])

    except Exception as e:
        print("❌ Xatolik:", e)

print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()
 
