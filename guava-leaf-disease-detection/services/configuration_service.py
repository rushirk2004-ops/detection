"""
Configuration Service
Reads and updates YAML settings safely.
"""
import os
import yaml
from typing import Dict, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "settings.yaml")

DEFAULT_SETTINGS = {
    "system": {
        "app_name": "Guava Leaf & Fruit Disease Detection System",
        "version": "2.0.0",
        "academic_year": "2026-2027",
        "default_language": "English"
    },
    "inference": {
        "uncertainty_threshold": 0.60,
        "default_model": "ResNet-50",
        "supported_models": ["ResNet-50", "EfficientNet-B3"]
    },
    "classes": {
        "leaf": ["Canker", "Dot", "Healthy", "Mummification", "Rust"],
        "fruit": ["Anthracnose", "Fruit Fly", "Healthy Fruit", "Scab", "Stylar End Rot"]
    },
    "storage": {
        "database_path": "storage/guava_system.db",
        "allow_image_retention_default": False
    }
}

def load_settings() -> Dict[str, Any]:
    """Loads configuration dictionary from settings.yaml."""
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_SETTINGS
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data else DEFAULT_SETTINGS
    except Exception:
        return DEFAULT_SETTINGS

def update_uncertainty_threshold(new_threshold: float) -> bool:
    """Updates uncertainty threshold in settings.yaml."""
    settings = load_settings()
    if "inference" not in settings:
        settings["inference"] = {}
    settings["inference"]["uncertainty_threshold"] = round(new_threshold, 2)
    
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(settings, f, default_flow_style=False)
        return True
    except Exception:
        return False
