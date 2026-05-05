
# Telegram Bot Reporter Helper

A simple helper project for preparing structured abuse reports about Telegram bots.  
The tool is intended for educational, defensive, and moderation-assistance purposes only.

> ⚠️ **Disclaimer:** This project must only be used for legitimate reports against bots that violate Telegram rules. Do not use it for harassment, false reports, spam, brigading, or attacks against real users.

---

## Features

- ✅ **Bot-focused reporting workflow**
- ✅ **Session health check**
- ✅ **Multiple report categories**
- ✅ **English and Russian interface support**
- ✅ **Structured complaint messages**
- ✅ **Simple text-based configuration**

---

## Report Reasons

Supported report categories:

- Spam
- Violence
- Pornography
- Child Abuse
- Fake / Impersonation
- Copyright Violation
- Personal Details
- Other

---

## How It Works

Before starting, the script checks available Telegram sessions and verifies whether they can connect successfully.

After that, the user can choose a report reason and prepare a structured complaint message for a suspicious or abusive Telegram bot.

---

## Setup

### 1. Get Telegram API Credentials

Go to [my.telegram.org](https://my.telegram.org), open **API development tools**, and create an application.

Then replace the values in `main.py`:

```python
API_ID = 123456
API_HASH = "your_api_hash_here"
````

### 2. Add Your Session File

Place your Pyrogram `.session` file in the project folder.

Then add it to `sessions.txt`:

```txt
my_session.session
```

> Use only your own Telegram account/session. Do not use purchased, stolen, shared, or unauthorized sessions.

### 3. Optional: Configure Connection

If your environment requires a proxy for legitimate connectivity reasons, configure it according to your local laws, Telegram rules, and hosting provider policies.

Do not use proxies to evade limits, hide abuse, or automate mass actions.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run

```bash
python main.py
```

---

## Language Support

| Language | Interface | Report Messages |
| -------- | --------- | --------------- |
| English  | ✅         | ✅               |
| Русский  | ✅         | ✅               |

---

## Responsible Use

This project is intended only for:

* Reporting malicious bots
* Documenting abuse
* Learning how Telegram API-based tools are structured
* Defensive moderation workflows

This project must not be used for:

* False reporting
* Mass reporting
* Harassment
* Targeting real users
* Evading Telegram limits
* Using unauthorized accounts or sessions

---

## Disclaimer

This software is provided for educational and defensive purposes only.

The author is not responsible for misuse of this software. By using this project, you accept full legal and ethical responsibility for your actions.

---

## License

MIT License
