"""
Unified Inference Engine
Single, verified inference implementation shared by both Farmer and Admin panels.
"""
import time
import torch
import torch.nn.functional as F
from PIL import Image
from typing import Dict, Any, Optional

from core.validation import validate_image_file, validate_plant_subject
from core.preprocessing import prepare_image_for_model
from core.model_loader import load_trained_model, get_optimal_device
from core.gradcam import generate_gradcam_visualization

LEAF_CLASSES = ['Canker', 'Dot', 'Healthy', 'Mummification', 'Rust']
DEFAULT_UNCERTAINTY_THRESHOLD = 0.60  # 60%

def run_disease_inference(
    image_source,
    target_type: str = "Leaf",
    model_name: str = "ResNet-50",
    uncertainty_threshold: float = DEFAULT_UNCERTAINTY_THRESHOLD,
    generate_gradcam: bool = True,
    device: Optional[torch.device] = None
) -> Dict[str, Any]:
    """
    Executes deep learning inference on a given guava leaf or fruit image.
    
    Returns structured result dict.
    """
    start_time = time.perf_counter()
    
    # 1. Target check
    if target_type.lower() == "fruit":
        return {
            "success": False,
            "target_type": "Fruit",
            "error_code": "FRUIT_MODEL_NOT_AVAILABLE",
            "message": "Fruit disease detection model is currently under development. Guava leaf disease detection is fully active and trained.",
            "predicted_class": None,
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "probabilities": {},
            "is_uncertain": True,
            "latency_ms": 0.0,
            "gradcam_vis": None
        }

    # 2. Validate Image
    is_valid, val_err, pil_img = validate_image_file(image_source)
    if not is_valid:
        return {
            "success": False,
            "target_type": target_type,
            "error_code": "INVALID_IMAGE",
            "message": val_err,
            "predicted_class": None,
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "probabilities": {},
            "is_uncertain": True,
            "latency_ms": 0.0,
            "gradcam_vis": None
        }

    # 2.5 Foliage / Plant Verification Gate (Rejects human selfies, pets, non-plants)
    is_plant, plant_code, plant_meta = validate_plant_subject(pil_img)
    if not is_plant:
        return {
            "success": False,
            "target_type": target_type,
            "error_code": plant_code,
            "message": plant_meta.get("reason_en"),
            "message_mr": plant_meta.get("reason_mr"),
            "plant_metrics": plant_meta,
            "predicted_class": None,
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "probabilities": {},
            "is_uncertain": True,
            "latency_ms": 0.0,
            "gradcam_vis": None
        }

    # 3. Setup Device & Load Model
    if device is None:
        device = get_optimal_device()

    try:
        model, meta = load_trained_model(model_name=model_name, device=device)
    except Exception as e:
        return {
            "success": False,
            "target_type": target_type,
            "error_code": "MODEL_LOAD_FAILED",
            "message": f"Could not initialize {model_name}: {str(e)}",
            "predicted_class": None,
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "probabilities": {},
            "is_uncertain": True,
            "latency_ms": 0.0,
            "gradcam_vis": None
        }

    # 4. Preprocess Image
    try:
        tensor, rgb_image = prepare_image_for_model(pil_img, device=device)
    except Exception as e:
        return {
            "success": False,
            "target_type": target_type,
            "error_code": "PREPROCESSING_FAILED",
            "message": f"Preprocessing failed: {str(e)}",
            "predicted_class": None,
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "probabilities": {},
            "is_uncertain": True,
            "latency_ms": 0.0,
            "gradcam_vis": None
        }

    # 5. Predict Probabilities
    try:
        with torch.no_grad():
            logits = model(tensor)
            probs = F.softmax(logits, dim=1).squeeze(0)
            
        top_prob, top_idx = torch.max(probs, dim=0)
        confidence = float(top_prob.item())
        pred_idx = int(top_idx.item())
        
        predicted_class = LEAF_CLASSES[pred_idx]
        is_uncertain = confidence < uncertainty_threshold
        
        prob_dict = {
            LEAF_CLASSES[i]: round(float(probs[i].item()), 4)
            for i in range(len(LEAF_CLASSES))
        }
        
    except Exception as e:
        return {
            "success": False,
            "target_type": target_type,
            "error_code": "INFERENCE_ERROR",
            "message": f"Forward pass error: {str(e)}",
            "predicted_class": None,
            "confidence": 0.0,
            "confidence_pct": 0.0,
            "probabilities": {},
            "is_uncertain": True,
            "latency_ms": 0.0,
            "gradcam_vis": None
        }

    # 6. Grad-CAM Visualization
    gradcam_vis = None
    gradcam_error = None
    if generate_gradcam and meta.get("weights_loaded", False):
        try:
            gradcam_vis, _, gradcam_error = generate_gradcam_visualization(
                model=model,
                model_name=model_name,
                image_tensor=tensor,
                original_rgb_image=rgb_image,
                target_category_idx=pred_idx
            )
        except Exception as e:
            gradcam_error = str(e)

    latency = round((time.perf_counter() - start_time) * 1000.0, 2)

    return {
        "success": True,
        "target_type": "Leaf",
        "model_name": model_name,
        "architecture": meta.get("architecture"),
        "weights_loaded": meta.get("weights_loaded", False),
        "device": device.type,
        "predicted_class": predicted_class,
        "predicted_index": pred_idx,
        "confidence": round(confidence, 4),
        "confidence_pct": round(confidence * 100.0, 2),
        "probabilities": prob_dict,
        "is_uncertain": is_uncertain,
        "uncertainty_threshold": uncertainty_threshold,
        "latency_ms": latency,
        "gradcam_vis": gradcam_vis,
        "gradcam_error": gradcam_error,
        "message": "Prediction completed successfully."
    }
