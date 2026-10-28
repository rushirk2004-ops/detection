"""
Model Evaluation Service
Evaluates ResNet-50 and EfficientNet-B3 on the test dataset.
Computes real Confusion Matrices, Accuracy, Precision, Recall, and F1-Scores.
"""
import os
import json
import torch
import numpy as np
from typing import Dict, Any, Optional
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

from core.model_loader import load_trained_model, get_optimal_device, MODEL_REGISTRY
from core.preprocessing import IMAGENET_MEAN, IMAGENET_STD

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
METRICS_CACHE_FILE = os.path.join(RESULTS_DIR, "evaluation_metrics.json")
CLASSES = ['Canker', 'Dot', 'Healthy', 'Mummification', 'Rust']

def evaluate_model_on_test_data(model_name: str = "ResNet-50", batch_size: int = 32, max_batches: Optional[int] = None) -> Dict[str, Any]:
    """
    Runs actual evaluation on the test set.
    """
    test_dir = os.path.join(PROJECT_ROOT, "data", "test")
    if not os.path.exists(test_dir):
        return {"error": f"Test dataset directory '{test_dir}' not found."}
        
    device = get_optimal_device()
    model, meta = load_trained_model(model_name=model_name, device=device)
    
    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])
    
    test_dataset = datasets.ImageFolder(root=test_dir, transform=val_test_transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    y_true = []
    y_pred = []
    
    with torch.no_grad():
        for batch_idx, (inputs, labels) in enumerate(test_loader):
            if max_batches and batch_idx >= max_batches:
                break
            inputs = inputs.to(device)
            outputs = model(inputs)
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            y_pred.extend(preds)
            y_true.extend(labels.numpy())
            
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    acc = float(accuracy_score(y_true, y_pred))
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(CLASSES))))
    
    # Per-class metrics
    p_per, r_per, f1_per, sup_per = precision_recall_fscore_support(y_true, y_pred, average=None, zero_division=0)
    per_class = {}
    for idx, c in enumerate(CLASSES):
        per_class[c] = {
            "precision": round(float(p_per[idx]) * 100, 2),
            "recall": round(float(r_per[idx]) * 100, 2),
            "f1_score": round(float(f1_per[idx]) * 100, 2),
            "support": int(sup_per[idx])
        }
        
    result = {
        "model_name": model_name,
        "total_test_samples": len(y_true),
        "overall_accuracy_pct": round(acc * 100, 2),
        "precision_pct": round(float(p) * 100, 2),
        "recall_pct": round(float(r) * 100, 2),
        "f1_score_pct": round(float(f1) * 100, 2),
        "confusion_matrix": cm.tolist(),
        "classes": CLASSES,
        "per_class_metrics": per_class
    }
    
    return result

def get_or_run_evaluation(model_name: str = "ResNet-50", force_rerun: bool = False) -> Dict[str, Any]:
    """
    Returns cached evaluation metrics or runs the evaluation and caches them.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    cached_all = {}
    if os.path.exists(METRICS_CACHE_FILE) and not force_rerun:
        try:
            with open(METRICS_CACHE_FILE, "r", encoding="utf-8") as f:
                cached_all = json.load(f)
                if model_name in cached_all:
                    return cached_all[model_name]
        except Exception:
            pass
            
    metrics = evaluate_model_on_test_data(model_name=model_name)
    cached_all[model_name] = metrics
    
    try:
        with open(METRICS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cached_all, f, indent=2)
    except Exception:
        pass
        
    return metrics
