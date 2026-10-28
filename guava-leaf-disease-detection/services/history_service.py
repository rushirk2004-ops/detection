"""
Prediction History and Audit Logging Service
Manages local SQLite persistence for predictions, audit trail, and user privacy settings.
"""
import os
import sqlite3
import datetime
from typing import List, Dict, Any, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STORAGE_DIR = os.path.join(PROJECT_ROOT, "storage")
DB_PATH = os.path.join(STORAGE_DIR, "guava_system.db")

def get_db_connection() -> sqlite3.Connection:
    """Creates directory if needed and returns a connection to the SQLite database."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database schema."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Predictions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                image_name TEXT,
                target_type TEXT NOT NULL,
                model_name TEXT NOT NULL,
                predicted_class TEXT NOT NULL,
                confidence REAL NOT NULL,
                is_uncertain INTEGER NOT NULL,
                latency_ms REAL,
                image_blob BLOB
            )
        """)
        
        # Audit logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT
            )
        """)
        
        # Key-value settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Admin users table for sign-up / registration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        conn.commit()

# Ensure tables exist at module load
init_db()

def record_prediction(
    predicted_class: str,
    confidence: float,
    model_name: str,
    target_type: str = "Leaf",
    image_name: Optional[str] = None,
    is_uncertain: bool = False,
    latency_ms: float = 0.0,
    image_bytes: Optional[bytes] = None,
    opt_in_storage: bool = False
) -> int:
    """
    Saves a prediction record.
    Image bytes are only stored if opt_in_storage is True (Privacy Protection).
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blob_to_save = image_bytes if opt_in_storage else None
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions 
            (timestamp, image_name, target_type, model_name, predicted_class, confidence, is_uncertain, latency_ms, image_blob)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            now_str,
            image_name or "uploaded_sample.jpg",
            target_type,
            model_name,
            predicted_class,
            round(confidence, 4),
            1 if is_uncertain else 0,
            latency_ms,
            blob_to_save
        ))
        conn.commit()
        return cursor.lastrowid

def get_prediction_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Returns recent predictions from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, image_name, target_type, model_name, predicted_class, confidence, is_uncertain, latency_ms,
                   (image_blob IS NOT NULL) AS has_stored_image
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def clear_prediction_history() -> int:
    """Deletes all records from predictions table."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        return cursor.rowcount

def log_audit_event(username: str, action: str, details: str = ""):
    """Records an administrative event to the audit log."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (timestamp, username, action, details)
            VALUES (?, ?, ?, ?)
        """, (now_str, username, action, details))
        conn.commit()

def get_audit_logs(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieves recent audit logs."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, username, action, details
            FROM audit_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_summary_statistics() -> Dict[str, Any]:
    """Computes total counts and disease distribution from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions")
        total_queries = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM predictions WHERE is_uncertain = 1")
        uncertain_queries = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT predicted_class, COUNT(*) as cnt 
            FROM predictions 
            GROUP BY predicted_class
        """)
        distribution = {row["predicted_class"]: row["cnt"] for row in cursor.fetchall()}
        
        return {
            "total_queries": total_queries,
            "uncertain_queries": uncertain_queries,
            "distribution": distribution
        }

def add_admin_user(username: str, password_hash: str, salt: str) -> bool:
    """Adds a newly registered administrator."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO admin_users (username, password_hash, salt, created_at)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, salt, now_str))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # Username already taken

def get_admin_user(username: str) -> Optional[Dict[str, Any]]:
    """Retrieves an admin user record by username."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, salt, created_at FROM admin_users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None
