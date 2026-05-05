import subprocess
import random


def switch_vpn_country_v2():
    countries = ["Germany", "Netherlands", "Switzerland", "France", "Sweden", "Japan", "USA", "Canada"]
    country = random.choice(countries)

    applescript = f'''
    tell application "hidemy.name VPN"
        activate
    end tell
    delay 1
    tell application "System Events"
        tell process "hidemy.name VPN"
            set frontmost to true
            keystroke "f" using command down
            delay 0.5
            keystroke "{country}"
            delay 1
            keystroke return
        end tell
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True, timeout=15)
        print(f"✅ VPN должен переключиться на {country}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


if __name__ == "__main__":
    switch_vpn_country_v2()