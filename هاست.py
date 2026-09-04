import asyncio
import sqlite3
import aiohttp
import re
import requests
import random
import time
import json
import httpx
import os
import hashlib
import string
import uuid
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import jdatetime
from rubka.asynco import Robot, Message
from rubka.button import InlineBuilder, ChatKeypadBuilder
from rubka import filters
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import urllib.parse

DB_PATH = "chats.db"
ADMIN_CHAT_ID = "u0IqpIc0f73ba4571cafd30ce3b14628"
ADMIN_ID = [ADMIN_CHAT_ID]
CHANNEL_LINK = "@tafe_gif2"
CHANNEL_CREATOR = "@Amcyxba"
AI_API_URL = "https://api-free.ir/api/chat.php"

bot = Robot("CAGHAD0RELOJGLAWKNSDNFFJNJNITNDTOXIFWGMPFHTUZSZEWZLRYXFQUQQYKIJY",enable_offset=True,max_msg_age=90000)

# ==================== ساختارهای داده جدید ====================
admin_states = {}
broadcast_tasks = {}
group_rules = {}
bot_status = {}
active_groups = {}
user_warns: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
user_games: Dict[str, dict] = {}
user_cooldowns: Dict[str, Dict[str, float]] = defaultdict(dict)
daily_rewards: Dict[str, Dict[str, str]] = defaultdict(dict)
poll_votes: Dict[str, Dict[int, str]] = defaultdict(dict)
group_settings: Dict[str, dict] = defaultdict(dict)
message_history: Dict[str, List[int]] = defaultdict(list)
user_notes: Dict[str, Dict[int, List[dict]]] = defaultdict(lambda: defaultdict(list))
bot_giveaways: Dict[str, dict] = {}
user_badges: Dict[str, Dict[int, List[str]]] = defaultdict(lambda: defaultdict(list))
group_custom_commands: Dict[str, Dict[str, str]] = defaultdict(dict)
user_levels: Dict[str, Dict[int, dict]] = defaultdict(lambda: defaultdict(lambda: {"xp": 0, "level": 1}))
group_banlist: Dict[str, List[int]] = defaultdict(list)
group_filter_patterns: Dict[str, List[str]] = defaultdict(list)
user_reports: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
group_welcome_msgs: Dict[str, str] = {}
group_goodbye_msgs: Dict[str, str] = {}
group_captcha_settings: Dict[str, dict] = {}
user_captcha: Dict[str, Dict[int, dict]] = defaultdict(dict)
group_timers: Dict[str, Dict[str, int]] = defaultdict(dict)
quiz_questions: Dict[str, list] = {}
group_events: Dict[str, list] = defaultdict(list)
user_achievements: Dict[str, Dict[int, List[str]]] = defaultdict(lambda: defaultdict(list))
group_petitions: Dict[str, dict] = {}
bot_music_queue: Dict[str, list] = defaultdict(list)
user_favorites: Dict[str, Dict[int, List[int]]] = defaultdict(lambda: defaultdict(list))
group_custom_reactions: Dict[str, Dict[str, str]] = defaultdict(dict)
group_auto_responders: Dict[str, Dict[str, str]] = defaultdict(dict)
group_warnings_settings: Dict[str, dict] = defaultdict(lambda: {"max_warns": 3, "action": "mute", "duration": 3600})
group_invite_links: Dict[str, Dict[str, str]] = defaultdict(dict)
group_topics: Dict[str, dict] = {}
user_birthdays: Dict[str, Dict[int, str]] = defaultdict(dict)
group_reminders: Dict[str, List[dict]] = defaultdict(list)
group_blacklist_words: Dict[str, List[str]] = defaultdict(list)
group_whitelist_links: Dict[str, List[str]] = defaultdict(list)
group_log_channels: Dict[str, str] = {}
group_auto_roles: Dict[str, dict] = defaultdict(dict)
group_voice_chat: Dict[str, dict] = {}
group_bot_protection: Dict[str, bool] = defaultdict(bool)

# ==================== ساختارهای جدید برای قابلیت‌های اضافه شده ====================
# قفل‌های جدید
group_locks: Dict[str, Dict[str, bool]] = defaultdict(lambda: defaultdict(bool))
# ban locks
group_ban_locks: Dict[str, Dict[str, bool]] = defaultdict(lambda: defaultdict(bool))
# warn locks
group_warn_locks: Dict[str, Dict[str, bool]] = defaultdict(lambda: defaultdict(bool))
# ویژه و معاف
special_users: Dict[str, List[str]] = defaultdict(list)
exempt_users: Dict[str, List[str]] = defaultdict(list)
# اطلاعات کاربری
user_profiles: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(lambda: defaultdict(dict))
# تنظیمات خودکار
auto_delete_settings: Dict[str, bool] = defaultdict(bool)
auto_delete_time: Dict[str, int] = defaultdict(lambda: 10)
# تایمر دستورات
command_timers: Dict[str, Dict[str, int]] = defaultdict(dict)
# سخنگو
speaker_personal: Dict[str, bool] = defaultdict(bool)
speaker_polite: Dict[str, bool] = defaultdict(bool)
speaker_rude: Dict[str, bool] = defaultdict(bool)
speaker_default: Dict[str, bool] = defaultdict(lambda: True)
speaker_learning: Dict[str, bool] = defaultdict(lambda: True)
calculator_enabled: Dict[str, bool] = defaultdict(lambda: True)
# یادگیری پیشرفته
advanced_learning: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
# گزارشات
reports_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

# ==================== دیتابیس‌های جدید ====================
def init_db_advanced():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        
        # جداول قبلی
        c.execute("""CREATE TABLE IF NOT EXISTS user_levels (
            chat_id TEXT, user_id TEXT, xp INTEGER, level INTEGER, 
            last_xp_time INTEGER, PRIMARY KEY (chat_id, user_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_badges (
            user_id TEXT, chat_id TEXT, badge TEXT, earned_time INTEGER, 
            PRIMARY KEY (user_id, chat_id, badge))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS custom_commands (
            chat_id TEXT, command TEXT, response TEXT, created_by TEXT, 
            created_time INTEGER, PRIMARY KEY (chat_id, command))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_warns (
            chat_id TEXT, user_id TEXT, warn_count INTEGER, 
            last_warn_time INTEGER, PRIMARY KEY (chat_id, user_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_invites (
            chat_id TEXT, link TEXT, creator_id TEXT, created_time INTEGER, 
            uses INTEGER, PRIMARY KEY (chat_id, link))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_topics (
            chat_id TEXT, topic_id TEXT, topic_name TEXT, creator_id TEXT, 
            PRIMARY KEY (chat_id, topic_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_birthdays (
            chat_id TEXT, user_id TEXT, birthday TEXT, 
            PRIMARY KEY (chat_id, user_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_reminders (
            chat_id TEXT, reminder_id TEXT, user_id TEXT, 
            reminder_text TEXT, remind_time INTEGER, PRIMARY KEY (chat_id, reminder_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_blacklist (
            chat_id TEXT, word TEXT, added_by TEXT, added_time INTEGER, 
            PRIMARY KEY (chat_id, word))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_whitelist (
            chat_id TEXT, link_pattern TEXT, added_by TEXT, 
            PRIMARY KEY (chat_id, link_pattern))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_logs (
            chat_id TEXT, log_channel TEXT, settings TEXT, 
            PRIMARY KEY (chat_id, log_channel))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_auto_roles (
            chat_id TEXT, role_name TEXT, role_id TEXT, 
            min_level INTEGER, PRIMARY KEY (chat_id, role_name))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_notes (
            chat_id TEXT, user_id TEXT, note_id TEXT, note_text TEXT, 
            created_by TEXT, created_time INTEGER, PRIMARY KEY (chat_id, user_id, note_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_giveaways (
            chat_id TEXT, giveaway_id TEXT, prize TEXT, winner_count INTEGER, 
            end_time INTEGER, created_by TEXT, participants TEXT, 
            PRIMARY KEY (chat_id, giveaway_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_quiz (
            chat_id TEXT, quiz_id TEXT, question TEXT, options TEXT, 
            correct_answer INTEGER, created_by TEXT, PRIMARY KEY (chat_id, quiz_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_events (
            chat_id TEXT, event_id TEXT, event_name TEXT, event_time INTEGER, 
            event_description TEXT, created_by TEXT, participants TEXT, 
            PRIMARY KEY (chat_id, event_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_achievements (
            user_id TEXT, chat_id TEXT, achievement TEXT, earned_time INTEGER, 
            PRIMARY KEY (user_id, chat_id, achievement))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_filter_patterns (
            chat_id TEXT, pattern TEXT, added_by TEXT, severity INTEGER, 
            PRIMARY KEY (chat_id, pattern))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_auto_responders (
            chat_id TEXT, trigger TEXT, response TEXT, mode TEXT, 
            created_by TEXT, PRIMARY KEY (chat_id, trigger))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_cooldowns (
            chat_id TEXT, user_id TEXT, command TEXT, last_use INTEGER, 
            PRIMARY KEY (chat_id, user_id, command))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_warnings_settings (
            chat_id TEXT PRIMARY KEY, max_warns INTEGER, action TEXT, duration INTEGER)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_welcome (
            chat_id TEXT PRIMARY KEY, welcome_text TEXT, media_id TEXT, is_active INTEGER)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_goodbye (
            chat_id TEXT PRIMARY KEY, goodbye_text TEXT, media_id TEXT, is_active INTEGER)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_captcha (
            chat_id TEXT PRIMARY KEY, is_active INTEGER, difficulty TEXT, kick_time INTEGER)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_timers (
            chat_id TEXT, timer_name TEXT, timer_time INTEGER, repeat INTEGER, 
            action TEXT, created_by TEXT, PRIMARY KEY (chat_id, timer_name))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS bot_music_queue (
            chat_id TEXT, song_id TEXT, title TEXT, url TEXT, added_by TEXT, 
            added_time INTEGER, PRIMARY KEY (chat_id, song_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_favorites (
            user_id TEXT, chat_id TEXT, message_id INTEGER, saved_time INTEGER, 
            PRIMARY KEY (user_id, chat_id, message_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_custom_reactions (
            chat_id TEXT, trigger TEXT, reaction TEXT, mode TEXT, 
            created_by TEXT, PRIMARY KEY (chat_id, trigger))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_petitions (
            chat_id TEXT, petition_id TEXT, title TEXT, description TEXT, 
            target_votes INTEGER, current_votes INTEGER, created_by TEXT, 
            end_time INTEGER, PRIMARY KEY (chat_id, petition_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS petition_signatures (
            chat_id TEXT, petition_id TEXT, user_id TEXT, signed_time INTEGER, 
            PRIMARY KEY (chat_id, petition_id, user_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS daily_rewards (
            user_id TEXT, chat_id TEXT, last_claim_date TEXT, streak INTEGER, 
            PRIMARY KEY (user_id, chat_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_voice_chat (
            chat_id TEXT PRIMARY KEY, is_active INTEGER, title TEXT, 
            schedule_time INTEGER, created_by TEXT)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_bot_protection (
            chat_id TEXT PRIMARY KEY, is_active INTEGER, kick_new_bots INTEGER, 
            ban_known_bots INTEGER)""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_tags (
            chat_id TEXT, tag_name TEXT, user_ids TEXT, created_by TEXT, 
            created_time INTEGER, PRIMARY KEY (chat_id, tag_name))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_polls_advanced (
            chat_id TEXT, poll_id TEXT, question TEXT, options TEXT, 
            is_anonymous INTEGER, multiple_choices INTEGER, created_by TEXT, 
            end_time INTEGER, votes TEXT, PRIMARY KEY (chat_id, poll_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_links (
            chat_id TEXT, link_type TEXT, link_url TEXT, title TEXT, 
            added_by TEXT, added_time INTEGER, PRIMARY KEY (chat_id, link_url))""")
        
        # جداول جدید برای قابلیت‌های اضافه شده
        c.execute("""CREATE TABLE IF NOT EXISTS group_locks (
            chat_id TEXT, lock_type TEXT, is_active INTEGER, 
            PRIMARY KEY (chat_id, lock_type))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_ban_locks (
            chat_id TEXT, lock_type TEXT, is_active INTEGER, 
            PRIMARY KEY (chat_id, lock_type))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_warn_locks (
            chat_id TEXT, lock_type TEXT, is_active INTEGER, 
            PRIMARY KEY (chat_id, lock_type))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS special_users (
            chat_id TEXT, user_id TEXT, added_by TEXT, added_time INTEGER, 
            PRIMARY KEY (chat_id, user_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS exempt_users (
            chat_id TEXT, user_id TEXT, added_by TEXT, added_time INTEGER, 
            PRIMARY KEY (chat_id, user_id))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT, chat_id TEXT, field_name TEXT, field_value TEXT, 
            set_by TEXT, set_time INTEGER, PRIMARY KEY (user_id, chat_id, field_name))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS group_settings (
            chat_id TEXT, setting_name TEXT, setting_value TEXT, 
            PRIMARY KEY (chat_id, setting_name))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS advanced_learning (
            chat_id TEXT, keyword TEXT, response TEXT, 
            created_by TEXT, created_time INTEGER, PRIMARY KEY (chat_id, keyword, response))""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS command_timers (
            chat_id TEXT, command_name TEXT, cooldown INTEGER, 
            PRIMARY KEY (chat_id, command_name))""")
        
        conn.commit()

# فراخوانی تابع دیتابیس جدید
init_db_advanced()

