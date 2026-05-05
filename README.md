# Telegram Multi-Reporter

Multi-account reporting tool for Telegram bots using Pyrogram with proxy rotation, session health checks, and multiple report reasons.

**⚠️ DISCLAIMER: THIS TOOL IS FOR REPORTING BOTS ONLY. DO NOT USE AGAINST REAL USERS.**

---

## Features

- ✅ **Multiple accounts** — load unlimited `.session` files
- ✅ **Proxy rotation** — random SOCKS5/HTTP proxies from pool
- ✅ **Session health check** — auto-detect and skip dead sessions
- ✅ **8 report reasons** — Spam, Violence, Pornography, Child Abuse, Fake, Copyright, Personal Details, Other
- ✅ **EN/RU language support** — switch interface language
- ✅ **Random delays** — avoid detection
- ✅ **Real report message** — sends descriptive complaint text with each report

---

## Requirements

- Python 3.10+
- Telegram API credentials ([my.telegram.org](https://my.telegram.org))
- Pyrogram `.session` files (purchased separately)
- SOCKS5 or HTTP proxies (purchased separately)

---

## Installation

```bash
git clone https://github.com/tolerant2u/telegram-reporter.git
cd telegram-reporter
pip install -r requirements.txt
