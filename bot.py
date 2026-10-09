"""
=============================================================================
ArisuFxBot - Unity AssetBundle Modder & Hex Padder Telegram Bot
Created & Developed by: ArisuGpt
Official Telegram Channel: @hackinjectlab
GitHub: https://github.com/arisugpt/ArisuFxBot
=============================================================================
"""

import os
import sys
import json
import time
import shutil

# Ensure UTF-8 output encoding for console across all OS (Windows, Linux, Termux)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import telebot
from telebot import types
from tabulate import tabulate

from config import (
    BOT_TOKEN,
    AUTHOR,
    TELEGRAM_CHANNEL,
    TELEGRAM_URL,
    MAX_FILE_SIZE,
    SESSION_TIMEOUT_SECONDS
)
from session_manager import SessionManager, UserSession

# Initialize Bot & Session Manager
if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
    print("=" * 60)
    print("[-] ERROR: BOT_TOKEN is not set!")
    print("[-] Please edit 'config.py' or 'bot.py' and enter your bot token.")
    print("=" * 60)
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
session_manager = SessionManager(timeout_seconds=SESSION_TIMEOUT_SECONDS)


def log_action(tag: str, user_id: int, username: str = "", message: str = ""):
    """Print structured, real-time live logs to console"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    uname = f"@{username}" if username else "NoUsername"
    print(f"[{timestamp}] [{tag}] [User: {user_id} | {uname}] {message}")


# ===========================================================================
# 🔘 INLINE KEYBOARDS
# ===========================================================================

def get_main_menu_keyboard():
    """Generates the interactive main menu keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    b_info = types.InlineKeyboardButton("📋 Asset Info Table", callback_data="action_info_table")
    b_export_dump = types.InlineKeyboardButton("📤 Export Dump", callback_data="action_export_dump")
    b_import_dump = types.InlineKeyboardButton("📥 Import Dump", callback_data="action_import_dump")
    b_export_raw = types.InlineKeyboardButton("📦 Export Raw Data", callback_data="action_export_raw")
    b_import_raw = types.InlineKeyboardButton("📥 Import Raw Data", callback_data="action_import_raw")
    b_save = types.InlineKeyboardButton("💾 Save & Compress", callback_data="action_save_compress")
    b_hex = types.InlineKeyboardButton("🔢 Hex Padding (0x00)", callback_data="action_hex_padding")
    b_reset = types.InlineKeyboardButton("🔄 Reset Session", callback_data="action_reset_session")
    
    markup.add(b_info)
    markup.add(b_export_dump, b_import_dump)
    markup.add(b_export_raw, b_import_raw)
    markup.add(b_save)
    markup.add(b_hex)
    markup.add(b_reset)
    return markup


def get_compression_keyboard():
    """Generates compression selection keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    b_lz4 = types.InlineKeyboardButton("⚡ LZ4 (Fast & Standard)", callback_data="compress_lz4")
    b_lzma = types.InlineKeyboardButton("🗜️ LZMA (Maximum Compression)", callback_data="compress_lzma")
    b_none = types.InlineKeyboardButton("📦 Uncompressed (None)", callback_data="compress_none")
    b_back = types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="action_back_menu")
    markup.add(b_lz4, b_lzma, b_none, b_back)
    return markup


def get_dump_format_keyboard():
    """Generates format selection keyboard for export"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    b_txt = types.InlineKeyboardButton("📄 Text (.txt)", callback_data="dump_fmt_txt")
    b_json = types.InlineKeyboardButton("📋 JSON (.json)", callback_data="dump_fmt_json")
    b_cancel = types.InlineKeyboardButton("❌ Cancel", callback_data="action_back_menu")
    markup.add(b_txt, b_json, b_cancel)
    return markup


# ===========================================================================
# 🚀 COMMAND HANDLERS
# ===========================================================================

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    log_action("COMMAND /start", user_id, username, "User started the bot.")
    
    welcome_text = (
        "🎮 *Welcome to ArisuFxBot!*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "A high-performance Unity AssetBundle Modder, Inspector & Hex Padder powered by *ArisuFxPy*.\n\n"
        "✨ *Features:*\n"
        "• 📋 View full Asset Hierarchy & Info Table\n"
        "• 📤 Export TypeTree Dump (.txt / .json)\n"
        "• 📥 Import & Patch TypeTree Dump\n"
        "• 📦 Export / Import Raw Binary (.dat)\n"
        "• 💾 Save & Compress (LZ4 / LZMA / None)\n"
        "• 🔢 Hex Padding (0x00 Null Byte Injector)\n"
        "• 🧹 Automatic 10-Min Session & Disk Cleanup\n\n"
        f"👑 *Created by:* {AUTHOR}\n"
        f"📢 *Official Telegram:* [{TELEGRAM_CHANNEL}]({TELEGRAM_URL})\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👉 *To begin, upload or send your Unity AssetBundle (.bundle, .bin, .unity3d, .assets) file below!*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", disable_web_page_preview=True)