# ==================== توابع جدید دیتابیس ====================
async def db_execute(query, params=(), fetch_one=False, fetch_all=False):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# ==================== توابع مدیریت سطح و تجربه ====================
async def add_user_xp(chat_id, user_id, xp_amount=5):
    """اضافه کردن تجربه به کاربر"""
    current = await db_execute(
        "SELECT xp, level FROM user_levels WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    
    current_time = int(time.time())
    
    if current:
        xp, level = current
        new_xp = xp + xp_amount
        new_level = level
        
        # محاسبه سطح جدید
        xp_needed = level * 100
        while new_xp >= xp_needed:
            new_xp -= xp_needed
            new_level += 1
            xp_needed = new_level * 100
            
            # اهدای نشان ویژه برای سطح‌های خاص
            if new_level % 5 == 0:
                await award_user_badge(user_id, chat_id, f"level_{new_level}")
        
        await db_execute(
            "INSERT OR REPLACE INTO user_levels (chat_id, user_id, xp, level, last_xp_time) VALUES (?, ?, ?, ?, ?)",
            (chat_id, user_id, new_xp, new_level, current_time)
        )
        
        if new_level > level:
            return {"level_up": True, "new_level": new_level}
    else:
        await db_execute(
            "INSERT INTO user_levels (chat_id, user_id, xp, level, last_xp_time) VALUES (?, ?, ?, ?, ?)",
            (chat_id, user_id, xp_amount, 1, current_time)
        )
    
    return {"level_up": False}

async def get_user_level_info(chat_id, user_id):
    """دریافت اطلاعات سطح کاربر"""
    row = await db_execute(
        "SELECT xp, level FROM user_levels WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    if row:
        xp, level = row
        xp_needed = level * 100
        xp_current = xp
        xp_remaining = xp_needed - xp_current
        progress = (xp_current / xp_needed) * 100
        return {
            "level": level,
            "xp": xp_current,
            "xp_needed": xp_needed,
            "xp_remaining": xp_remaining,
            "progress": round(progress, 1)
        }
    return {"level": 0, "xp": 0, "xp_needed": 100, "xp_remaining": 100, "progress": 0}

async def get_group_leaderboard(chat_id, limit=10):
    """دریافت برترین‌های گروه"""
    rows = await db_execute(
        "SELECT user_id, level, xp FROM user_levels WHERE chat_id=? ORDER BY level DESC, xp DESC LIMIT ?",
        (chat_id, limit), fetch_all=True
    )
    return rows or []

# ==================== توابع مدیریت نشان‌ها ====================
async def award_user_badge(user_id, chat_id, badge):
    """اهدای نشان به کاربر"""
    current_time = int(time.time())
    try:
        await db_execute(
            "INSERT OR IGNORE INTO user_badges (user_id, chat_id, badge, earned_time) VALUES (?, ?, ?, ?)",
            (user_id, chat_id, badge, current_time)
        )
        return True
    except:
        return False

async def get_user_badges(user_id, chat_id=None):
    """دریافت نشان‌های کاربر"""
    if chat_id:
        rows = await db_execute(
            "SELECT badge, earned_time FROM user_badges WHERE user_id=? AND chat_id=? ORDER BY earned_time DESC",
            (user_id, chat_id), fetch_all=True
        )
    else:
        rows = await db_execute(
            "SELECT badge, chat_id, earned_time FROM user_badges WHERE user_id=? ORDER BY earned_time DESC",
            (user_id,), fetch_all=True
        )
    return rows or []

# ==================== توابع مدیریت دستورات سفارشی ====================
async def add_custom_command(chat_id, command, response, creator_id):
    """افزودن دستور سفارشی"""
    current_time = int(time.time())
    await db_execute(
        "INSERT OR REPLACE INTO custom_commands (chat_id, command, response, created_by, created_time) VALUES (?, ?, ?, ?, ?)",
        (chat_id, command.lower(), response, creator_id, current_time)
    )
    group_custom_commands[chat_id][command.lower()] = response

async def remove_custom_command(chat_id, command):
    """حذف دستور سفارشی"""
    await db_execute(
        "DELETE FROM custom_commands WHERE chat_id=? AND command=?",
        (chat_id, command.lower())
    )
    if command.lower() in group_custom_commands[chat_id]:
        del group_custom_commands[chat_id][command.lower()]

async def get_custom_command(chat_id, command):
    """دریافت پاسخ دستور سفارشی"""
    if command.lower() in group_custom_commands[chat_id]:
        return group_custom_commands[chat_id][command.lower()]
    
    row = await db_execute(
        "SELECT response FROM custom_commands WHERE chat_id=? AND command=?",
        (chat_id, command.lower()), fetch_one=True
    )
    if row:
        group_custom_commands[chat_id][command.lower()] = row[0]
        return row[0]
    return None

async def list_custom_commands(chat_id):
    """لیست دستورات سفارشی"""
    rows = await db_execute(
        "SELECT command, response, created_by FROM custom_commands WHERE chat_id=?",
        (chat_id,), fetch_all=True
    )
    return rows or []

# ==================== توابع مدیریت اخطارها ====================
async def add_user_warn(chat_id, user_id, admin_id=None, reason=""):
    """افزودن اخطار به کاربر"""
    current_time = int(time.time())
    row = await db_execute(
        "SELECT warn_count FROM group_warns WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    
    if row:
        new_count = row[0] + 1
        await db_execute(
            "UPDATE group_warns SET warn_count=?, last_warn_time=? WHERE chat_id=? AND user_id=?",
            (new_count, current_time, chat_id, user_id)
        )
    else:
        new_count = 1
        await db_execute(
            "INSERT INTO group_warns (chat_id, user_id, warn_count, last_warn_time) VALUES (?, ?, ?, ?)",
            (chat_id, user_id, new_count, current_time)
        )
    
    user_warns[chat_id][user_id] = new_count
    return new_count

async def remove_user_warn(chat_id, user_id, count=1):
    """کاهش اخطار کاربر"""
    row = await db_execute(
        "SELECT warn_count FROM group_warns WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    
    if row:
        new_count = max(0, row[0] - count)
        if new_count == 0:
            await db_execute(
                "DELETE FROM group_warns WHERE chat_id=? AND user_id=?",
                (chat_id, user_id)
            )
            if user_id in user_warns[chat_id]:
                del user_warns[chat_id][user_id]
        else:
            await db_execute(
                "UPDATE group_warns SET warn_count=? WHERE chat_id=? AND user_id=?",
                (new_count, chat_id, user_id)
            )
            user_warns[chat_id][user_id] = new_count
        return new_count
    return 0

async def get_user_warn_count(chat_id, user_id):
    """تعداد اخطارهای کاربر"""
    if user_id in user_warns[chat_id]:
        return user_warns[chat_id][user_id]
    
    row = await db_execute(
        "SELECT warn_count FROM group_warns WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    if row:
        user_warns[chat_id][user_id] = row[0]
        return row[0]
    return 0

async def get_warn_settings(chat_id):
    """دریافت تنظیمات اخطار"""
    row = await db_execute(
        "SELECT max_warns, action, duration FROM group_warnings_settings WHERE chat_id=?",
        (chat_id,), fetch_one=True
    )
    if row:
        return {"max_warns": row[0], "action": row[1], "duration": row[2]}
    return {"max_warns": 3, "action": "mute", "duration": 3600}

async def set_warn_settings(chat_id, max_warns, action, duration):
    """تنظیمات اخطار"""
    await db_execute(
        "INSERT OR REPLACE INTO group_warnings_settings (chat_id, max_warns, action, duration) VALUES (?, ?, ?, ?)",
        (chat_id, max_warns, action, duration)
    )
    group_warnings_settings[chat_id] = {"max_warns": max_warns, "action": action, "duration": duration}

# ==================== توابع جدید برای قابلیت‌های اضافه شده ====================

# ==================== توابع مدیریت قفل‌ها ====================
async def set_lock(chat_id, lock_type, is_active):
    """تنظیم قفل"""
    await db_execute(
        "INSERT OR REPLACE INTO group_locks (chat_id, lock_type, is_active) VALUES (?, ?, ?)",
        (chat_id, lock_type, 1 if is_active else 0)
    )
    group_locks[chat_id][lock_type] = is_active

async def get_lock(chat_id, lock_type):
    """دریافت وضعیت قفل"""
    if lock_type in group_locks[chat_id]:
        return group_locks[chat_id][lock_type]
    
    row = await db_execute(
        "SELECT is_active FROM group_locks WHERE chat_id=? AND lock_type=?",
        (chat_id, lock_type), fetch_one=True
    )
    if row:
        group_locks[chat_id][lock_type] = bool(row[0])
        return bool(row[0])
    return False

async def set_ban_lock(chat_id, lock_type, is_active):
    """تنظیم قفل بن"""
    await db_execute(
        "INSERT OR REPLACE INTO group_ban_locks (chat_id, lock_type, is_active) VALUES (?, ?, ?)",
        (chat_id, lock_type, 1 if is_active else 0)
    )
    group_ban_locks[chat_id][lock_type] = is_active

async def get_ban_lock(chat_id, lock_type):
    """دریافت وضعیت قفل بن"""
    if lock_type in group_ban_locks[chat_id]:
        return group_ban_locks[chat_id][lock_type]
    
    row = await db_execute(
        "SELECT is_active FROM group_ban_locks WHERE chat_id=? AND lock_type=?",
        (chat_id, lock_type), fetch_one=True
    )
    if row:
        group_ban_locks[chat_id][lock_type] = bool(row[0])
        return bool(row[0])
    return False

async def set_warn_lock(chat_id, lock_type, is_active):
    """تنظیم قفل اخطار"""
    await db_execute(
        "INSERT OR REPLACE INTO group_warn_locks (chat_id, lock_type, is_active) VALUES (?, ?, ?)",
        (chat_id, lock_type, 1 if is_active else 0)
    )
    group_warn_locks[chat_id][lock_type] = is_active

async def get_warn_lock(chat_id, lock_type):
    """دریافت وضعیت قفل اخطار"""
    if lock_type in group_warn_locks[chat_id]:
        return group_warn_locks[chat_id][lock_type]
    
    row = await db_execute(
        "SELECT is_active FROM group_warn_locks WHERE chat_id=? AND lock_type=?",
        (chat_id, lock_type), fetch_one=True
    )
    if row:
        group_warn_locks[chat_id][lock_type] = bool(row[0])
        return bool(row[0])
    return False

async def get_all_locks(chat_id):
    """دریافت لیست تمام قفل‌ها"""
    rows = await db_execute(
        "SELECT lock_type, is_active FROM group_locks WHERE chat_id=?",
        (chat_id,), fetch_all=True
    )
    locks = {}
    for lock_type, is_active in rows or []:
        locks[lock_type] = bool(is_active)
    return locks

async def get_all_ban_locks(chat_id):
    """دریافت لیست تمام قفل‌های بن"""
    rows = await db_execute(
        "SELECT lock_type, is_active FROM group_ban_locks WHERE chat_id=?",
        (chat_id,), fetch_all=True
    )
    locks = {}
    for lock_type, is_active in rows or []:
        locks[lock_type] = bool(is_active)
    return locks

async def get_all_warn_locks(chat_id):
    """دریافت لیست تمام قفل‌های اخطار"""
    rows = await db_execute(
        "SELECT lock_type, is_active FROM group_warn_locks WHERE chat_id=?",
        (chat_id,), fetch_all=True
    )
    locks = {}
    for lock_type, is_active in rows or []:
        locks[lock_type] = bool(is_active)
    return locks

# ==================== توابع مدیریت ویژه و معاف ====================
async def add_special_user(chat_id, user_id, admin_id):
    """افزودن کاربر ویژه"""
    current_time = int(time.time())
    await db_execute(
        "INSERT OR IGNORE INTO special_users (chat_id, user_id, added_by, added_time) VALUES (?, ?, ?, ?)",
        (chat_id, user_id, admin_id, current_time)
    )
    if user_id not in special_users[chat_id]:
        special_users[chat_id].append(user_id)

async def remove_special_user(chat_id, user_id):
    """حذف کاربر ویژه"""
    await db_execute(
        "DELETE FROM special_users WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    if user_id in special_users[chat_id]:
        special_users[chat_id].remove(user_id)

async def is_special_user(chat_id, user_id):
    """بررسی ویژه بودن کاربر"""
    if user_id in special_users[chat_id]:
        return True
    
    row = await db_execute(
        "SELECT 1 FROM special_users WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    if row:
        special_users[chat_id].append(user_id)
        return True
    return False

async def add_exempt_user(chat_id, user_id, admin_id):
    """افزودن کاربر معاف"""
    current_time = int(time.time())
    await db_execute(
        "INSERT OR IGNORE INTO exempt_users (chat_id, user_id, added_by, added_time) VALUES (?, ?, ?, ?)",
        (chat_id, user_id, admin_id, current_time)
    )
    if user_id not in exempt_users[chat_id]:
        exempt_users[chat_id].append(user_id)

async def remove_exempt_user(chat_id, user_id):
    """حذف کاربر معاف"""
    await db_execute(
        "DELETE FROM exempt_users WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    if user_id in exempt_users[chat_id]:
        exempt_users[chat_id].remove(user_id)

async def is_exempt_user(chat_id, user_id):
    """بررسی معاف بودن کاربر"""
    if user_id in exempt_users[chat_id]:
        return True
    
    row = await db_execute(
        "SELECT 1 FROM exempt_users WHERE chat_id=? AND user_id=?",
        (chat_id, user_id), fetch_one=True
    )
    if row:
        exempt_users[chat_id].append(user_id)
        return True
    return False

# ==================== توابع مدیریت پروفایل کاربری ====================
async def set_user_profile(chat_id, user_id, field, value, set_by):
    """تنظیم فیلد پروفایل کاربر"""
    current_time = int(time.time())
    await db_execute(
        "INSERT OR REPLACE INTO user_profiles (user_id, chat_id, field_name, field_value, set_by, set_time) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, chat_id, field, value, set_by, current_time)
    )
    user_profiles[chat_id][user_id][field] = value

async def get_user_profile(chat_id, user_id, field):
    """دریافت فیلد پروفایل کاربر"""
    if field in user_profiles[chat_id][user_id]:
        return user_profiles[chat_id][user_id][field]
    
    row = await db_execute(
        "SELECT field_value FROM user_profiles WHERE user_id=? AND chat_id=? AND field_name=?",
        (user_id, chat_id, field), fetch_one=True
    )
    if row:
        user_profiles[chat_id][user_id][field] = row[0]
        return row[0]
    return None

async def get_user_full_profile(chat_id, user_id):
    """دریافت کامل پروفایل کاربر"""
    rows = await db_execute(
        "SELECT field_name, field_value FROM user_profiles WHERE user_id=? AND chat_id=?",
        (user_id, chat_id), fetch_all=True
    )
    profile = {}
    for field_name, field_value in rows or []:
        profile[field_name] = field_value
        user_profiles[chat_id][user_id][field_name] = field_value
    return profile

# ==================== توابع مدیریت تنظیمات گروه ====================
async def set_group_setting(chat_id, setting, value):
    """تنظیم یک تنظیم برای گروه"""
    await db_execute(
        "INSERT OR REPLACE INTO group_settings (chat_id, setting_name, setting_value) VALUES (?, ?, ?)",
        (chat_id, setting, str(value))
    )
    
    if setting == "auto_delete":
        auto_delete_settings[chat_id] = value == "True"
    elif setting == "auto_delete_time":
        auto_delete_time[chat_id] = int(value)
    elif setting == "speaker_personal":
        speaker_personal[chat_id] = value == "True"
    elif setting == "speaker_polite":
        speaker_polite[chat_id] = value == "True"
    elif setting == "speaker_rude":
        speaker_rude[chat_id] = value == "True"
    elif setting == "speaker_default":
        speaker_default[chat_id] = value == "True"
    elif setting == "speaker_learning":
        speaker_learning[chat_id] = value == "True"
    elif setting == "calculator_enabled":
        calculator_enabled[chat_id] = value == "True"

async def get_group_setting(chat_id, setting, default=None):
    """دریافت یک تنظیم از گروه"""
    if setting == "auto_delete" and chat_id in auto_delete_settings:
        return auto_delete_settings[chat_id]
    elif setting == "auto_delete_time" and chat_id in auto_delete_time:
        return auto_delete_time[chat_id]
    elif setting == "speaker_personal" and chat_id in speaker_personal:
        return speaker_personal[chat_id]
    elif setting == "speaker_polite" and chat_id in speaker_polite:
        return speaker_polite[chat_id]
    elif setting == "speaker_rude" and chat_id in speaker_rude:
        return speaker_rude[chat_id]
    elif setting == "speaker_default" and chat_id in speaker_default:
        return speaker_default[chat_id]
    elif setting == "speaker_learning" and chat_id in speaker_learning:
        return speaker_learning[chat_id]
    elif setting == "calculator_enabled" and chat_id in calculator_enabled:
        return calculator_enabled[chat_id]
    
    row = await db_execute(
        "SELECT setting_value FROM group_settings WHERE chat_id=? AND setting_name=?",
        (chat_id, setting), fetch_one=True
    )
    if row:
        value = row[0]
        if value == "True":
            value = True
        elif value == "False":
            value = False
        elif value.isdigit():
            value = int(value)
        
        if setting == "auto_delete":
            auto_delete_settings[chat_id] = value
        elif setting == "auto_delete_time":
            auto_delete_time[chat_id] = value
        elif setting == "speaker_personal":
            speaker_personal[chat_id] = value
        elif setting == "speaker_polite":
            speaker_polite[chat_id] = value
        elif setting == "speaker_rude":
            speaker_rude[chat_id] = value
        elif setting == "speaker_default":
            speaker_default[chat_id] = value
        elif setting == "speaker_learning":
            speaker_learning[chat_id] = value
        elif setting == "calculator_enabled":
            calculator_enabled[chat_id] = value
        
        return value
    return default

# ==================== توابع مدیریت یادگیری پیشرفته ====================
async def add_advanced_learning(chat_id, keyword, response, created_by):
    """افزودن یادگیری پیشرفته"""
    current_time = int(time.time())
    await db_execute(
        "INSERT INTO advanced_learning (chat_id, keyword, response, created_by, created_time) VALUES (?, ?, ?, ?, ?)",
        (chat_id, keyword, response, created_by, current_time)
    )
    if keyword not in advanced_learning[chat_id]:
        advanced_learning[chat_id][keyword] = []
    advanced_learning[chat_id][keyword].append(response)

async def remove_advanced_learning(chat_id, keyword, response=None):
    """حذف یادگیری پیشرفته"""
    if response:
        await db_execute(
            "DELETE FROM advanced_learning WHERE chat_id=? AND keyword=? AND response=?",
            (chat_id, keyword, response)
        )
        if keyword in advanced_learning[chat_id] and response in advanced_learning[chat_id][keyword]:
            advanced_learning[chat_id][keyword].remove(response)
    else:
        await db_execute(
            "DELETE FROM advanced_learning WHERE chat_id=? AND keyword=?",
            (chat_id, keyword)
        )
        if keyword in advanced_learning[chat_id]:
            del advanced_learning[chat_id][keyword]

async def get_advanced_learning(chat_id, keyword):
    """دریافت یادگیری پیشرفته"""
    if keyword in advanced_learning[chat_id]:
        return advanced_learning[chat_id][keyword]
    
    rows = await db_execute(
        "SELECT response FROM advanced_learning WHERE chat_id=? AND keyword=?",
        (chat_id, keyword), fetch_all=True
    )
    if rows:
        advanced_learning[chat_id][keyword] = [row[0] for row in rows]
        return [row[0] for row in rows]
    return []

async def get_all_advanced_learning(chat_id):
    """دریافت تمام یادگیری‌های پیشرفته"""
    rows = await db_execute(
        "SELECT keyword, response FROM advanced_learning WHERE chat_id=?",
        (chat_id,), fetch_all=True
    )
    data = defaultdict(list)
    for keyword, response in rows or []:
        data[keyword].append(response)
        if keyword not in advanced_learning[chat_id]:
            advanced_learning[chat_id][keyword] = []
        if response not in advanced_learning[chat_id][keyword]:
            advanced_learning[chat_id][keyword].append(response)
    return data

# ==================== توابع مدیریت تایمر دستورات ====================
async def set_command_timer(chat_id, command, cooldown):
    """تنظیم تایمر برای دستور"""
    await db_execute(
        "INSERT OR REPLACE INTO command_timers (chat_id, command_name, cooldown) VALUES (?, ?, ?)",
        (chat_id, command, cooldown)
    )
    command_timers[chat_id][command] = cooldown

async def get_command_timer(chat_id, command):
    """دریافت تایمر دستور"""
    if command in command_timers[chat_id]:
        return command_timers[chat_id][command]
    
    row = await db_execute(
        "SELECT cooldown FROM command_timers WHERE chat_id=? AND command_name=?",
        (chat_id, command), fetch_one=True
    )
    if row:
        command_timers[chat_id][command] = row[0]
        return row[0]
    return 0

# ==================== توابع مدیریت حذف خودکار ====================
async def auto_delete_message(chat_id, message_id, delay=None):
    """حذف خودکار پیام"""
    if delay is None:
        delay = auto_delete_time.get(chat_id, 10)
    
    if auto_delete_settings.get(chat_id, False):
        await asyncio.sleep(delay)
        try:
            await bot.delete_message(chat_id, message_id)
        except:
            pass

# ==================== توابع جدید سرگرمی و کاربردی ====================
async def calculate_expression(expression):
    """ماشین حساب"""
    try:
        # پاکسازی عبارت
        expression = expression.replace(' ', '')
        expression = expression.replace('^', '**')
        expression = expression.replace('×', '*')
        expression = expression.replace('÷', '/')
        expression = expression.replace('−', '-')
        expression = expression.replace('+', '+')
        
        # بررسی امنیتی
        if re.search(r'[a-zA-Z]', expression):
            return None
        
        result = eval(expression)
        return f"🧮 **نتیجه:**\n{expression} = {result:,}"
    except:
        return None

async def get_weather(city):
    """هواشناسی"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.codebazan.ir/weather/?city={city}")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    return f"""🌤 **هواشناسی {city}**
━━━━━━━━━━━━━━━
🌡 دما: {data['temp']}°C
💧 رطوبت: {data['humidity']}%
💨 باد: {data['wind']} km/h
☁️ وضعیت: {data['weather']}
📅 تاریخ: {data['date']}
🕒 زمان: {data['time']}"""
    except:
        pass
    return "❌ خطا در دریافت اطلاعات هواشناسی"

async def text_to_speech(text, gender="male"):
    """تبدیل متن به ویس"""
    try:
        gender_code = "m" if gender == "مرد" else "f"
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.codebazan.ir/tts/?text={text}&gender={gender_code}")
            if response.status_code == 200:
                # در اینجا لینک فایل صوتی برگردانده می‌شود
                return f"🎤 **ویس {gender}:**\n{response.text}"
    except:
        pass
    return "❌ خطا در تبدیل متن به ویس"

async def enhance_image():
    """افزایش کیفیت تصویر"""
    # این تابع باید با API افزایش کیفیت تصویر کار کند
    return "🖼 قابلیت افزایش کیفیت تصویر در حال توسعه است"

async def get_gold_price():
    """قیمت طلا"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.codebazan.ir/arz/?type=gold")
            if response.status_code == 200:
                data = response.json()
                text = "💰 **قیمت طلا و سکه** 💰\n━━━━━━━━━━━━━━━\n"
                for item in data.get("Result", []):
                    text += f"🔹 {item['name']}: {item['price']} تومان\n"
                return text
    except:
        pass
    return "❌ خطا در دریافت قیمت طلا"

async def get_stock():
    """بورس"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.codebazan.ir/bourse/")
            if response.status_code == 200:
                data = response.json()
                text = "📈 **اطلاعات بورس** 📈\n━━━━━━━━━━━━━━━\n"
                text += f"🔹 شاخص کل: {data.get('index', 'نامشخص')}\n"
                text += f"🔹 تغییر: {data.get('change', 'نامشخص')}\n"
                text += f"🔹 ارزش بازار: {data.get('value', 'نامشخص')}"
                return text
    except:
        pass
    return "❌ خطا در دریافت اطلاعات بورس"

async def get_prayer_times(city):
    """اوقات شرعی"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.codebazan.ir/owghat/?city={city}")
            if response.status_code == 200:
                data = response.json()
                return f"""🕌 **اوقات شرعی {city}**
━━━━━━━━━━━━━━━
🌅 اذان صبح: {data.get('azan_sobh', 'نامشخص')}
☀️ طلوع آفتاب: {data.get('tolo', 'نامشخص')}
🕐 اذان ظهر: {data.get('azan_zohr', 'نامشخص')}
🌇 غروب آفتاب: {data.get('ghorub', 'نامشخص')}
🌃 اذان مغرب: {data.get('azan_maghreb', 'نامشخص')}
🌙 نیمه شب شرعی: {data.get('night', 'نامشخص')}"""
    except:
        pass
    return "❌ خطا در دریافت اوقات شرعی"

# ==================== مجموعه‌های جدید سرگرمی ====================
# جملات فلسفی
philosophical_quotes = [
    "زندگی ساده است، اما ما اصرار داریم که آن را پیچیده کنیم.",
    "تنها راه برای انجام کار بزرگ این است که عاشق کاری باشید که انجام می‌دهید.",
    "شادترین مردم کسانی نیستند که بهترین چیزها را دارند، بلکه کسانی هستند که از آنچه دارند بهترین استفاده را می‌کنند.",
    "موفقیت از شکست به شکست است بدون اینکه شور و اشتیاق خود را از دست بدهید.",
    "آینده ای که می‌بینید، آینده ای است که به آن باور دارید.",
    "ذهن خود را تغییر دهید و دنیای خود را تغییر خواهید داد.",
    "تنها محدودیت برای موفقیت فردا، تردیدهای امروز شماست.",
    "زندگی مثل دوچرخه سواری است، برای حفظ تعادل باید به حرکت ادامه دهید.",
    "مهم این نیست که چه اتفاقی برایتان می‌افتد، بلکه مهم این است که چگونه واکنش نشان می‌دهید.",
    "خوشبختی یک سفر است نه یک مقصد."
]

# تست‌های شخصیت
personality_tests = {
    "رنگ مورد علاقه": {
        "قرمز": ["پر انرژی", "رقابتی", "پرشور", "🔴"],
        "آبی": ["آرام", "منطقی", "مطمئن", "🔵"],
        "سبز": ["مهربان", "طبیعت‌گرا", "تعادل‌جو", "🟢"],
        "زرد": ["خلاق", "خوش‌بین", "اجتماعی", "🟡"],
        "سیاه": ["قدرتمند", "مرموز", "مستقل", "⚫"],
        "سفید": ["پاک", "کمال‌گرا", "منظم", "⚪"],
        "بنفش": ["هنرمند", "رویایی", "منحصربفرد", "🟣"],
        "صورتی": ["مهربان", "عاشقانه", "لطیف", "🌸"]
    },
    "فصل مورد علاقه": {
        "بهار": ["شاداب", "امیدوار", "نوگرا", "🌱"],
        "تابستان": ["پر انرژی", "ماجراجو", "گرم", "☀️"],
        "پاییز": ["تأملی", "هنری", "بالغ", "🍂"],
        "زمستان": ["آرام", "تحلیلگر", "صبور", "❄️"]
    }
}

# فال حافظ
hafez_fal = [
    "ای دوست دل به مهر تو چون شیشه کردم صاف / از هر چه رنگ تعلقی است آزادش کردم",
    "بیا که قصر امل سخت سست بنیاد است / بیار باده که بنیاد عمر بر باد است",
    "دوش دیدم که ملایک در میخانه زدند / گل آدم بسرشتند و به پیمانه زدند",
    "صوفی شهر بین که چون لقمه شبهه می‌خورد / پاردمش دراز باد آن حیوان خوش علف",
    "اگر آن ترک شیرازی به دست آرد دل ما را / به خال هندویش بخشم سمرقند و بخارا را",
    "روزگاریست که دل در پی دیدار تو بود / نه وصف تو نگنجد در گفتار تو بود",
    "ساقیا جام می ام ده که نگارنده غیب / نیستش غیر ره دلبر به دل رهبریی",
    "در دیر مغان آمد یارم قدحی در دست / مست از می و میخواران از نرگس مستش مست"
]

# معماها و جواب‌ها
riddles = [
    {"question": "چیزی که هر چه بیشتر از آن برداری، بزرگتر می‌شود؟", "answer": "گودال"},
    {"question": "چه چیزی پر از سوراخ است ولی می‌تواند آب را نگه دارد؟", "answer": "اسفنج"},
    {"question": "چه چیز همیشه می‌آید ولی هیچ وقت نمی‌رسد؟", "answer": "فردا"},
    {"question": "کدام کلمه همیشه غلط نوشته می‌شود؟", "answer": "غلط"},
    {"question": "چه سوالی هرگز نمی‌توانی با بله جواب بدهی؟", "answer": "خوابی؟"},
    {"question": "چیزی که با هر بار استفاده کوچکتر می‌شود؟", "answer": "صابون"},
    {"question": "کدام ماه ۲۸ روز دارد؟", "answer": "همه ماه‌ها"},
    {"question": "چیزی که چشم دارد ولی نمی‌بیند؟", "answer": "سیب زمینی"},
]

# احکام شرعی
islamic_rules = [
    "🕌 **احکام نماز**: نماز واجب روزانه ۵ وعده است: صبح (۲ رکعت)، ظهر (۴ رکعت)، عصر (۴ رکعت)، مغرب (۳ رکعت)، عشا (۴ رکعت)",
    "📿 **اذان**: قبل از هر نماز مستحب است اذان و اقامه گفته شود.",
    "🤲 **قبله**: همه مسلمانان باید رو به قبله (کعبه) نماز بخوانند.",
    "💧 **وضو**: برای نماز باید وضو داشت. با خواب، باد معده، مدفوع و ادرار وضو باطل می‌شود.",
    "🧼 **غسل**: در موارد جنابت، حیض، نفاس و مس میت باید غسل کرد.",
    "☪️ **روزه**: در ماه رمضان روزه واجب است. امساک از اذان صبح تا مغرب.",
    "💰 **خمس**: یک پنجم درآمد اضافه بر مخارج سال باید به سادات داده شود.",
    "🤝 **زکات**: زکات بر ۹ چیز واجب است: گندم، جو، خرما، کشمش، طلا، نقره، شتر، گاو، گوسفند",
    "🕋 **حج**: برای کسانی که توانایی مالی و جسمی دارند یک بار در عمر واجب است.",
    "📖 **قرآن**: خواندن قرآن مستحب است و ثواب بسیار دارد."
]

# دعاها
prayers = [
    "🤲 **دعای فرج**: اللهم کن لولیک الحجة بن الحسن صلواتک علیه و علی آبائه فی هذه الساعة و فی کل ساعة ولیاً و حافظاً و قائداً و ناصراً و دلیلاً و عیناً حتی تسکنه ارضک طوعاً و تمتعه فیها طویلاً",
    "🤲 **دعای کمیل**: اللهم انی اسئلک برحمتک التی وسعت کل شیء...",
    "🤲 **دعای توسل**: اللهم انی اسئلک و اتوجه الیک بنبیک نبی الرحمة...",
    "🤲 **دعای عهد**: اللهم رب النور العظیم و رب الکرسی الرفیع...",
    "🤲 **دعای ندبه**: الحمد لله رب العالمین و صلی الله علی سیدنا محمد نبیه و آله و سلم...",
    "🤲 **دعای سمات**: اللهم انی اسئلک باسمک العظیم الاعظم...",
    "🤲 **دعای مجیر**: سبحانک یا لا اله الا انت الغوث الغوث...",
    "🤲 **دعای ابوحمزه ثمالی**: الهی لا تؤدبنی بعقوبتک...",
]

# لطیفه‌ها
jokes = [
    "یکی میگه رفتم دکتر بهم گفت آلزایمر گرفتی! گفتم چیزیم نیست! گفت یادت رفت من گفتم؟ 😂",
    "شاگرد استاد: استاد خواب دیدم امتحان قبول شدم! استاد: پسر خوب فردا امتحان داری، خواب می‌بینی؟! 🤣",
    "زن به شوهرش: عزیزم به نظرت من چاق شدم؟ شوهر: عزیزم تو هیچوقت چاق نبودی! زن: پس الان چاق شدم؟ شوهر: 🤐",
    "رفتم خواستگاری، پدر دختر گفت داماد چی کاره‌ای؟ گفتم شاعرم! گفت پس فردا یه شعری بگو ببینم چی میگی! گفتم عیب نداره! گفت ولی فردا عروسیه! 🤔",
    "دوتا پشه نشسته بودن روی دکل، یکی گفت بیایم بریم خونه؟ اون یکی گفت بریم، اینجا که اینترنت نداره! 🦟",
    "رفتم بانک گفتم وام می‌خوام، گفتن ضامن چی داری؟ گفتم خدا! گفتن قبول! ولی سفته هم می‌خوایم! 🙏",
]

# حقایق جالب
fun_facts = [
    "🐙 اختاپوس‌ها سه قلب دارند!",
    "🍌 موز در واقع نوعی توت است!",
    "🐝 زنبورها می‌توانند انسان‌ها را تشخیص دهند!",
    "🌍 ۹۹٪ از طلای زمین در هسته آن است!",
    "💧 انسان می‌تواند ۳ هفته بدون غذا زنده بماند، اما فقط ۳ روز بدون آب!",
    "🧠 مغز انسان در خواب فعال‌تر از بیداری است!",
    "🌊 ۹۰٪ از اقیانوس‌ها هنوز کشف نشده‌اند!",
    "🦒 زرافه با زبانش می‌تواند گوش‌های خود را تمیز کند!",
    "🐄 گاوها بهترین دوست دارند و با دوستان خود وقت می‌گذرانند!",
    "🦋 پروانه‌ها با پاهایشان می‌چشند!",
]

# فال‌های روزانه
daily_fortunes = [
    "✨ امروز روز خوبی برای شروع کارهای جدید است!",
    "💫 منتظر یک خبر خوب از طرف یک دوست قدیمی باش!",
    "⭐ فرصت‌های جدیدی به سراغت می‌آید، آماده باش!",
    "🌟 نگران نباش، مشکل امروز تو راه حل دارد!",
    "💝 کسی مخفیانه به تو فکر می‌کند!",
    "🎯 به هدفت نزدیک‌تر از آنی که فکر می‌کنی!",
    "🌈 رنگین کمان زندگی‌ات در شرف ظهور است!",
    "🎁 امروز یه هدیه غیرمنتظره می‌گیری!",
]

# پیشنهادات فیلم و سریال
movie_suggestions = [
    "🎬 پیشنهاد فیلم: اینتراستلار - داستانی درباره سفر در زمان و عشق به خانواده",
    "🎬 پیشنهاد فیلم: شازده کوچولو - انیمیشنی زیبا درباره دوستی و زندگی",
    "🎬 پیشنهاد فیلم: فارست گامپ - زندگی پرماجرای یه پسر ساده‌دل",
    "🎬 پیشنهاد سریال: بازی تاج‌وتخت - فانتزی و حماسی",
    "🎬 پیشنهاد سریال: برکینگ بد - داستان یه معلم شیمی که پولساز میشه",
    "🎬 پیشنهاد فیلم: سه برادر - کمدی ایرانی با بازی حمید لولایی",
    "🎬 پیشنهاد انیمه: اتک آن تایتان - اکشن و درام",
    "🎬 پیشنهاد مستند: سیاره ما - درباره طبیعت و محیط زیست",
]

# نکات آموزشی زبان انگلیسی
english_tips = [
    "📚 **انگلیسی**: برای مکالمه روزمره: How are you doing? = حالت چطوره؟",
    "📚 **انگلیسی**: I'm looking forward to seeing you = مشتاق دیدارت هستم",
    "📚 **انگلیسی**: It's a piece of cake = آب خوردنه! (خیلی آسان)",
    "📚 **انگلیسی**: Break a leg! = موفق باشی! (در اجرا)",
    "📚 **انگلیسی**: Once in a blue moon = یه وقت‌هایی خیلی نادر",
    "📚 **انگلیسی**: Better late than never = دیر رسیدن بهتر از هرگز نرسیدنه",
    "📚 **انگلیسی**: Keep up the good work = به کار خوبت ادامه بده",
    "📚 **انگلیسی**: It's not my cup of tea = به درد من نمیخوره",
]

# نکات سلامتی
health_tips = [
    "💪 روزانه ۸ لیوان آب بنوشید!",
    "🥦 میوه و سبزیجات تازه رو در برنامه غذایی روزانه داشته باشید!",
    "🏃‍♂️ روزانه حداقل ۳۰ دقیقه پیاده‌روی کنید!",
    "😴 خواب کافی (۷-۸ ساعت) برای سلامتی ضروری است!",
    "🧘 مدیتیشن و تنفس عمیق استرس را کاهش می‌دهد!",
    "📱 قبل از خواب از گوشی استفاده نکنید!",
    "☕ مصرف کافئین را بعد از ظهر محدود کنید!",
    "🌞 صبح‌ها ۱۵ دقیقه نور خورشید دریافت کنید!",
]

# طالع بینی ماه تولد
birthday_horoscope = {
    "فروردین": {"symbol": "♈", "element": "آتش", "personality": "شجاع، پرانرژی، رهبر", "lucky_day": "سه‌شنبه"},
    "اردیبهشت": {"symbol": "♉", "element": "خاک", "personality": "صبور، قابل اعتماد، پایدار", "lucky_day": "جمعه"},
    "خرداد": {"symbol": "♊", "element": "هوا", "personality": "کنجکاو، اجتماعی، باهوش", "lucky_day": "چهارشنبه"},
    "تیر": {"symbol": "♋", "element": "آب", "personality": "احساساتی، خانواده‌دوست، حساس", "lucky_day": "دوشنبه"},
    "مرداد": {"symbol": "♌", "element": "آتش", "personality": "مغرور، سخاوتمند، خلاق", "lucky_day": "یکشنبه"},
    "شهریور": {"symbol": "♍", "element": "خاک", "personality": "منظم، تحلیلگر، دقیق", "lucky_day": "چهارشنبه"},
    "مهر": {"symbol": "♎", "element": "هوا", "personality": "منصف، اجتماعی، دیپلماتیک", "lucky_day": "جمعه"},
    "آبان": {"symbol": "♏", "element": "آب", "personality": "مرموز، پرشور، مصمم", "lucky_day": "سه‌شنبه"},
    "آذر": {"symbol": "♐", "element": "آتش", "personality": "ماجراجو، خوش‌بین، صادق", "lucky_day": "پنجشنبه"},
    "دی": {"symbol": "♑", "element": "خاک", "personality": "مسئول، منظم، سخت‌کوش", "lucky_day": "شنبه"},
    "بهمن": {"symbol": "♒", "element": "هوا", "personality": "نوآور، مستقل، انساندوست", "lucky_day": "پنجشنبه"},
    "اسفند": {"symbol": "♓", "element": "آب", "personality": "هنرمند، مهربان، رویایی", "lucky_day": "دوشنبه"},
}

# ==================== توابع جدید سرگرمی ====================
async def get_random_fortune():
    """فال روزانه"""
    return random.choice(daily_fortunes)

async def get_random_joke():
    """لطیفه تصادفی"""
    return random.choice(jokes)

async def get_random_fact():
    """حقیقت جالب"""
    return random.choice(fun_facts)

async def get_random_movie():
    """پیشنهاد فیلم"""
    return random.choice(movie_suggestions)

async def get_english_tip():
    """نکته آموزشی انگلیسی"""
    return random.choice(english_tips)

async def get_health_tip():
    """نکته سلامتی"""
    return random.choice(health_tips)

async def get_random_prayer():
    """دعای تصادفی"""
    return random.choice(prayers)

async def get_random_islamic_rule():
    """حکم شرعی تصادفی"""
    return random.choice(islamic_rules)

async def get_random_philosophy():
    """جمله فلسفی"""
    return random.choice(philosophical_quotes)

async def get_random_riddle():
    """معمای تصادفی"""
    riddle = random.choice(riddles)
    return f"🧩 **معما:**\n{riddle['question']}\n\n📝 برای دیدن جواب بنویس: جواب معما"

async def get_riddle_answer(question):
    """جواب معما"""
    for riddle in riddles:
        if riddle["question"] == question:
            return f"🔍 **جواب معمای قبلی:**\n{riddle['answer']}"
    return None

async def get_hafez_fal():
    """فال حافظ"""
    return random.choice(hafez_fal)

async def get_personality_test(category, choice):
    """تست شخصیت"""
    if category in personality_tests and choice in personality_tests[category]:
        traits = personality_tests[category][choice]
        return f"🎭 **تست شخصیت - {category}**\n\nشما {choice} را انتخاب کردید:\n• {traits[0]}\n• {traits[1]}\n• {traits[2]}\n{traits[3]}"
    return None

async def get_birthday_horoscope(month):
    """طالع بینی ماه تولد"""
    if month in birthday_horoscope:
        info = birthday_horoscope[month]
        return f"""♈ **طالع بینی متولدین {month}** ♈
━━━━━━━━━━━━━━━
🔮 **نماد:** {info['symbol']}
🔥 **عنصر:** {info['element']}
👤 **شخصیت:** {info['personality']}
🍀 **روز خوش شانس:** {info['lucky_day']}"""
    return None

async def calculate_age(birth_year, birth_month, birth_day):
    """محاسبه سن دقیق"""
    try:
        today = jdatetime.date.today()
        birth_date = jdatetime.date(int(birth_year), int(birth_month), int(birth_day))
        age = today.year - birth_date.year
        
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        next_birthday = jdatetime.date(today.year, birth_date.month, birth_date.day)
        if next_birthday < today:
            next_birthday = jdatetime.date(today.year + 1, birth_date.month, birth_date.day)
        
        days_to_birthday = (next_birthday - today).days
        
        return {
            "age": age,
            "days_to_birthday": days_to_birthday,
            "next_birthday": next_birthday.strftime("%Y/%m/%d")
        }
    except:
        return None

# ==================== ادامه کد اصلی ربات ====================
# [بقیه کدهای اصلی ربات بدون تغییر باقی می‌ماند]
# دیتابیس پایه و توابع قبلی
speaker_db = {
    "سلام": ["سلام جونم😍😍", "درود گل"],
    "درود": ["درود بر تو", "شلام", "درود", "سلام"],
    "خبی": ["با وجود تو ارع", "شاید", "مشتی من باتم", "ای با"],
    "خوبی": ["با وجود تو ارع", "شاید", "مشتی من باتم", "ای با"],
    "اسمت چیه": ["مدیریت گروه نوب"],
    "جالبه": ["خیلیییی", "واقعا میگی ؟", "خوبه"],
    "نه": ["چرا?", "بله", "هعب"],
    ".": ["نت مخوای؟", "شماره کارت بده پیل بزنم"],
    "آخ": ["اخ قلبم شکست", "زنده ای؟", "جان"],
    "ربات": ["جون", "چ دختری", "ن با بات چیه", "هستی بزنیم؟"],
    "آفه": ["نه حراجه", "چی؟", "ممممم"],
    "خاموش کن": ["دروغ میگه روشن کن", "ننننن", "ایفففف"],
    "شب": ["خوش", "میموندی", "خدافظ"],
    "شب بخیر": ["نوش جونت", "صب بیا کارت دارم", "لا", "فویک"],
    "بات": ["بابات ؟", "چیه", "چی", "با منی؟"],
    "این چیه": ["این ب درخت میگن"],
    "ن بابا": ["من بات نیستم", "چشک"],
    "عااااا": ["امممم"],
    "خوبه": ["اکیه"],
    "چخبر": ["سلامتی 🦠"],
    "چی شده": ["هیچ", "خودت بهتر میدونی"]
}

# تنظیمات قوانین
rules_config, rules_fa = {
    "active": True,
    "link": True,
    "mention": True,
    "hashtag": False,
    "emoji": False,
    "only_emoji": False,
    "number": False,
    "command": False,
    "metadata": True,
    "bold": False,
    "italic": False,
    "underline": False,
    "strike": False,
    "quote": False,
    "spoiler": False,
    "code": False,
    "mono": False,
    "photo": False,
    "video": False,
    "audio": False,
    "voice": False,
    "music": False,
    "document": False,
    "archive": False,
    "executable": False,
    "font": False,
    "sticker": False,
    "forward": True,
    "contact": False,
    "location": False,
    "live_location": False,
    "poll": False,
    "anti_flood": True,
    "anti_ad": True,
    "anti_curse": True,
    "anti_hung": True,
    "anti_emoji": True,
    "anti_edit": True,
    "anti_mention": True,
    "gif": True
}, {
    "active": "فعال",
    "link": "لینک",
    "mention": "منشن",
    "hashtag": "هشتگ",
    "emoji": "ایموجی",
    "only_emoji": "فقط ایموجی",
    "number": "عدد",
    "command": "دستور",
    "metadata": "متادیتا",
    "bold": "متن بولد",
    "italic": "متن ایتالیک",
    "underline": "زیرخط",
    "strike": "خط خورده",
    "quote": "کوت",
    "spoiler": "اسپویلر",
    "code": "کد",
    "mono": "مونواسپیس",
    "photo": "عکس",
    "video": "ویدیو",
    "audio": "صوت",
    "voice": "ویس",
    "music": "موزیک",
    "document": "سند / فایل",
    "archive": "فایل فشرده",
    "executable": "فایل اجرایی",
    "font": "فونت",
    "sticker": "استیکر",
    "forward": "فوروارد",
    "contact": "شماره تماس",
    "location": "لوکیشن",
    "live_location": "لوکیشن زنده",
    "poll": "نظرسنجی",
    "anti_flood": "کد هنگی",
    "anti_ad": "ضد تبلیغ",
    "anti_curse": "ضد فحش",
    "anti_hung": "ضد هنگی",
    "anti_emoji": "ضد ایموجی",
    "anti_edit": "ضد ویرایش",
    "anti_mention": "ضد منشن",
    "gif": "گیف"
}

filtered_words = set()
ad_patterns = [
    r'ب[\.\/]*یو', r'بی[\.\/]*و', r'ل[\.\/]*ی[\.\/]*ن[\.\/]*ک',
    r'ع[\.\/]*ض[\.\/]*و', r'ج[\.\/]*و[\.\/]*ی[\.\/]*ن',
    r'پ[\.\/]*ی', r'س[\.\/]*ر[\.\/]*ی[\.\/]*ع',
    r'ب[\.\/]*ر[\.\/]*ن[\.\/]*ا[\.\/]*م[\.\/]*ه',
    r'چ[\.\/]*ت', r'چ[\.\/]*ک', r'ت[\.\/]*ب[\.\/]*ل[\.\/]*ی[\.\/]*غ'
]
hung_patterns = [
    r'1\.1\.1\.1\.1\.1\.1', r'2\.2\.2\.2\.2', r'1\.2\.3\.1\.2\.3',
    r'0\.0\.0\.0\.', r'5\.5\.5\.5', r'6\.6\.0\.3',
    r'Filter', r'Ban', r'report'
]
emoji_list = '🔥👺✨🗿😐🙂😂♥️🫸🥺💦😑😌😒🥲💋🚶🏻‍♂️😘👍🤲🖕💎✅💕🤌🫷🤣👉😁🚫❓❗🙏😅👏🥳😭😅🥲😪😛🤗🥱☹️🤮🤢😈👻🌚🌝💩😹😻😼😸😹😿❤️🧡💛💚🩵💙🩸👀💀🦴🦷🐨🐼🐹🐭🐰🦊🦝🐻🐮🐷🦁🐯🐱🐶🐺🦍🍎🍉🍑🍊🥭🍍🍌🍐🍏🍋🍋🥝🫒🍇🍕🍭🍬🍫🧸'

TAG_TEXTS = [
    "کجایی رفتی؟", "آنلاین نمیشی چرا؟", "یه سر بیا!", "چرا همیشه دیر میای؟",
    "کی برمی‌گردی؟", "هیچ خبری ازت نیست!", "منتظرت بودیم!", "دیر کردی بیا!",
    "یه پیامی بده دیگه!", "گروه رو با بی‌خبری ترک کردی!", "باز هم غیب شدی؟",
    "حواست کجاست؟", "کجا رفته‌ای که پیدات نمی‌کنیم؟", "چرا هیچ‌وقت آنلاین نمی‌شی؟",
    "چطور همیشه ناپدید می‌شی؟", "کجایید که هیچ خبری ازتون نیست؟",
    "گروه بدون شما خیلی بی‌روح شده!", "منتظریم بیای، خب!", "هیچ خبری ازت نیست!",
    "تو که همیشه می‌اومدی، چرا الان نیستی؟", "دلمون تنگ شده، بیا دیگه!",
    "منتظر خبری ازت هستیم!", "کی از ما خبر می‌گیری؟",
    "گروه بدون شما هیچ جذابیتی نداره!", "حواست کجاست که خبری ازت نیست؟",
    "کجا گم شدی؟", "بی‌خبری چه معنی می‌ده؟", "هرجا که هستی، بیا دیگه!",
    "گروه رو بدون تو نمی‌چرخونه!", "یادت رفته گروه رو؟",
    "منتظریم تو بیای تا بحث رو ادامه بدیم!", "پیدات نمی‌کنیم اصلاً!",
    "یادته که هنوز اینجا منتظریم؟", "منتظریم یه علامت ازت ببینیم!",
    "گروه بدون تو سوت و کوره!", "حتی یک پیام هم نمی‌فرستی؟",
    "آیا هنوز تو گروهی؟", "کی میای که ادامه بدیم؟", "یه سر بزن دیگه!",
    "کی میای تو گروه فعال بشی؟", "ما هنوز هم منتظریم!",
    "گروه با حضور تو تکمیل میشه!", "ما رو تنها گذاشتی؟", "چرا خبری ازت نیست؟",
    "مگه قرار نبود همیشه آنلاین باشی؟", "چرا غیب زدی؟", "بی‌خبر نرو!",
    "خبری ازت نیست!", "پیدات نمیشه اصلاً!", "کجا گم شدی؟",
    "دلمون برات تنگ شده!", "همیشه غایبی!", "چرا جواب نمیدی؟",
    "منتظریم بیای!", "کی برمی‌گردی؟", "یه پیام بده!", "سرت شلوغه؟",
    "حواست به ما نیست!", "گروه بدون تو سوت و کوره!", "کلاً ناپدید شدی!",
    "چرا سر نمی‌زنی؟", "آنلاین میشی یا نه؟", "یه علامت بده زنده‌ای!",
    "بازم نیستی!", "ما رو یادت رفته؟", "چرا اینقدر ساکتی؟",
    "یه سر بزن خب!", "کجایی که نیستی؟", "تو که همیشه میومدی!",
    "گروه رو ول کردی؟", "غیب کامل زدی!", "دیگه نمیای؟",
    "منتظر ظهورتیم!", "کجایی آخه؟", "دلت برای گروه تنگ نشده؟",
    "پیدات نمی‌کنیم!", "یه خبری از خودت بده!"
]

challenge_list = [
    "به یک غریبه لبخند بزن و سلام کن",
    "یک روز کامل بدون گوشی موبایل زندگی کن",
    "یک کتاب 100 صفحه‌ای در 24 ساعت بخوان",
    "با یک فرد مسن مکالمه عمیق داشته باش",
    "یک مهارت جدید در یوتیوب یاد بگیر",
    "برای خانواده‌ات غذای مورد علاقه‌شان را بپز",
    "یک روز کامل فارسی را با لهجه متفاوت صحبت کن",
    "10 دقیقه مدیتیشن انجام بده",
    "یک نقاشی بکش و در شبکه‌های اجتماعی منتشر کن",
    "برای یک حیوان بی‌پناه غذا تهیه کن",
    "یک شعر حفظ کن و برای دیگران بخوان",
    "با دست غیر مسلط خود بنویس",
    "یک روز کامل صرفه‌جویی در مصرف آب داشته باش",
    "یک دستور غذایی جدید را امتحان کن",
    "برای دوستانت یک هدیه کوچک و معنادار بخر",
    "یک ورزش جدید را امتحان کن",
    "خانه‌ات را به طور کامل تمیز کن",
    "یک نامه تشکر برای والدینت بنویس",
    "یک روز کامل از شبکه‌های اجتماعی دور باش",
    "یک هدف جدید برای یک ماه آینده تعیین کن"
]

hadiths = [
    "پیامبر اکرم (ص) فرمودند: بهترین شما کسی است که برای مردم سودمندتر باشد.",
    "امام علی (ع) فرمودند: دانش را بیاموزید ولو در چین باشد.",
    "پیامبر (ص) فرمودند: هر کس صبح کند و به فکر مسلمانان نباشد، مسلمان نیست.",
    "امام صادق (ع) فرمودند: نعمت‌های خدا را بشمارید تا بر شما افزوده شود.",
    "پیامبر (ص) فرمودند: با مردم به نیکی رفتار کنید.",
    "امام علی (ع) فرمودند: سکوت دری از درهای حکمت است.",
    "پیامبر (ص) فرمودند: تواضع کنید تا خداوند شما را بلندمرتبه کند.",
    "امام حسین (ع) فرمودند: اگر دین ندارید، آزاده باشید.",
    "پیامبر (ص) فرمودند: خوش‌اخلاقی نیمی از دین است.",
    "امام علی (ع) فرمودند: صبر، کلید رهایی از سختی‌هاست.",
    "پیامبر (ص) فرمودند: بهترین عبادت، انتظار فرج است.",
    "امام صادق (ع) فرمودند: ایمان، گفتار و کردار است.",
    "پیامبر (ص) فرمودند: علم بی‌عمل مانند درخت بی‌ثمر است.",
    "امام علی (ع) فرمودند: از کاری که عاقبتش پشیمانی است بپرهیزید.",
    "پیامبر (ص) فرمودند: مؤمن آینه مؤمن دیگر است."
]

memories = [
    "اولین روز مدرسه را به یاد دارم که دست مادرم را محکم گرفته بودم و از ترس گریه می‌کردم.",
    "یادش بخیر وقتی بچه بودیم، تابستان‌ها تا دیروقت در کوچه بازی می‌کردیم.",
    "اولین دوچرخه‌سواری ام را هیچ‌وقت فراموش نمی‌کنم، زمین خوردم ولی دوباره بلند شدم.",
    "یادم هست برای تولدم یک عروسک هدیه گرفتم که سال‌ها همراه من بود.",
    "اولین سفرم به شمال را به خاطر دارم، بوی دریا هنوز در خاطرم مانده است.",
    "دبیرستان که بودیم، با دوستانم روی پشت بام مدرسه ناهار می‌خوردیم.",
    "یادش بخیر شب‌های قدر که با خانواده تا صبح بیدار می‌ماندیم.",
    "اولین بار که آشپزی کردم، غذا را سوزاندم اما خانواده با خوشحالی خوردند.",
    "وقتی برف می‌آمد، با برادرانم آدم برفی درست می‌کردیم.",
    "خاطره اولین کنسرتی که رفتم، هنوز با تمام جزئیات در ذهنم است."
]

stories = [
    "پسرکی هر روز به دریا می‌رفت و ستاره‌های دریایی را که به ساحل افتاده بودند به دریا برمی‌گرداند. مردی به او گفت: 'این همه ستاره دریایی هست، کار تو چه تغییری می‌کند؟' پسرک یکی را به دریا انداخت و گفت: 'برای این یکی که تغییری کرد.'",
    "فیل‌ها در سیرک با طناب نازکی بسته می‌شوند. وقتی بچه هستند با همان طناب می‌بندندشان و نمی‌توانند فرار کنند. وقتی بزرگ می‌شوند باور دارند که نمی‌توانند طناب را پاره کنند، پس حتی امتحان هم نمی‌کنند.",
    "دوستی دو قورباغه در چاه عمیقی افتادند. دیگر قورباغه‌ها گفتند تسلیم شوند. یکی تسلیم شد و مرد. دیگری به تلاش ادامه داد و در نهایت با جهشی بلند از چاه بیرون پرید. معلوم شد ناشنوا بود و فکر می‌کرد دیگران او را تشویق می‌کنند.",
    "مردی هر روز به گدایی کمک می‌کرد. یک روز گدا پرسید: 'چرا به من کمک می‌کنی؟' مرد گفت: 'من گدایی می‌کردم که کسی به من کمک کند. تو به من کمک کردی که بفهمم کمک کردن چه حسی دارد.'",
    "پیرمردی در حال کاشتن درخت بود. جوانی گفت: 'چرا درخت می‌کاری؟ تا میوه بدهد خیلی وقت می‌خواهد.' پیرمرد پاسخ داد: 'اگر همه مثل تو فکر کنند، هیچ‌وقت درختی وجود نخواهد داشت.'",
    "کشاورزی دو بذر کاشت. یکی گفت: 'می‌ترسم ریشه بدهم.' دیگری شجاعت کرد و ریشه داد. امروز اولی هنوز بذر است و دومی درختی تنومند.",
    "لاک‌پشت و خرگوش مسابقه دادند. خرگوش مطمئن از بردش خوابید. لاک‌پشت آهسته اما پیوسته حرکت کرد و برنده شد. پایداری همیشه از سرعت مهم‌تر است.",
    "شاهزاده‌ای سنگ قیمتی گم کرد. جویندگان زیادی آمدند ولی پیدا نکردند. کودکی آمد و سنگ را پیدا کرد. از او پرسیدند: 'چطور پیدا کردی؟' گفت: 'من فقط جای خالی آن را نگاه کردم.'",
    "مرغی تخم طلا می‌گذاشت. صاحبش طمع کرد و شکمش را پاره کرد تا همه طلاها را یکجا بگیرد. اما چیزی نیافت و مرغ را هم از دست داد.",
    "پیرمردی روی نیمکت پارک نشسته بود. پسری آمد و کنارش نشست. پیرمرد گفت: 'زندگی مثل دویدن در باران است. بعضی می‌دوند و خیس می‌شوند، بعضی آهسته می‌روند و کمتر خیس می‌شوند. اما همه در نهایت به مقصد می‌رسند.'"
]

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS chats (chat_id TEXT PRIMARY KEY, type TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS admins (chat_id TEXT PRIMARY KEY, creator_id TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS speaker_status (chat_id TEXT PRIMARY KEY, status TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS antilink (chat_id TEXT PRIMARY KEY, status TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS learn (chat_id TEXT, question TEXT, answer TEXT, PRIMARY KEY (chat_id, question))""")
        c.execute("""CREATE TABLE IF NOT EXISTS rules (
            chat_id TEXT PRIMARY KEY, 
            anti_ad TEXT DEFAULT 'on',
            anti_curse TEXT DEFAULT 'on',
            anti_hung TEXT DEFAULT 'on',
            anti_emoji TEXT DEFAULT 'on',
            anti_edit TEXT DEFAULT 'on',
            anti_mention TEXT DEFAULT 'on',
            gif TEXT DEFAULT 'on'
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS filtered_words (chat_id TEXT, word TEXT, PRIMARY KEY (chat_id, word))""")
        c.execute("""CREATE TABLE IF NOT EXISTS users (chat_id TEXT, user_id TEXT PRIMARY KEY)""")
        c.execute("""CREATE TABLE IF NOT EXISTS mutes (chat_id TEXT, user_id TEXT, mute_time INTEGER, mute_duration INTEGER, is_permanent INTEGER, PRIMARY KEY (chat_id, user_id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS members (chat_id TEXT, user_id TEXT, PRIMARY KEY (chat_id, user_id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS user_stats (chat_id TEXT, user_id TEXT, message_count INTEGER DEFAULT 0, date INTEGER, PRIMARY KEY (chat_id, user_id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS group_lock (chat_id TEXT PRIMARY KEY, is_locked INTEGER DEFAULT 0)""")
        c.execute("""CREATE TABLE IF NOT EXISTS assistant_admins (chat_id TEXT, user_id TEXT, PRIMARY KEY (chat_id, user_id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS messages (chat_id TEXT, message_id INTEGER, timestamp INTEGER, PRIMARY KEY (chat_id, message_id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS group_rules_text (chat_id TEXT PRIMARY KEY, rules_text TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS bot_status_chat (chat_id TEXT PRIMARY KEY, status TEXT DEFAULT 'on')""")
        c.execute("""CREATE TABLE IF NOT EXISTS active_groups (chat_id TEXT PRIMARY KEY, group_info TEXT)""")
        conn.commit()

init_db()

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = sqlite3.connect(self.db_path)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.commit()
            self._conn.close()

async def _execute_db_query(query, params=(), fetch_one=False, fetch_all=False):
    try:
        with DatabaseManager(DB_PATH) as cursor:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

async def is_first_message(chat_id):
    result = await _execute_db_query("SELECT 1 FROM chats WHERE chat_id = ?", (chat_id,), fetch_one=True)
    return result is None

async def save_chat_id(chat_id, chat_type):
    await _execute_db_query("INSERT OR IGNORE INTO chats (chat_id, type) VALUES (?, ?)", (chat_id, chat_type))

async def set_group_creator(chat_id, creator_id):
    await _execute_db_query("INSERT OR REPLACE INTO admins (chat_id, creator_id) VALUES (?, ?)", (chat_id, creator_id))

async def get_group_creator(chat_id):
    row = await _execute_db_query("SELECT creator_id FROM admins WHERE chat_id = ?", (chat_id,), fetch_one=True)
    return row[0] if row else None

async def is_group_creator(chat_id, user_id):
    creator = await get_group_creator(chat_id)
    return str(user_id) == str(creator)

async def set_speaker_status(chat_id, status):
    await _execute_db_query("INSERT OR REPLACE INTO speaker_status (chat_id, status) VALUES (?, ?)", (chat_id, status))

async def get_speaker_status(chat_id):
    row = await _execute_db_query("SELECT status FROM speaker_status WHERE chat_id = ?", (chat_id,), fetch_one=True)
    return row and row[0] == "on"

async def save_learning(chat_id, question, answer):
    await _execute_db_query("INSERT OR REPLACE INTO learn (chat_id, question, answer) VALUES (?, ?, ?)", (chat_id, question.strip(), answer.strip()))

async def get_learning(chat_id, text):
    row = await _execute_db_query("SELECT answer FROM learn WHERE chat_id = ? AND question = ?", (chat_id, text.strip()), fetch_one=True)
    return row[0] if row else None

async def delete_learning(chat_id, question):
    await _execute_db_query("DELETE FROM learn WHERE chat_id = ? AND question = ?", (chat_id, question.strip()))

async def list_learnings(chat_id):
    return await _execute_db_query("SELECT question, answer FROM learn WHERE chat_id = ?", (chat_id,), fetch_all=True)

async def get_counts():
    groups = await _execute_db_query("SELECT COUNT(*) FROM chats WHERE type='group'", fetch_one=True)
    users = await _execute_db_query("SELECT COUNT(*) FROM chats WHERE type='private'", fetch_one=True)
    return (groups[0] if groups else 0), (users[0] if users else 0)

async def get_total_count():
    total = await _execute_db_query("SELECT COUNT(*) FROM chats", fetch_one=True)
    return total[0] if total else 0

async def get_all_chats():
    result = await _execute_db_query("SELECT chat_id FROM chats", fetch_all=True)
    return [r[0] for r in result] if result else []

async def set_antilink_status(chat_id, status):
    await _execute_db_query("INSERT OR REPLACE INTO antilink (chat_id, status) VALUES (?, ?)", (chat_id, status))

async def get_antilink_status(chat_id):
    row = await _execute_db_query("SELECT status FROM antilink WHERE chat_id = ?", (chat_id,), fetch_one=True)
    return row and row[0] == "on"

async def get_rule_status(chat_id, rule_type):
    row = await _execute_db_query(f"SELECT {rule_type} FROM rules WHERE chat_id = ?", (chat_id,), fetch_one=True)
    return row and row[0] == "on"

async def set_rule_status(chat_id, rule_type, status):
    await _execute_db_query(f"INSERT OR REPLACE INTO rules (chat_id, {rule_type}) VALUES (?, ?)", (chat_id, status))

async def init_rules(chat_id):
    await _execute_db_query("INSERT OR REPLACE INTO rules (chat_id, anti_ad, anti_curse, anti_hung, anti_emoji, anti_edit, anti_mention, gif) VALUES (?, 'on', 'on', 'on', 'on', 'on', 'on', 'on')", (chat_id,))

async def add_filtered_word(chat_id, word):
    await _execute_db_query("INSERT OR IGNORE INTO filtered_words (chat_id, word) VALUES (?, ?)", (chat_id, word))

async def remove_filtered_word(chat_id, word):
    await _execute_db_query("DELETE FROM filtered_words WHERE chat_id = ? AND word = ?", (chat_id, word))

async def get_filtered_words(chat_id):
    rows = await _execute_db_query("SELECT word FROM filtered_words WHERE chat_id = ?", (chat_id,), fetch_all=True)
    return [row[0] for row in rows] if rows else []

async def add_assistant_admin(chat_id, user_id):
    await _execute_db_query("INSERT OR IGNORE INTO assistant_admins (chat_id, user_id) VALUES (?, ?)", (chat_id, user_id))

async def remove_assistant_admin(chat_id, user_id):
    await _execute_db_query("DELETE FROM assistant_admins WHERE chat_id=? AND user_id=?", (chat_id, user_id))

async def is_assistant_admin(chat_id, user_id):
    if await is_group_creator(chat_id, user_id):
        return True
    row = await _execute_db_query("SELECT 1 FROM assistant_admins WHERE chat_id=? AND user_id=?", (chat_id, user_id), fetch_one=True)
    return row is not None

async def toggle_group_lock(chat_id, is_locked):
    await _execute_db_query("INSERT OR REPLACE INTO group_lock (chat_id, is_locked) VALUES (?, ?)", (chat_id, is_locked))

async def is_group_locked(chat_id):
    row = await _execute_db_query("SELECT is_locked FROM group_lock WHERE chat_id=?", (chat_id,), fetch_one=True)
    return row and row[0] == 1

async def save_member(chat_id, user_id):
    await _execute_db_query("INSERT OR IGNORE INTO members (chat_id, user_id) VALUES (?, ?)", (chat_id, user_id))

async def get_members(chat_id):
    rows = await _execute_db_query("SELECT user_id FROM members WHERE chat_id=?", (chat_id,), fetch_all=True)
    return [row[0] for row in rows] if rows else []

async def increase_message_count(chat_id, user_id):
    await _execute_db_query("""
    INSERT INTO user_stats (chat_id, user_id, message_count, date)
    VALUES (?, ?, 1, ?)
    ON CONFLICT(chat_id, user_id)
    DO UPDATE SET message_count = message_count + 1, date = ?
    """, (chat_id, user_id, int(time.time()), int(time.time())))

async def mute_user_db(chat_id, user_id, mute_duration=0, is_permanent=0):
    await _execute_db_query("""
    INSERT OR REPLACE INTO mutes (chat_id, user_id, mute_time, mute_duration, is_permanent)
    VALUES (?, ?, ?, ?, ?)
    """, (chat_id, user_id, int(time.time()), mute_duration, is_permanent))

async def unmute_user_db(chat_id, user_id):
    await _execute_db_query("DELETE FROM mutes WHERE chat_id=? AND user_id=?", (chat_id, user_id))

async def is_muted(chat_id, user_id):
    row = await _execute_db_query("SELECT 1 FROM mutes WHERE chat_id=? AND user_id=?", (chat_id, user_id), fetch_one=True)
    return row is not None

async def get_muted_users(chat_id):
    rows = await _execute_db_query("SELECT user_id FROM mutes WHERE chat_id=?", (chat_id,), fetch_all=True)
    return [row[0] for row in rows] if rows else []

async def get_user_stats(chat_id, user_id):
    row = await _execute_db_query("SELECT message_count FROM user_stats WHERE chat_id=? AND user_id=?", (chat_id, user_id), fetch_one=True)
    return row[0] if row else 0

async def get_group_stats(chat_id):
    total_messages = await _execute_db_query("SELECT SUM(message_count) FROM user_stats WHERE chat_id=?", (chat_id,), fetch_one=True)
    active_users = await _execute_db_query("SELECT COUNT(*) FROM user_stats WHERE chat_id=?", (chat_id,), fetch_one=True)
    admin_count = await _execute_db_query("SELECT COUNT(*) FROM assistant_admins WHERE chat_id=?", (chat_id,), fetch_one=True)
    muted_users = await _execute_db_query("SELECT COUNT(*) FROM mutes WHERE chat_id=?", (chat_id,), fetch_one=True)
    
    return {
        "total_messages": total_messages[0] if total_messages and total_messages[0] else 0,
        "active_users": active_users[0] if active_users else 0,
        "admin_count": (admin_count[0] if admin_count else 0) + 1,
        "muted_users": muted_users[0] if muted_users else 0
    }

async def save_message_to_db(chat_id, message_id):
    await _execute_db_query("INSERT OR REPLACE INTO messages (chat_id, message_id, timestamp) VALUES (?, ?, ?)", 
                          (chat_id, message_id, int(time.time())))

async def get_recent_messages(chat_id, limit=100):
    rows = await _execute_db_query("SELECT message_id FROM messages WHERE chat_id=? ORDER BY timestamp DESC LIMIT ?", 
                                  (chat_id, limit), fetch_all=True)
    return [row[0] for row in rows] if rows else []

async def delete_messages_from_db(chat_id, message_ids):
    for msg_id in message_ids:
        await _execute_db_query("DELETE FROM messages WHERE chat_id=? AND message_id=?", (chat_id, msg_id))

async def set_group_rules(chat_id, rules_text):
    await _execute_db_query("INSERT OR REPLACE INTO group_rules_text (chat_id, rules_text) VALUES (?, ?)", (chat_id, rules_text))

async def get_group_rules(chat_id):
    row = await _execute_db_query("SELECT rules_text FROM group_rules_text WHERE chat_id=?", (chat_id,), fetch_one=True)
    return row[0] if row else "📝 هنوز قوانینی برای این گروه تنظیم نشده است."

async def set_bot_status(chat_id, status):
    await _execute_db_query("INSERT OR REPLACE INTO bot_status_chat (chat_id, status) VALUES (?, ?)", (chat_id, status))

async def get_bot_status(chat_id):
    row = await _execute_db_query("SELECT status FROM bot_status_chat WHERE chat_id=?", (chat_id,), fetch_one=True)
    return row[0] if row else "on"

async def save_active_group(chat_id, group_info):
    await _execute_db_query("INSERT OR REPLACE INTO active_groups (chat_id, group_info) VALUES (?, ?)", (chat_id, group_info))

async def get_active_groups():
    rows = await _execute_db_query("SELECT chat_id, group_info FROM active_groups", fetch_all=True)
    return rows if rows else []

def random_tag_text():
    return random.choice(TAG_TEXTS)

def load_curse_words():
    try:
        with open('fohshs.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'curse_words =' in content:
                curse_words = eval(content.split('curse_words =')[1].strip())
                return curse_words
    except:
        pass
    return []

def load_challenges():
    return challenge_list

def load_hadiths():
    return hadiths

def load_memories():
    return memories

def load_stories():
    return stories

def check_rules(message: Message, chat_antilink_status, chat_rules):
    violations = []
    
    if chat_antilink_status and message.has_link: 
        violations.append("لینک")
    
    if rules_config["forward"] and hasattr(message, 'is_forward') and message.is_forward:
        violations.append("فوروارد")
    
    if chat_rules.get("anti_mention") and message.text and "@" in message.text:
        violations.append("منشن")
    
    if chat_rules.get("anti_ad") and message.text:
        text_lower = message.text.lower()
        for pattern in ad_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append("تبلیغ")
                break
    
    if chat_rules.get("anti_curse") and message.text:
        text_lower = message.text.lower()
        curse_words = load_curse_words()
        for word in curse_words:
            if word.lower() in text_lower:
                violations.append("فحش")
                break
    
    if chat_rules.get("anti_hung") and message.text:
        for pattern in hung_patterns:
            if re.search(pattern, message.text):
                violations.append("کد هنگی")
                break
    
    if chat_rules.get("anti_emoji") and message.text:
        for emoji in emoji_list:
            if emoji in message.text:
                violations.append("ایموجی ممنوع")
                break
    
    if message.text and filtered_words:
        text_lower = message.text.lower()
        for word in filtered_words:
            if word.lower() in text_lower:
                violations.append("محتوی نامناسب")
                break
    
    if chat_rules.get("anti_edit") and hasattr(message, 'is_edited') and message.is_edited:
        violations.append("ویرایش پیام")
    
    if rules_config.get("anti_flood") and message.text and message.text.count(".") >= 40:
        violations.append("کد هنگی")
    
    if chat_rules.get("gif") and hasattr(message, 'is_gif') and message.is_gif:
        violations.append("گیف")
    
    if rules_config["mention"] and message.is_mention: 
        violations.append("منشن")
    if rules_config["metadata"] and message.has_metadata: 
        violations.append("متادیتا")
    
    return violations

async def send_channel_reminder():
    while True:
        await asyncio.sleep(12 * 3600)
        
        try:
            all_chats = await get_all_chats()
            reminder_text = f"📢 لطفاً از کانال ما دیدن کنید و عضو شوید ❤️\n{CHANNEL_LINK}"
            
            for chat_id in all_chats:
                try:
                    await bot.send_message(chat_id, reminder_text)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Failed to send reminder to {chat_id}: {e}")
                    
        except Exception as e:
            print(f"Error in send_channel_reminder: {e}")

def build_stats_buttons(groups, users, total):
    return InlineBuilder()\
        .row(
            InlineBuilder().button_simple("1", "تعداد گروه‌ها"),
            InlineBuilder().button_simple("2", f"{groups}")
        )\
        .row(
            InlineBuilder().button_simple("1", "تعداد کاربران"),
            InlineBuilder().button_simple("2", f"{users}")
        )\
        .row(
            InlineBuilder().button_simple("1", "🗂️ کل چت‌ها"),
            InlineBuilder().button_simple("2", f"{total}")
        )\
        .build()

def build_admin_panel():
    return (
        ChatKeypadBuilder()
        .row(
            ChatKeypadBuilder().button(id="stats", text="📊 آمار ربات")
        )
        .row(
            ChatKeypadBuilder().button(id="broadcast_text", text="📝 ارسال همگانی"),
            ChatKeypadBuilder().button(id="broadcast_fwd", text="➡️ فروارد همگانی")
        )
        .row(
            ChatKeypadBuilder().button(id="close_panel", text="❌ بستن پنل")
        )
        .build()
    )

async def ask_speaker_local(text):
    cleaned_text = text.strip().lower()
    
    for question in speaker_db.keys():
        if cleaned_text == question.lower():
            return random.choice(speaker_db[question])
    
    return None

async def process_message_with_rules(bot: Robot, message: Message, chat_id, chat_rules, antilink_status):
    if await is_group_creator(chat_id, message.sender_id):
        return False
    
    bot_status_chat = await get_bot_status(chat_id)
    if bot_status_chat == "off":
        return False
    
    violations = check_rules(message, antilink_status, chat_rules)
    
    if violations:
        texts = "، ".join(violations)
        
        delete_after = 60
        if "کد هنگی" in texts:
            delete_after = 600
        
        try:
            await bot.delete_message(chat_id, message.message_id)
            
            warning_msg = await message.reply(
                f"⛔ اخطار\n"
                f"> [کاربر]({message.sender_id}) عزیز\n"
                f"📌 دلیل: {texts}\n"
                f"⚠️ پیام شما به دلیل نقض قوانین حذف شد.",
                delete_after=delete_after
            )
            
        except Exception as e:
            print(f"Error processing rule violation: {e}")
        
        return True
    return False

async def send_request(url, method="GET", **kwargs):
    async with httpx.AsyncClient() as client:
        if method.upper() == "GET":
            response = await client.get(url, **kwargs)
        else:
            response = await client.post(url, **kwargs)
        return response.json()

async def ask_ai_question(question: str):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{AI_API_URL}?text={question}",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("result", "پاسخی دریافت نشد.")
            else:
                return f"خطا در ارتباط با هوش مصنوعی. کد خطا: {response.status_code}"
    
    except httpx.TimeoutException:
        return "⏳ زمان انتظار برای پاسخ هوش مصنوعی به پایان رسید."
    except Exception as e:
        return f"خطا در دریافت پاسخ: {str(e)}"

def font(text_font: str):
    fonts = """ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ
    ⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵
    🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿
    aɮᴄɖɛʄɢɦɨʝҡʟʍռօքզʀstʊʋաxʏʐ
    ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ
    ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ
    αвcɔεғɢнıנκʟмпσρǫяƨтυνшхчz
    αβcძεδĝhιjκlʍπøρφƦՏ†uνωχψz
    αвc∂єƒgнιנкℓмησρqяѕтυνωχуz
    αв¢đefgħıנκłмиøρqяšтυνωχчz
    ąҍçժҽƒցհìʝҟӀʍղօքզɾʂէմѵա×վՀ
    คც८ძ૯Բ૭ҺɿʆқՆɱՈ૦ƿҩՐς੮υ౮ω૪עઽ
    αßςdεƒghïյκﾚmη⊕pΩrš†u∀ωxψz
    ค๒ς๔єŦɠђเןкl๓ภ๏թợгรtยvฬxץz
    ﾑ乃ζÐ乇ｷǤんﾉﾌズﾚᄊ刀Ծｱq尺ㄎｲЦЏЩﾒﾘ乙
    αβcδεŦĝhιjκlʍπøρφƦ$†uυωχψz
    ձъƈժεբցհﻨյĸlოռօթզгรէսνա×ყ۲
    Λɓ¢Ɗ£ƒɢɦĩʝҚŁɱהøṖҨŔŞŦŪƔωЖ¥Ẑ
    ΛБϾÐΞŦghłjКŁmЛФpǪЯstuvШЖЏz
    ɐbɔdǝɟɓɥıſʞๅɯnodbɹsʇnʌʍxʎz
    ɒbɔbɘʇϱнiįʞlмиoppяƨтυvwxγz
    闩乃亡刀乇下彑⼶工亅片乚从力口ㄗ디尺丂亇凵ム山乂丫乙
    ልፎርሏይፑፘዘፗጋኸረጠበዐየዓዩናፐሀህሠጰሃጓ
    ᎪᏴᏟᎠᎬᎰᏀᎻᏆᎫᏦᏞᎷNᏫᏢᎧᏒᏚᎢᏌᏙᎳᏡᎩᏃ
    ѦƁҀΔΣӺǤⴼΪɈҞⱢᛖƝѲƤǪƦƼϮƲѴѠӼƳⱫ
    ꁲꃃꊐꅓꂅꊰꁅꍬꀤꀭꂪ꒒ꂵꊮꏿꉣꐎꉸꌗꉢꏵꏝꅐꉧꌦꏣ
    ᗩᗷᑕᗪᕮᖴᘜᕼᖗᒍᖉᒐᗰᘉᗝᑭᘯᖇᔕᙢᑌᕓᗯ᙭ᖻᘔ
    ᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦᏞᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃ
    ᎯᏰℭⅅ℮ℱᏩℋᏐℐӃℒℳℕᎾ⅌ℚℜᏕƬƲᏉᏔℵᎽℤ
    ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ
    𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉
    ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵟᴿˢᵀᵁⱽᵂˣᵞᶻ
    ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ
    🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉
    🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨z
    🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉
    𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙
    𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁
    𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍
    𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭
    𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹
    𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕿𝕴𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕵𝖀𝖁𝖂𝖃𝚼𝖅
    𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌ𝔗ℑ𝔎𝔏m𝔑𝔒𝔓𝔔ℜ𝔖𝔍𝔘𝔙𝔚𝔛ϒℨ
    𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕
    𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏i𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡
    ᚣᛒᛈᚦᛊᚫᛩᚻᛨᛇᛕᚳᚥᚺθᚹԚᚱᛢᛠᛘᛉᚠᚷᚴZ
    𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩
    𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴z
    𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ
    𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾p𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈z
    Æþ©ÐEFζĦЇ¿ズᄂMÑΘǷØҐŠτυ¥wχyշ
    Æß©Ð£FGHÏJK|MÑØþQ®§TµVWX¥Z
    ÂßĈÐЄŦǤĦĪʖҚĿ♏ИØPҨR$ƚЦVЩX￥Ẕ
    ค๖¢໓ēfງhiวkl๓ຖ໐p๑rŞtนงຟxฯຊ
    ΔƁCDΣFGHIJƘLΜ∏ΘƤႳΓЅƬƱƲШЖΨZ
    ΛßƇDƐFƓĤĪĴҠĿMИ♡ṖҨŔSƬƱѴѠӾYZ
    ѦѣСԀЄҒԌӉіјҠLӍИѺթҨГՏҬԱѴЩӼүՀ
    𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗i𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡s𝓣𝓤𝓥𝓦𝓧𝓨𝓩
    ﾑ乃ζÐ乇ｷǤんﾉﾌズﾚᄊ刀ԾｱQ尺ㄎｲЦЏЩﾒﾘ乙""".splitlines()
    chosen_font = random.choice(fonts).strip()
    a_z = "abcdefghijklmnopqrstuvwxyz"
    translate = str.maketrans(a_z, chosen_font)
    return text_font.lower().translate(translate)

async def get_currency_prices():
    try:
        async with httpx.AsyncClient() as cl:
            requ=await cl.get("https://arzdigital.com/coins/",headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(requ.text, 'html.parser')
        j={"bitcoin":"بیت کوین","ethereum":"اتریوم","xrp":"رپیل","tether":"تتر","bnb":"بایننس","solana":"سولنا","tron":"ترون"}
        m={}
        pn=["toman","dollar"]
        for key,item in j.items():
            for u in pn:
                span_tag = soup.find('span', class_=f'pulser-{u}-{key}').text
                if not item in m:
                    m[item]={}
                m[item][u]=span_tag
        tt="""قیمت 7 ارز دیجیتال به صورت لحظه ای 💱
"""
        for key,item in m.items():
            tt+=f"""
 - {key} -
🇮🇷 تومان : {item['toman']}
🇺🇸 دلار : {item['dollar']}
"""
        return tt
    except:
        return "❌ خطا در دریافت اطلاعات ارز دیجیتال"

async def get_time_info():
    try:
        response = await send_request("https://api.parssource.ir/date/", timeout=10)
        dat = response['result']
        date = f"""تاریخ : {dat['jalaly']['date']} 📆
ساعت : {dat['jalaly']['time']} 🕒
روز هفته : {dat['jalaly']['dey_week']} 📆
ماه : {dat['jalaly']['mont']} 📅
حیوان سال : {dat['jalaly']['animal']} 🐾
فصل : {dat['jalaly']['season']} 🌳
مناسبت امروز : {dat['jalaly']['mon']} 🌇
مانده به عید : {str(dat['jalaly']['eid'])} 🌍
تاریخ میلادی : {dat['Gregorian']['date']} 📆
ساعت میلادی : {dat['Gregorian']['time']} 🕒"""
        return date
    except:
        return "❌ خطا در دریافت اطلاعات زمان"

bot.start_save_message()
@bot.on_message()
async def save_message(bot, message): 
    return

@bot.on_message(filters.text_equals("بن"))
async def info(bot: Robot, message: Message):
    data = await bot.get_message(message.chat_id, message.reply_to_message_id)
    if await bot.ban_member_chat(chat_id=message.chat_id,user_id=data['sender_id']):
        await message.reply(f"> [کاربر]({data['sender_id']}) مورد نظر از گروه اخراج شد")

@bot.on_message(filters.text_equals("آن بن"))
async def info2(bot: Robot, message: Message):
    data = await bot.get_message(message.chat_id, message.reply_to_message_id)
    if await bot.unban_chat_member(chat_id=message.chat_id, user_id=data['sender_id']):
        await message.reply(f"[کاربر]({data['sender_id']}) مورد نظر از لیست بن خارج شد")

@bot.on_message_group()
async def group_handler(bot: Robot, message: Message):
    chat_id = message.chat_id
    user_id = message.sender_id
    text = message.text or ""

    await save_member(chat_id, user_id)
    await increase_message_count(chat_id, user_id)
    
    # اضافه کردن تجربه برای هر پیام
    level_up = await add_user_xp(chat_id, user_id, 2)
    if level_up.get("level_up"):
        await message.reply(f"🎉 **تبریک!**\n[کاربر]({user_id}) به سطح **{level_up['new_level']}** رسید! ✨")

    antilink_status = await get_antilink_status(chat_id)
    chat_rules = {
        "anti_ad": await get_rule_status(chat_id, "anti_ad"),
        "anti_curse": await get_rule_status(chat_id, "anti_curse"),
        "anti_hung": await get_rule_status(chat_id, "anti_hung"),
        "anti_emoji": await get_rule_status(chat_id, "anti_emoji"),
        "anti_edit": await get_rule_status(chat_id, "anti_edit"),
        "anti_mention": await get_rule_status(chat_id, "anti_mention"),
        "gif": await get_rule_status(chat_id, "gif")
    }

    if await is_group_locked(chat_id) and not await is_assistant_admin(chat_id, user_id):
        await message.delete()
        return

    if await is_muted(chat_id, user_id):
        await message.delete()
        return

    if await process_message_with_rules(bot, message, chat_id, chat_rules, antilink_status):
        return

    if await is_first_message(chat_id):
        await save_chat_id(chat_id, "group")
        group_name = await bot.get_name(chat_id)
        
        await set_speaker_status(chat_id, "on")
        await set_antilink_status(chat_id, "on")
        await init_rules(chat_id)
        
        # تنظیمات پیش‌فرض برای قابلیت‌های جدید
        await set_group_setting(chat_id, "auto_delete", False)
        await set_group_setting(chat_id, "auto_delete_time", 10)
        await set_group_setting(chat_id, "speaker_personal", False)
        await set_group_setting(chat_id, "speaker_polite", False)
        await set_group_setting(chat_id, "speaker_rude", False)
        await set_group_setting(chat_id, "speaker_default", True)
        await set_group_setting(chat_id, "speaker_learning", True)
        await set_group_setting(chat_id, "calculator_enabled", True)
        
        group_info = {
            "name": group_name,
            "id": chat_id,
            "creator": user_id,
            "date": datetime.now().isoformat()
        }
        await save_active_group(chat_id, json.dumps(group_info))
        
        await message.reply(
            f"🌟 با عرض سلام خدمت تمامی اعضای گروه\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🏷 نام گروه : {group_name}\n"
            f"🤖 ربات سخنگو با موفقیت در این گروه فعال شد!\n"
            f"💬 حالت سخنگو : 🟢 روشن\n"
            f"🔗 ضد لینک : 🟢 روشن\n"
            f"📢 ضد تبلیغ : 🟢 روشن\n"
            f"🤬 ضد فحش : 🟢 روشن\n"
            f"⚠️ ضد هنگی : 🟢 روشن\n"
            f"😀 ضد ایموجی : 🟢 روشن\n"
            f"✏️ ضد ویرایش : 🟢 روشن\n"
            f"📛 ضد منشن : 🟢 روشن\n"
            f"🎬 ضد گیف : 🟢 روشن\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👑 برای فعال‌سازی کامل، دستور «فعال» را ارسال کنید تا مالک گروه تنظیم شود.\n"
            f"👨‍💻 سازنده ربات: @Amcyxba"
        )
        return

    if text in ["فعال", "تنظیم ادمین", "مالک"]:
        creator = await get_group_creator(chat_id)
        if creator is None:
            await set_group_creator(chat_id, user_id)
            await award_user_badge(user_id, chat_id, "group_founder")  # اهدای نشان
            await message.reply("✅ شما به عنوان سازنده تنظیم شدید.\n🏅 نشان «بنیانگذار گروه» به شما اهدا شد!")
        elif str(creator) == str(user_id):
            await message.reply("✅ شما قبلاً سازنده هستید.")
        else:
            await message.reply("❌ فقط سازنده فعلی می‌تواند تغییر دهد.")
        return

    # ==================== دستورات جدید مالک و ویژه ====================
    if await is_group_creator(chat_id, user_id):
        if text == "انتقال مالکیت" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                new_owner = data['sender_id']
                await set_group_creator(chat_id, new_owner)
                await message.reply(f"✅ مالکیت گروه به [کاربر]({new_owner}) منتقل شد.")
            return
        
        elif text == "ویژه" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                await add_special_user(chat_id, target_id, user_id)
                await message.reply(f"✅ [کاربر]({target_id}) به لیست ویژه اضافه شد.")
            return
        
        elif text == "حذف ویژه" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                await remove_special_user(chat_id, target_id)
                await message.reply(f"✅ [کاربر]({target_id}) از لیست ویژه حذف شد.")
            return

    # ==================== دستورات ویژه و مالک ====================
    if await is_group_creator(chat_id, user_id) or await is_special_user(chat_id, user_id):
        
        if text == "معاف" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                await add_exempt_user(chat_id, target_id, user_id)
                await message.reply(f"✅ [کاربر]({target_id}) معاف شد.")
            return
        
        elif text == "حذف معاف" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                await remove_exempt_user(chat_id, target_id)
                await message.reply(f"✅ [کاربر]({target_id}) از لیست معاف حذف شد.")
            return
        
        elif text.startswith("تنظیم لقب") and message.reply_to_message_id:
            parts = text.split(" ", 2)
            if len(parts) >= 3:
                nickname = parts[2]
                data = await bot.get_message(chat_id, message.reply_to_message_id)
                if data and 'sender_id' in data:
                    target_id = data['sender_id']
                    await set_user_profile(chat_id, target_id, "لقب", nickname, user_id)
                    await message.reply(f"✅ لقب «{nickname}» برای [کاربر]({target_id}) تنظیم شد.")
            return
        
        elif text.startswith("تنظیم اصل") and message.reply_to_message_id:
            parts = text.split(" ", 2)
            if len(parts) >= 3:
                origin = parts[2]
                data = await bot.get_message(chat_id, message.reply_to_message_id)
                if data and 'sender_id' in data:
                    target_id = data['sender_id']
                    await set_user_profile(chat_id, target_id, "اصل", origin, user_id)
                    await message.reply(f"✅ اصل «{origin}» برای [کاربر]({target_id}) تنظیم شد.")
            return
        
        elif text == "حذف لقب" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                await set_user_profile(chat_id, target_id, "لقب", "", user_id)
                await message.reply(f"✅ لقب [کاربر]({target_id}) حذف شد.")
            return
        
        elif text == "حذف اصل" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                await set_user_profile(chat_id, target_id, "اصل", "", user_id)
                await message.reply(f"✅ اصل [کاربر]({target_id}) حذف شد.")
            return
        
        elif text == "حذف قوانین":
            await set_group_rules(chat_id, "")
            await message.reply("✅ قوانین گروه پاک شد.")
            return
        
        elif text == "تعداد اخطار" and message.reply_to_message_id:
            data = await bot.get_message(chat_id, message.reply_to_message_id)
            if data and 'sender_id' in data:
                target_id = data['sender_id']
                warn_count = await get_user_warn_count(chat_id, target_id)
                await message.reply(f"⚠️ تعداد اخطارهای [کاربر]({target_id}): {warn_count}")
            return
        
        elif text == "لیست قفل":
            locks = await get_all_locks(chat_id)
            ban_locks = await get_all_ban_locks(chat_id)
            warn_locks = await get_all_warn_locks(chat_id)
            
            lock_names = {
                "ایدی": "ایدی", "لینک": "لینک", "متن": "متن", "استیکر": "استیکر",
                "ویس": "ویس", "ویدیو": "ویدیو", "آهنگ": "آهنگ", "عکس": "عکس",
                "گیف": "گیف", "فایل": "فایل", "کلمات انگلیسی": "کلمات انگلیسی",
                "ریپلای": "ریپلای", "فوروارد": "فوروارد", "ادیت": "ادیت",
                "ایموجی": "ایموجی", "کد": "کد", "فحش": "فحش", "نظرسنجی": "نظرسنجی",
                "عدد": "عدد", "شماره موبایل": "شماره موبایل", "هشتگ": "هشتگ", "گروه": "گروه"
            }
            
            text_msg = "🔒 **لیست قفل‌ها** 🔒\n━━━━━━━━━━━━━━━\n"
            text_msg += "**🔐 قفل‌های عادی:**\n"
            for lock_fa, lock_en in lock_names.items():
                status = "🔓 باز" if not locks.get(lock_en, False) else "🔒 قفل"
                text_msg += f"• {lock_fa}: {status}\n"
            
            text_msg += "\n**⛔ قفل‌های بن:**\n"
            for lock_fa, lock_en in lock_names.items():
                status = "🔓 باز" if not ban_locks.get(lock_en, False) else "⛔ بن"
                text_msg += f"• {lock_fa}: {status}\n"
            
            text_msg += "\n**⚠️ قفل‌های اخطار:**\n"
            for lock_fa, lock_en in lock_names.items():
                status = "🔓 باز" if not warn_locks.get(lock_en, False) else "⚠️ اخطار"
                text_msg += f"• {lock_fa}: {status}\n"
            
            await message.reply(text_msg)
            return

    # ==================== دستورات قفل / باز برای همه ====================
    if await is_assistant_admin(chat_id, user_id):
        # قفل‌های عادی
        lock_pattern = r"^([^\s]+) (قفل|باز)$"
        match = re.match(lock_pattern, text)
        if match:
            lock_type, action = match.groups()
            is_lock = action == "قفل"
            
            # نگاشت نام فارسی به انگلیسی
            lock_map = {
                "ایدی": "ایدی", "لینک": "لینک", "متن": "متن", "استیکر": "استیکر",
                "ویس": "ویس", "ویدیو": "ویدیو", "آهنگ": "آهنگ", "عکس": "عکس",
                "گیف": "گیف", "فایل": "فایل", "کلمات انگلیسی": "کلمات انگلیسی",
                "ریپلای": "ریپلای", "فوروارد": "فوروارد", "ادیت": "ادیت",
                "ایموجی": "ایموجی", "کد": "کد", "فحش": "فحش", "نظرسنجی": "نظرسنجی",
                "عدد": "عدد", "شماره موبایل": "شماره موبایل", "هشتگ": "هشتگ", "گروه": "گروه"
            }
            
            if lock_type in lock_map:
                await set_lock(chat_id, lock_map[lock_type], is_lock)
                status_text = "قفل" if is_lock else "باز"
                await message.reply(f"✅ {lock_type} {status_text} شد.")
            return
        
        # قفل‌های بن
        ban_lock_pattern = r"^بن ([^\s]+) (قفل|باز)$"
        match = re.match(ban_lock_pattern, text)
        if match:
            lock_type, action = match.groups()
            is_lock = action == "قفل"
            
            lock_map = {
                "ایدی": "ایدی", "لینک": "لینک", "متن": "متن", "استیکر": "استیکر",
                "ویس": "ویس", "ویدیو": "ویدیو", "آهنگ": "آهنگ", "عکس": "عکس",
                "گیف": "گیف", "فایل": "فایل", "کلمات انگلیسی": "کلمات الإنجليزية",
                "ریپلای": "ریپلای", "فوروارد": "فوروارد", "ادیت": "ادیت",
                "ایموجی": "ایموجی", "کد": "کد", "فحش": "فحش", "نظرسنجی": "نظرسنجی",
                "عدد": "عدد", "شماره موبایل": "شماره موبایل", "هشتگ": "هشتگ", "گروه": "گروه"
            }
            
            if lock_type in lock_map:
                await set_ban_lock(chat_id, lock_map[lock_type], is_lock)
                status_text = "قفل" if is_lock else "باز"
                await message.reply(f"✅ بن {lock_type} {status_text} شد.")
            return
        
        # قفل‌های اخطار
        warn_lock_pattern = r"^اخطار ([^\s]+) (قفل|باز)$"
        match = re.match(warn_lock_pattern, text)
        if match:
            lock_type, action = match.groups()
            is_lock = action == "قفل"
            
            lock_map = {
                "ایدی": "ایدی", "لینک": "لینک", "متن": "متن", "استیکر": "استیکر",
                "ویس": "ویس", "ویدیو": "ویدیو", "آهنگ": "آهنگ", "عکس": "عکس",
                "گیف": "گیف", "فایل": "فایل", "کلمات انگلیسی": "کلمات الإنجليزية",
                "ریپلای": "ریپلای", "فوروارد": "فوروارد", "ادیت": "ادیت",
                "ایموجی": "ایموجی", "کد": "کد", "فحش": "فحش", "نظرسنجی": "نظرسنجی",
                "عدد": "عدد", "شماره موبایل": "شماره موبایل", "هشتگ": "هشتگ", "گروه": "گروه"
            }
            
            if lock_type in lock_map:
                await set_warn_lock(chat_id, lock_map[lock_type], is_lock)
                status_text = "قفل" if is_lock else "باز"
                await message.reply(f"✅ اخطار {lock_type} {status_text} شد.")
            return

    # ==================== ادامه دستورات قبلی ====================
    if await is_assistant_admin(chat_id, user_id):
        if text.startswith("حذف") and len(text.split()) == 2:
            try:
                num_messages = int(text.split()[1])
                if num_messages <= 0:
                    await message.reply("❗ تعداد پیام‌ها باید بزرگتر از صفر باشد.")
                    return
                
                messages_to_delete = await get_recent_messages(chat_id, num_messages)
                if not messages_to_delete:
                    await message.reply("❗ هیچ پیام قابل حذف در این گروه وجود ندارد.")
                    return
                
                for msg_id in messages_to_delete:
                    try:
                        await bot.delete_message(chat_id, msg_id)
                    except:
                        pass
                
                await delete_messages_from_db(chat_id, messages_to_delete)
                
                auto_del = await get_group_setting(chat_id, "auto_delete", False)
                if auto_del:
                    await message.reply(f"✅ {len(messages_to_delete)} پیام اخیر حذف شد.", delete_after=5)
                else:
                    await message.reply(f"✅ {len(messages_to_delete)} پیام اخیر حذف شد.")
            except ValueError:
                pass
        
        elif text.startswith("قفل گروه"):
            parts = text.split()
            if len(parts) >= 3 and parts[2].isdigit():
                lock_duration = int(parts[2])
                await toggle_group_lock(chat_id, 1)
                await message.reply(f"✅ گروه به مدت {lock_duration} ثانیه قفل شد.")
                await asyncio.sleep(lock_duration)
                await toggle_group_lock(chat_id, 0)
                await message.reply("✅ مدت زمان قفل گروه تمام شد. قفل گروه باز شد.")
            else:
                await message.reply("❗ لطفا مدت زمان قفل گروه را به درستی وارد کنید.")
            return
        
        elif text == "باز کردن قفل گروه":
            await toggle_group_lock(chat_id, 0)
            await message.reply("✅ قفل گروه باز شد. پیام‌ها قابل ارسال هستند.")
            return
        
        elif text == "افزودن ادمین":
            if not message.reply_to_message_id:
                await message.reply("❗ روی پیام کاربر ریپلای کن")
                return
            
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if info and 'sender_id' in info:
                target_id = info['sender_id']
                await add_assistant_admin(chat_id, target_id)
                await award_user_badge(target_id, chat_id, "group_admin")  # اهدای نشان
                await message.reply(f"✅ [کاربر]({target_id}) ادمین کمکی شد\n🏅 نشان «مدیر گروه» دریافت کرد!")
            return
        
        elif text == "حذف ادمین":
            if not message.reply_to_message_id:
                await message.reply("❗ روی پیام کاربر ریپلای کن")
                return
            
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if info and 'sender_id' in info:
                target_id = info['sender_id']
                await remove_assistant_admin(chat_id, target_id)
                await message.reply(f"❌ [کاربر]({target_id}) از ادمینی حذف شد")
            return
        
        elif text == "لیست ادمین":
            rows = await _execute_db_query("SELECT user_id FROM assistant_admins WHERE chat_id=?", (chat_id,), fetch_all=True)
            if not rows:
                await message.reply("❗ ادمین کمکی وجود ندارد")
                return
            
            text_msg = "🛡️ **ادمین‌های کمکی :**\n\n"
            for (uid,) in rows:
                text_msg += f">- [کاربر]({uid})\n"
            await message.reply(text_msg)
            return
        
        elif text == "آمار" and message.reply_to_message_id:
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if info and 'sender_id' in info:
                target_id = info['sender_id']
                count = await get_user_stats(chat_id, target_id)
                level_info = await get_user_level_info(chat_id, target_id)
                badges = await get_user_badges(target_id, chat_id)
                warn_count = await get_user_warn_count(chat_id, target_id)
                
                badges_text = "، ".join([b[0] for b in badges[:5]]) if badges else "بدون نشان"
                profile = await get_user_full_profile(chat_id, target_id)
                nickname = profile.get("لقب", "ندارد")
                origin = profile.get("اصل", "ندارد")
                
                await message.reply(
                    f"📊 **آمار کامل کاربر**\n\n"
                    f"👤 [کاربر]({target_id})\n"
                    f"🏷 لقب: {nickname}\n"
                    f"🌍 اصل: {origin}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💬 تعداد پیام‌ها: **{count}**\n"
                    f"⭐ سطح: **{level_info['level']}** (تجربه: {level_info['xp']}/{level_info['xp_needed']})\n"
                    f"🏅 نشان‌ها: {badges_text}\n"
                    f"⚠️ اخطارها: **{warn_count}**\n"
                    f"📈 پیشرفت: {level_info['progress']}%"
                )
            return
        
        elif text == "آمار گروه":
            group_name = await bot.get_name(chat_id)
            now = jdatetime.datetime.now()
            time_text = now.strftime("%Y/%m/%d | %H:%M")
            
            stats = await get_group_stats(chat_id)
            leaderboard = await get_group_leaderboard(chat_id, 5)
            
            rows = await _execute_db_query(
                "SELECT user_id, message_count FROM user_stats WHERE chat_id=? ORDER BY message_count DESC LIMIT 3", 
                (chat_id,), fetch_all=True
            )
            
            medals = ["🥇", "🥈", "🥉"]
            top_text = "\n".join(
                f">{medals[i]} [کاربر]({uid}) — {count} پیام" if i < len(medals) else f"> [کاربر]({uid}) — {count} پیام"
                for i, (uid, count) in enumerate(rows or [])
            )
            
            leaderboard_text = "\n".join(
                f"{i+1}. [کاربر]({uid}) - سطح {level} ({xp} XP)"
                for i, (uid, level, xp) in enumerate(leaderboard)
            ) if leaderboard else "هنوز کاربری وجود ندارد"
            
            await message.reply(
                f"📊 **گزارش آماری — \"{group_name}\"**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🕒 **زمان :** {time_text}\n"
                f"👥 **اعضای فعال :** {stats['active_users']}\n"
                f"🛡️ **مدیران :** {stats['admin_count']}\n"
                f"💬 **کل پیام‌ها :** {stats['total_messages']}\n"
                f"🔇 **کاربران سکوت‌شده :** {stats['muted_users']}\n\n"
                f"🏆 **مشارکت‌کنندگان برتر :**\n{top_text if top_text else 'هنوز کاربری وجود ندارد'}\n\n"
                f"⭐ **برترین سطوح :**\n{leaderboard_text}"
            )
            return
        
        elif text.startswith("تگ"):
            members = await get_members(chat_id)
            if not members:
                await message.reply("❗ کاربری ذخیره نشده")
                return
            
            parts = text.split()
            chunk_size = 20
            tag_type = "random"
            
            if len(parts) >= 2:
                if parts[1].isdigit():
                    chunk_size = int(parts[1])
                elif parts[1] == "همه":
                    chunk_size = len(members)
                elif parts[1] == "ادمین":
                    admins = await _execute_db_query("SELECT user_id FROM assistant_admins WHERE chat_id=?", (chat_id,), fetch_all=True)
                    members = [a[0] for a in admins] if admins else []
                    chunk_size = len(members)
                    tag_type = "admins"
                elif parts[1] == "فعال":
                    active = await _execute_db_query(
                        "SELECT user_id FROM user_stats WHERE chat_id=? ORDER BY message_count DESC LIMIT 20",
                        (chat_id,), fetch_all=True
                    )
                    members = [a[0] for a in active] if active else []
                    chunk_size = len(members)
                    tag_type = "active"
                elif parts[1] == "ویژه":
                    members = special_users[chat_id].copy()
                    chunk_size = len(members)
                    tag_type = "special"
                elif parts[1] == "معاف":
                    members = exempt_users[chat_id].copy()
                    chunk_size = len(members)
                    tag_type = "exempt"
            
            if not members:
                await message.reply("❗ کاربری برای تگ وجود ندارد")
                return
            
            if len(members) <= chunk_size:
                chunks = [members]
            else:
                chunks = [members[i:i + chunk_size] for i in range(0, len(members), chunk_size)]
            
            for group in chunks:
                if tag_type == "admins":
                    text_msg = "👑 **تگ مدیران:**\n" + " , ".join(f"[ادمین]({uid})" for uid in group)
                elif tag_type == "active":
                    text_msg = "🔥 **تگ کاربران فعال:**\n" + " , ".join(f"[فعال]({uid})" for uid in group)
                elif tag_type == "special":
                    text_msg = "⭐ **تگ کاربران ویژه:**\n" + " , ".join(f"[ویژه]({uid})" for uid in group)
                elif tag_type == "exempt":
                    text_msg = "🛡️ **تگ کاربران معاف:**\n" + " , ".join(f"[معاف]({uid})" for uid in group)
                else:
                    text_msg = " , ".join(f"[{random_tag_text()}]({uid})" for uid in group)
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=text_msg,
                    reply_to_message_id=message.message_id
                )
                await asyncio.sleep(0.5)
            return
        
        elif text.startswith("سکوت"):
            if not message.reply_to_message_id:
                await message.reply("❗ روی پیام کاربر ریپلای کن")
                return
            
            try:
                parts = text.split()
                if len(parts) == 2:
                    try:
                        mute_duration = int(parts[1])
                        is_permanent = 0
                    except ValueError:
                        if parts[1].lower() == "دائمی":
                            mute_duration = 0
                            is_permanent = 1
                        else:
                            await message.reply("❗ لطفا مدت زمان سکوت یا 'دائمی' را وارد کنید.")
                            return
                elif len(parts) == 3 and parts[1].lower() == "دائمی":
                    mute_duration = 0
                    is_permanent = 1
                else:
                    await message.reply("❗ لطفا مدت زمان سکوت یا 'دائمی' را وارد کنید.")
                    return

                info = await bot.get_message(chat_id, message.reply_to_message_id)
                if not info or 'sender_id' not in info:
                    await message.reply("❗ نتوانستم اطلاعات کاربر را دریافت کنم.")
                    return
                
                target_id = info['sender_id']
                
                await mute_user_db(chat_id, target_id, mute_duration, is_permanent)
                
                if is_permanent:
                    await message.reply(f"✅ [کاربر]({target_id}) برای همیشه سکوت شد.")
                else:
                    await message.reply(f"✅ [کاربر]({target_id}) برای {mute_duration} ثانیه سکوت شد.")
                
                if mute_duration > 0:
                    await asyncio.sleep(mute_duration)
                    await unmute_user_db(chat_id, target_id)
                    await message.reply(f"⏳ مدت زمان سکوت برای کاربر [کاربر]({target_id}) تمام شد.")
                    
            except ValueError as e:
                print(e)
                await message.reply("❗ لطفا مدت زمان سکوت را به درستی وارد کنید.")
            return
        
        elif text == "پاکسازی سکوت":
            await _execute_db_query("DELETE FROM mutes WHERE chat_id=?", (chat_id,))
            await message.reply("✅ **لیست سکوت با موفقیت پاک شد**")
            return
        
        elif text == "حذف سکوت":
            if not message.reply_to_message_id:
                await message.reply("❗ **لطفاً روی پیام کاربر ریپلای کنید تا سکوت آن حذف شود**")
                return
            
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if not info or 'sender_id' not in info:
                await message.reply("❗ نتوانستم اطلاعات کاربر را دریافت کنم.")
                return
            
            target_id = info['sender_id']
            await unmute_user_db(chat_id, target_id)
            await message.reply(f"🔊 سکوت [کاربر]({target_id}) برداشته شد")
            return
        
        elif text == "لیست سکوت":
            muted_users = await get_muted_users(chat_id)
            if not muted_users:
                await message.reply("✅ لیست سکوت خالی است")
                return
            
            response_text = "🔇 **کاربران سکوت‌شده** :\n\n" + "\n".join(f">- [کاربر]({uid})" for uid in muted_users)
            await message.reply(response_text)
            return
        
        elif text == "وضعیت":
            rules_status = []
            for rule, fa in rules_fa.items():
                if rule in chat_rules:
                    status = "✓ فعال" if chat_rules[rule] else "× غیرفعال"
                    rules_status.append(f"> {fa}: {status}")
            
            state_text = "\n".join(rules_status)
            await message.reply(
                f"📊 **وضعیت قوانین گروه** --{await bot.get_name(chat_id)}-- :\n\n{state_text}\n\n"
                f"⚙️ برای تغییر وضعیت قوانین، از دستورهای مرتبط استفاده کنید."
            )
            return
        
        elif text == "خاموش همه":
            for rule in chat_rules.keys():
                await set_rule_status(chat_id, rule, "off")
            await message.reply("🔕 همه قوانین خاموش شدند")
            return
        
        elif text == "روشن همه":
            for rule in chat_rules.keys():
                await set_rule_status(chat_id, rule, "on")
            await message.reply("🔔 همه قوانین روشن شدند")
            return
        
        # ========== دستورات جدید مدیریتی ==========
        elif text == "اخطار" and message.reply_to_message_id:
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if info and 'sender_id' in info:
                target_id = info['sender_id']
                warn_count = await add_user_warn(chat_id, target_id, user_id)
                
                warn_settings = await get_warn_settings(chat_id)
                max_warns = warn_settings["max_warns"]
                
                await message.reply(f"⚠️ [کاربر]({target_id}) اخطار دریافت کرد!\n📌 تعداد اخطارها: {warn_count}/{max_warns}")
                
                # اعمال خودکار جریمه
                if warn_count >= max_warns:
                    action = warn_settings["action"]
                    duration = warn_settings["duration"]
                    
                    if action == "mute":
                        await mute_user_db(chat_id, target_id, duration)
                        await message.reply(f"🔇 کاربر به دلیل {max_warns} اخطار، {duration} ثانیه سکوت شد!")
                    elif action == "kick":
                        await bot.ban_member_chat(chat_id, target_id)
                        await bot.unban_chat_member(chat_id, target_id)
                        await message.reply(f"👢 کاربر به دلیل {max_warns} اخطار از گروه اخراج شد!")
                    elif action == "ban":
                        await bot.ban_member_chat(chat_id, target_id)
                        await message.reply(f"⛔ کاربر به دلیل {max_warns} اخطار برای همیشه بن شد!")
                
                await remove_user_warn(chat_id, target_id, warn_count - 1)  # ریست اخطار
            return
        
        elif text == "کاهش اخطار" and message.reply_to_message_id:
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if info and 'sender_id' in info:
                target_id = info['sender_id']
                new_count = await remove_user_warn(chat_id, target_id)
                await message.reply(f"✅ یک اخطار از [کاربر]({target_id}) کاهش یافت. اخطارهای فعلی: {new_count}")
            return
        
        elif text == "پاکسازی اخطار" and message.reply_to_message_id:
            info = await bot.get_message(chat_id, message.reply_to_message_id)
            if info and 'sender_id' in info:
                target_id = info['sender_id']
                await _execute_db_query("DELETE FROM group_warns WHERE chat_id=? AND user_id=?", (chat_id, target_id))
                if target_id in user_warns[chat_id]:
                    del user_warns[chat_id][target_id]
                await message.reply(f"✅ تمام اخطارهای [کاربر]({target_id}) پاک شد!")
            return
        
        elif text.startswith("تنظیم اخطار"):
            parts = text.split()
            if len(parts) >= 4:
                try:
                    max_warns = int(parts[2])
                    action = parts[3]
                    duration = int(parts[4]) if len(parts) > 4 else 3600
                    
                    if action not in ["mute", "kick", "ban", "none"]:
                        await message.reply("❌ نوع جریمه باید mute, kick, ban یا none باشد")
                        return
                    
                    await set_warn_settings(chat_id, max_warns, action, duration)
                    await message.reply(f"✅ تنظیمات اخطار بروزرسانی شد:\nحداکثر اخطار: {max_warns}\nجریمه: {action}\nمدت: {duration} ثانیه")
                except:
                    await message.reply("❌ فرمت صحیح: تنظیم اخطار [تعداد] [mute/kick/ban/none] [مدت]")
            else:
                await message.reply("❌ فرمت صحیح: تنظیم اخطار [تعداد] [mute/kick/ban/none] [مدت]")
            return
        
        elif text.startswith("پیام خوشامد"):
            welcome_text = text.replace("پیام خوشامد", "").strip()
            if welcome_text:
                await set_welcome_message(chat_id, welcome_text)
                await message.reply(f"✅ پیام خوش‌آمدگویی تنظیم شد:\n{welcome_text}")
            else:
                current = await get_welcome_message(chat_id)
                if current:
                    await message.reply(f"📝 پیام خوش‌آمدگویی فعلی:\n{current}")
                else:
                    await message.reply("❌ پیام خوش‌آمدگویی تنظیم نشده است.\nبرای تنظیم: پیام خوشامد [متن]")
            return
        
        elif text.startswith("پیام خداحافظ"):
            goodbye_text = text.replace("پیام خداحافظ", "").strip()
            if goodbye_text:
                await set_goodbye_message(chat_id, goodbye_text)
                await message.reply(f"✅ پیام خداحافظی تنظیم شد:\n{goodbye_text}")
            else:
                current = await get_goodbye_message(chat_id)
                if current:
                    await message.reply(f"📝 پیام خداحافظی فعلی:\n{current}")
                else:
                    await message.reply("❌ پیام خداحافظی تنظیم نشده است.")
            return
        
        elif text == "کپچا روشن":
            await set_captcha_settings(chat_id, True, "medium", 300)
            await message.reply("✅ سیستم کپچا روشن شد. کاربران جدید باید کپچا را حل کنند.")
            return
        
        elif text == "کپچا خاموش":
            await set_captcha_settings(chat_id, False)
            await message.reply("❌ سیستم کپچا خاموش شد.")
            return
        
        elif text.startswith("دستور جدید"):
            # فرمت: دستور جدید !cmd پاسخ
            parts = text.split(" ", 3)
            if len(parts) >= 4:
                cmd = parts[2]
                response = parts[3]
                await add_custom_command(chat_id, cmd, response, user_id)
                await message.reply(f"✅ دستور جدید «{cmd}» با موفقیت اضافه شد!")
            else:
                await message.reply("❌ فرمت صحیح: دستور جدید !cmd پاسخ")
            return
        
        elif text.startswith("حذف دستور"):
            parts = text.split(" ")
            if len(parts) >= 3:
                cmd = parts[2]
                await remove_custom_command(chat_id, cmd)
                await message.reply(f"✅ دستور «{cmd}» حذف شد!")
            else:
                await message.reply("❌ فرمت صحیح: حذف دستور !cmd")
            return
        
        elif text == "لیست دستورات":
            commands = await list_custom_commands(chat_id)
            if commands:
                msg = "📋 **دستورات سفارشی گروه:**\n\n"
                for cmd, resp, creator in commands[:20]:
                    msg += f"🔹 {cmd}: {resp[:30]}...\n"
                await message.reply(msg)
            else:
                await message.reply("📭 هیچ دستور سفارشی‌ای تعریف نشده است.")
            return
        
        # ========== دستورات جدید تنظیمات ==========
        elif text == "حذف خودکار روشن":
            await set_group_setting(chat_id, "auto_delete", True)
            await message.reply("✅ حذف خودکار روشن شد.")
            return
        
        elif text == "حذف خودکار خاموش":
            await set_group_setting(chat_id, "auto_delete", False)
            await message.reply("❌ حذف خودکار خاموش شد.")
            return
        
        elif text.startswith("حذف خودکار زمان"):
            parts = text.split()
            if len(parts) >= 4 and parts[3].isdigit():
                time_sec = int(parts[3])
                await set_group_setting(chat_id, "auto_delete_time", time_sec)
                await message.reply(f"✅ زمان حذف خودکار به {time_sec} ثانیه تنظیم شد.")
            return
        
        elif text == "سخنگو شخصی روشن":
            await set_group_setting(chat_id, "speaker_personal", True)
            await message.reply("✅ سخنگوی شخصی روشن شد.")
            return
        
        elif text == "سخنگو شخصی خاموش":
            await set_group_setting(chat_id, "speaker_personal", False)
            await message.reply("❌ سخنگوی شخصی خاموش شد.")
            return
        
        elif text == "سخنگو باادب روشن":
            await set_group_setting(chat_id, "speaker_polite", True)
            await set_group_setting(chat_id, "speaker_rude", False)
            await message.reply("✅ سخنگوی باادب روشن شد.")
            return
        
        elif text == "سخنگو بی ادب روشن":
            await set_group_setting(chat_id, "speaker_rude", True)
            await set_group_setting(chat_id, "speaker_polite", False)
            await message.reply("✅ سخنگوی بی ادب روشن شد.")
            return
        
        elif text == "سخنگو پیشفرض روشن":
            await set_group_setting(chat_id, "speaker_default", True)
            await message.reply("✅ سخنگوی پیشفرض روشن شد.")
            return
        
        elif text == "سخنگو پیشفرض خاموش":
            await set_group_setting(chat_id, "speaker_default", False)
            await message.reply("❌ سخنگوی پیشفرض خاموش شد.")
            return
        
        elif text == "یادگیری فعال":
            await set_group_setting(chat_id, "speaker_learning", True)
            await message.reply("✅ یادگیری فعال شد.")
            return
        
        elif text == "یادگیری غیرفعال":
            await set_group_setting(chat_id, "speaker_learning", False)
            await message.reply("❌ یادگیری غیرفعال شد.")
            return
        
        elif text == "ماشین حساب فعال":
            await set_group_setting(chat_id, "calculator_enabled", True)
            await message.reply("✅ ماشین حساب فعال شد.")
            return
        
        elif text == "ماشین حساب غیرفعال":
            await set_group_setting(chat_id, "calculator_enabled", False)
            await message.reply("❌ ماشین حساب غیرفعال شد.")
            return
        
        for rule, fa in rules_fa.items():
            if text in [fa, f"قفل {fa}"]:
                current_status = chat_rules.get(rule)
                new_status = "off" if current_status else "on"
                await set_rule_status(chat_id, rule, new_status)
                status_text = "فعال" if new_status == "on" else "غیرفعال"
                await message.reply(f"✔️ وضعیت **{fa}** {status_text} شد")
                return

    # ========== دستورات جدید کاربران عادی ==========
    if text == "مقام":
        if await is_group_creator(chat_id, user_id):
            rank = "👑 مالک گروه"
        elif await is_special_user(chat_id, user_id):
            rank = "⭐ کاربر ویژه"
        elif await is_assistant_admin(chat_id, user_id):
            rank = "🛡️ ادمین کمکی"
        elif await is_exempt_user(chat_id, user_id):
            rank = "🛡️ کاربر معاف"
        else:
            rank = "👤 کاربر عادی"
        
        await message.reply(f"📌 **مقام شما در گروه:**\n{rank}")
        return
    
    if text == "آمارم":
        count = await get_user_stats(chat_id, user_id)
        level_info = await get_user_level_info(chat_id, user_id)
        badges = await get_user_badges(user_id, chat_id)
        warn_count = await get_user_warn_count(chat_id, user_id)
        
        badges_text = "، ".join([b[0] for b in badges[:5]]) if badges else "بدون نشان"
        profile = await get_user_full_profile(chat_id, user_id)
        nickname = profile.get("لقب", "ندارد")
        origin = profile.get("اصل", "ندارد")
        
        await message.reply(
            f"📊 **آمار شما**\n\n"
            f"👤 [کاربر]({user_id})\n"
            f"🏷 لقب: {nickname}\n"
            f"🌍 اصل: {origin}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💬 تعداد پیام‌ها: **{count}**\n"
            f"⭐ سطح: **{level_info['level']}** (تجربه: {level_info['xp']}/{level_info['xp_needed']})\n"
            f"🏅 نشان‌ها: {badges_text}\n"
            f"⚠️ اخطارها: **{warn_count}**\n"
            f"📈 پیشرفت: {level_info['progress']}%"
        )
        return
    
    if text == "آمار" and not message.reply_to_message_id:
        count = await get_user_stats(chat_id, user_id)
        level_info = await get_user_level_info(chat_id, user_id)
        await message.reply(
            f"📊 **آمار شما**\n\n"
            f"👤 [کاربر]({user_id})\n"
            f"💬 تعداد پیام‌ها: **{count}**\n"
            f"⭐ سطح: **{level_info['level']}** (تجربه: {level_info['xp']}/{level_info['xp_needed']})\n"
            f"📈 پیشرفت: {level_info['progress']}%"
        )
        return
    
    if text == "اصلم" or text == "اصل":
        profile = await get_user_full_profile(chat_id, user_id)
        origin = profile.get("اصل", "تنظیم نشده")
        await message.reply(f"🌍 **اصل شما:** {origin}")
        return
    
    if text == "لقبم" or text == "لقب":
        profile = await get_user_full_profile(chat_id, user_id)
        nickname = profile.get("لقب", "تنظیم نشده")
        await message.reply(f"🏷 **لقب شما:** {nickname}")
        return
    
    if text.startswith("تنظیم نام") and not message.reply_to_message_id:
        name = text.replace("تنظیم نام", "").strip()
        if name:
            await set_user_profile(chat_id, user_id, "نام", name, user_id)
            await message.reply(f"✅ نام شما به «{name}» تنظیم شد.")
        return
    
    if text.startswith("تنظیم فامیلی") and not message.reply_to_message_id:
        lastname = text.replace("تنظیم فامیلی", "").strip()
        if lastname:
            await set_user_profile(chat_id, user_id, "فامیلی", lastname, user_id)
            await message.reply(f"✅ فامیلی شما به «{lastname}» تنظیم شد.")
        return
    
    if text.startswith("تنظیم لقب") and not message.reply_to_message_id:
        nickname = text.replace("تنظیم لقب", "").strip()
        if nickname:
            await set_user_profile(chat_id, user_id, "لقب", nickname, user_id)
            await message.reply(f"✅ لقب شما به «{nickname}» تنظیم شد.")
        return
    
    if text.startswith("تنظیم اصل") and not message.reply_to_message_id:
        origin = text.replace("تنظیم اصل", "").strip()
        if origin:
            await set_user_profile(chat_id, user_id, "اصل", origin, user_id)
            await message.reply(f"✅ اصل شما به «{origin}» تنظیم شد.")
        return
    
    if text == "جوک":
        await message.reply(f"😂 **جوک:**\n{await get_random_joke()}")
        return
    
    if text == "بیو":
        try:
            response = requests.get("https://api.codebazan.ir/bio")
            if response.status_code == 200:
                await message.reply(response.text)
            else:
                await message.reply("⚠️ خطایی در دریافت بیوگرافی رخ داد.")
        except:
            await message.reply("⚠️ خطا در دریافت بیوگرافی")
        return
    
    if text == "ارز":
        try:
            response = requests.get("http://api.codebazan.ir/arz/?type=arz")
            if response.status_code == 200:
                currencies = response.json()["Result"]
                text_msg = "💰 **نرخ ارزهای رایج امروز** 💰\n\n"
                for idx, currency in enumerate(currencies[:10], start=1):
                    text_msg += f"🔹 [{idx}]: {currency['name']} = {currency['price']} تومان\n"
                text_msg += "\n📌 آخرین نرخ ارزها - بروز رسانی لحظه‌ای! ⏳"
            else:
                text_msg = "خطا در دریافت نرخ ارز"
        except:
            text_msg = "⚠️ خطا در دریافت نرخ ارز"
        await message.reply(text_msg)
        return
    
    if text == "ارز طلا":
        gold_price = await get_gold_price()
        await message.reply(gold_price)
        return
    
    if text == "بورس":
        stock_info = await get_stock()
        await message.reply(stock_info)
        return
    
    if text == "دانستنی":
        await message.reply(f"🤔 **آیا می‌دانستید؟**\n{await get_random_fact()}")
        return
    
    if text == "داستان":
        stories = load_stories()
        if stories:
            story = random.choice(stories)
            await message.reply(f"📚 **داستان کوتاه:**\n\n{story}")
        return
    
    if text == "سعدی":
        # اشعار سعدی
        poems = [
            "بنی آدم اعضای یکدیگرند / که در آفرینش ز یک گوهرند",
            "چو عضوی به درد آورد روزگار / دگر عضوها را نماند قرار",
            "تو کز محنت دیگران بی غمی / نشاید که نامت نهند آدمی",
            "عاقلان را ادب به جان آید / جاهلان را ادب به تن آید",
            "چو دخلت نیست خرج آهسته تر کن / که می گویند ملاحان سرودی"
        ]
        await message.reply(f"🍃 **شعر از سعدی:**\n\n{random.choice(poems)}")
        return
    
    if text == "فال":
        fortune = await get_random_fortune()
        await message.reply(f"🔮 **فال روزانه شما** 🔮\n━━━━━━━━━━━━━━━\n{fortune}")
        return
    
    if text.startswith("فونت فارسی"):
        txt = text.replace("فونت فارسی", "").strip()
        if txt:
            await message.reply(f"🔤 **فونت فارسی:**\n{txt}")
        return
    
    if text.startswith("فونت انگلیسی"):
        txt = text.replace("فونت انگلیسی", "").strip()
        if txt:
            font_text = font(txt)
            await message.reply(f"🔤 **فونت انگلیسی:**\n{font_text}")
        return
    
    if text.startswith("اوقات شرعی"):
        city = text.replace("اوقات شرعی", "").strip()
        if city:
            prayer_times = await get_prayer_times(city)
            await message.reply(prayer_times)
        else:
            await message.reply("❌ لطفاً نام شهر را وارد کنید.\nمثال: اوقات شرعی تهران")
        return
    
    if text.startswith("هواشناسی"):
        city = text.replace("هواشناسی", "").strip()
        if city:
            weather = await get_weather(city)
            await message.reply(weather)
        else:
            await message.reply("❌ لطفاً نام شهر را وارد کنید.\nمثال: هواشناسی تهران")
        return
    
    if text.startswith("ویس مرد"):
        txt = text.replace("ویس مرد", "").strip()
        if txt:
            voice = await text_to_speech(txt, "مرد")
            await message.reply(voice)
        return
    
    if text.startswith("ویس زن"):
        txt = text.replace("ویس زن", "").strip()
        if txt:
            voice = await text_to_speech(txt, "زن")
            await message.reply(voice)
        return
    
    if text == "افزایش کیفیت" and message.reply_to_message_id:
        # اینجا باید کد افزایش کیفیت عکس قرار گیرد
        await message.reply("🖼 قابلیت افزایش کیفیت تصویر در حال توسعه است")
        return
    
    if text == "گزارشات":
        # نمایش آمار گزارشات
        text_msg = "📊 **گزارشات گروه** 📊\n━━━━━━━━━━━━━━━\n"
        text_msg += f"• پیام‌های متنی: {reports_stats[chat_id].get('text', 0)}\n"
        text_msg += f"• عکس: {reports_stats[chat_id].get('photo', 0)}\n"
        text_msg += f"• ویدیو: {reports_stats[chat_id].get('video', 0)}\n"
        text_msg += f"• استیکر: {reports_stats[chat_id].get('sticker', 0)}\n"
        text_msg += f"• فایل: {reports_stats[chat_id].get('file', 0)}\n"
        text_msg += f"• لینک: {reports_stats[chat_id].get('link', 0)}\n"
        text_msg += f"• فوروارد: {reports_stats[chat_id].get('forward', 0)}"
        await message.reply(text_msg)
        return

    # ========== قابلیت یادگیری پیشرفته ==========
    learning_enabled = await get_group_setting(chat_id, "speaker_learning", True)
    if learning_enabled:
        # بررسی یادگیری با ! (یادگیری)
        if text.startswith("!"):
            parts = text[1:].split("!", 1)
            if len(parts) == 2:
                keyword = parts[0].strip()
                response = parts[1].strip()
                if keyword and response:
                    await add_advanced_learning(chat_id, keyword, response, user_id)
                    await message.reply(f"✅ یاد گرفتم! برای «{keyword}» جواب «{response}» رو ذخیره کردم.")
                    return
            
            # بررسی حذف یادگیری با !!
            elif text.startswith("!!"):
                keyword = text[2:].strip()
                if keyword:
                    await remove_advanced_learning(chat_id, keyword)
                    await message.reply(f"✅ تمام جواب‌های «{keyword}» حذف شد.")
                    return
            
            # بررسی حذف یک جواب خاص با !!
            elif "!!" in text:
                parts = text.split("!!")
                if len(parts) == 2:
                    keyword = parts[0].strip()
                    response = parts[1].strip()
                    if keyword and response:
                        await remove_advanced_learning(chat_id, keyword, response)
                        await message.reply(f"✅ جواب «{response}» برای «{keyword}» حذف شد.")
                        return
        
        # نمایش کلیدواژه‌ها با ! #متن
        elif text.startswith("! #"):
            keyword = text[3:].strip()
            responses = await get_advanced_learning(chat_id, keyword)
            if responses:
                msg = f"📚 **جواب‌های «{keyword}»:**\n\n"
                for i, resp in enumerate(responses, 1):
                    msg += f"{i}. {resp}\n"
                await message.reply(msg)
            else:
                await message.reply(f"📭 هیچ جوابی برای «{keyword}» ذخیره نشده.")
            return
        
        # بررسی پاسخ از یادگیری پیشرفته
        responses = await get_advanced_learning(chat_id, text)
        if responses:
            await message.reply(random.choice(responses))
            return

    # ========== ماشین حساب ==========
    calc_enabled = await get_group_setting(chat_id, "calculator_enabled", True)
    if calc_enabled and re.match(r'^[\d\s\+\-\*\/\%\(\)\.]+$', text.replace(' ', '')):
        result = await calculate_expression(text)
        if result:
            await message.reply(result)
            return

    # ========== دستورات قبلی ==========
    if text == "سطح":
        level_info = await get_user_level_info(chat_id, user_id)
        progress_bar = "▓" * int(level_info['progress'] / 10) + "░" * (10 - int(level_info['progress'] / 10))
        
        await message.reply(
            f"⭐ **اطلاعات سطح شما** ⭐\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 کاربر: [کاربر]({user_id})\n"
            f"🎚️ سطح: **{level_info['level']}**\n"
            f"📊 تجربه: {level_info['xp']}/{level_info['xp_needed']}\n"
            f"📈 پیشرفت: {progress_bar} {level_info['progress']}%\n"
            f"🎯 تجربه مورد نیاز تا سطح بعد: {level_info['xp_remaining']}"
        )
        return
    
    elif text == "نشان‌ها":
        badges = await get_user_badges(user_id, chat_id)
        if badges:
            badge_icons = {
                "group_founder": "👑 بنیانگذار",
                "group_admin": "🛡️ مدیر",
                "level_5": "🥉 برنزی",
                "level_10": "🥈 نقره‌ای",
                "level_20": "🥇 طلایی",
                "level_50": "💎 الماسی"
            }
            
            msg = "🏅 **نشان‌های شما:**\n\n"
            for badge, time in badges:
                badge_name = badge_icons.get(badge, badge)
                date = datetime.fromtimestamp(time).strftime("%Y/%m/%d")
                msg += f"• {badge_name} - دریافت در {date}\n"
            await message.reply(msg)
        else:
            await message.reply("📭 شما هنوز هیچ نشانی دریافت نکرده‌اید!")
        return
    
    elif text == "لیست برترین‌ها":
        leaderboard = await get_group_leaderboard(chat_id, 10)
        if leaderboard:
            msg = "🏆 **برترین‌های گروه** 🏆\n━━━━━━━━━━━━━━━\n"
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            
            for i, (uid, level, xp) in enumerate(leaderboard):
                medal = medals[i] if i < len(medals) else "🔹"
                msg += f"{medal} [کاربر]({uid}) - سطح {level} ({xp} XP)\n"
            
            await message.reply(msg)
        else:
            await message.reply("📭 هنوز کاربری در این گروه فعالیت نکرده است!")
        return
    
    elif text == "بازی ریاضی":
        game = await start_math_game(chat_id, user_id)
        await message.reply(game["question"])
        return
    
    elif text == "بازی کلمات":
        game = await start_word_game(chat_id, user_id)
        await message.reply(game["question"])
        return
    
    elif text == "بازی حدس عدد":
        game = await start_guess_number_game(chat_id, user_id)
        await message.reply(game["question"])
        return
    
    elif text.startswith("جواب "):
        game_id = None
        for gid, game in user_games.items():
            if game["chat_id"] == chat_id and game["user_id"] == user_id:
                game_id = gid
                break
        
        if game_id:
            answer = text[5:].strip()
            success, result = await check_game_answer(game_id, user_id, answer)
            await message.reply(result)
        else:
            await message.reply("❌ شما بازی فعالی ندارید!")
        return
    
    elif text == "فال حافظ":
        fal = await get_hafez_fal()
        await message.reply(f"🍃 **فال حافظ** 🍃\n━━━━━━━━━━━━━━━\n{fal}\n━━━━━━━━━━━━━━━\n✨ الهی به امید تو...")
        return
    
    elif text == "معما":
        riddle = await get_random_riddle()
        await message.reply(riddle)
        return
    
    elif text == "جواب معما":
        answer = await get_riddle_answer(riddle_question)
        if answer:
            await message.reply(answer)
        else:
            await message.reply("❌ معمایی برای جواب دادن وجود ندارد!")
        return
    
    elif text == "لطیفه":
        joke = await get_random_joke()
        await message.reply(f"😂 **لطیفه:**\n{joke}")
        return
    
    elif text == "حقیقت جالب":
        fact = await get_random_fact()
        await message.reply(f"🤔 **آیا می‌دانستید؟**\n{fact}")
        return
    
    elif text == "پیشنهاد فیلم":
        movie = await get_random_movie()
        await message.reply(movie)
        return
    
    elif text == "نکته انگلیسی":
        tip = await get_english_tip()
        await message.reply(tip)
        return
    
    elif text == "سلامتی":
        tip = await get_health_tip()
        await message.reply(f"💚 **نکته سلامتی:**\n{tip}")
        return
    
    elif text == "دعا":
        prayer = await get_random_prayer()
        await message.reply(prayer)
        return
    
    elif text == "حکم شرعی":
        rule = await get_random_islamic_rule()
        await message.reply(rule)
        return
    
    elif text == "جمله فلسفی":
        quote = await get_random_philosophy()
        await message.reply(f"💭 **جمله فلسفی:**\n{quote}")
        return
    
    elif text == "قبله":
        qibla = await get_qibla_direction()
        await message.reply(qibla)
        return
    
    elif text == "رمضان":
        ramadan = await get_ramadan_info()
        await message.reply(ramadan)
        return
    
    elif text.startswith("تست شخصیت "):
        parts = text[12:].strip().split(" ")
        if len(parts) >= 2:
            category = parts[0]
            choice = " ".join(parts[1:])
            result = await get_personality_test(category, choice)
            if result:
                await message.reply(result)
            else:
                await message.reply("❌ تست شخصیت یافت نشد!\nمثال: تست شخصیت رنگ قرمز")
        else:
            await message.reply("❌ فرمت صحیح: تست شخصیت [دسته] [گزینه]\nمثال: تست شخصیت رنگ قرمز")
        return
    
    elif text.startswith("طالع بینی "):
        month = text[11:].strip()
        horoscope = await get_birthday_horoscope(month)
        if horoscope:
            await message.reply(horoscope)
        else:
            await message.reply("❌ ماه وارد شده صحیح نیست!\nمثال: طالع بینی فروردین")
        return
    
    elif text.startswith("سن "):
        date_str = text[4:].strip()
        try:
            parts = date_str.split("/")
            if len(parts) == 3:
                age_info = await calculate_age(parts[0], parts[1], parts[2])
                if age_info:
                    await message.reply(
                        f"🎂 **اطلاعات سن شما**\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📅 سن: **{age_info['age']}** سال\n"
                        f"🎈 مانده به تولد بعدی: **{age_info['days_to_birthday']}** روز\n"
                        f"📆 تاریخ تولد بعدی: {age_info['next_birthday']}"
                    )
                else:
                    await message.reply("❌ تاریخ وارد شده نامعتبر است!")
            else:
                await message.reply("❌ فرمت صحیح: سن 1370/01/01")
        except:
            await message.reply("❌ فرمت صحیح: سن 1370/01/01")
        return

    elif text == "احادیث":
        all_hadiths = load_hadiths()
        random_hadith = random.choice(all_hadiths)
        await message.reply(f"📖 **حدیث تصادفی:**\n\n{random_hadith}\n\n➡️ برای حدیث دیگر: حدیث")
        return
    
    elif text == "خاطرات":
        all_memories = load_memories()
        random_memory = random.choice(all_memories)
        await message.reply(f"📓 **خاطره:**\n\n{random_memory}")
        return
    
    elif text == "داستان‌ها":
        all_stories = load_stories()
        random_story = random.choice(all_stories)
        await message.reply(f"📚 **داستان کوتاه:**\n\n{random_story}")
        return
    
    elif text == "چالش‌ها":
        challenges = load_challenges()
        random_challenge = random.choice(challenges)
        await message.reply(f"🎯 **چالش امروز:**\n\n{random_challenge}")
        return

    elif text.startswith("+"):
        try:
            question = text[1:].strip()
            
            if not question:
                await message.reply("❌ لطفاً سوال خود را بعد از علامت + وارد کنید.")
                return
            
            processing_msg = await message.reply("🤖 در حال پردازش سوال شما... لطفاً صبر کنید.")
            
            ai_response = await ask_ai_question(question)
            
            try:
                await bot.delete_message(chat_id, processing_msg.message_id)
            except:
                pass
            
            await message.reply(f"🤖 **پاسخ هوش مصنوعی:**\n\n{ai_response}")
        
        except Exception as e:
            await message.reply(f"❌ خطا در ارتباط با هوش مصنوعی: {str(e)}")
        return

    # بررسی دستورات سفارشی
    if text.startswith("!"):
        cmd_response = await get_custom_command(chat_id, text)
        if cmd_response:
            await message.reply(cmd_response)
            return

    if text in ["دستورات", "راهنما", "help"]:
        help_message = ("کانال دستورات: @tfycyvh")
        
        # تقسیم پیام بلند به چند بخش
        if len(help_message) > 4096:
            parts = [help_message[i:i+4096] for i in range(0, len(help_message), 4096)]
            for part in parts:
                await message.reply(part)
        else:
            await message.reply(help_message)
        return

    if text in ["ربات روشن", "ربات خاموش"]:
        if await is_group_creator(chat_id, user_id):
            if text == "ربات روشن":
                await set_bot_status(chat_id, "on")
                await message.reply("✅ ربات در این گروه روشن شد.")
            else:
                await set_bot_status(chat_id, "off")
                await message.reply("❌ ربات در این گروه خاموش شد.")
        else:
            await message.reply("❌ فقط سازنده گروه می‌تواند ربات را روشن/خاموش کند.")
        return

    if text == "قوانین":
        rules_text = await get_group_rules(chat_id)
        await message.reply(f"📜 **قوانین گروه**\n\n{rules_text}")
        return

    if text.startswith("تنظیم قوانین "):
        if await is_assistant_admin(chat_id, user_id):
            rules_text = text.replace("تنظیم قوانین ", "").strip()
            if rules_text:
                await set_group_rules(chat_id, rules_text)
                await message.reply("✅ قوانین گروه با موفقیت تنظیم شد.")
            else:
                await message.reply("❌ لطفاً متن قوانین را وارد کنید.")
        else:
            await message.reply("❌ فقط ادمین‌ها می‌توانند قوانین را تنظیم کنند.")
        return

    if text == "چالش":
        challenges = load_challenges()
        if challenges:
            challenge = random.choice(challenges)
            await message.reply(f"⌯ #CHALECH\n\n🌼«{challenge}»")
        else:
            await message.reply("❌ لیست چالش‌ها خالی است.")
        return

    if text == "حدیث":
        hadiths = load_hadiths()
        if hadiths:
            hadith = random.choice(hadiths)
            await message.reply(f"⌯ #HADITH\n\n🌼«{hadith}»")
        else:
            await message.reply("❌ لیست احادیث خالی است.")
        return

    if text == "خاطره":
        memories = load_memories()
        if memories:
            memory = random.choice(memories)
            await message.reply(f"⌯ #MEMORY\n\n🌼«{memory}»")
        else:
            await message.reply("❌ لیست خاطرات خالی است.")
        return

    if text == "داستان":
        stories = load_stories()
        if stories:
            story = random.choice(stories)
            await message.reply(f"⌯ #STORY\n\n🌼«{story}»")
        else:
            await message.reply("❌ لیست داستان‌ها خالی است.")
        return

    if text == "ساعت":
        time_info = await get_time_info()
        await message.reply(time_info)
        return

    if text.startswith("فونت "):
        text_to_font = text.replace("فونت ", "").strip()
        if text_to_font:
            font_text = font(text_to_font)
            await message.reply(f"🔤 **فونت زیبا:**\n\n{font_text}")
        else:
            await message.reply("❌ لطفاً متنی برای تبدیل به فونت وارد کنید.")
        return

    if text == "ارزدیجیتال":
        currency_prices = await get_currency_prices()
        await message.reply(currency_prices)
        return

    if text.startswith("سرچ "):
        app_name = text.replace("سرچ ", "").strip()
        if app_name:
            try:
                rapp = (await send_request(f"https://hakhamanesh-bot.ir/api/myket/?text={app_name}&lang=fa&count=3"))["data"]
                text_send = f"""🔍 **جستجو برای: {app_name}**
━━━━━━━━━━━━━━━

**🔹 نتیجه اول:** 
📱 نام: {rapp[0]['title']}
🖼 عکس: {rapp[0]['photo']}
⬇️ لینک مستقیم: {rapp[0]['download']}
🔗 لینک مایکت: {rapp[0]['link']}

**🔸 نتیجه دوم:** 
📱 نام: {rapp[1]['title']}
🖼 عکس: {rapp[1]['photo']}
⬇️ لینک مستقیم: {rapp[1]['download']}
🔗 لینک مایکت: {rapp[1]['link']}

**🔹 نتیجه سوم:** 
📱 نام: {rapp[2]['title']}
🖼 عکس: {rapp[2]['photo']}
⬇️ لینک مستقیم: {rapp[2]['download']}
🔗 لینک مایکت: {rapp[2]['link']}"""
                await message.reply(text_send)
            except Exception as e:
                await message.reply(f"❌ خطا در جستجو: {str(e)}")
        else:
            await message.reply("❌ لطفاً نام برنامه را وارد کنید.")
        return

    if text.startswith("تاس "):
        try:
            parts = text.split()
            if len(parts) == 2:
                user_choice = parts[1].lower()
                if user_choice not in ["زوج", "فرد"]:
                    await message.reply("❌ لطفاً «زوج» یا «فرد» را انتخاب کنید.")
                    return
                
                dice_result = random.randint(1, 6)
                is_even = dice_result % 2 == 0
                result_text = "زوج" if is_even else "فرد"
                
                if (user_choice == "زوج" and is_even) or (user_choice == "فرد" and not is_even):
                    await message.reply(f"🎲 تاس افتاد: {dice_result} ({result_text})\n✅ درست حدس زدی! آفرین! 🎉")
                    await add_user_xp(chat_id, user_id, 5)  # جایزه تجربه
                else:
                    await message.reply(f"🎲 تاس افتاد: {dice_result} ({result_text})\n❌ اشتباه حدس زدی! دفعه بعد شانس با توئه! 😉")
            else:
                await message.reply("❌ فرمت: تاس زوج/فرد")
        except Exception as e:
            await message.reply(f"❌ خطا در بازی تاس: {str(e)}")
        return

    if text in ["سازنده", "مالک ربات", "خالق"]:
        await message.reply(f"👨‍💻 سازنده ربات: {CHANNEL_CREATOR}\n📢 کانال: {CHANNEL_LINK}")
        return

    if await is_group_creator(chat_id, user_id):
        if text == "ضد لینک روشن":
            await set_antilink_status(chat_id, "on")
            await message.reply("✅ ضد لینک روشن شد.")
            return
        elif text == "ضد لینک خاموش":
            await set_antilink_status(chat_id, "off")
            await message.reply("❌ ضد لینک خاموش شد.")
            return
        elif text == "سخنگو روشن":
            await set_speaker_status(chat_id, "on")
            await message.reply("✅ سخنگو روشن شد.")
            return
        elif text == "سخنگو خاموش":
            await set_speaker_status(chat_id, "off")
            await message.reply("❌ سخنگو خاموش شد.")
            return
        elif text == "ضد تبلیغ روشن":
            await set_rule_status(chat_id, "anti_ad", "on")
            await message.reply("✅ ضد تبلیغ روشن شد.")
            return
        elif text == "ضد تبلیغ خاموش":
            await set_rule_status(chat_id, "anti_ad", "off")
            await message.reply("❌ ضد تبلیغ خاموش شد.")
            return
        elif text == "ضد فحش روشن":
            await set_rule_status(chat_id, "anti_curse", "on")
            await message.reply("✅ ضد فحش روشن شد.")
            return
        elif text == "ضد فحش خاموش":
            await set_rule_status(chat_id, "anti_curse", "off")
            await message.reply("❌ ضد فحش خاموش شد.")
            return
        elif text == "ضد هنگی روشن":
            await set_rule_status(chat_id, "anti_hung", "on")
            await message.reply("✅ ضد هنگی روشن شد.")
            return
        elif text == "ضد هنگی خاموش":
            await set_rule_status(chat_id, "anti_hung", "off")
            await message.reply("❌ ضد هنگی خاموش شد.")
            return
        elif text == "ضد ایموجی روشن":
            await set_rule_status(chat_id, "anti_emoji", "on")
            await message.reply("✅ ضد ایموجی روشن شد.")
            return
        elif text == "ضد ایموجی خاموش":
            await set_rule_status(chat_id, "anti_emoji", "off")
            await message.reply("❌ ضد ایموجی خاموش شد.")
            return
        elif text == "ضد ویرایش روشن":
            await set_rule_status(chat_id, "anti_edit", "on")
            await message.reply("✅ ضد ویرایش روشن شد.")
            return
        elif text == "ضد ویرایش خاموش":
            await set_rule_status(chat_id, "anti_edit", "off")
            await message.reply("❌ ضد ویرایش خاموش شد.")
            return
        elif text == "ضد منشن روشن":
            await set_rule_status(chat_id, "anti_mention", "on")
            await message.reply("✅ ضد منشن روشن شد.")
            return
        elif text == "ضد منشن خاموش":
            await set_rule_status(chat_id, "anti_mention", "off")
            await message.reply("❌ ضد منشن خاموش شد.")
            return
        elif text == "ضد گیف روشن":
            await set_rule_status(chat_id, "gif", "on")
            await message.reply("✅ ضد گیف روشن شد.")
            return
        elif text == "ضد گیف خاموش":
            await set_rule_status(chat_id, "gif", "off")
            await message.reply("❌ ضد گیف خاموش شد.")
            return
        elif text.startswith("فیلتر "):
            word = text.replace("فیلتر ", "").strip()
            if word:
                filtered_words.add(word.lower())
                await add_filtered_word(chat_id, word)
                await message.reply(f"✅ کلمه '{word}' به لیست فیلتر اضافه شد.")
            else:
                await message.reply("❌ لطفاً یک کلمه برای فیلتر کردن وارد کنید.")
            return
        
        if text.startswith("یادگیری -"):
            parts = text.split("-", 2)
            if len(parts) == 3:
                _, question, answer = parts
                await save_learning(chat_id, question, answer)
                await message.reply(f"🤖 یاد گرفتم که وقتی گفتن '{question.strip()}' بگم '{answer.strip()}'")
            else:
                await message.reply("❌ فرمت درست نیست!\nمثال: یادگیری - سلام - خوبی")
            return
        if text.startswith("حذف یادگیری -"):
            parts = text.split("-", 1)
            if len(parts) == 2:
                _, question = parts
                await delete_learning(chat_id, question)
                await message.reply(f"🗑 یادگیری '{question.strip()}' حذف شد.")
            else:
                await message.reply("❌ فرمت درست نیست!\nمثال: حذف یادگیری - سلام")
            return
        if text == "لیست یادگیری‌ها":
            data = await list_learnings(chat_id)
            if not data:
                await message.reply("🤖 هنوز چیزی یاد نگرفتم!")
            else:
                msg = "📚 **یادگیری‌های فعلی:**\n\n"
                for q, a in data:
                    msg += f"• {q} → {a}\n"
                
                if len(msg) > 4096:
                    parts = [msg[i:i+4096] for i in range(0, len(msg), 4096)]
                    for part in parts:
                        await message.reply(part)
                else:
                    await message.reply(msg)
            return
        if text == "وضعیت گروه":
            creator = await get_group_creator(chat_id)
            creator_name = f"@{creator}" if creator else "⚠️ هنوز تنظیم نشده"
            speaker_status_str = "🟢 روشن" if await get_speaker_status(chat_id) else "🔴 خاموش"
            antilink_status_str = "🟢 روشن" if await get_antilink_status(chat_id) else "🔴 خاموش"
            anti_ad_status = "🟢 روشن" if await get_rule_status(chat_id, "anti_ad") else "🔴 خاموش"
            anti_curse_status = "🟢 روشن" if await get_rule_status(chat_id, "anti_curse") else "🔴 خاموش"
            anti_hung_status = "🟢 روشن" if await get_rule_status(chat_id, "anti_hung") else "🔴 خاموش"
            anti_emoji_status = "🟢 روشن" if await get_rule_status(chat_id, "anti_emoji") else "🔴 خاموش"
            anti_edit_status = "🟢 روشن" if await get_rule_status(chat_id, "anti_edit") else "🔴 خاموش"
            anti_mention_status = "🟢 روشن" if await get_rule_status(chat_id, "anti_mention") else "🔴 خاموش"
            gif_status = "🟢 روشن" if await get_rule_status(chat_id, "gif") else "🔴 خاموش"
            learn_count = len(await list_learnings(chat_id) or [])
            bot_status_chat = await get_bot_status(chat_id)
            bot_status_str = "🟢 روشن" if bot_status_chat == "on" else "🔴 خاموش"
            
            assistant_admins = await _execute_db_query("SELECT COUNT(*) FROM assistant_admins WHERE chat_id=?", (chat_id,), fetch_one=True)
            assistant_count = assistant_admins[0] if assistant_admins else 0
            
            commands_count = len(await list_custom_commands(chat_id))
            
            # آمار تنظیمات جدید
            auto_delete = await get_group_setting(chat_id, "auto_delete", False)
            auto_delete_str = "🟢 روشن" if auto_delete else "🔴 خاموش"
            speaker_personal = await get_group_setting(chat_id, "speaker_personal", False)
            speaker_personal_str = "🟢 روشن" if speaker_personal else "🔴 خاموش"
            learning_enabled = await get_group_setting(chat_id, "speaker_learning", True)
            learning_str = "🟢 روشن" if learning_enabled else "🔴 خاموش"
            calc_enabled = await get_group_setting(chat_id, "calculator_enabled", True)
            calc_str = "🟢 روشن" if calc_enabled else "🔴 خاموش"
            
            await message.reply(
                f"🎯 **وضعیت فعلی گروه** 🤖\n"
                f"━━━━━━━━━━━━━━━\n"
                f"👑 سازنده : {creator_name}\n"
                f"🛡️ ادمین‌های کمکی : {assistant_count} نفر\n"
                f"⭐ کاربران ویژه : {len(special_users[chat_id])}\n"
                f"🛡️ کاربران معاف : {len(exempt_users[chat_id])}\n"
                f"🤖 وضعیت ربات : {bot_status_str}\n"
                f"💬 وضعیت سخنگو : {speaker_status_str}\n"
                f"🔗 وضعیت ضد لینک : {antilink_status_str}\n"
                f"📢 وضعیت ضد تبلیغ : {anti_ad_status}\n"
                f"🤬 وضعیت ضد فحش : {anti_curse_status}\n"
                f"⚠️ وضعیت ضد هنگی : {anti_hung_status}\n"
                f"😀 وضعیت ضد ایموجی : {anti_emoji_status}\n"
                f"✏️ وضعیت ضد ویرایش : {anti_edit_status}\n"
                f"📛 وضعیت ضد منشن : {anti_mention_status}\n"
                f"🎬 وضعیت ضد گیف : {gif_status}\n"
                f"🗑 حذف خودکار : {auto_delete_str}\n"
                f"📝 سخنگوی شخصی : {speaker_personal_str}\n"
                f"🎓 یادگیری : {learning_str}\n"
                f"🧮 ماشین حساب : {calc_str}\n"
                f"📚 تعداد یادگیری‌ها : {learn_count}\n"
                f"⚙️ دستورات سفارشی : {commands_count}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"👨‍💻 سازنده ربات: @DRAGONTIT"
            )
            return

    if text == "دیالوگ":
        try:
            response = requests.get("https://api-free.ir/api2/dialog/")
            if response.status_code == 200:
                dialog = response.json()["result"]
                await message.reply(dialog)
            else:
                await message.reply("⚠️ خطایی در دریافت دیالوگ رخ داد.")
        except Exception as e:
            await message.reply(f"⚠️ خطا در دریافت دیالوگ: {str(e)}")
        return

    elif text == "انگیزشی":
        try:
            response = requests.get("http://haji-api.ir/angizeshi")
            if response.status_code == 200:
                await message.reply(response.text)
            else:
                await message.reply("⚠️ خطایی در دریافت متن انگیزشی رخ داد.")
        except Exception as e:
            await message.reply(f"⚠️ خطا در دریافت متن انگیزشی: {str(e)}")
        return

    elif text == "اخبار":
        try:
            response = requests.get("https://api-free.ir/api2/news.php?token=f9b4a870986af3276d4806b4962799fe")
            if response.status_code == 200:
                news = response.json()
                if news:
                    text_msg = "📰 **اخبار روز:**\n\n"
                    for i, item in enumerate(news[:10], 1):
                        text_msg += f"🔹 [{i}]: {item['title']}\n"
                else:
                    text_msg = "⚠️ هیچ خبری یافت نشد."
            else:
                text_msg = "⚠️ خطا در دریافت اخبار، لطفاً بعداً امتحان کنید."
        except Exception as e:
            text_msg = f"⚠️ خطایی رخ داد: {str(e)}"
        await message.reply(text_msg)
        return

    elif text.startswith("عکس"):
        try:
            topic = text.replace("عکس", "").strip()
            if not topic:
                await message.reply("❌ لطفاً موضوعی برای دریافت عکس وارد کنید!")
                return

            await message.reply("⏳ لطفا منتظر باشید...")
            response = requests.get(f"http://api-free.ir/api/img.php?text={topic}&v=3.5")
            
            if response.status_code == 200:
                images = response.json().get("result", [])
                if images:
                    url = random.choice(images)
                    await message.reply(f"🖼 **عکس با موضوع '{topic}':**\n{url}")
                else:
                    await message.reply("⚠️ هیچ تصویری برای این موضوع پیدا نشد.")
            else:
                await message.reply("⚠️ خطا در دریافت تصویر، لطفاً بعداً امتحان کنید.")
        except Exception as e:
            await message.reply(f"⚠️ خطایی رخ داد: {str(e)}")
        return

    elif text in ["بیوگرافی", "بیو"]:
        try:
            response = requests.get("https://api.codebazan.ir/bio")
            if response.status_code == 200:
                await message.reply(response.text)
            else:
                await message.reply("⚠️ خطایی در دریافت بیوگرافی رخ داد.")
        except Exception as e:
            await message.reply(f"⚠️ خطا در دریافت بیوگرافی: {str(e)}")
        return

    elif text == "وضعیتم":
        try:
            emotions = {
                "هیجان", "عصبانیت", "فعالیت ذهنی", "افسردگی", "انرژی",
                "خشم", "شادی", "اعتماد به نفس", "تنهایی", "استرس",
                "امید", "عشق", "متغیر", "خستگی", "فشار ذهنی",
                "دلزدگی", "خجالت", "نیاز به حمایت", "گیجی", "تردید",
                "نفرت", "انگیزه", "بی‌حوصلگی", "اجتماعی بودن", "کنجکاوی",
                "تمرکز"
            }

            emotions_data = {emotion: random.randint(0, 100) for emotion in emotions}
            kol = sum(emotions_data.values()) / len(emotions_data)

            text_msg = "\n".join([f"🔹 {key}: {value}%" for key, value in emotions_data.items()])
            final_text = f"""🎭 **تحلیل احساسات شما** 🎭
━━━━━━━━━━━━━━━
{text_msg}
━━━━━━━━━━━━━━━
📢 **حالت کلی شما:** {kol:.1f}%
🎭 احساسات متغیرند، فردا بهتر خواهد شد! 💖"""
            
            await message.reply(final_text)
        except Exception as e:
            await message.reply(f"⚠️ خطا در تحلیل احساسات: {str(e)}")
        return

    elif text.startswith('تولد'):
        try:
            t = text.replace("تولد", "").strip()
            if "/" not in t:
                await message.reply("❌ فرمت را اشتباه وارد کردی! نمونه‌ی درست: تولد 1385/10/10")
                return

            t = t.split('/')
            if len(t) != 3 or not all(i.isdigit() for i in t):
                await message.reply("❌ فرمت را اشتباه وارد کردی! نمونه‌ی درست: تولد 1385/10/10")
                return

            years, month, day = t
            response = requests.get(f"https://api.codebazan.ir/birth?year={years}&month={month}&day={day}")
            if response.status_code == 200:
                respect = response.json()["results"]
                text_msg = f"""🎂 **اطلاعات تولد شما** ✨
━━━━━━━━━━━━━━━
📅 سال: {respect["Sal"]}
📆 ماه: {respect["Mah"]}
🗓 روز: {respect["Roz"]}
🎈 روز تولدت: {respect["RozHafte"]}
⏳ تعداد روزهایی که زنده‌ای: {respect["Roze"]} روز
🐾 حیوان سال تولدت: {respect["HeyvanSal"]}
♈ نماد ماه تولدت: {respect["NamadMah"]}
━━━━━━━━━━━━━━━
زندگی یه سفره، از هر لحظه‌اش لذت ببر! 🌟💖"""
            else:
                text_msg = "خطا در دریافت اطلاعات، لطفاً بعداً امتحان کنید."

        except Exception as e:
            text_msg = f"⚠️ خطایی رخ داد: {str(e)}"
        
        await message.reply(text_msg)
        return

    learned = await get_learning(chat_id, text)
    if learned:
        await message.reply(learned)
        return

    if await get_speaker_status(chat_id):
        cleaned_text = text.strip().lower()
        for question in speaker_db.keys():
            if cleaned_text == question.lower():
                await message.reply(random.choice(speaker_db[question]))
                return

@bot.on_message_private()
async def private_handler(bot: Robot, message: Message):
    chat_id = message.chat_id
    try:
        id_button = message.aux_data.button_id
    except:
        id_button = None
    sender_id = message.sender_id
    text = message.text

    if await is_first_message(chat_id):
        await save_chat_id(chat_id, "private")

    if str(chat_id) == str(ADMIN_CHAT_ID):
        if text in ["/panel", "پنل"]:
            await message.reply_keypad(
                "👑 **پنل مدیریت ربات** 👑\n\nلطفا یک گزینه را انتخاب کنید:",
                keypad=build_admin_panel()
            )
            return

        if id_button:
            if id_button == "stats":
                groups, users = await get_counts()
                total = await get_total_count()
                stats_msg = (
                    f"📊 **آمار لحظه‌ای ربات:**\n\n"
                    f"▫️ تعداد گروه‌ها: {groups}\n"
                    f"▫️ تعداد کاربران: {users}\n"
                    f"▪️ کل چت‌های فعال: {total}"
                )
                await message.reply(stats_msg)
                return

            if id_button == "broadcast_text":
                admin_states[sender_id] = "awaiting_broadcast_text"
                await message.reply("📝 لطفا متن پیام همگانی را ارسال کنید. برای لغو /cancel را بفرستید.")
                return

            if id_button == "broadcast_fwd":
                admin_states[sender_id] = "awaiting_broadcast_forward"
                await message.reply("➡️ لطفا پیامی که می‌خواهید برای همه فوروارد شود را اینجا فوروارد کنید. برای لغو /cancel را بفرستید.")
                return

            if id_button == "close_panel":
                await message.reply("✅ پنل با موفقیت بسته شد.")
                await bot.remove_keypad(message.chat_id)
                return

        admin_state = admin_states.get(sender_id)
        if admin_state:
            if text == "/cancel":
                del admin_states[sender_id]
                await message.reply("❌ عملیات لغو شد.")
                return

            if admin_state == "awaiting_broadcast_text":
                del admin_states[sender_id]
                sent_msg = await message.reply("⏳ در حال ارسال پیام همگانی...")
                all_chats = await get_all_chats()
                total_chats = len(all_chats)
                success_count = 0
                for i, c_id in enumerate(all_chats):
                    try:
                        await bot.send_message(c_id, text)
                        success_count += 1
                        if (i + 1) % 10 == 0: 
                            await bot.edit_message_text(chat_id, sent_msg.message_id, f"⏳ در حال ارسال... ({i+1}/{total_chats})")
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        print(f"Failed to send broadcast to {c_id}: {e}")
                await bot.edit_message_text(chat_id, sent_msg.message_id, f"✅ پیام همگانی برای {success_count} از {total_chats} چت با موفقیت ارسال شد.")
                return

            if admin_state == "awaiting_broadcast_forward":
                del admin_states[sender_id]
                sent_msg = await message.reply("⏳ در حال فوروارد همگانی...")
                all_chats = await get_all_chats()
                total_chats = len(all_chats)
                success_count = 0
                for i, c_id in enumerate(all_chats):
                    try:
                        await bot.forward_messages(chat_id, [message.message_id], c_id)
                        success_count += 1
                        if (i + 1) % 10 == 0:
                            await bot.edit_message_text(chat_id, sent_msg.message_id, f"⏳ در حال فوروارد... ({i+1}/{total_chats})")
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        print(f"Failed to forward broadcast to {c_id}: {e}")
                await bot.edit_message_text(chat_id, sent_msg.message_id, f"✅ پیام برای {success_count} از {total_chats} چت با موفقیت فوروارد شد.")
                return

    elif text.startswith("+"):
        try:
            question = text[1:].strip()
            
            if not question:
                await message.reply("❌ لطفاً سوال خود را بعد از علامت + وارد کنید.")
                return
            
            processing_msg = await message.reply("🤖 در حال پردازش سوال شما...")
            
            ai_response = await ask_ai_question(question)
            
            try:
                await bot.delete_message(chat_id, processing_msg.message_id)
            except:
                pass
            
            await message.reply(f"🤖 **پاسخ هوش مصنوعی:**\n\n{ai_response}")
        
        except Exception as e:
            await message.reply(f"❌ خطا در ارتباط با هوش مصنوعی: {str(e)}")
        return

    if text == "/start":
        groups, users = await get_counts()
        total = await get_total_count()
        name = await bot.get_name(chat_id)
        msg = (
            f"سلام **{name}** 👋✨\n"
            "به ربات سخنگو خوش اومدی 🤖💬\n\n"
            "من یه ربات سخنگوی هوشمندم که می‌تونم توی گروه‌هات با بقیه حرف بزنم و حتی ازت یاد بگیرم 😄\n\n"
            "📢 **برای فعال‌سازی من در گروه:**\n"
            "1️⃣ منو به گروهت اضافه کن.\n"
            "2️⃣ دسترسی‌های کامل (ادمین) رو برام فعال کن ✅\n"
            "3️⃣ داخل گروه بنویس: «فعال» تا به عنوان مالک ثبت بشی.\n\n"
            "🤖 **دستور هوش مصنوعی:**\n"
            "+سوال خودت را اینجا بنویس (مثال: +پایتون چیست؟)\n\n"
            "🎮 **بازی‌ها و سرگرمی:**\n"
            "بازی ریاضی - بازی کلمات - بازی حدس عدد\n"
            "فال حافظ - فال روز - معما - لطیفه\n\n"
            "اگه سوالی داشتید داخل گروه بنویس «راهنما» تا راهنمای کامل برات بیاد 💡\n\n"
            f"👨‍💻 **سازنده ربات:** امیر علی ساوهی"
        )
        await message.reply_inline(msg, inline_keypad=build_stats_buttons(groups, users, total))
    else:
        if str(sender_id) != str(ADMIN_CHAT_ID):
            await message.reply("سلام! من رو به گروهت اضافه کن تا بتونم اونجا فعالیت کنم. برای دیدن دستورات /start رو بفرست.\n\n🤖 برای پرسش از هوش مصنوعی: +سوال خودت را بنویس")

async def main():
    reminder_task = asyncio.create_task(send_channel_reminder())
    
    print("🤖 ربات فوق پیشرفته در حال اجرا...")
    print("📊 بیش از 150 دستور مدیریتی و سرگرمی فعال شد!")
    print("👑 ادمین: {ADMIN_CHAT_ID}")
    print("✅ تمام قابلیت‌های درخواستی اضافه شد:")
    print("   • بن لینک قفل/باز و اخطار لینک قفل/باز")
    print("   • دستورات مدیریت گروه پیشرفته (مالک، ویژه، کاربران عادی)")
    print("   • قابلیت یادگیری پیشرفته با ! و !!")
    print("   • سخنگوی باادب و بی ادب")
    print("   • ماشین حساب")
    print("   • حذف خودکار")
    print("   • انتقال مالکیت")
    print("   • و بیش از 50 قابلیت دیگر...")
    
    await bot.run()
    
    reminder_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())