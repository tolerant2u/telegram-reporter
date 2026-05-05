# main_pyrogram.py — с проверкой сессий перед запуском и пропуском мёртвых
import asyncio
import random
import os
from pyrogram import Client
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import (
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
    InputReportReasonFake,
    InputReportReasonCopyright,
    InputReportReasonPersonalDetails,
    InputReportReasonOther,
)

# ================== НАСТРОЙКИ ==================
API_ID = 123456        # ← ЗАМЕНИ / USE UR OWN
API_HASH = "abc123..." # ← ЗАМЕНИ / USE UR OWN

PROXIES_FILE = "proxies.txt"
SESSIONS_FILE = "sessions.txt"

MIN_DELAY = 30
MAX_DELAY = 60

# ================================================

REASONS = {
    "spam": InputReportReasonSpam(),
    "violence": InputReportReasonViolence(),
    "pornography": InputReportReasonPornography(),
    "child_abuse": InputReportReasonChildAbuse(),
    "fake": InputReportReasonFake(),
    "copyright": InputReportReasonCopyright(),
    "personal": InputReportReasonPersonalDetails(),
    "other": InputReportReasonOther(),
}

REASON_NAMES = {
    "spam": "Спам",
    "violence": "Насилие",
    "pornography": "Порнография",
    "child_abuse": "Детское насилие (ЦП)",
    "fake": "Фейк / Подделка",
    "copyright": "Авторские права",
    "personal": "Личные данные",
    "other": "Другое",
}


def load_lines(filename):
    if not os.path.exists(filename):
        print(f"[!] Файл {filename} не найден.")
        open(filename, "w", encoding="utf-8").close()
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def load_proxies():
    lines = load_lines(PROXIES_FILE)
    proxies = []
    for line in lines:
        parts = line.split(":")
        if len(parts) == 4:
            ip, port, user, pwd = parts
            proxies.append({
                "scheme": "socks5",
                "hostname": ip,
                "port": int(port),
                "username": user,
                "password": pwd,
            })
        elif len(parts) == 2:
            ip, port = parts
            proxies.append({
                "scheme": "http",
                "hostname": ip,
                "port": int(port),
            })
    return proxies


async def check_session(session_name, idx):
    """Проверяет одну сессию. Возвращает (idx, session_name, True/False, username/ошибка)."""
    name = session_name.replace(".session", "")
    client = Client(name=name, api_id=API_ID, api_hash=API_HASH)
    try:
        await client.start()
        me = await client.get_me()
        username = f"@{me.username}" if me.username else "—"
        return (idx, session_name, True, username)
    except Exception as e:
        return (idx, session_name, False, f"{type(e).__name__}")
    finally:
        try:
            await client.stop()
        except:
            pass


async def report_with_session(session_name, proxy, target, reason_obj, reason_name, idx):
    name = session_name.replace(".session", "")
    client = Client(
        name=name,
        api_id=API_ID,
        api_hash=API_HASH,
        proxy=proxy if proxy else None,
    )
    started = False
    try:
        await client.start()
        started = True
        me = await client.get_me()

        try:
            username = f"@{me.username}" if me.username else "—"
        except Exception:
            username = "—"

        if proxy:
            ip_display = f"{proxy['hostname']}:{proxy['port']}"
        else:
            ip_display = "прямое (VPN)"

        print(f"[{idx}] {username} (ID: {me.id}) | IP: {ip_display}")

        try:
            clean_target = target.replace("@", "")
            peer = await client.resolve_peer(clean_target)
        except Exception:
            print(f"[{idx}] ❌ Не удалось найти «{target}». Пропускаю.")
            return False

        await client.invoke(
            Report(
                peer=peer,
                id=[],
                reason=reason_obj,
                message=""
            )
        )
        print(f"[{idx}] ✅ Жалоба («{reason_name}») на {target} отправлена.")
        return True
    except Exception as e:
        print(f"[{idx}] ❌ Ошибка: {type(e).__name__}: {e}")
        return False
    finally:
        if started:
            try:
                await client.stop()
            except ConnectionError:
                pass