@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    log_action("COMMAND /help", user_id, username, "User asked for help.")
    
    help_text = (
        "📖 *ArisuFxBot Usage Guide*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "1. *Upload Bundle:* Send any `.bundle`, `.bin`, `.assets`, or `.unity3d` file (up to 20MB).\n"
        "2. *Select Action:* Use the inline buttons to view info, export dumps, or edit.\n"
        "3. *Dump Export/Import:* Dump assets as readable JSON/Text, edit values, and re-import them.\n"
        "4. *Raw Data:* Dump exact binary bytes (.dat) or inject updated raw assets.\n"
        "5. *Compress & Repack:* Save your modified bundle with LZ4 (recommended) or LZMA.\n"
        "6. *Hex Padding:* Match target size byte-by-byte using 0x00 injection.\n"
        "7. *Session Cleanup:* All temporary files are automatically deleted after 10 minutes of inactivity.\n\n"
        "Commands:\n"
        "/start - Welcome screen\n"
        "/help - Display this guide\n"
        "/status - View current active bundle session\n"
        "/reset - Delete current session & free memory\n"
        "/cancel - Cancel current pending input\n\n"
        f"👑 *Developer:* {AUTHOR} | {TELEGRAM_CHANNEL}"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")


@bot.message_handler(commands=['status'])
def handle_status(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    log_action("COMMAND /status", user_id, username, "Checking session status.")
    
    session = session_manager.get_session(user_id)
    if not session.env:
        bot.reply_to(message, "⚠️ No active bundle loaded! Send a file to start.")
        return

    remaining_time = max(0, int(SESSION_TIMEOUT_SECONDS - (time.time() - session.last_active)))
    file_size = os.path.getsize(session.current_filepath) if os.path.exists(session.current_filepath) else 0
    num_assets = len(session.env.objects)
    
    status_text = (
        "📊 *Active Session Status*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *File:* `{session.original_filename}`\n"
        f"• *Current Size:* `{file_size:,} bytes`\n"
        f"• *Total Assets:* `{num_assets}`\n"
        f"• *Inactivity Timeout:* `{remaining_time // 60}m {remaining_time % 60}s remaining`\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, status_text, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())


@bot.message_handler(commands=['reset', 'cancel'])
def handle_reset_or_cancel(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    log_action("COMMAND /reset", user_id, username, "User requested session reset / cancel.")
    
    session_manager.reset_session(user_id)
    bot.reply_to(message, "🧹 Session wiped and memory cleared! Send a new bundle file anytime.")


# ===========================================================================
# 📥 DOCUMENT / FILE UPLOAD HANDLER
# ===========================================================================

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    doc = message.document
    
    log_action("FILE UPLOAD", user_id, username, f"Received file: {doc.file_name} ({doc.file_size} bytes)")
    
    session = session_manager.get_session(user_id)
    
    # Check if user is in an IMPORT state (Dump or Raw Data)
    if session.state == "WAITING_DUMP_FILE":
        process_imported_dump_file(message, session)
        return
    elif session.state == "WAITING_RAW_FILE":
        process_imported_raw_file(message, session)
        return

    # Check file size limit
    if doc.file_size > MAX_FILE_SIZE:
        bot.reply_to(
            message,
            f"❌ *File too large!* ({doc.file_size / (1024*1024):.1f}MB)\n"
            f"Telegram Bot API limits bot downloads to 20MB. Please upload a smaller file.",
            parse_mode="Markdown"
        )
        return

    status_msg = bot.reply_to(message, "⏳ *Downloading and analyzing AssetBundle...*", parse_mode="Markdown")
    
    try:
        file_info = bot.get_file(doc.file_id)
        downloaded_bytes = bot.download_file(file_info.file_path)
        
        save_path = os.path.join(session.session_dir, doc.file_name)
        with open(save_path, "wb") as f:
            f.write(downloaded_bytes)
            
        # Parse bundle via ArisuFxPy
        session.set_file(save_path, doc.file_name)
        
        asset_count = len(session.env.objects)
        log_action("BUNDLE LOADED", user_id, username, f"Loaded '{doc.file_name}' with {asset_count} assets.")
        
        menu_text = (
            f"✅ *AssetBundle Loaded Successfully!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📁 *Filename:* `{doc.file_name}`\n"
            f"📊 *File Size:* `{len(downloaded_bytes):,} bytes`\n"
            f"🧩 *Total Assets:* `{asset_count}`\n"
            f"⏱️ *Session Auto-Cleanup:* In 10 minutes of inactivity\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Select an operation below:"
        )
        bot.edit_message_text(
            menu_text,
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id,
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        
    except Exception as e:
        log_action("ERROR LOAD", user_id, username, f"Failed to load bundle: {e}")
        bot.edit_message_text(
            f"❌ *Failed to parse AssetBundle:*\n`{str(e)}`\n\nEnsure this is a valid Unity AssetBundle or Serialized File.",
            chat_id=status_msg.chat.id,
            message_id=status_msg.message_id,
            parse_mode="Markdown"
        )


# ===========================================================================
# 🔘 INLINE BUTTON CALLBACKS
# ===========================================================================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    action = call.data
    
    log_action("BUTTON CLICK", user_id, username, f"Clicked button: {action}")
    session = session_manager.get_session(user_id)
    session.touch()
    
    # Check if a bundle is loaded
    if not session.env and action not in ["action_reset_session"]:
        bot.answer_callback_query(call.id, "⚠️ No active bundle found! Please send a bundle first.")
        bot.send_message(call.message.chat.id, "⚠️ No bundle loaded. Please upload a `.bundle` or `.bin` file to start!")
        return

    bot.answer_callback_query(call.id)

    # 1. Back to menu
    if action == "action_back_menu":
        session.state = "IDLE"
        session.state_data.clear()
        bot.edit_message_text(
            "📋 *Main Menu:* Select an option below:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )

    # 2. Asset Info Table
    elif action == "action_info_table":
        handle_action_info_table(call, session)

    # 3. Export Dump
    elif action == "action_export_dump":
        session.state = "WAITING_EXPORT_DUMP_PATH_ID"
        bot.send_message(
            call.message.chat.id,
            "📤 *Export TypeTree Dump*\n\nPlease enter the *Path ID* of the asset you want to dump (or send /cancel):",
            parse_mode="Markdown"
        )

    # 4. Import Dump
    elif action == "action_import_dump":
        session.state = "WAITING_IMPORT_DUMP_PATH_ID"
        bot.send_message(
            call.message.chat.id,
            "📥 *Import TypeTree Dump*\n\nPlease enter the *Path ID* of the target asset to patch (or send /cancel):",
            parse_mode="Markdown"
        )

    # 5. Export Raw Data
    elif action == "action_export_raw":
        session.state = "WAITING_EXPORT_RAW_PATH_ID"
        bot.send_message(
            call.message.chat.id,
            "📦 *Export Raw Asset (.dat)*\n\nPlease enter the *Path ID* to export raw bytes (or send /cancel):",
            parse_mode="Markdown"
        )

    # 6. Import Raw Data
    elif action == "action_import_raw":
        session.state = "WAITING_IMPORT_RAW_PATH_ID"
        bot.send_message(
            call.message.chat.id,
            "📥 *Import Raw Asset (.dat)*\n\nPlease enter the *Path ID* to inject raw bytes (or send /cancel):",
            parse_mode="Markdown"
        )

    # 7. Save & Compress
    elif action == "action_save_compress":
        bot.edit_message_text(
            "💾 *Save & Compress AssetBundle*\n\nSelect your desired compression format:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=get_compression_keyboard()
        )

    # 8. Perform Compression
    elif action in ["compress_lz4", "compress_lzma", "compress_none"]:
        handle_perform_compression(call, session, action)

    # 9. Hex Padding
    elif action == "action_hex_padding":
        handle_action_hex_padding_prompt(call, session)

    # 10. Format selection for Dump Export
    elif action in ["dump_fmt_txt", "dump_fmt_json"]:
        handle_perform_export_dump(call, session, action)

    # 11. Reset Session
    elif action == "action_reset_session":
        session_manager.reset_session(user_id)
        bot.edit_message_text(
            "🧹 *Session Reset Successfully!*\nMemory and temporary files have been wiped.\nSend a new file anytime to start fresh.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )


# ===========================================================================
# 📋 ASSET INFO TABLE GENERATION
# ===========================================================================

def handle_action_info_table(call, session: UserSession):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    log_action("INFO TABLE", user_id, username, f"Generating asset info table ({len(session.env.objects)} objects)")
    
    table_rows = []
    for idx, obj in enumerate(session.env.objects, 1):
        type_name = getattr(obj.type, "name", str(obj.type))
        name = ""
        try:
            data = obj.read()
            name = getattr(data, "name", getattr(data, "m_Name", ""))
        except Exception:
            name = ""
        table_rows.append([idx, obj.path_id, type_name, name or "-", f"{obj.byte_size:,}"])
        
    headers = ["#", "Path ID", "Type", "Name", "Size (bytes)"]
    table_str = tabulate(table_rows, headers=headers, tablefmt="grid")
    
    # Save as file so user can download it
    table_file_path = os.path.join(session.session_dir, f"{session.original_filename}_info_table.txt")
    with open(table_file_path, "w", encoding="utf-8") as f:
        f.write(f"AssetBundle: {session.original_filename}\n")
        f.write(f"Total Objects: {len(session.env.objects)}\n")
        f.write("Generated by ArisuFxBot (Telegram: @hackinjectlab)\n")
        f.write("=" * 70 + "\n\n")
        f.write(table_str)
        
    caption = f"📋 *Asset Info Table for `{session.original_filename}`*\nTotal Assets: `{len(session.env.objects)}`"
    with open(table_file_path, "rb") as f:
        bot.send_document(
            call.message.chat.id,
            f,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )


# ===========================================================================
# 📤 EXPORT DUMP LOGIC
# ===========================================================================

def handle_perform_export_dump(call, session: UserSession, format_choice: str):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    path_id = session.state_data.get("export_path_id")
    fmt = "json" if format_choice == "dump_fmt_json" else "txt"
    
    log_action("EXPORT DUMP", user_id, username, f"Exporting Path ID {path_id} as {fmt}")
    
    target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
    if not target_obj:
        bot.send_message(call.message.chat.id, f"❌ Asset with Path ID `{path_id}` not found!", parse_mode="Markdown")
        return

    try:
        tree = target_obj.read_typetree()
        dump_content = json.dumps(tree, indent=2, ensure_ascii=False)
        
        dump_filename = f"dump_{path_id}.{fmt}"
        dump_path = os.path.join(session.session_dir, dump_filename)
        with open(dump_path, "w", encoding="utf-8") as f:
            f.write(dump_content)
            
        type_name = getattr(target_obj.type, "name", str(target_obj.type))
        caption = (
            f"✅ *Dump Exported Successfully!*\n"
            f"• *Path ID:* `{path_id}`\n"
            f"• *Type:* `{type_name}`\n"
            f"• *Format:* `{fmt.upper()}`\n\n"
            f"Edit this file in any text editor and re-import via *📥 Import Dump*."
        )
        with open(dump_path, "rb") as f:
            bot.send_document(
                call.message.chat.id,
                f,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
        session.state = "IDLE"
        session.state_data.clear()
    except Exception as e:
        log_action("ERROR DUMP", user_id, username, f"Dump failed: {e}")
        bot.send_message(call.message.chat.id, f"❌ Failed to dump Path ID `{path_id}`: {e}", parse_mode="Markdown")


# ===========================================================================
# 📥 IMPORT DUMP FILE PROCESSING
# ===========================================================================

def process_imported_dump_file(message, session: UserSession):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    path_id = session.state_data.get("import_path_id")
    doc = message.document
    
    log_action("IMPORT DUMP FILE", user_id, username, f"Applying dump file: {doc.file_name} to Path ID: {path_id}")
    
    target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
    if not target_obj:
        bot.reply_to(message, f"❌ Error: Path ID `{path_id}` not found in loaded bundle!", parse_mode="Markdown")
        session.state = "IDLE"
        return
        
    try:
        file_info = bot.get_file(doc.file_id)
        file_bytes = bot.download_file(file_info.file_path)
        content_text = file_bytes.decode("utf-8")
        
        parsed_tree = json.loads(content_text)
        target_obj.save_typetree(parsed_tree)
        
        log_action("DUMP PATCHED", user_id, username, f"Successfully patched Path ID: {path_id}")
        bot.reply_to(
            message,
            f"🎉 *Success!* TypeTree dump successfully patched into Path ID: `{path_id}`.\n\n"
            f"👉 Don't forget to click *💾 Save & Compress* to export your final modded bundle file!",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        session.state = "IDLE"
        session.state_data.clear()
    except Exception as e:
        log_action("ERROR IMPORT DUMP", user_id, username, f"Failed: {e}")
        bot.reply_to(message, f"❌ *Failed to import dump:* {e}\nEnsure your file contains valid JSON structure.", parse_mode="Markdown")


# ===========================================================================
# 📥 IMPORT RAW FILE PROCESSING
# ===========================================================================

def process_imported_raw_file(message, session: UserSession):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    path_id = session.state_data.get("import_raw_path_id")
    doc = message.document
    
    log_action("IMPORT RAW FILE", user_id, username, f"Injecting raw dat: {doc.file_name} into Path ID: {path_id}")
    
    target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
    if not target_obj:
        bot.reply_to(message, f"❌ Error: Path ID `{path_id}` not found!", parse_mode="Markdown")
        session.state = "IDLE"
        return

    try:
        file_info = bot.get_file(doc.file_id)
        raw_bytes = bot.download_file(file_info.file_path)
        target_obj.set_raw_data(raw_bytes)
        
        log_action("RAW INJECTED", user_id, username, f"Injected {len(raw_bytes)} bytes into Path ID {path_id}")
        bot.reply_to(
            message,
            f"🎉 *Success!* Injected `{len(raw_bytes):,} bytes` of raw data into Path ID: `{path_id}`.\n\n"
            f"👉 Click *💾 Save & Compress* to repack your bundle file!",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        session.state = "IDLE"
        session.state_data.clear()
    except Exception as e:
        log_action("ERROR IMPORT RAW", user_id, username, f"Failed: {e}")
        bot.reply_to(message, f"❌ *Failed to inject raw data:* {e}", parse_mode="Markdown")


# ===========================================================================
# 💾 PERFORM COMPRESSION & SAVE
# ===========================================================================

def handle_perform_compression(call, session: UserSession, compress_action: str):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    
    packer_map = {
        "compress_lz4": "lz4",
        "compress_lzma": "lzma",
        "compress_none": "none"
    }
    packer = packer_map.get(compress_action, "lz4")
    log_action("COMPRESSION START", user_id, username, f"Packing bundle with packer='{packer}'")
    
    status_msg = bot.send_message(call.message.chat.id, f"⏳ *Repacking and compressing bundle with {packer.upper()}...*", parse_mode="Markdown")
    
    try:
        packed_bytes = session.env.file.save(packer=packer)
        
        out_filename = f"modded_{session.original_filename}"
        out_path = os.path.join(session.session_dir, out_filename)
        with open(out_path, "wb") as f:
            f.write(packed_bytes)
            
        # Update current filepath in session so user can immediately Hex Pad it if they want
        session.current_filepath = out_path
        
        log_action("COMPRESSION SUCCESS", user_id, username, f"Saved '{out_filename}' ({len(packed_bytes):,} bytes)")
        
        caption = (
            f"🎉 *Bundle Successfully Saved & Repacked!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 *File:* `{out_filename}`\n"
            f"⚡ *Compression:* `{packer.upper()}`\n"
            f"📊 *Final Size:* `{len(packed_bytes):,} bytes`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 *Modded via {AUTHOR} ({TELEGRAM_CHANNEL})*"
        )
        with open(out_path, "rb") as f:
            bot.send_document(
                call.message.chat.id,
                f,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
        bot.delete_message(call.message.chat.id, status_msg.message_id)
        
    except Exception as e:
        log_action("ERROR COMPRESSION", user_id, username, f"Packing failed: {e}")
        bot.edit_message_text(
            f"❌ *Failed to pack bundle:* {e}",
            chat_id=call.message.chat.id,
            message_id=status_msg.message_id,
            parse_mode="Markdown"
        )


# ===========================================================================
# 🔢 HEX PADDING (0x00 INJECTOR)
# ===========================================================================

def handle_action_hex_padding_prompt(call, session: UserSession):
    user_id = call.from_user.id
    username = call.from_user.username or ""
    
    if not os.path.exists(session.current_filepath):
        bot.send_message(call.message.chat.id, "❌ Error: Working file not found on server!")
        return

    current_size = os.path.getsize(session.current_filepath)
    session.state = "WAITING_HEX_PADDING"
    
    log_action("HEX PADDING PROMPT", user_id, username, f"Prompting for target size. Current: {current_size} bytes")
    
    msg_text = (
        f"🔢 *Hex Padding (0x00 Null Byte Injector)*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📁 *Working File:* `{os.path.basename(session.current_filepath)}`\n"
        f"📊 *Current Size:* `{current_size:,} bytes`\n\n"
        f"👉 Please enter your *Target Byte Size* in exact numbers (e.g. `{current_size + 2048}`):\n"
        f"(Or send /cancel to abort)"
    )
    bot.send_message(call.message.chat.id, msg_text, parse_mode="Markdown")


# ===========================================================================
# 💬 TEXT MESSAGE / STEP HANDLER
# ===========================================================================

@bot.message_handler(func=lambda msg: True, content_types=['text'])
def handle_text_messages(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    text = message.text.strip()
    
    # Check for cancel command
    if text.lower() in ["/cancel", "cancel"]:
        session = session_manager.get_session(user_id)
        session.state = "IDLE"
        session.state_data.clear()
        bot.reply_to(message, "❌ Operation cancelled. Returned to main menu.", reply_markup=get_main_menu_keyboard())
        return

    session = session_manager.get_session(user_id)
    session.touch()
    
    # 1. Waiting for Export Dump Path ID
    if session.state == "WAITING_EXPORT_DUMP_PATH_ID":
        try:
            path_id = int(text)
        except ValueError:
            bot.reply_to(message, "⚠️ Invalid Path ID! Please enter a numeric Path ID (or /cancel):")
            return
            
        target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
        if not target_obj:
            bot.reply_to(message, f"❌ Path ID `{path_id}` not found in loaded bundle! Please re-check the Info Table.")
            return

        session.state_data["export_path_id"] = path_id
        session.state = "IDLE"
        bot.reply_to(
            message,
            f"✅ Path ID `{path_id}` selected.\nChoose your export format:",
            parse_mode="Markdown",
            reply_markup=get_dump_format_keyboard()
        )

    # 2. Waiting for Import Dump Path ID
    elif session.state == "WAITING_IMPORT_DUMP_PATH_ID":
        try:
            path_id = int(text)
        except ValueError:
            bot.reply_to(message, "⚠️ Invalid Path ID! Please enter numbers only (or /cancel):")
            return
            
        target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
        if not target_obj:
            bot.reply_to(message, f"❌ Path ID `{path_id}` not found in loaded bundle!")
            return

        session.state_data["import_path_id"] = path_id
        session.state = "WAITING_DUMP_FILE"
        bot.reply_to(
            message,
            f"📥 Path ID `{path_id}` chosen.\n\nNow please **upload / send** your modified `.json` or `.txt` dump file as a Document:",
            parse_mode="Markdown"
        )

    # 3. Waiting for Export Raw Path ID
    elif session.state == "WAITING_EXPORT_RAW_PATH_ID":
        try:
            path_id = int(text)
        except ValueError:
            bot.reply_to(message, "⚠️ Invalid Path ID! Please enter numeric Path ID:")
            return

        target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
        if not target_obj:
            bot.reply_to(message, f"❌ Path ID `{path_id}` not found!")
            return

        try:
            raw_bytes = target_obj.get_raw_data()
            raw_filename = f"raw_{path_id}.dat"
            raw_path = os.path.join(session.session_dir, raw_filename)
            with open(raw_path, "wb") as f:
                f.write(raw_bytes)

            log_action("EXPORT RAW", user_id, username, f"Exported {len(raw_bytes)} bytes for Path ID: {path_id}")
            with open(raw_path, "rb") as f:
                bot.send_document(
                    message.chat.id,
                    f,
                    caption=f"📦 *Raw Data (.dat) Exported*\n• *Path ID:* `{path_id}`\n• *Bytes:* `{len(raw_bytes):,}`",
                    parse_mode="Markdown",
                    reply_markup=get_main_menu_keyboard()
                )
            session.state = "IDLE"
        except Exception as e:
            bot.reply_to(message, f"❌ Failed to extract raw bytes: {e}")

    # 4. Waiting for Import Raw Path ID
    elif session.state == "WAITING_IMPORT_RAW_PATH_ID":
        try:
            path_id = int(text)
        except ValueError:
            bot.reply_to(message, "⚠️ Invalid Path ID! Please enter numeric Path ID:")
            return

        target_obj = next((o for o in session.env.objects if o.path_id == path_id), None)
        if not target_obj:
            bot.reply_to(message, f"❌ Path ID `{path_id}` not found!")
            return

        session.state_data["import_raw_path_id"] = path_id
        session.state = "WAITING_RAW_FILE"
        bot.reply_to(
            message,
            f"📥 Path ID `{path_id}` selected.\n\nNow please **upload / send** your `.dat` file as a Document:",
            parse_mode="Markdown"
        )

    # 5. Waiting for Hex Padding target size
    elif session.state == "WAITING_HEX_PADDING":
        try:
            target_size = int(text)
        except ValueError:
            bot.reply_to(message, "⚠️ Invalid number! Please enter numbers only (e.g. 1048576):")
            return

        current_size = os.path.getsize(session.current_filepath)
        
        if current_size == target_size:
            bot.reply_to(message, f"ℹ️ File is already exactly `{target_size:,} bytes`. No padding needed!", reply_markup=get_main_menu_keyboard())
            session.state = "IDLE"
            return
            
        if current_size > target_size:
            diff = current_size - target_size
            bot.reply_to(
                message,
                f"❌ *Error:* Current file (`{current_size:,} bytes`) is BIGGER than target (`{target_size:,} bytes`) by `{diff:,} bytes`.\n"
                f"Cannot shrink files with null padding!",
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
            session.state = "IDLE"
            return

        padding_needed = target_size - current_size
        log_action("HEX PADDING EXEC", user_id, username, f"Current: {current_size}, Target: {target_size}, Padding: +{padding_needed} bytes")
        
        try:
            base_name = os.path.basename(session.current_filepath)
            padded_filename = f"padded_{base_name}"
            padded_path = os.path.join(session.session_dir, padded_filename)
            shutil.copyfile(session.current_filepath, padded_path)
            
            with open(padded_path, "ab") as f:
                f.write(b'\x00' * padding_needed)
                
            verified_size = os.path.getsize(padded_path)
            session.current_filepath = padded_path
            
            caption = (
                f"✅ *Hex Padding Complete!*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📁 *File:* `{padded_filename}`\n"
                f"🎯 *Target Size:* `{target_size:,} bytes`\n"
                f"➕ *Added Null (0x00) Bytes:* `{padding_needed:,}`\n"
                f"🔍 *Verified Size:* `{verified_size:,} bytes`\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👑 *ArisuFxBot | {AUTHOR}*"
            )
            with open(padded_path, "rb") as f:
                bot.send_document(
                    message.chat.id,
                    f,
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=get_main_menu_keyboard()
                )
            session.state = "IDLE"
        except Exception as e:
            log_action("ERROR HEX PADDING", user_id, username, f"Padding failed: {e}")
            bot.reply_to(message, f"❌ Failed to pad file: {e}", reply_markup=get_main_menu_keyboard())
            session.state = "IDLE"

    else:
        # Default fallback
        if not session.env:
            bot.reply_to(message, "👋 Welcome! Please send/upload a Unity `.bundle` or `.bin` file to begin.")
        else:
            bot.reply_to(message, "💡 Please use the buttons below to interact with your loaded bundle:", reply_markup=get_main_menu_keyboard())


# ===========================================================================
# 🏁 MAIN ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("      🚀 ARISUFXBOT - UNITY ASSETBUNDLE TELEGRAM BOT")
    print(f"      👑 Developed & Created by: {AUTHOR}")
    print(f"      📢 Official Telegram Channel: {TELEGRAM_CHANNEL}")
    print(f"      ⏱️ Inactive Session Purge: Every {SESSION_TIMEOUT_SECONDS // 60} minutes")
    print("=" * 65)
    print("[*] Testing Telegram Bot API connection...")
    
    try:
        me = bot.get_me()
        print(f"[+] Connected to Telegram successfully as @{me.username} ({me.first_name})!")
        print(f"[+] Bot ID: {me.id}")
        print("[*] Listening for user messages, uploads, and button clicks...")
        print("=" * 65)
        bot.infinity_polling(timeout=20, long_polling_timeout=20)
    except KeyboardInterrupt:
        print("\n[!] Shutting down ArisuFxBot gracefully...")
    except Exception as e:
        print(f"\n[-] Critical Polling Error: {e}")
