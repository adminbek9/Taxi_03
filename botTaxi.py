from telethon import TelegramClient, events

api_id = 22731419
api_hash = '2e2a9ce500a5bd08bae56f6ac2cc4890'

client = TelegramClient('taxi_session', api_id, api_hash)

# Kalit so‘zlar
keywords = [
    'odam bor', 'rishtondan toshkentga odam bor', 'toshkentdan rishtonga odam bor',
    'odam bor 1', 'rishtonga odam bor', 'toshkentga odam bor',
    'pochta bor', 'rishtonga pochta bor', 'rishtondan pochta bor',
    'toshkentga pochta bor', 'toshkentdan pochta bor',
    'ketadi', 'ketishadi', 'ketishi kerak', 'ketishi', 'ayol kishi ketadi'
]

target_chat = '@rozimuhammadTaxi'

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if event.is_private:
            return

        text = event.raw_text or ""
        if not any(keyword in text.lower() for keyword in keywords):
            return

        chat = await event.get_chat()

        # Chat ma’lumotlarini olish
        if hasattr(chat, 'username') and chat.username:
            chat_link = f"https://t.me/{chat.username}/{event.message.id}"
            chat_name = chat.title or chat.username
            source_line = f"{chat_name} ({chat_link})"
        else:
            sender = await event.get_sender()
            if hasattr(sender, 'username') and sender.username:
                source_line = f"Foydalanuvchi: @{sender.username} (Link yo‘q, yopiq guruh)"
            else:
                source_line = "Shaxsiy foydalanuvchi (username yo‘q)"

        message_to_send = (
            f"🚖 <b>Xabar topildi!</b>\n\n"
            f"📄 <b>Matn:</b>\n{text}\n\n"
            f"📍 <b>Qayerdan:</b>\n{source_line}\n\n"
            f"🤝 <i>Hamkorlik va do‘stlik yo‘lidamiz. Siz bilan birgamiz!</i>"
        )

        await client.send_message(target_chat, message_to_send, parse_mode='html')
        print("✅ Yuborildi:", text[:60])

    except Exception as e:
        print("❌ Xatolik:", e)

print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()
