"""
Model Loader and Checkpoint Manager
Safely loads ResNet-50 and EfficientNet-B3 architectures and their trained weights.
"""
import os
import sys
import torch
import torch.nn as nn
from typing import Dict, Any, Tuple, Optional

# Ensure src models can be resolved
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if os.path.join(PROJECT_ROOT, 'src') not in sys.path:
    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from models.resnet50_model import get_resnet50
from models.efficientnetb3_model import get_efficientnetb3

MODEL_REGISTRY = {
    "ResNet-50": {
        "factory": get_resnet50,
        "default_weights": os.path.join(PROJECT_ROOT, "models", "saved_models", "resnet50_best.pt"),
        "architecture": "ResNet-50 (Residual Deep Learning)",
        "num_classes": 5
    },
    "EfficientNet-B3": {
        "factory": get_efficientnetb3,
        "default_weights": os.path.join(PROJECT_ROOT, "models", "saved_models", "efficientnet_best.pt"),
        "architecture": "EfficientNet-B3 (Compound Scaled CNN)",
        "num_classes": 5
    }
}

_LOADED_MODELS_CACHE: Dict[str, Tuple[nn.Module, Dict[str, Any]]] = {}

def get_optimal_device() -> torch.device:
    """Returns CUDA if available, else CPU."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_model_info(model_name: str) -> Dict[str, Any]:
    """Retrieves metadata and checkpoint status for a given model architecture."""
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model architecture '{model_name}'. Available: {list(MODEL_REGISTRY.keys())}")
    
    config = MODEL_REGISTRY[model_name]
    weights_path = config["default_weights"]
    weights_exist = os.path.exists(weights_path)
    file_size_mb = os.path.getsize(weights_path) / (1024 * 1024) if weights_exist else 0.0
    mod_time = os.path.getmtime(weights_path) if weights_exist else 0.0

    return {
        "model_name": model_name,
        "architecture": config["architecture"],
        "num_classes": config["num_classes"],
        "weights_path": weights_path,
        "weights_exist": weights_exist,
        "weights_size_mb": round(file_size_mb, 2),
        "last_modified": mod_time
    }

def load_trained_model(
    model_name: str = "ResNet-50",
    device: Optional[torch.device] = None,
    use_cache: bool = True
) -> Tuple[nn.Module, Dict[str, Any]]:
    """
    Safely loads a requested model, attaches weights if available, sets to eval mode.
    
    Returns:
        (model: nn.Module, metadata: Dict[str, Any])
    """
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unsupported model '{model_name}'. Supported: {list(MODEL_REGISTRY.keys())}")
    
    if device is None:
        device = get_optimal_device()
        
    cache_key = f"{model_name}_{device.type}"
    if use_cache and cache_key in _LOADED_MODELS_CACHE:
        return _LOADED_MODELS_CACHE[cache_key]

    config = MODEL_REGISTRY[model_name]
    factory_fn = config["factory"]
    num_classes = config["num_classes"]
    weights_path = config["default_weights"]
    
    model = factory_fn(num_classes=num_classes)
    weights_loaded = False
    error_msg = None
    
    if os.path.exists(weights_path):
        try:
            # Safe checkpoint loading
            try:
                state_dict = torch.load(weights_path, map_location=device, weights_only=True)
            except TypeError:
                state_dict = torch.load(weights_path, map_location=device)
            model.load_state_dict(state_dict)
            weights_loaded = True
        except Exception as e:
            error_msg = f"Failed to load checkpoint '{weights_path}': {str(e)}"
    else:
        error_msg = f"Weight file not found at: {weights_path}"

    model.to(device)
    model.eval()  # Strictly set to evaluation mode

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    meta = {
        "model_name": model_name,
        "architecture": config["architecture"],
        "num_classes": num_classes,
        "device": device.type,
        "weights_path": weights_path,
        "weights_loaded": weights_loaded,
        "total_params": total_params,
        "trainable_params": trainable_params,
        "load_error": error_msg
    }

    if use_cache:
        _LOADED_MODELS_CACHE[cache_key] = (model, meta)

    return model, meta
