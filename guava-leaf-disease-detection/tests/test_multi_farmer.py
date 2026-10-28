"""
Automated Test Suite for Multi-Farmer Account System: Guava Agri-AI Platform
Validates:
1. Multi-farmer registration and unique ID generation
2. Duplicate username prevention
3. Password hashing with bcrypt
4. Farmer authentication (login/logout)
5. Account deactivation / reactivation
6. Diagnosis history association with farmer_id and server-side isolation
7. Unauthorized record deletion prevention
8. Profile update and password change operations
"""
import os
import sys
import uuid
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.authentication import (
    register_farmer_account, authenticate_farmer, change_farmer_password,
    is_farmer_session_valid, create_farmer_session
)
from services.database import (
    get_farmer_by_id, get_farmer_by_username, update_farmer_profile,
    set_farmer_status, record_farmer_diagnosis, get_farmer_diagnoses,
    delete_farmer_diagnosis, get_farmer_diagnosis_stats, list_all_farmers
)

def test_farmer_registration_and_unique_id():
    u_suffix = uuid.uuid4().hex[:6]
    username = f"farmer_{u_suffix}"
    
    ok, msg, farmer_id = register_farmer_account(
        full_name="Ramesh Patil",
        username=username,
        mobile_number="9876543210",
        email=f"{username}@farm.org",
        village="Baramati",
        taluka="Baramati",
        district="Pune",
        state="Maharashtra",
        password="SecurePass@2026",
        confirm_password="SecurePass@2026"
    )
    assert ok is True
    assert farmer_id is not None
    assert farmer_id.startswith("FARM-")

    # Verify farmer exists in database
    farmer = get_farmer_by_id(farmer_id)
    assert farmer is not None
    assert farmer["full_name"] == "Ramesh Patil"
    assert farmer["username"] == username
    assert farmer["password_hash"] != "SecurePass@2026"  # Never plain text

def test_duplicate_username_rejection():
    u_suffix = uuid.uuid4().hex[:6]
    username = f"dup_{u_suffix}"

    ok1, _, fid1 = register_farmer_account(
        full_name="First Farmer",
        username=username,
        mobile_number="9876543211",
        email=None,
        village="Nashik",
        taluka="Nashik",
        district="Nashik",
        state="Maharashtra",
        password="Password123",
        confirm_password="Password123"
    )
    assert ok1 is True

    # Try registering again with exact same username
    ok2, msg2, fid2 = register_farmer_account(
        full_name="Second Farmer",
        username=username,
        mobile_number="9876543212",
        email=None,
        village="Pune",
        taluka="Haveli",
        district="Pune",
        state="Maharashtra",
        password="DifferentPass123",
        confirm_password="DifferentPass123"
    )
    assert ok2 is False
    assert "already registered" in msg2
    assert fid2 is None

def test_farmer_authentication_and_session():
    u_suffix = uuid.uuid4().hex[:6]
    username = f"auth_{u_suffix}"
    pwd = "FarmerSecret@123"

    ok, _, fid = register_farmer_account(
        full_name="Suresh Deshmukh",
        username=username,
        mobile_number="9823456789",
        email=None,
        village="Solapur",
        taluka="North Solapur",
        district="Solapur",
        state="Maharashtra",
        password=pwd,
        confirm_password=pwd
    )
    assert ok is True

    # Valid Login
    auth_ok, auth_msg, profile = authenticate_farmer(username, pwd)
    assert auth_ok is True
    assert profile is not None
    assert profile["farmer_id"] == fid
    assert "password_hash" not in profile  # Sanitized

    # Session Creation
    session = create_farmer_session(profile)
    assert is_farmer_session_valid(session) is True

    # Invalid Password
    bad_ok, bad_msg, _ = authenticate_farmer(username, "WrongPassword")
    assert bad_ok is False
    assert "Invalid password" in bad_msg

