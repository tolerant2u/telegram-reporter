# renumber_sessions.py — перенумеровывает ВСЕ .session файлы
import os
import glob

SESSIONS_FILE = "sessions.txt"
FOLDER = "."


def main():
    # Ищем все .session файлы без исключений
    all_files = glob.glob(os.path.join(FOLDER, "*.session"))

    if not all_files:
        print("[!] Не найдено .session файлов")
        return

    # Сортируем по дате создания
    all_files.sort(key=lambda f: os.path.getctime(f))

    print(f"Найдено {len(all_files)} файлов:")
    for f in all_files:
        print(f"   {os.path.basename(f)}")

    confirm = input("\nПеренумеровать все в session_1.session, session_2.session... ? (y/n): ")
    if confirm.lower() != "y":
        print("Отмена.")
        return

    # Сначала переименовываем во временные имена (чтобы не было конфликтов)
    temp_names = []
    for i, old_path in enumerate(all_files, 1):
        temp_name = f"_temp_{i}.session"
        temp_path = os.path.join(FOLDER, temp_name)
        os.rename(old_path, temp_path)
        temp_names.append(temp_path)

    # Теперь переименовываем в финальные
    new_names = []
    for i, temp_path in enumerate(temp_names, 1):
        new_name = f"session_{i}.session"
        new_path = os.path.join(FOLDER, new_name)
        os.rename(temp_path, new_path)
        print(f"   ✓ session_{i}.session")
        new_names.append(new_name)

    # Обновляем sessions.txt
    with open(SESSIONS_FILE, "w") as f:
        for name in new_names:
            f.write(name + "\n")

    print(f"\n✅ Готово. {len(new_names)} файлов перенумерованы, sessions.txt обновлён.")


if __name__ == "__main__":
    main()