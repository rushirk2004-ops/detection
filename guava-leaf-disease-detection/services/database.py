"""
Database Management Service: Guava Agri-AI Multi-Farmer Platform
Manages SQLite schemas for Farmers, Diagnosis History, Audit Logs, Admin Users,
and System Settings with parameterized queries, indexes, and cascade constraints.
"""
import os
import sqlite3
import datetime
import uuid
import json
from typing import List, Dict, Any, Optional, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STORAGE_DIR = os.path.join(PROJECT_ROOT, "storage")
DB_PATH = os.path.join(STORAGE_DIR, "guava_system.db")
UPLOAD_DIR = os.path.join(STORAGE_DIR, "farmer_uploads")

def get_db_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database with row factory enabled."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_all_tables():
    """Initializes all database tables, foreign keys, and indexes."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Farmers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                mobile_number TEXT NOT NULL,
                email TEXT,
                village TEXT NOT NULL,
                taluka TEXT NOT NULL,
                district TEXT NOT NULL,
                state TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL,
                account_status TEXT DEFAULT 'active'
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_farmers_username ON farmers(username);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_farmers_status ON farmers(account_status);")
        
        # 2. Diagnosis History Table (Associated with farmer_id)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id TEXT NOT NULL,
                target_type TEXT NOT NULL,
                image_path TEXT,
                image_blob BLOB,
                predicted_disease TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                model_name TEXT,
                latency_ms REAL,
                is_uncertain INTEGER DEFAULT 0,
                diagnosis_date TEXT NOT NULL,
                treatment_recommendations TEXT,
                FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_diag_farmer ON diagnosis_history(farmer_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_diag_date ON diagnosis_history(diagnosis_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_diag_disease ON diagnosis_history(predicted_disease);")

        # 3. Legacy Predictions Table (For backwards compatibility with automated tests)
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

        # 4. Audit Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT
            )
        """)

        # 5. Key-Value Settings Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # 6. Admin Users Table
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

# Initialize tables immediately on module load
init_all_tables()

# ==================== FARMER CRUD OPERATIONS ====================

def generate_farmer_id() -> str:
    """Generates a human-readable unique farmer identifier (e.g. FARM-A78B29)."""
    random_hex = uuid.uuid4().hex[:6].upper()
    return f"FARM-{random_hex}"

def create_farmer(
    full_name: str,
    username: str,
    mobile_number: str,
    email: Optional[str],
    village: str,
    taluka: str,
    district: str,
    state: str,
    password_hash: str,
    salt: str
) -> Tuple[bool, str, Optional[str]]:
    """
    Registers a new farmer into the database using parameterized queries.
    Returns (success, message, farmer_id).
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    farmer_id = generate_farmer_id()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO farmers 
                (farmer_id, full_name, username, mobile_number, email, village, taluka, district, state, password_hash, salt, created_at, account_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
            """, (
                farmer_id,
                full_name.strip(),
                username.strip().lower(),
                mobile_number.strip(),
                email.strip() if email else None,
                village.strip(),
                taluka.strip(),
                district.strip(),
                state.strip(),
                password_hash,
                salt,
                now_str
            ))
            conn.commit()
            return True, "Registration successful!", farmer_id
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: farmers.username" in str(e):
                return False, f"Username '{username}' is already registered. Please choose another username.", None
            return False, f"Database error: {str(e)}", None

def get_farmer_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Retrieves a farmer record by username (case-insensitive)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farmers WHERE LOWER(username) = ?", (username.strip().lower(),))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_farmer_by_id(farmer_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a farmer record by farmer_id."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_farmer_profile(
    farmer_id: str,
    full_name: str,
    mobile_number: str,
    email: Optional[str],
    village: str,
    taluka: str,
    district: str,
    state: str
) -> Tuple[bool, str]:
    """Updates profile information for an existing farmer."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE farmers 
            SET full_name = ?, mobile_number = ?, email = ?, village = ?, taluka = ?, district = ?, state = ?
            WHERE farmer_id = ?
        """, (
            full_name.strip(),
            mobile_number.strip(),
            email.strip() if email else None,
            village.strip(),
            taluka.strip(),
            district.strip(),
            state.strip(),
            farmer_id
        ))
        conn.commit()
        if cursor.rowcount > 0:
            return True, "Profile updated successfully!"
        return False, "Farmer account not found."

