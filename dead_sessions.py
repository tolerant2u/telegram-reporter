import asyncio
from pathlib import Path

from pyrogram import Client


API_ID = 123456
API_HASH = "abc123..."

SESSIONS_FILE = "sessions.txt"


def load_lines(filename):
    path = Path(filename)
    if not path.exists():
        print(f"[!] Файл {filename} не найден. Создаю пустой файл.")
        path.write_text("", encoding="utf-8")
        return []

    with path.open("r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def normalize_session_name(session_entry):
    session_path = Path(session_entry)
    if session_path.suffix == ".session":
        return str(session_path.with_suffix(""))
    return session_entry


def session_file_exists(session_entry):
    session_path = Path(session_entry)
    if session_path.suffix == ".session":
        return session_path.exists()
    return Path(f"{session_entry}.session").exists()


async def check_session(session_entry, idx):
    name = normalize_session_name(session_entry)
    client = Client(name=name, api_id=API_ID, api_hash=API_HASH)

    try:
        await client.start()
        me = await client.get_me()
        username = f"@{me.username}" if me.username else "-"
        return {
            "idx": idx,
            "entry": session_entry,
            "ok": True,
            "info": f"{username} | ID: {me.id}",
        }
    except Exception as e:
        return {
            "idx": idx,
            "entry": session_entry,
            "ok": False,
            "info": f"{type(e).__name__}: {e}",
        }
    finally:
        try:
            await client.stop()
        except Exception:
            pass


async def main():
    print("=" * 50)
    print("Pyrogram Session Checker")
    print("=" * 50)

    session_entries = load_lines(SESSIONS_FILE)
    if not session_entries:
        print("[!] Нет сессий. Заполни sessions.txt")
        return

    existing = []
    missing = []

    for idx, entry in enumerate(session_entries, 1):
        if session_file_exists(entry):
            existing.append((idx, entry))
        else:
            missing.append((idx, entry))

    if missing:
        print(f"\n[!] Не найдены файлы сессий: {len(missing)}")
        for idx, entry in missing:
            print(f"   [{idx}] {entry}")
        print("\nНичего из sessions.txt не удаляю.")

    if not existing:
        print("\n[!] Не найдено ни одного файла сессии. Выход.")
        return

    print(f"\nПроверяю доступные сессии: {len(existing)}\n")
    checks = await asyncio.gather(
        *[check_session(entry, idx) for idx, entry in existing]
    )

    alive = []
    dead = []

    for result in checks:
        if result["ok"]:
            alive.append(result)
            print(f"   [{result['idx']}] {result['entry']} -> {result['info']} OK")
        else:
            dead.append(result)
            print(f"   [{result['idx']}] {result['entry']} -> BAD {result['info']}")

    print("\n" + "=" * 50)
    print(
        f"Живых: {len(alive)} | "
        f"Битых/неавторизованных: {len(dead)} | "
        f"Файлов не найдено: {len(missing)}"
    )
    print("=" * 50)

    if dead:
        print("\nБитые сессии:")
        for result in dead:
            print(f"   [{result['idx']}] {result['entry']} -> {result['info']}")

    if missing:
        print("\nОтсутствующие файлы:")
        for idx, entry in missing:
            print(f"   [{idx}] {entry}")

    print("\nГотово. sessions.txt не изменялся.")


if __name__ == "__main__":
    asyncio.run(main())
