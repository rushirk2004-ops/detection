"""
Image Preprocessing Module
Handles consistent resizing, RGB conversion, and ImageNet tensor normalization.
"""
import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple

DEFAULT_IMG_SIZE = (224, 224)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def get_inference_transforms(img_size: Tuple[int, int] = DEFAULT_IMG_SIZE):
    """
    Standard torchvision transform matching the model training pipeline.
    """
    return transforms.Compose([
        transforms.Resize(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

def prepare_image_for_model(pil_image: Image.Image, device: torch.device = None, img_size: Tuple[int, int] = DEFAULT_IMG_SIZE) -> Tuple[torch.Tensor, Image.Image]:
    """
    Takes any PIL image, converts it safely to RGB, resizes and normalizes it.
    
    Returns:
        (tensor: torch.Tensor [1, 3, H, W], rgb_image: Image.Image)
    """
    if not isinstance(pil_image, Image.Image):
        raise TypeError("Expected PIL.Image.Image object")
        
    # Ensure RGB (converts RGBA, Grayscale, CMYK, etc.)
    if pil_image.mode != 'RGB':
        rgb_image = pil_image.convert('RGB')
    else:
        rgb_image = pil_image.copy()
        
    transform = get_inference_transforms(img_size)
    tensor = transform(rgb_image).unsqueeze(0)  # Add batch dimension [1, 3, 224, 224]
    
    if device is not None:
        tensor = tensor.to(device)
        
    return tensor, rgb_image
