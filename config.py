"""
=============================================================================
ArisuFxBot - Unity AssetBundle Modder & Hex Padder Telegram Bot
Created & Developed by: ArisuGpt
Official Telegram: @hackinjectlab
=============================================================================
"""

import os

# ===========================================================================
# 🔑 BOT CONFIGURATION - EDIT YOUR TELEGRAM BOT TOKEN HERE
# ===========================================================================
# You can edit this file in any text editor (Notepad, nano, vim, Acode on Android)
# Enter the token you received from Telegram's @BotFather between the quotes:
DEFAULT_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# If environment variable BOT_TOKEN is set, it will take precedence:
BOT_TOKEN = os.environ.get("BOT_TOKEN", DEFAULT_BOT_TOKEN).strip()

# ===========================================================================
# ⚙️ BOT SETTINGS
# ===========================================================================
# Inactive session timeout in seconds (Default: 600 seconds = 10 minutes)
SESSION_TIMEOUT_SECONDS = int(os.environ.get("SESSION_TIMEOUT_SECONDS", "600"))

# Base temporary directory for user sessions
SESSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sessions")

# Maximum upload file size in bytes (Telegram Bot API limit is 20MB for downloads)
MAX_FILE_SIZE = 20 * 1024 * 1024

# Channel & Developer Credits
AUTHOR = "ArisuGpt"
TELEGRAM_CHANNEL = "@hackinjectlab"
TELEGRAM_URL = "https://t.me/hackinjectlab"
GITHUB_REPO = "https://github.com/arisugpt/ArisuFxBot"
