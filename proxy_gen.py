# gen_proxies.py — интерактивный генератор proxies.txt
print("=" * 40)
print("ГЕНЕРАТОР PROXIES.TXT")
print("=" * 40)

ip = input("IP-адрес: ").strip()
start_port = int(input("Начальный порт (обычно 10000): ").strip())
login = input("Логин: ").strip()
password = input("Пароль: ").strip()
count = int(input("Сколько портов генерировать? (Enter = 1000): ").strip() or "1000")

with open("proxies.txt", "w") as f:
    for i in range(count):
        port = start_port + i
        f.write(f"{ip}:{port}:{login}:{password}\n")

print(f"\n✅ Готово: {count} прокси записаны в proxies.txt")
print(f"   IP: {ip}")
print(f"   Порты: {start_port}–{start_port + count - 1}")
print(f"   Логин: {login}")
print(f"   Пароль: {password}")