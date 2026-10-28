"""
Authentication and Authorization Service
Implements secure password hashing with salt, database user verification, admin registration,
and session management.
"""
import hashlib
import os
import time
import secrets
from typing import Tuple, Dict, Any, Optional

from services.history_service import add_admin_user, get_admin_user, log_audit_event

DEFAULT_ADMIN_USER = "admin"
# Default password: admin@guava2026
DEFAULT_SALT = "guava_agri_secure_salt_2026"
ADMIN_REGISTRATION_KEY = "GUAVA2026"  # Optional security key for admin registration

def hash_password(password: str, salt: str = DEFAULT_SALT) -> str:
    """Computes PBKDF2-HMAC-SHA256 hash for secure storage."""
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations=100000
    )
    return key.hex()

# Precomputed default hash for 'admin@guava2026'
DEFAULT_HASH = hash_password("admin@guava2026", DEFAULT_SALT)

def register_admin(username: str, password: str, confirm_password: str, access_key: str = "") -> Tuple[bool, str]:
    """
    Registers a new administrator with validation and unique salt hashing.
    """
    uname = username.strip()
    if not uname:
        return False, "Username is required."
    if len(uname) < 3:
        return False, "Username must be at least 3 characters long."
    if not uname.isalnum() and "_" not in uname:
        return False, "Username must contain only letters, numbers, or underscores."
        
    if not password:
        return False, "Password is required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if password != confirm_password:
        return False, "Passwords do not match."
        
    # Check registration authorization key
    if access_key.strip() != ADMIN_REGISTRATION_KEY:
        return False, "Invalid Admin Registration Access Key. Contact system administrator for the key (Default: GUAVA2026)."

    # Check if username exists in database
    existing = get_admin_user(uname)
    if existing or uname.lower() == DEFAULT_ADMIN_USER.lower():
        return False, f"Username '{uname}' already exists. Please choose a different username."

    # Generate random cryptographic salt
    user_salt = secrets.token_hex(16)
    pwd_hash = hash_password(password, user_salt)
    
    success = add_admin_user(uname, pwd_hash, user_salt)
    if success:
        log_audit_event(uname, "ADMIN_REGISTERED", f"New administrator '{uname}' registered successfully.")
        return True, f"Admin account '{uname}' registered successfully! You can now log in."
    else:
        return False, "Failed to create account in database. Username may already exist."

def verify_credentials(username: str, password: str) -> Tuple[bool, str]:
    """
    Verifies user credentials against the SQLite database and fallback default admin.
    """
    uname = username.strip()
    if not uname or not password:
        return False, "Username and password are required."

    # 1. Check in database first
    db_user = get_admin_user(uname)
    if db_user:
        salt = db_user["salt"]
        expected_hash = db_user["password_hash"]
        computed_hash = hash_password(password, salt)
        if computed_hash == expected_hash:
            return True, "Authentication successful."
        else:
            return False, "Invalid password."

    # 2. Check default super-admin fallback
    if uname == DEFAULT_ADMIN_USER:
        computed_hash = hash_password(password, DEFAULT_SALT)
        if computed_hash == DEFAULT_HASH:
            return True, "Authentication successful."
        else:
            return False, "Invalid password."

    return False, "Administrator account not found."

def create_admin_session(username: str, timeout_minutes: int = 60) -> Dict[str, Any]:
    """Creates a timestamped admin session dictionary."""
    now = time.time()
    return {
        "authenticated": True,
        "username": username,
        "login_time": now,
        "expires_at": now + (timeout_minutes * 60),
        "role": "System Administrator"
    }

def is_session_valid(session: Optional[Dict[str, Any]]) -> bool:
    """Checks if session exists and is not expired."""
    if not session or not session.get("authenticated", False):
        return False
    if time.time() > session.get("expires_at", 0):
        return False
    return True