def update_farmer_password(farmer_id: str, new_password_hash: str, new_salt: str) -> Tuple[bool, str]:
    """Updates password for a farmer."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE farmers 
            SET password_hash = ?, salt = ?
            WHERE farmer_id = ?
        """, (new_password_hash, new_salt, farmer_id))
        conn.commit()
        if cursor.rowcount > 0:
            return True, "Password updated successfully!"
        return False, "Farmer account not found."

def list_all_farmers(search_query: str = "", status_filter: str = "all", limit: int = 100) -> List[Dict[str, Any]]:
    """Returns a list of registered farmers with search and status filtering for admin dashboard."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT farmer_id, full_name, username, mobile_number, email, village, taluka, district, state, created_at, account_status FROM farmers WHERE 1=1"
        params = []

        if search_query.strip():
            sq = f"%{search_query.strip().lower()}%"
            query += " AND (LOWER(full_name) LIKE ? OR LOWER(username) LIKE ? OR mobile_number LIKE ? OR LOWER(village) LIKE ? OR LOWER(district) LIKE ?)"
            params.extend([sq, sq, sq, sq, sq])

        if status_filter in ["active", "inactive"]:
            query += " AND account_status = ?"
            params.append(status_filter)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def count_farmers(status_filter: str = "all") -> int:
    """Returns total count of registered farmers."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if status_filter in ["active", "inactive"]:
            cursor.execute("SELECT COUNT(*) FROM farmers WHERE account_status = ?", (status_filter,))
        else:
            cursor.execute("SELECT COUNT(*) FROM farmers")
        return cursor.fetchone()[0]

def set_farmer_status(farmer_id: str, new_status: str) -> bool:
    """Sets a farmer's account status (active/inactive)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE farmers SET account_status = ? WHERE farmer_id = ?", (new_status, farmer_id))
        conn.commit()
        return cursor.rowcount > 0

# ==================== DIAGNOSIS HISTORY OPERATIONS ====================

def record_farmer_diagnosis(
    farmer_id: str,
    target_type: str,
    predicted_disease: str,
    confidence_score: float,
    model_name: str,
    latency_ms: float = 0.0,
    is_uncertain: bool = False,
    treatment_recommendations: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    filename: Optional[str] = None
) -> int:
    """
    Saves a diagnosis record associated with the authenticated farmer's ID.
    If image_bytes is provided, securely saves to disk and/or blob.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saved_path = None

    if image_bytes:
        ext = os.path.splitext(filename or "sample.jpg")[1] or ".jpg"
        clean_ext = ext if ext.lower() in [".jpg", ".jpeg", ".png"] else ".jpg"
        safe_fname = f"{farmer_id}_{uuid.uuid4().hex[:10]}{clean_ext}"
        saved_path = os.path.join(UPLOAD_DIR, safe_fname)
        try:
            with open(saved_path, "wb") as f:
                f.write(image_bytes)
        except Exception:
            saved_path = None

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO diagnosis_history 
            (farmer_id, target_type, image_path, image_blob, predicted_disease, confidence_score, model_name, latency_ms, is_uncertain, diagnosis_date, treatment_recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            farmer_id,
            target_type,
            saved_path,
            image_bytes if saved_path is None else None,
            predicted_disease,
            round(confidence_score, 4),
            model_name,
            round(latency_ms, 2),
            1 if is_uncertain else 0,
            now_str,
            treatment_recommendations or ""
        ))
        conn.commit()
        diag_id = cursor.lastrowid

        # Also insert into legacy predictions table for backwards compatibility
        cursor.execute("""
            INSERT INTO predictions 
            (timestamp, image_name, target_type, model_name, predicted_class, confidence, is_uncertain, latency_ms, image_blob)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            now_str,
            filename or "foliage_sample.jpg",
            target_type,
            model_name,
            predicted_disease,
            round(confidence_score, 4),
            1 if is_uncertain else 0,
            round(latency_ms, 2),
            image_bytes
        ))
        conn.commit()
        return diag_id

def get_farmer_diagnoses(
    farmer_id: str,
    target_filter: Optional[str] = None,
    disease_filter: Optional[str] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Returns diagnosis history belonging exclusively to the specified farmer_id.
    Server-side authorization guarantee.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM diagnosis_history WHERE farmer_id = ?"
        params = [farmer_id]

        if target_filter and target_filter.lower() != "all":
            query += " AND LOWER(target_type) = ?"
            params.append(target_filter.lower())

        if disease_filter and disease_filter.lower() != "all":
            query += " AND predicted_disease = ?"
            params.append(disease_filter)

        query += " ORDER BY diagnosis_id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_farmer_diagnosis_stats(farmer_id: str) -> Dict[str, Any]:
    """Computes personalized statistics for a specific farmer."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM diagnosis_history WHERE farmer_id = ?", (farmer_id,))
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM diagnosis_history WHERE farmer_id = ? AND predicted_disease = 'Healthy'", (farmer_id,))
        healthy = cursor.fetchone()[0]

        diseased = total - healthy if total >= healthy else 0

        cursor.execute("SELECT diagnosis_date FROM diagnosis_history WHERE farmer_id = ? ORDER BY diagnosis_id DESC LIMIT 1", (farmer_id,))
        last_row = cursor.fetchone()
        last_date = last_row[0] if last_row else None

        cursor.execute("""
            SELECT predicted_disease, COUNT(*) as cnt 
            FROM diagnosis_history 
            WHERE farmer_id = ? 
            GROUP BY predicted_disease
        """, (farmer_id,))
        distribution = {row["predicted_disease"]: row["cnt"] for row in cursor.fetchall()}

        return {
            "total_diagnoses": total,
            "healthy_samples": healthy,
            "disease_cases": diseased,
            "last_diagnosis_date": last_date,
            "distribution": distribution
        }

