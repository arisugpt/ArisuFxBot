"""
=============================================================================
ArisuFxBot - Session Manager & Automatic Memory/Disk Cleanup
Created & Developed by: ArisuGpt | Telegram: @hackinjectlab
=============================================================================
"""

import os
import sys
import shutil
import time
import threading
import gc
from typing import Dict, Optional, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import ArisuFxPy
from config import SESSIONS_DIR, SESSION_TIMEOUT_SECONDS

class UserSession:
    def __init__(self, user_id: int):
        self.user_id: int = user_id
        self.session_dir: str = os.path.join(SESSIONS_DIR, str(user_id))
        self.last_active: float = time.time()
        self.env: Optional[Any] = None
        self.original_filename: str = ""
        self.current_filepath: str = ""
        self.state: str = "IDLE"  # IDLE, WAITING_DUMP_PATH_ID, WAITING_DUMP_FILE, etc.
        self.state_data: Dict[str, Any] = {}
        
        # Ensure session folder exists
        os.makedirs(self.session_dir, exist_ok=True)

    def touch(self):
        """Update last active timestamp"""
        self.last_active = time.time()

    def set_file(self, filepath: str, filename: str):
        """Sets the working bundle file and loads it into ArisuFxPy Environment"""
        self.touch()
        self.current_filepath = filepath
        self.original_filename = filename
        
        # Load environment via ArisuFxPy
        self.env = ArisuFxPy.load(filepath)

    def close(self):
        """Cleanly releases loaded environment and removes disk directory"""
        self.env = None
        self.state_data.clear()
        self.state = "IDLE"
        if os.path.exists(self.session_dir):
            try:
                shutil.rmtree(self.session_dir, ignore_errors=True)
            except Exception as e:
                print(f"[-] [CLEANUP ERROR] Failed to delete session dir for user {self.user_id}: {e}")
        gc.collect()


class SessionManager:
    def __init__(self, timeout_seconds: int = SESSION_TIMEOUT_SECONDS):
        self.timeout_seconds: int = timeout_seconds
        self.sessions: Dict[int, UserSession] = {}
        self.lock = threading.Lock()
        
        # Ensure base directory exists
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        
        # Start background cleaner daemon thread
        self.cleaner_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleaner_thread.start()
        print(f"[*] [CLEANUP ENGINE] Auto-cleaner thread started (Timeout: {self.timeout_seconds // 60} minutes)")

    def get_session(self, user_id: int) -> UserSession:
        """Retrieve existing session or create a new one"""
        with self.lock:
            if user_id not in self.sessions:
                self.sessions[user_id] = UserSession(user_id)
            session = self.sessions[user_id]
            session.touch()
            return session

    def reset_session(self, user_id: int):
        """Manually destroy and reset user session"""
        with self.lock:
            if user_id in self.sessions:
                session = self.sessions.pop(user_id)
                session.close()
                print(f"[+] [RESET] User {user_id} session manually reset and purged.")

    def _cleanup_loop(self):
        """Runs continuously in background, purging inactive sessions after timeout"""
        while True:
            time.sleep(30)  # Check every 30 seconds
            now = time.time()
            expired_users = []
            
            with self.lock:
                for uid, sess in self.sessions.items():
                    if (now - sess.last_active) > self.timeout_seconds:
                        expired_users.append(uid)
                
                for uid in expired_users:
                    sess = self.sessions.pop(uid, None)
                    if sess:
                        sess.close()
                        print(f"🧹 [AUTO-CLEANUP] User {uid} session was inactive for {self.timeout_seconds // 60}m. Cleaned from RAM & Disk!")
