from telethon import TelegramClient, events
from telethon.tl.types import User, Chat, Channel

api_id = 22731419
api_hash = '2e2a9ce500a5bd08bae56f6ac2cc4890'

client = TelegramClient('taxi_session', api_id, api_hash)

# Filtrlash uchun kalit so'zlar ro'yxati (kichik-katta harf farqsiz)
keywords = [
    'odam bor', 'rishtondan toshkentga odam bor', 'toshkentdan rishtonga odam bor',
    'odam bor 1', 'rishtonga odam bor', 'toshkentga odam bor',
    'pochta bor', 'rishtonga pochta bor', 'rishtondan pochta bor',
    'toshkentga pochta bor', 'toshkentdan pochta bor',
    'ketadi', 'ketishadi', 'ketishi kerak', 'ketishi', 'ayol kishi ketadi'
]

# Maqsadli kanal (natijalar shu yerga yuboriladi)
target_chat = '@rozimuhammadTaxi'

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # Faqat shaxsiy chatlarni chiqarib tashlaymiz
        if event.is_private:
            return

        # Xabar matni
        text = event.raw_text
        if not text:
            return

        # Kichik harfga o'tkazib tekshiramiz
        text_lower = text.lower()
        if not any(keyword in text_lower for keyword in keywords):
            return

        # Chat ma'lumotlarini olish
        chat = await event.get_chat()

        # Link bor bo‘lsa — linkli format
        if hasattr(chat, 'username') and chat.username:
            chat_link = f"https://t.me/{chat.username}/{event.message.id}"
            chat_name = chat.title or chat.username
            source_line = f"{chat_name} ({chat_link})"
        else:
            chat_name = chat.title or "Noma’lum guruh/kanal"
            source_line = f"{chat_name} (Link yo‘q, yopiq guruh)"

        # Xabar tayyorlash
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