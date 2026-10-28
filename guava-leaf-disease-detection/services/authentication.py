"""
Authentication and Authorization Service: Guava Agri-AI Platform
Supports secure password hashing using bcrypt/PBKDF2, multi-farmer registration,
farmer login/session validation, farmer password updates, and administrator authentication.
"""
import hashlib
import os
import time
import secrets
import re
from typing import Tuple, Dict, Any, Optional

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

from services.database import (
    create_farmer, get_farmer_by_username, get_farmer_by_id,
    update_farmer_password
)
from services.history_service import add_admin_user, get_admin_user, log_audit_event

DEFAULT_ADMIN_USER = "admin"
DEFAULT_SALT = "guava_agri_secure_salt_2026"
ADMIN_REGISTRATION_KEY = "GUAVA2026"

# ==================== PASSWORD HASHING UTILITIES ====================

def hash_password(password: str, salt: str = DEFAULT_SALT) -> str:
    """Computes PBKDF2-HMAC-SHA256 hash for administrator accounts and fallback."""
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations=100000
    )
    return key.hex()

DEFAULT_HASH = hash_password("admin@guava2026", DEFAULT_SALT)

def hash_farmer_password(password: str) -> Tuple[str, str]:
    """
    Computes a cryptographic hash for farmer passwords using bcrypt (or PBKDF2 fallback).
    Returns (password_hash, salt).
    """
    if HAS_BCRYPT:
        salt_bytes = bcrypt.gensalt(rounds=12)
        hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt_bytes)
        return hashed_bytes.decode('utf-8'), salt_bytes.decode('utf-8')
    else:
        user_salt = secrets.token_hex(16)
        return hash_password(password, user_salt), user_salt

def verify_farmer_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifies a plain password against the stored bcrypt or PBKDF2 hash."""
    if HAS_BCRYPT and stored_hash.startswith("$2b$"):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        except Exception:
            return False
    # Fallback comparison using PBKDF2
    return hash_password(password, salt) == stored_hash

# ==================== FARMER AUTHENTICATION ====================

def register_farmer_account(
    full_name: str,
    username: str,
    mobile_number: str,
    email: Optional[str],
    village: str,
    taluka: str,
    district: str,
    state: str,
    password: str,
    confirm_password: str
) -> Tuple[bool, str, Optional[str]]:
    """
    Validates farmer registration details and securely registers the farmer.
    Returns (success, message, farmer_id).
    """
    # 1. Field validation
    fn = full_name.strip()
    if not fn or len(fn) < 2:
        return False, "Full Name is required (minimum 2 characters).", None

    un = username.strip().lower()
    if not un or len(un) < 3:
        return False, "Username must be at least 3 characters long.", None
    if not re.match(r"^[a-zA-Z0-9_]+$", un):
        return False, "Username may only contain letters, numbers, and underscores.", None

    mob = mobile_number.strip().replace(" ", "").replace("-", "")
    if not mob or len(mob) < 10 or not mob.isdigit():
        return False, "Valid 10-digit mobile number is required.", None

    if email and email.strip():
        em = email.strip()
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", em):
            return False, "Please enter a valid email address or leave it blank.", None
    else:
        em = None

    vil = village.strip()
    if not vil:
        return False, "Village name is required.", None

    tal = taluka.strip()
    if not tal:
        return False, "Taluka name is required.", None

    dist = district.strip()
    if not dist:
        return False, "District name is required.", None

    st = state.strip()
    if not st:
        return False, "State name is required.", None

    # 2. Password validation
    if not password:
        return False, "Password is required.", None
    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", None
    if password != confirm_password:
        return False, "Password and Confirm Password do not match.", None

    # 3. Check for existing username
    existing = get_farmer_by_username(un)
    if existing:
        return False, f"Username '{un}' is already registered. Please choose another username.", None

    # 4. Hash password and store in SQLite
    pwd_hash, salt = hash_farmer_password(password)
    ok, msg, f_id = create_farmer(
        full_name=fn,
        username=un,
        mobile_number=mob,
        email=em,
        village=vil,
        taluka=tal,
        district=dist,
        state=st,
        password_hash=pwd_hash,
        salt=salt
    )
    if ok:
        log_audit_event(un, "FARMER_REGISTERED", f"New farmer registered with ID: {f_id}")
    return ok, msg, f_id

def authenticate_farmer(username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authenticates a farmer using username and password.
    Returns (success, message, farmer_profile_data).
    """
    un = username.strip().lower()
    if not un or not password:
        return False, "Please enter both username and password.", None

    farmer = get_farmer_by_username(un)
    if not farmer:
        return False, "Farmer account not found with this username.", None

    if farmer.get("account_status") != "active":
        return False, "This farmer account is currently inactive. Please contact system support.", None

    stored_hash = farmer["password_hash"]
    salt = farmer["salt"]

    if verify_farmer_password(password, stored_hash, salt):
        log_audit_event(un, "FARMER_LOGIN_SUCCESS", f"Farmer {farmer['farmer_id']} logged in.")
        # Return sanitized profile (excluding password_hash and salt)
        profile = {k: v for k, v in farmer.items() if k not in ["password_hash", "salt"]}
        return True, "Login successful!", profile
    else:
        log_audit_event(un, "FARMER_LOGIN_FAILED", "Invalid password attempt.")
        return False, "Invalid password. Please check your credentials.", None