async def main():
    print("=" * 50)
    print("Pyrogram Multi-Reporter | v2.1 HEALTH CHECK")
    print("=" * 50)

    session_files = load_lines(SESSIONS_FILE)

    if not session_files:
        print("[!] Нет сессий. Заполни sessions.txt")
        return

    # Проверяем, существуют ли файлы, и фильтруем
    missing = [s for s in session_files if not os.path.exists(s)]
    if missing:
        print(f"[!] Пропущено {len(missing)} несуществующих файлов:")
        for m in missing:
            print(f"   — {m}")
        session_files = [s for s in session_files if os.path.exists(s)]
        # Обновляем sessions.txt, чтобы в следующий раз не проверять
        with open(SESSIONS_FILE, "w") as f:
            for s in session_files:
                f.write(s + "\n")
        print(f"   sessions.txt обновлён — мёртвые удалены.\n")

    if not session_files:
        print("[!] Не осталось живых сессий. Выход.")
        return

    # ==== ПРОВЕРКА ВСЕХ СЕССИЙ ====
    print(f"\n🔍 Проверяю {len(session_files)} сессий...\n")
    checks = await asyncio.gather(*[
        check_session(s, i) for i, s in enumerate(session_files, 1)
    ])

    alive = []
    dead = []
    for idx, name, ok, info in checks:
        if ok:
            print(f"   [{idx}] {name} → {info} ✅")
            alive.append((idx, name))
        else:
            print(f"   [{idx}] {name} → ❌ {info}")
            dead.append((idx, name))

    print(f"\n📊 Живых: {len(alive)} | Мёртвых: {len(dead)}")

    if dead:
        print("💀 Мёртвые сессии (удали их из sessions.txt и сами файлы):")
        for idx, name in dead:
            print(f"   [{idx}] {name}")

    if not alive:
        print("[!] Нет живых сессий. Выход.")
        return

    # ==== ПРОКСИ ====
    all_proxies = load_proxies()
    if not all_proxies:
        print("[!] ВНИМАНИЕ: Нет прокси. Использую прямое подключение.")
        proxies = [None] * len(alive)
    else:
        random.shuffle(all_proxies)
        proxies = all_proxies[:len(alive)]
        print(f"✅ Загружено {len(all_proxies)} прокси. Выбрано {len(proxies)} случайных.")

    # ==== ВВОД ЦЕЛИ ====
    while True:
        target = input("\n🎯 Введи ссылку или @username цели: ").strip()
        if not target:
            print("❌ Не может быть пустым.")
            continue
        print("\n" + "=" * 40)
        print("⚠️  ПРОВЕРЬ ЦЕЛЬ ПЕРЕД ЗАПУСКОМ")
        print("=" * 40)
        print(f"   Цель: {target}")
        print(f"   Символов: {len(target)}")
        print("=" * 40)
        confirm = input("Всё верно? (y/n/exit): ").strip().lower()
        if confirm == "y":
            break
        elif confirm == "exit":
            print("Выход.")
            return
        else:
            print("↺ Введи заново.\n")

    # ==== ВЫБОР ПРИЧИНЫ ====
    print("\n📌 Причины:")
    for key, name in REASON_NAMES.items():
        print(f"   [{key}] {name}")
    reason_key = input("Введи ключ причины (Enter = child_abuse): ").strip().lower()
    if reason_key not in REASONS:
        reason_key = "child_abuse"
    reason_name = REASON_NAMES[reason_key]
    print(f"✓ Выбрано: {reason_name}")

    # ==== КОЛ-ВО АККАУНТОВ ====
    max_n = len(alive)
    use_count = input(f"\nСколько аккаунтов? (1–{max_n}, Enter = все): ").strip()
    n = max_n
    if use_count.isdigit():
        n = max(1, min(int(use_count), max_n))

    # ==== ФИНАЛЬНАЯ ПРОВЕРКА ====
    print("\n" + "=" * 50)
    print("📋 ФИНАЛЬНАЯ ПРОВЕРКА")
    print("=" * 50)
    print(f"   Цель:     {target}")
    print(f"   Причина:  {reason_name}")
    print(f"   Аккаунтов: {n} из {max_n} живых")
    if all_proxies:
        print(f"   Прокси:    случайные из пула {len(all_proxies)} шт.")
    else:
        print(f"   Прокси:    прямое подключение")
    print("=" * 50)

    final = input("\n🚀 ЗАПУСКАЕМ? (y/n): ").strip().lower()
    if final != "y":
        print("Отмена.")
        return

    print(f"\n⚡ Старт. Задержка между жалобами: {MIN_DELAY}–{MAX_DELAY} сек.\n")

    success = 0
    for i in range(n):
        original_idx, session_name = alive[i]
        proxy = proxies[i] if i < len(proxies) else None

        result = await report_with_session(
            session_name, proxy, target, REASONS[reason_key], reason_name, original_idx
        )
        if result:
            success += 1

        if i < n - 1:
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"   ⏳ Жду {delay} сек...")
            await asyncio.sleep(delay)

    print(f"\n🏁 Готово. Успешных жалоб: {success}/{n}")


if __name__ == "__main__":
    asyncio.run(main())