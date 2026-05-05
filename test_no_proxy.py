# test_no_proxy.py — тест Pyrogram без прокси
import asyncio
import os
from pyrogram import Client
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonChildAbuse

# ================== НАСТРОЙКИ ==================
API_ID = 2040       # ← ЗАМЕНИ
API_HASH = "b18441a1ff607e10a989891a5462e627" # ← ЗАМЕНИ

# Имя файла сессии (например, session_1.session)
SESSION_FILE = "session_1.session"

# Цель для теста
TARGET = "@fqyiibot"
# ================================================


async def main():
    name = SESSION_FILE.replace(".session", "")

    client = Client(
        name=name,
        api_id=API_ID,
        api_hash=API_HASH,
    )

    try:
        await client.start()
        me = await client.get_me()
        username = f"@{me.username}" if me.username else "—"
        print(f"✅ Залогинился как {username} (ID: {me.id})")

        clean_target = TARGET.replace("@", "")
        peer = await client.resolve_peer(clean_target)

        await client.invoke(
            Report(
                peer=peer,
                id=[],
                reason=InputReportReasonChildAbuse(),
                message=""
            )
        )
        print(f"✅ Жалоба (Детское насилие ЦП) на {TARGET} отправлена!")

    except Exception as e:
        print(f"❌ Ошибка: {type(e).__name__}: {e}")

    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())