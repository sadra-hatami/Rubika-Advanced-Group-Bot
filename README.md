<div align="center">

# Rubika Advanced Group Bot
# 🐉🤖

### A Large-Scale Persian Rubika Group Platform

A high-capacity group bot for Rubika with **moderation**, **automation**, **leveling**, **custom commands**, **entertainment**, and **SQLite persistence** — the current flagship group project in this collection.

<br>

# 👨‍💻 **Sadra Hatami**

### *Developer • Software Engineer • Creator*

<br>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rubka](https://img.shields.io/badge/Rubka-Rubika%20Bot-8E44AD?style=for-the-badge)](https://pypi.org/)
[![AsyncIO](https://img.shields.io/badge/AsyncIO-Asynchronous-2C3E50?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![aiohttp](https://img.shields.io/badge/aiohttp-HTTP%20Client-2C3E50?style=for-the-badge)](https://docs.aiohttp.org/)
[![Requests](https://img.shields.io/badge/Requests-HTTP%20Library-20232A?style=for-the-badge)](https://requests.readthedocs.io/)
[![HTTPX](https://img.shields.io/badge/HTTPX-HTTP%20Client-5A29E4?style=for-the-badge)](https://www.python-httpx.org/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Parsing-4CAF50?style=for-the-badge)](https://www.crummy.com/software/BeautifulSoup/)
[![Jdatetime](https://img.shields.io/badge/jdatetime-Jalali%20Date-009688?style=for-the-badge)](https://pypi.org/project/jdatetime/)
[![AI](https://img.shields.io/badge/AI-Integrated-FF6F00?style=for-the-badge)](#-ai-system)
[![Automation](https://img.shields.io/badge/Automation-Enabled-0078D6?style=for-the-badge)](#️-automation)
[![Moderation](https://img.shields.io/badge/Moderation-Enabled-C0392B?style=for-the-badge)](#️-security--moderation)
[![XP](https://img.shields.io/badge/XP%20%26%20Levels-Enabled-8E44AD?style=for-the-badge)](#-levels-xp--badges)
[![Games](https://img.shields.io/badge/Games-Enabled-E67E22?style=for-the-badge)](#-games--entertainment)
[![Persian](https://img.shields.io/badge/Language-Persian-success?style=for-the-badge)](https://en.wikipedia.org/wiki/Persian_language)
[![RTL](https://img.shields.io/badge/Direction-RTL-1ABC9C?style=for-the-badge)](https://en.wikipedia.org/wiki/Right-to-left)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
![Open Source](https://img.shields.io/badge/Open_Source-Project-black?style=for-the-badge&logo=github)

<br>

[🌐 GitHub Profile](https://github.com/sadra-hatami)
•
[📘 نسخه فارسی راهنما](README.fa.md)
•
[📧 Email](mailto:sadra.hatami.1732@gmail.com)

</div>

---

# 📑 Table of Contents

- [About](#-about)
- [Related Repositories](#-related-repositories)
- [Why This Version?](#-why-this-version)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Technologies](#️-technologies)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#️-usage)
- [Target Audience](#-target-audience)
- [Roadmap](#️-roadmap)
- [FAQ](#-faq)
- [Security Notes](#-security-notes)
- [Contributing](#-contributing)
- [Contact](#-contact)
- [License](#-license)
- [Copyright](#-copyright)
- [Support](#-support)

---

# 📖 About

**Rubika Advanced Group Bot** is the current flagship group platform in this profile.

It is a large asynchronous Rubika bot: owners add it to a group, grant admin rights, and turn systems on per chat. Settings, levels, warnings, custom commands, and logs live in SQLite so they survive a restart.

This repository now holds the newest group codebase. The previous full group platform lives in [Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot).

> **Tagline:** *A Persian Rubika group platform with moderation, automation, leveling, and entertainment tools.*

---

# 🔗 Related Repositories

The messaging projects in this profile now split like this:

| Repository | What it is now |
|------------|----------------|
| **[Rubika Advanced Group Bot](https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot)** | Newest group platform (this repo) |
| **[Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot)** | Previous complete group platform |
| **[Countries War Bot](https://github.com/sadra-hatami/Countries-War-Bot)** | Nation strategy game bot |
| **[Telegram Rubika Account Panel](https://github.com/sadra-hatami/Telegram-Rubika-Account-Panel)** | Telegram panel for a Rubika user account |

Use this repository when a group needs the latest platform.  
Use **Rubika Group Bot** when you want the earlier full group build.  
Use **Countries War Bot** for the strategy game.  
Use the **Account Panel** only for Telegram control of a user account, not for group management.

---

# 🚀 Why This Version?

The earlier group platform already combined locks, games, and saved settings.

This version extends that idea:

- More per-group tables in SQLite
- XP, levels, and badges
- Custom commands and auto responders
- Welcome, goodbye, and reminder tools
- Polls, events, giveaways, and notes
- Stronger operator controls for a running community

It is still one process and one database file. It is not a cloud dashboard.

---

# ✨ Key Features

## 🛡️ Moderation

- Content filters and lock-style controls
- Warnings with configurable action
- Blacklist words and whitelist links
- Bot protection for the group
- Optional log channel

## ⚙️ Automation

- Welcome and goodbye messages
- Custom commands
- Auto responders and custom reactions
- Timers and reminders
- Invite-link records

## 🏆 Engagement

- XP and levels
- Badges and achievements
- Group leaderboard
- Daily rewards
- User notes and favorites

## 🎮 Group tools

- Polls and quizzes
- Events and giveaways
- Tags and topics
- Optional AI reply hook

## 💾 Persistence

- SQLite (`chats.db` and related tables)
- Per-group settings that survive a restart

---

# 📁 Project Structure

```text
Rubika-Advanced-Group-Bot/
├── index.py
├── chats.db          # created at runtime — do not commit
└── README.md
```

Run the bot from `index.py`. Keep tokens, admin IDs, and channel links out of the file.

---

# 🛠️ Technologies

- Python 3.8+
- `rubka`
- asyncio
- SQLite
- aiohttp / httpx / requests
- BeautifulSoup
- jdatetime

---

# 🚀 Installation

```bash
git clone https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot.git
cd Rubika-Advanced-Group-Bot
pip install rubka aiohttp httpx requests beautifulsoup4 jdatetime
```

```bash
python index.py
```

---

# ⚙️ Configuration

```text
RUBIKA_BOT_TOKEN
RUBIKA_ADMIN_ID
AI_API_URL
```

`.gitignore`:

```text
.env
chats.db
__pycache__/
```

---

# ▶️ Usage

1. Set secrets in the environment.
2. Start `index.py`.
3. Add the bot to a Rubika group.
4. Grant administrator permission.
5. Activate the group, then turn systems on as needed.

Most tools are **group features**. A private chat with the bot is not a substitute for adding it to a group.

---

# 🎓 Target Audience

- Group owners who need a full community platform
- Developers studying a large `rubka` application
- People who already used the previous build in [Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot)

---

# 🗺️ Roadmap

- Remove unused stub blocks
- Split handlers into packages
- Safer default secrets
- Clearer command documentation

---

# ❓ FAQ

### How is this different from Rubika Group Bot now?

**Rubika Group Bot** keeps the previous complete group platform.  
**This repository** is the newest, larger group codebase.

### How is this different from Countries War Bot?

That project is a nation strategy game. This project manages a Rubika group.

### Do settings survive a restart?

Yes, when SQLite is working. Do not delete `chats.db` if you want to keep group data.

---

# 🔐 Security Notes

- Never commit the bot token, admin chat ID, or channel join links.
- If those values were ever published, replace them.
- Keep `chats.db` private.

---

# 🤝 Contributing

Cleanup, documentation, and safer configuration are welcome.

---

# 📬 Contact

**Developer:**

### Sadra Hatami

📧 [Email](mailto:sadra.hatami.1732@gmail.com)

🌐 [GitHub](https://github.com/sadra-hatami)

---

# 📄 License

This project is licensed under the **MIT License**.

---

# © Copyright

© 2026 **Sadra Hatami**

---

# ⭐ Support

If this platform helped you run a Rubika group, please consider giving it a ⭐ on GitHub.

---

<div align="center">

## Designed & Developed with ❤️ for the developer community of Iran and the world by **Sadra Hatami**

</div>
