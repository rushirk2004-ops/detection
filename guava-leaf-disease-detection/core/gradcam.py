"""
Explainable AI (XAI) Grad-CAM Module
Generates visual class activation heatmaps to show where models focus.
"""
import torch
import torch.nn as nn
import numpy as np
import cv2
from PIL import Image
from typing import Optional, List, Tuple

try:
    from pytorch_grad_cam import GradCAM
    from pytorch_grad_cam.utils.image import show_cam_on_image
    PYTORCH_GRAD_CAM_AVAILABLE = True
except ImportError:
    PYTORCH_GRAD_CAM_AVAILABLE = False

def get_target_layers_for_model(model: nn.Module, model_name: str) -> List[nn.Module]:
    """
    Returns the appropriate target convolutional layer for Grad-CAM based on model architecture.
    """
    if "resnet" in model_name.lower():
        if hasattr(model, 'layer4'):
            return [model.layer4[-1]]
    elif "efficientnet" in model_name.lower():
        if hasattr(model, 'features'):
            return [model.features[-1]]
            
    # Fallback search for the last convolutional or sequential block
    conv_layers = [m for m in model.modules() if isinstance(m, nn.Conv2d)]
    if conv_layers:
        return [conv_layers[-1]]
        
    raise ValueError(f"Could not automatically detect target layer for Grad-CAM in model '{model_name}'.")

def generate_gradcam_visualization(
    model: nn.Module,
    model_name: str,
    image_tensor: torch.Tensor,
    original_rgb_image: Image.Image,
    target_category_idx: Optional[int] = None
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[str]]:
    """
    Computes Grad-CAM heatmap and blended visualization.
    
    Args:
        model: Loaded PyTorch model
        model_name: Name of architecture ('ResNet-50' or 'EfficientNet-B3')
        image_tensor: Preprocessed tensor [1, 3, 224, 224] on matching device
        original_rgb_image: PIL Image in RGB mode
        target_category_idx: Target class index (None uses argmax)
        
    Returns:
        (visualization_rgb: np.ndarray [H, W, 3], grayscale_heatmap: np.ndarray [H, W], error: Optional[str])
    """
    if not PYTORCH_GRAD_CAM_AVAILABLE:
        return None, None, "pytorch_grad_cam package is not installed."
        
    try:
        target_layers = get_target_layers_for_model(model, model_name)
        cam = GradCAM(model=model, target_layers=target_layers)
        
        # Prepare targets if specified
        targets = None
        # Compute grayscale heatmap [0..1]
        grayscale_cam = cam(input_tensor=image_tensor, targets=targets)[0, :]
        
        # Resize original image to (224, 224)
        resized_pil = original_rgb_image.resize((224, 224), Image.Resampling.BILINEAR)
        img_np = np.array(resized_pil, dtype=np.float32) / 255.0
        
        # Overlay heatmap using colormap
        vis = show_cam_on_image(img_np, grayscale_cam, use_rgb=True)
        return vis, grayscale_cam, None
    except Exception as e:
        return None, None, f"Grad-CAM generation error: {str(e)}"