def test_farmer_profile_update_and_password_change():
    u_suffix = uuid.uuid4().hex[:6]
    username = f"prof_{u_suffix}"
    old_pwd = "OldPassword@123"
    new_pwd = "NewPassword@456"

    ok, _, fid = register_farmer_account(
        full_name="Original Name",
        username=username,
        mobile_number="9123456780",
        email=None,
        village="OldVillage",
        taluka="Taluka1",
        district="Dist1",
        state="Maharashtra",
        password=old_pwd,
        confirm_password=old_pwd
    )
    assert ok is True

    # Update profile
    up_ok, _ = update_farmer_profile(
        farmer_id=fid,
        full_name="Updated Name",
        mobile_number="9123456789",
        email="updated@test.com",
        village="NewVillage",
        taluka="Taluka2",
        district="Dist2",
        state="Maharashtra"
    )
    assert up_ok is True
    updated_farmer = get_farmer_by_id(fid)
    assert updated_farmer["full_name"] == "Updated Name"
    assert updated_farmer["village"] == "NewVillage"

    # Change password
    chg_ok, _ = change_farmer_password(fid, old_pwd, new_pwd, new_pwd)
    assert chg_ok is True

    # Verify old password fails and new password works
    old_login, _, _ = authenticate_farmer(username, old_pwd)
    assert old_login is False

    new_login, _, _ = authenticate_farmer(username, new_pwd)
    assert new_login is True

def test_diagnosis_association_and_isolation():
    """Verifies that each farmer only accesses and manages their own private records."""
    u1 = f"f1_{uuid.uuid4().hex[:5]}"
    u2 = f"f2_{uuid.uuid4().hex[:5]}"
    _, _, fid1 = register_farmer_account("Farmer One", u1, "9999999901", None, "V1", "T1", "D1", "M1", "Pass123!", "Pass123!")
    _, _, fid2 = register_farmer_account("Farmer Two", u2, "9999999902", None, "V2", "T2", "D2", "M2", "Pass123!", "Pass123!")

    # Farmer 1 records diagnosis
    d1_id = record_farmer_diagnosis(
        farmer_id=fid1,
        target_type="Leaf",
        predicted_disease="Canker",
        confidence_score=0.965,
        model_name="EfficientNet-B3",
        latency_ms=35.0,
        is_uncertain=False,
        treatment_recommendations="Copper Oxychloride spray"
    )
    assert d1_id > 0

    # Farmer 2 records diagnosis
    d2_id = record_farmer_diagnosis(
        farmer_id=fid2,
        target_type="Leaf",
        predicted_disease="Healthy",
        confidence_score=0.985,
        model_name="ResNet-50",
        latency_ms=42.0,
        is_uncertain=False,
        treatment_recommendations="No spray required"
    )
    assert d2_id > 0

    # Farmer 1 retrieves history -> should ONLY contain d1_id
    f1_history = get_farmer_diagnoses(farmer_id=fid1)
    f1_diag_ids = [r["diagnosis_id"] for r in f1_history]
    assert d1_id in f1_diag_ids
    assert d2_id not in f1_diag_ids  # Farmer 2's record is isolated!

    # Farmer 2 retrieves history -> should ONLY contain d2_id
    f2_history = get_farmer_diagnoses(farmer_id=fid2)
    f2_diag_ids = [r["diagnosis_id"] for r in f2_history]
    assert d2_id in f2_diag_ids
    assert d1_id not in f2_diag_ids  # Farmer 1's record is isolated!

    # Server-Side Authorization: Farmer 1 attempts to delete Farmer 2's record
    unauthorized_delete = delete_farmer_diagnosis(diagnosis_id=d2_id, farmer_id=fid1)
    assert unauthorized_delete is False, "Security violation: Farmer 1 was able to delete Farmer 2's diagnosis!"

    # Authorized Deletion: Farmer 1 deletes own record
    authorized_delete = delete_farmer_diagnosis(diagnosis_id=d1_id, farmer_id=fid1)
    assert authorized_delete is True

def test_admin_farmer_management_and_account_deactivation():
    u = f"f_manage_{uuid.uuid4().hex[:5]}"
    _, _, fid = register_farmer_account("Test Deactivate", u, "9888888888", None, "V", "T", "D", "M", "Pass123!", "Pass123!")

    # Admin lists farmers
    all_f = list_all_farmers(search_query=u)
    assert len(all_f) == 1
    assert all_f[0]["farmer_id"] == fid

    # Admin deactivates farmer account
    set_farmer_status(fid, "inactive")
    f_record = get_farmer_by_id(fid)
    assert f_record["account_status"] == "inactive"

    # Inactive farmer attempts login -> rejected
    login_ok, login_msg, _ = authenticate_farmer(u, "Pass123!")
    assert login_ok is False
    assert "inactive" in login_msg.lower()

    # Admin reactivates account
    set_farmer_status(fid, "active")
    re_login_ok, _, _ = authenticate_farmer(u, "Pass123!")
    assert re_login_ok is True
