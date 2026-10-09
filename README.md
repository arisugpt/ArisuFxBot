# 🚀 ArisuFxBot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=for-the-badge&logo=telegram)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)
![Author](https://img.shields.io/badge/Author-ArisuGpt-purple?style=for-the-badge)

**A high-performance Telegram Bot for extracting, inspecting, modding, repacking, and hex-padding Unity AssetBundles.**  
Powered by **[ArisuFxPy](https://github.com/arisugpt/ArisuFxPy)**.

[📢 Official Telegram Channel](https://t.me/hackinjectlab) • [🐛 Report Issues](https://github.com/arisugpt/ArisuFxBot/issues)

</div>

---

## 🌟 Key Features

- 📋 **Asset Hierarchy & Info Table**: Extract all Path IDs, Class Types, Asset Names (with `Unnamed Asset` fallback), and byte sizes into a clean, searchable table document (`.txt`).
- 📤 **TypeTree Dump Export**: Dump asset data hierarchies into human-readable `.txt` or `.json` formats.
- 📥 **TypeTree Dump Import & Patching**: Upload edited JSON/Text dumps to instantly patch game assets.
- 📦 **Raw Data Extraction & Injection**: Export raw asset binaries (`.dat`) or inject custom modified payloads.
- 💾 **Save & Compression**: Repack bundles with standard **LZ4** (Fast), **LZMA** (High Compression), or uncompressed (**None**).
- 🔢 **Hex Padding (0x00 Null Byte Injector)**: Pad any modified file to an exact target byte size with `0x00` null bytes and automatic size verification.
- 🧹 **Automatic Inactivity Cleanup**: Sweeps user memory and purges temporary disk files after **10 minutes** of inactivity to keep your Termux / VPS lightweight.
- 📊 **Real-Time Console Logs**: Live terminal logging for all user interactions, button clicks, file uploads, and modding operations.

---

## 🚀 Future Upgrades: Adding Image, Audio & Video Features

If you want to upgrade this bot with advanced media extraction features (such as exporting textures to `.png`, dumping audio to `.wav`, or extracting 3D models), you can easily plug into the rich class system of **[ArisuFxPy](https://github.com/arisugpt/ArisuFxPy)**:

- 🖼️ **Textures & Images**: Use `classes.Texture2D` (access `obj.read().image` to export PIL / PNG images).
- 🎵 **Audio Clips**: Use `classes.AudioClip` (access `obj.read().samples` to extract raw audio streams).
- 🎬 **Video & Cutscenes**: Use `classes.MovieTexture` or `classes.VideoClip`.
- 🧊 **3D Meshes**: Use `classes.Mesh` to parse vertices, faces, and export 3D `.obj` models.

> 📖 **Want to learn more & view full class references?**  
> To explore class structures, methods, and complete code samples, you must visit and read our official core library repository:  
> 👉 **[Visit ArisuFxPy on GitHub](https://github.com/arisugpt/ArisuFxPy)**

---

## 🔑 Bot Token Configuration

You can easily configure your Telegram Bot Token in **two different ways**:

### Method 1: Manual Edit (Recommended for Beginners)
Open `config.py` (or `bot.py`) in any text editor (**Notepad** on PC, **nano** on VPS/Termux, or **Acode** on Android):
```python
# Open config.py and replace with your token from @BotFather:
DEFAULT_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

### Method 2: Environment Variable
```bash
export BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

---

## 📱 Android Termux Installation Guide

Run ArisuFxBot directly on your Android phone without needing a computer or VPS!

### Step 1: Install Termux & Dependencies
Open Termux and run:
```bash
pkg update && pkg upgrade -y
pkg install python git clang -y
```

### Step 2: Clone Repository
```bash
git clone https://github.com/arisugpt/ArisuFxBot.git
cd ArisuFxBot
```

### Step 3: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 4: Configure Bot Token
Open `config.py` in `nano`:
```bash
nano config.py
```
*(Paste your Bot Token inside `DEFAULT_BOT_TOKEN = "..."`, press `Ctrl+O` then `Enter` to save, and `Ctrl+X` to exit)*

### Step 5: Start the Bot
```bash
python bot.py
```

> 💡 **Keep Bot Running in Background on Termux:**
> ```bash
> pkg install tmux -y
> tmux new -s arisufx
> python bot.py
> ```
> *(Detach anytime with `Ctrl+B` then `D`. Reattach with `tmux attach -t arisufx`)*

---

## 🖥️ VPS (Linux / Ubuntu / Debian) Installation Guide

Host ArisuFxBot 24/7 on any cloud VPS (DigitalOcean, AWS, Linode, Google Cloud, Oracle).

### Step 1: Update System & Install Python / Git
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

### Step 2: Clone Repository
```bash
git clone https://github.com/arisugpt/ArisuFxBot.git
cd ArisuFxBot
```

### Step 3: Setup Virtual Environment & Install Requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Token
```bash
nano config.py
```
*(Enter your Telegram Bot Token and save)*

### Step 5: Run as Background Service (Systemd)
To ensure your bot restarts automatically if the server reboots:

Create a service file:
```bash
sudo nano /etc/systemd/system/arisufxbot.service
```

Paste the following configuration:
```ini
[Unit]
Description=ArisuFxBot Telegram Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ArisuFxBot
ExecStart=/root/ArisuFxBot/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable arisufxbot
sudo systemctl start arisufxbot
```

Check live logs:
```bash
sudo journalctl -u arisufxbot -f
```

---

## 💻 Windows PC Installation Guide

1. **Install Python**: Download Python 3.10+ from [python.org](https://www.python.org/) (ensure **"Add Python to PATH"** is checked).
2. **Open Command Prompt / PowerShell**:
   ```powershell
   git clone https://github.com/arisugpt/ArisuFxBot.git
   cd ArisuFxBot
   pip install -r requirements.txt
   ```
3. **Edit Bot Token**:
   Open `config.py` in **Notepad**, paste your token, and save.
4. **Run Bot**:
   ```powershell
   python bot.py
   ```

---

## 🎮 Telegram Bot Commands

| Command | Description |
| :--- | :--- |
| `/start` | Launch bot and display interactive menu |
| `/help` | Detailed instructions for all modding features |
| `/status` | View active session details and remaining timeout |
| `/reset` | Clear session cache and free memory immediately |
| `/cancel` | Cancel any current pending input step |

---

## 🔒 Session Isolation & Auto-Cleanup

- Each user has a completely isolated session directory (`sessions/<user_id>/`).
- Active sessions automatically monitor idle time.
- If a user is inactive for **10 minutes**, the auto-cleaner daemon automatically frees RAM and wipes temporary files from disk to prevent storage bloat.

---

<br>

<div align="center">

```
╭────────────────────────────────────────────────────────────────────────╮
│                                                                        │
│                  👑  𝐂 𝐑 𝐄 𝐃 𝐈 𝐓 𝐒  &  𝐀 𝐔 𝐓 𝐇 𝐎 𝐑 𝐒 𝐇 𝐈 𝐏               │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯
```

### 👑 𝐂𝐫𝐞𝐝𝐢𝐭𝐬 & 𝐀𝐮𝐭𝐡𝐨𝐫𝐬𝐡𝐢𝐩

| 👤 **Architect & Lead Developer** | 📢 **Official Channel & Hub** |
| :---: | :---: |
| **`ArisuGpt`** | [**@hackinjectlab**](https://t.me/hackinjectlab) |

> 💎 *100% Concept, Modding Logic, Termux/VPS Port & Architecture originally created by **ArisuGpt**.*  
> 🔗 *Join the official channel for exclusive modding scripts, tools & updates:* [**t.me/hackinjectlab**](https://t.me/hackinjectlab)

<br>

```
╭────────────────────────────────────────────────────────────────────────╮
│                                                                        │
│                          📜  𝐋 𝐈 𝐂 𝐄 𝐍 𝐒 𝐄                             │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯
```

### 📜 𝐋𝐢𝐜𝐞𝐧𝐬𝐞

[![License: MIT](https://img.shields.io/badge/License-MIT-F5A623.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

```text
⚖️ Copyright (c) 2026 ArisuGpt (@hackinjectlab)

This project is licensed under the MIT License.
Permission is hereby granted to use, inspect, fork, and adapt for research.
```

<br>

```
╭────────────────────────────────────────────────────────────────────────╮
│                                                                        │
│       ⚠️  𝐄 𝐃 𝐔 𝐂 𝐀 𝐓 𝐈 𝐎 𝐍 𝐀 𝐋  &  𝐑 𝐄 𝐒 𝐄 𝐀 𝐑 𝐂 𝐇  𝐃 𝐈 𝐒 𝐂 𝐋 𝐀 𝐈 𝐌 𝐄 𝐑       │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯
```

### ⚠️ 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧𝐚𝐥 & 𝐑𝐞𝐬𝐞𝐚𝐫𝐜𝐡 𝐃𝐢𝐬𝐜𝐥𝐚𝐢𝐦𝐞𝐫

</div>

> [!CAUTION]
> #### 🛑 FOR EDUCATIONAL, SECURITY AUDIT & REVERSE-ENGINEERING STUDY ONLY
>
> 🔹 **Purely Research Oriented:** This software, library integrations, and Telegram Bot framework are created strictly for **educational research, internal data auditing, and reverse-engineering exploration** of Unity asset files.  
> 🔹 **Zero Tolerance for Misuse:** The creators and maintainers **do not endorse, encourage, or facilitate** piracy, copyright infringement, or unauthorized distribution of third-party proprietary assets.  
> 🔹 **User Accountability:** You are solely responsible for ensuring you have full legal rights, licenses, and permissions before unpacking, editing, or repacking any binary asset files.

<br>

<div align="center">

✦•······················•✦•······················•✦  
**Crafted with ⚡ and passion by ArisuGpt**  
*Telegram Community: [@hackinjectlab](https://t.me/hackinjectlab)*  
✦•······················•✦•······················•✦

</div>
