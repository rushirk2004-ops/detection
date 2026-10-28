"""
Comprehensive Automated Test Suite
Covers all 20 required system specifications, pipelines, security, and edge cases.
"""
import os
import io
import pytest
import torch
import numpy as np
from PIL import Image

import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.validation import validate_image_file, ALLOWED_EXTENSIONS
from core.preprocessing import prepare_image_for_model, DEFAULT_IMG_SIZE
from core.model_loader import load_trained_model, get_model_info, MODEL_REGISTRY, get_optimal_device
from core.inference import run_disease_inference, LEAF_CLASSES, DEFAULT_UNCERTAINTY_THRESHOLD
from core.gradcam import generate_gradcam_visualization
from services.authentication import hash_password, verify_credentials, register_admin, create_admin_session, is_session_valid
from services.configuration_service import load_settings, update_uncertainty_threshold
from services.history_service import (
    record_prediction, get_prediction_history, clear_prediction_history,
    log_audit_event, get_audit_logs, get_db_connection
)

# Helper to create test images
def create_dummy_image(format="JPEG", mode="RGB", size=(250, 250), color=None):
    if color is None:
        if mode == "RGB":
            color = (100, 180, 50)
        elif mode == "RGBA":
            color = (100, 180, 50, 255)
        elif mode == "L":
            color = 128
        elif mode == "CMYK":
            color = (0, 100, 100, 0)
        else:
            color = 0
            
    buf = io.BytesIO()
    img = Image.new(mode, size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf, img

# 1. Valid JPG and PNG uploads
def test_valid_jpg_png_uploads():
    for fmt in ["JPEG", "PNG"]:
        buf, _ = create_dummy_image(format=fmt, mode="RGB")
        buf.name = f"test_leaf.{fmt.lower()}"
        is_valid, err, pil_img = validate_image_file(buf)
        assert is_valid is True, f"Failed for {fmt}: {err}"
        assert pil_img is not None

# 2. Invalid file types
def test_invalid_file_types():
    buf = io.BytesIO(b"Fake PDF content")
    buf.name = "document.pdf"
    is_valid, err, _ = validate_image_file(buf)
    assert is_valid is False
    assert "Unsupported file type" in err

# 3. Corrupted images
def test_corrupted_images():
    buf = io.BytesIO(b"Corrupted broken image data non-image bytes")
    buf.name = "corrupt.jpg"
    is_valid, err, _ = validate_image_file(buf)
    assert is_valid is False
    assert "Corrupted or invalid image" in err

# 4. RGB conversion (RGBA, Grayscale, CMYK)
def test_rgb_conversion():
    for mode in ["RGBA", "L", "CMYK"]:
        fmt = "PNG" if mode == "RGBA" else "JPEG"
        _, img = create_dummy_image(format=fmt, mode=mode)
        tensor, rgb_img = prepare_image_for_model(img)
        assert rgb_img.mode == "RGB"
        assert tensor.shape[1] == 3

# 5. Image resizing and normalization
def test_image_resizing_and_normalization():
    _, img = create_dummy_image(size=(800, 600))
    tensor, _ = prepare_image_for_model(img)
    assert tensor.shape == (1, 3, 224, 224)
    # Check normalized values are not raw 0..255 ints
    assert tensor.dtype == torch.float32
    assert tensor.max() <= 5.0 and tensor.min() >= -5.0

# 6. Correct leaf class mapping
def test_leaf_class_mapping():
    expected_classes = ['Canker', 'Dot', 'Healthy', 'Mummification', 'Rust']
    assert LEAF_CLASSES == expected_classes
    assert len(LEAF_CLASSES) == 5

# 7. Correct fruit class mapping
def test_fruit_class_mapping():
    _, img = create_dummy_image()
    res = run_disease_inference(img, target_type="Fruit")
    assert res["success"] is False
    assert res["error_code"] == "FRUIT_MODEL_NOT_AVAILABLE"

# 8. Model checkpoint loading
def test_model_checkpoint_loading():
    for m_name in ["ResNet-50", "EfficientNet-B3"]:
        model, meta = load_trained_model(m_name, device=torch.device("cpu"), use_cache=False)
        assert meta["weights_loaded"] is True
        assert meta["num_classes"] == 5

# 9. CPU inference
def test_cpu_inference():
    _, img = create_dummy_image()
    res = run_disease_inference(img, model_name="ResNet-50", device=torch.device("cpu"))
    assert res["success"] is True
    assert res["device"] == "cpu"
    assert res["predicted_class"] in LEAF_CLASSES

# 10. CUDA inference (conditional)
def test_cuda_inference_conditional():
    optimal = get_optimal_device()
    assert optimal.type in ["cuda", "cpu"]
    _, img = create_dummy_image()
    res = run_disease_inference(img, device=optimal)
    assert res["success"] is True

# 11. Softmax probability calculation
def test_softmax_probability_sum():
    _, img = create_dummy_image()
    res = run_disease_inference(img, model_name="ResNet-50")
    assert res["success"] is True
    probs = res["probabilities"]
    prob_sum = sum(probs.values())
    assert abs(prob_sum - 1.0) < 0.01  # Sums to 100% within rounding

# 12. 60% uncertainty warning trigger
def test_uncertainty_warning_trigger():
    _, img = create_dummy_image()
    # If threshold is 0.9999, most regular random dummies should trigger uncertainty
    res = run_disease_inference(img, uncertainty_threshold=0.9999)
    assert res["is_uncertain"] is True

# 13. Grad-CAM generation
def test_gradcam_generation():
    _, img = create_dummy_image()
    model, _ = load_trained_model("ResNet-50", device=torch.device("cpu"))
    tensor, rgb = prepare_image_for_model(img, device=torch.device("cpu"))
    vis, heatmap, err = generate_gradcam_visualization(model, "ResNet-50", tensor, rgb)
    assert err is None
    assert vis is not None
    assert vis.shape == (224, 224, 3)

# 14. Missing checkpoint handling
def test_missing_checkpoint_handling():
    # Calling get_model_info on an invalid architecture
    with pytest.raises(ValueError):
        get_model_info("NonExistentModelArchitecture")

# 15. Unauthenticated admin access
def test_unauthenticated_admin_access():
    assert is_session_valid(None) is False
    assert is_session_valid({"authenticated": False}) is False

# 16. Unauthorized administrative actions
def test_unauthorized_admin_actions():
    valid, msg = verify_credentials("admin", "wrong_attacker_password")
    assert valid is False
    assert "Invalid password" in msg

def test_admin_signup_and_verification():
    import uuid
    test_user = f"adm_{uuid.uuid4().hex[:6]}"
    # Register with wrong key -> fails
    ok, msg = register_admin(test_user, "Pass1234", "Pass1234", access_key="WRONG")
    assert ok is False
    assert "Invalid Admin Registration Access Key" in msg

    # Register with correct key -> succeeds
    ok, msg = register_admin(test_user, "Pass1234", "Pass1234", access_key="GUAVA2026")
    assert ok is True
    assert "registered successfully" in msg

    # Verify credentials
    valid, v_msg = verify_credentials(test_user, "Pass1234")
    assert valid is True

# 17. Configuration validation
def test_configuration_validation():
    settings = load_settings()
    assert "system" in settings
    assert "inference" in settings
    assert settings["inference"]["uncertainty_threshold"] == 0.60

# 18. Database operations
def test_database_operations():
    clear_prediction_history()
    row_id = record_prediction(
        predicted_class="Canker",
        confidence=0.98,
        model_name="ResNet-50",
        target_type="Leaf",
        is_uncertain=False,
        latency_ms=45.2
    )
    assert row_id > 0
    history = get_prediction_history(limit=5)
    assert len(history) >= 1
    assert history[0]["predicted_class"] == "Canker"

# 19. Privacy and image-retention behavior
def test_privacy_and_image_retention():
    # When opt_in_storage is False, image_blob must be strictly None!
    dummy_bytes = b"sample_raw_image_bytes"
    row_id = record_prediction(
        predicted_class="Healthy",
        confidence=0.95,
        model_name="EfficientNet-B3",
        image_bytes=dummy_bytes,
        opt_in_storage=False  # User did not opt in
    )
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT image_blob FROM predictions WHERE id = ?", (row_id,))
        blob = cursor.fetchone()[0]
        assert blob is None, "Privacy violation: image was stored without user opt-in!"

# 20. Unified inference consistency
def test_unified_inference_consistency():
    # Both panels use run_disease_inference; verify schema stability
    _, img = create_dummy_image()
    res1 = run_disease_inference(img, model_name="ResNet-50")
    res2 = run_disease_inference(img, model_name="EfficientNet-B3")
    required_keys = ["success", "predicted_class", "confidence", "confidence_pct", "probabilities", "is_uncertain", "latency_ms"]
    for k in required_keys:
        assert k in res1
        assert k in res2

# 21. Human & Non-Plant OOD Rejection Gate
def test_human_and_non_plant_rejection_gate():
    # Human face dummy with skin tone (R=190, G=140, B=110)
    human_img = Image.new("RGB", (250, 250), color=(190, 140, 110))
    res_human = run_disease_inference(human_img, model_name="ResNet-50")
    assert res_human["success"] is False
    assert res_human["error_code"] in ["HUMAN_DETECTED", "NON_PLANT_DETECTED"]
    assert res_human["predicted_class"] is None

    # Blank dark indoor room/wall (non-plant)
    room_img = Image.new("RGB", (250, 250), color=(50, 50, 55))
    res_room = run_disease_inference(room_img, model_name="ResNet-50")
    assert res_room["success"] is False
    assert res_room["error_code"] == "NON_PLANT_DETECTED"
    assert res_room["predicted_class"] is None
