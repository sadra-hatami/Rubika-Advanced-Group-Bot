<div align="center">

# Rubika Advanced Group Bot
# 🤖

### A Powerful Persian Rubika Group Management, Automation & AI Bot

A comprehensive multifunctional Rubika bot built with Python, featuring advanced group management, moderation, automation, AI integration, learning systems, entertainment, user progression, custom commands, and database-backed group configuration.

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
[![AI](https://img.shields.io/badge/AI-Integrated-FF6F00?style=for-the-badge)](#-ai-system)
[![Automation](https://img.shields.io/badge/Automation-Enabled-0078D6?style=for-the-badge)](#️-automation)
[![Persian](https://img.shields.io/badge/Language-Persian-success?style=for-the-badge)](https://en.wikipedia.org/wiki/Persian_language)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
![GitHub](https://img.shields.io/badge/Open_Source-Project-black?style=for-the-badge&logo=github)

<br>

[🌐 GitHub Profile](https://github.com/sadra-hatami)
•
[📧 Email](mailto:sadra.hatami.1732@gmail.com)

</div>

---

# 📑 Table of Contents

- [About](#-about)
- [Related Repositories](#-related-repositories)
- [Why This Bot?](#-why-this-bot)
- [Key Features](#-key-features)
- [Group Management](#-group-management)
- [Security & Moderation](#️-security--moderation)
- [AI System](#-ai-system)
- [Learning System](#-learning-system)
- [User System](#-user-system)
- [Levels, XP & Badges](#-levels-xp--badges)
- [Automation](#️-automation)
- [Games & Entertainment](#-games--entertainment)
- [Reports & Statistics](#-reports--statistics)
- [Database](#-database)
- [Project Structure](#-project-structure)
- [Technologies](#️-technologies)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#️-usage)
- [Command Examples](#-command-examples)
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

**Rubika Advanced Group Bot** is a multifunctional Persian Rubika group bot developed with Python and the `rubka` library.

The project combines group administration, moderation, automation, AI interaction, learning, entertainment, user progression, custom commands, information services, and persistent SQLite storage into one platform.

It is designed for Persian-speaking Rubika communities. Administrators add the bot to a group, grant it admin rights, and activate it with `فعال`. After that, most systems can be turned on or off separately for that group.

The current implementation is a large asynchronous Python application (`index.py`) with SQLite persistence and optional external HTTP / API integrations.

> **Tagline:** *A powerful Persian Rubika bot for group management, AI, security, entertainment, learning, and automation.*

---

# 🔗 Related Repositories

These projects belong to the same Rubika / messaging collection, but they are not the same bot.

| Repository | Role |
|------------|------|
| **[Countries War Bot](https://github.com/sadra-hatami/Countries-War-Bot)** | Nation strategy game |
| **[Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot)** | Lightweight group lock bot |
| **[Rubika Advanced Group Bot](https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot)** | Full group management, automation, and extra tools |
| **[Telegram Rubika Account Panel](https://github.com/sadra-hatami/Telegram-Rubika-Account-Panel)** | Telegram panel for a Rubika user account (this repo) |

Use this repository when a group needs management, locks, games, AI, and saved settings.  
Use **Rubika Group Bot** when only simple locks are enough.  
Use **Telegram Rubika Account Panel** only when you need a Telegram remote control for a user account, not a group bot.

---

# 🚀 Why This Bot?

Managing a large group often needs several tools at once: locks, warnings, replies, games, and reports.

**Rubika Advanced Group Bot** keeps those systems in one process and one database.

The project focuses on:

- Group security and moderation
- Administrative automation
- Optional AI-powered answers
- Custom commands and learned replies
- User permissions, XP, and levels
- Interactive games
- Group reports and statistics
- Persistent SQLite storage
- Persian-language commands

---

# ✨ Key Features

## 🤖 Intelligence & Interaction

- AI-powered question answering
- Learning system
- Custom commands
- Automatic responses
- Speaker modes

## 👑 Group Administration

- Group owner management
- Assistant administrators
- Special users and exempt users
- Group rules and group status
- Content locks
- Warnings and mute management

## 🛡️ Moderation & Protection

- Anti-link, anti-advertisement, anti-curse
- Anti-emoji, anti-edit, anti-mention
- GIF and content-type locks
- Blacklist words and whitelist links
- Automatic message deletion

## 🏆 User Engagement

- XP and levels
- Badges and leaderboards
- User profiles and notes
- Daily rewards

## 🎮 Entertainment

- Math, word, number, and dice games
- Hafez fortune, riddles, jokes, and facts
- Extra fun commands for group chat

## 📊 Group Tools

- Reports and statistics
- Polls, events, timers, and reminders
- Tags, invite links, and auto responders

---

# 👑 Group Management

The bot is built for group owners and administrators.

## Bot control

```text
فعال
ربات روشن
ربات خاموش
```

`فعال` registers the group. After that, settings are stored per group in SQLite.

## Rules

```text
قوانین
تنظیم قوانین
```

## Locks

Example:

```text
لینک قفل
لینک باز
```

Lock categories include links, text, stickers, voice, video, images, GIFs, files, forwards, edits, emojis, and more.

Most lock and filter systems can be enabled independently. You do not have to turn every feature on.

---

# 🛡️ Security & Moderation

| System | Role |
|--------|------|
| Anti-Link | Controls unwanted links |
| Anti-Advertisement | Controls ads |
| Anti-Curse | Filters blocked language |
| Anti-Emoji | Controls emoji spam |
| Anti-Edit | Watches edited messages |
| Anti-Mention | Controls mentions |
| Auto-delete | Removes matched messages |

The bot must be a group admin with delete permission for these systems to work.

---

# 🤖 AI System

Questions can be sent with a `+` prefix, for example:

```text
+پایتون چیست؟
```

AI replies depend on an external API. If that API is not configured, the rest of the group tools can still run.

---

# 🧠 Learning System

Administrators can teach custom replies and commands so the bot answers repeated questions in that group.

---

# 👤 User System

The bot can keep group-specific user records such as profiles, notes, warnings, and permission levels.

---

# 🏆 Levels, XP & Badges

Active members can receive XP in the group. Levels and leaderboards are stored in the database and stay after a restart.

```text
لیست برترینها
```

---

# ⚙️ Automation

Optional automation includes welcome messages, auto replies, timers, reminders, and scheduled group tools. Each item can be limited to the groups where it is enabled.

---

# 🎮 Games & Entertainment

```text
بازی ریاضی
فال حافظ
```

Games are group features. They are not a full private-chat app.

---

# 📊 Reports & Statistics

Administrators can request group reports and activity summaries from the saved database records.

---

# 💾 Database

Settings are stored in SQLite (`chats.db`).

That includes:

- Per-group locks and filters
- Admins and permissions
- Warnings and mutes
- Custom commands
- XP and levels

Because data is on disk, most settings survive a restart. This is the main difference from the lightweight [Rubika Group Bot](https://github.com/sadra-hatami/Rubika-Group-Bot), which keeps lock flags in memory.

---

# 📁 Project Structure

```text
Rubika-Advanced-Group-Bot/
├── index.py      # Main bot application
├── chats.db      # Created at runtime (do not commit secrets)
└── README.md
```

Run the bot from `index.py`. Keep tokens and API URLs out of the file.

---

# 🛠️ Technologies

- Python 3.8+
- `rubka`
- asyncio
- SQLite
- aiohttp, requests, httpx
- BeautifulSoup
- jdatetime

---

# 🚀 Installation

```bash
git clone https://github.com/sadra-hatami/Rubika-Advanced-Group-Bot.git
cd Rubika-Advanced-Group-Bot
pip install rubka aiohttp requests httpx beautifulsoup4 jdatetime
```

```bash
python index.py
```

---

# ⚙️ Configuration

Use environment variables instead of hardcoded secrets:

```text
RUBIKA_BOT_TOKEN
RUBIKA_ADMIN_ID
AI_API_URL
```

Add to `.gitignore`:

```text
.env
chats.db
__pycache__/
```

---

# ▶️ Usage

1. Start `index.py`.
2. Add the bot to a Rubika group.
3. Grant administrator permission.
4. Send `فعال` in that group.
5. Turn individual systems on or off as needed.

The main features are **group features**. Opening a private chat with the bot is not a substitute for adding it to a group.

---

# 📚 Command Examples

```text
فعال
راهنما
وضعیت
قوانین
ربات روشن
ربات خاموش
ضد لینک روشن
ضد لینک خاموش
لینک قفل
لینک باز
+پایتون چیست؟
بازی ریاضی
فال حافظ
لیست برترینها
```

---

# 🎯 Target Audience

- Rubika group owners and administrators
- Communities that need moderation plus extra group tools
- Python developers studying a large `rubka` bot
- Users who already tried the smaller Group Bot and need more systems

---

# 🗺️ Roadmap

Possible later improvements:

- Clearer split between group handlers and private helpers
- Safer default configuration through `.env`
- Better logging
- Smaller optional modules for games and AI
- Documentation for each command family

---

# ❓ FAQ

### Does the bot work without a group?

Most features need a group. Locks, filters, XP, reports, and games are stored and applied per group.

### Can I enable only some features?

Yes. Systems such as anti-link, speaker, and auto-delete can be turned on or off separately.

### How is this different from Rubika Group Bot?

Rubika Group Bot is a small lock-only script. This repository is the full platform with database, moderation packs, games, and optional AI.

### How is this different from Telegram Rubika Account Panel?

That project is a Telegram remote control for a Rubika **user account** (`rubpy`). This project is a Rubika **group bot** (`rubka`).

### Do settings survive a restart?

Yes, when SQLite is working. Do not delete `chats.db` if you want to keep group configuration.

---

# 🔐 Security Notes

- Never commit the bot token or API keys.
- If a token was ever published, replace it.
- Give the bot only the group permissions it needs.
- Keep `chats.db` private; it can contain group and user records.

---

# 🤝 Contributing

Contributions are welcome:

- Bug reports
- Command documentation
- Safer configuration
- Performance and handler cleanup
- Pull requests

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

All rights reserved.

The source code, command texts, and project documentation are protected under applicable copyright laws.

---

# ⭐ Support

If this bot helped you manage a Rubika group, please consider giving it a ⭐ on GitHub.

---

<div align="center">

## Designed & Developed with ❤️ for the developer community of Iran and the world by **Sadra Hatami**

</div>