def delete_farmer_diagnosis(diagnosis_id: int, farmer_id: str) -> bool:
    """
    Deletes a diagnosis record owned by the farmer, removing stored images safely.
    Enforces server-side authorization check (WHERE diagnosis_id = ? AND farmer_id = ?).
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Find file path first
        cursor.execute("SELECT image_path FROM diagnosis_history WHERE diagnosis_id = ? AND farmer_id = ?", (diagnosis_id, farmer_id))
        row = cursor.fetchone()
        if not row:
            return False  # Record not found or unauthorized

        img_path = row["image_path"]
        if img_path and os.path.exists(img_path):
            try:
                # Protection against path traversal: ensure path is within UPLOAD_DIR
                norm_img = os.path.normpath(img_path)
                norm_up = os.path.normpath(UPLOAD_DIR)
                if norm_img.startswith(norm_up):
                    os.remove(img_path)
            except Exception:
                pass

        cursor.execute("DELETE FROM diagnosis_history WHERE diagnosis_id = ? AND farmer_id = ?", (diagnosis_id, farmer_id))
        conn.commit()
        return cursor.rowcount > 0

def get_system_diagnosis_stats() -> Dict[str, Any]:
    """Computes system-wide diagnosis counts for the administrator dashboard."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM diagnosis_history")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM diagnosis_history WHERE predicted_disease = 'Healthy'")
        healthy = cursor.fetchone()[0]

        diseased = total - healthy if total >= healthy else 0

        cursor.execute("""
            SELECT predicted_disease, COUNT(*) as cnt 
            FROM diagnosis_history 
            GROUP BY predicted_disease
        """)
        distribution = {row["predicted_disease"]: row["cnt"] for row in cursor.fetchall()}

        return {
            "total_diagnoses": total,
            "healthy_samples": healthy,
            "disease_cases": diseased,
            "distribution": distribution
        }

def get_all_system_diagnoses(limit: int = 100) -> List[Dict[str, Any]]:
    """Returns system-wide diagnosis history for the admin panel with farmer details."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.diagnosis_id, d.farmer_id, f.full_name, f.village, f.district,
                   d.target_type, d.predicted_disease, d.confidence_score, d.model_name,
                   d.diagnosis_date, d.is_uncertain
            FROM diagnosis_history d
            LEFT JOIN farmers f ON d.farmer_id = f.farmer_id
            ORDER BY d.diagnosis_id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