def change_farmer_password(
    farmer_id: str,
    current_password: str,
    new_password: str,
    confirm_new_password: str
) -> Tuple[bool, str]:
    """Changes password for an authenticated farmer."""
    farmer = get_farmer_by_id(farmer_id)
    if not farmer:
        return False, "Farmer account not found."

    if not verify_farmer_password(current_password, farmer["password_hash"], farmer["salt"]):
        return False, "Current password is incorrect."

    if not new_password or len(new_password) < 6:
        return False, "New password must be at least 6 characters long."

    if new_password != confirm_new_password:
        return False, "New passwords do not match."

    pwd_hash, salt = hash_farmer_password(new_password)
    ok, msg = update_farmer_password(farmer_id, pwd_hash, salt)
    if ok:
        log_audit_event(farmer["username"], "PASSWORD_CHANGED", f"Farmer {farmer_id} changed password.")
    return ok, msg

# ==================== SESSION HELPERS ====================

def create_farmer_session(farmer_data: Dict[str, Any], timeout_minutes: int = 120) -> Dict[str, Any]:
    """Creates a secure session object for an authenticated farmer."""
    return {
        "authenticated": True,
        "role": "farmer",
        "farmer_id": farmer_data["farmer_id"],
        "username": farmer_data["username"],
        "full_name": farmer_data["full_name"],
        "data": farmer_data,
        "created_at": time.time(),
        "expires_at": time.time() + (timeout_minutes * 60)
    }

def is_farmer_session_valid(session: Optional[Dict[str, Any]]) -> bool:
    """Verifies that the farmer session exists, has not expired, and matches role."""
    if not session or not isinstance(session, dict):
        return False
    if not session.get("authenticated", False):
        return False
    if session.get("role") != "farmer":
        return False
    if time.time() > session.get("expires_at", 0):
        return False
    return True

# ==================== ADMINISTRATOR AUTHENTICATION (BACKWARDS COMPATIBLE) ====================

def register_admin(username: str, password: str, confirm_password: str, access_key: str = "") -> Tuple[bool, str]:
    """Registers an administrator with unique salt hashing."""
    uname = username.strip()
    if not uname or len(uname) < 3:
        return False, "Username must be at least 3 characters long."
    if not uname.isalnum() and "_" not in uname:
        return False, "Username must contain only letters, numbers, or underscores."
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if password != confirm_password:
        return False, "Passwords do not match."
    if access_key.strip() != ADMIN_REGISTRATION_KEY:
        return False, "Invalid Admin Registration Access Key. Contact system administrator for key (Default: GUAVA2026)."

    existing = get_admin_user(uname)
    if existing or uname.lower() == DEFAULT_ADMIN_USER.lower():
        return False, f"Username '{uname}' already exists. Please choose a different username."

    user_salt = secrets.token_hex(16)
    pwd_hash = hash_password(password, user_salt)
    success = add_admin_user(uname, pwd_hash, user_salt)
    if success:
        log_audit_event(uname, "ADMIN_REGISTERED", f"New administrator '{uname}' registered successfully.")
        return True, f"Admin account '{uname}' registered successfully! You can now log in."
    return False, "Failed to create account in database."

def verify_credentials(username: str, password: str) -> Tuple[bool, str]:
    """Verifies administrator credentials against SQLite and fallback super-admin."""
    uname = username.strip()
    if not uname or not password:
        return False, "Username and password are required."

    db_user = get_admin_user(uname)
    if db_user:
        salt = db_user["salt"]
        expected_hash = db_user["password_hash"]
        computed_hash = hash_password(password, salt)
        if computed_hash == expected_hash:
            return True, "Authentication successful."
        return False, "Invalid password."

    if uname == DEFAULT_ADMIN_USER:
        computed_hash = hash_password(password, DEFAULT_SALT)
        if computed_hash == DEFAULT_HASH:
            return True, "Authentication successful."
        return False, "Invalid password."

    return False, "Administrator account not found."

def create_admin_session(username: str, timeout_minutes: int = 60) -> Dict[str, Any]:
    """Creates a secure admin session dictionary."""
    return {
        "authenticated": True,
        "role": "admin",
        "username": username,
        "created_at": time.time(),
        "expires_at": time.time() + (timeout_minutes * 60)
    }

def is_session_valid(session: Optional[Dict[str, Any]]) -> bool:
    """Verifies that an administrator session is valid and not expired."""
    if not session or not isinstance(session, dict):
        return False
    if not session.get("authenticated", False):
        return False
    if session.get("role") != "admin":
        return False
    if time.time() > session.get("expires_at", 0):
        return False
    return True
