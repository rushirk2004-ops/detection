"""
Image and Request Validation Module
Validates image files, formats, integrity, dimensions, and payloads.
"""
import io
import os
from typing import Tuple, Optional
from PIL import Image, UnidentifiedImageError

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB
MIN_IMAGE_DIM = 32

def validate_image_file(file_obj_or_path, filename: Optional[str] = None) -> Tuple[bool, str, Optional[Image.Image]]:
    """
    Validates an image from a path, file-like object, bytes, or existing PIL Image.
    
    Returns:
        (is_valid: bool, error_message: str, pil_image: Optional[Image.Image])
    """
    if file_obj_or_path is None:
        return False, "No file provided.", None
    
    # 1. Direct PIL Image instance
    if isinstance(file_obj_or_path, Image.Image):
        width, height = file_obj_or_path.size
        if width < MIN_IMAGE_DIM or height < MIN_IMAGE_DIM:
            return False, f"Image resolution ({width}x{height}) is too low. Minimum required: {MIN_IMAGE_DIM}x{MIN_IMAGE_DIM} pixels.", None
        return True, "", file_obj_or_path

    # 2. Check filename extension if provided
    fname = filename or getattr(file_obj_or_path, 'name', None)
    if fname:
        _, ext = os.path.splitext(fname)
        if ext and ext.lower() not in ALLOWED_EXTENSIONS:
            return False, f"Unsupported file type '{ext}'. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}", None
            
    # 3. Check file size if available (ensure it's an int, not a PIL size tuple)
    if hasattr(file_obj_or_path, 'size') and isinstance(file_obj_or_path.size, int):
        if file_obj_or_path.size > MAX_FILE_SIZE_BYTES:
            return False, f"File exceeds maximum size limit of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB.", None
    elif isinstance(file_obj_or_path, (str, os.PathLike)) and os.path.exists(file_obj_or_path):
        if os.path.getsize(file_obj_or_path) > MAX_FILE_SIZE_BYTES:
            return False, f"File exceeds maximum size limit of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB.", None

    try:
        # If it's a file path
        if isinstance(file_obj_or_path, (str, os.PathLike)):
            img = Image.open(file_obj_or_path)
            img.verify()
            img = Image.open(file_obj_or_path)
        elif isinstance(file_obj_or_path, bytes):
            stream = io.BytesIO(file_obj_or_path)
            img = Image.open(stream)
            img.verify()
            stream.seek(0)
            img = Image.open(stream)
        else:
            # File-like object (e.g. Streamlit UploadedFile)
            # Reset stream position before reading!
            if hasattr(file_obj_or_path, 'seek'):
                file_obj_or_path.seek(0)
                
            if hasattr(file_obj_or_path, 'getvalue'):
                content = file_obj_or_path.getvalue()
            else:
                content = file_obj_or_path.read()
                
            if hasattr(file_obj_or_path, 'seek'):
                file_obj_or_path.seek(0)
                
            if not content or len(content) == 0:
                return False, "Uploaded file is empty.", None
            if len(content) > MAX_FILE_SIZE_BYTES:
                return False, f"File size ({len(content)/(1024*1024):.1f}MB) exceeds {MAX_FILE_SIZE_BYTES//(1024*1024)}MB limit.", None
                
            stream = io.BytesIO(content)
            img = Image.open(stream)
            img.verify()
            stream.seek(0)
            img = Image.open(stream)
            
        # Check dimensions
        width, height = img.size
        if width < MIN_IMAGE_DIM or height < MIN_IMAGE_DIM:
            return False, f"Image resolution ({width}x{height}) is too low. Minimum required: {MIN_IMAGE_DIM}x{MIN_IMAGE_DIM} pixels.", None
            
        return True, "", img
    except (UnidentifiedImageError, OSError, ValueError) as e:
        return False, f"Corrupted or invalid image file: {str(e)}", None
    except Exception as e:
        return False, f"Failed to validate image: {str(e)}", None

def validate_plant_subject(pil_img: Image.Image) -> Tuple[bool, str, dict]:
    """
    Validates whether the image contains genuine plant/leaf foliage
    using the agricultural Excess Green Index (ExG = 2G - R - B) and Human Skin Detection.
    Rejects human faces, selfies, pets, furniture, and non-plant objects.
    """
    import cv2
    import numpy as np
    
    img_rgb = np.array(pil_img.convert('RGB'), dtype=np.float32)
    total_pixels = img_rgb.shape[0] * img_rgb.shape[1]
    
    r = img_rgb[:, :, 0]
    g = img_rgb[:, :, 1]
    b = img_rgb[:, :, 2]
    
    # 1. Excess Green Index (ExG): identifies vegetative foliage
    exg = (2.0 * g - r - b)
    pos_exg_ratio = float(np.sum(exg > 4.0) / total_pixels)
    
    # 2. Human Skin Detector (YCrCb color space)
    img_uint8 = np.array(pil_img.convert('RGB'), dtype=np.uint8)
    img_bgr = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2BGR)
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    lower_skin = np.array([0, 133, 77], dtype=np.uint8)
    upper_skin = np.array([255, 173, 127], dtype=np.uint8)
    mask_skin = cv2.inRange(ycrcb, lower_skin, upper_skin)
    skin_ratio = float(np.sum(mask_skin > 0) / total_pixels)
    
    # 3. Decision Boundary
    if skin_ratio > 0.14 and pos_exg_ratio < 0.08:
        return False, "HUMAN_DETECTED", {
            "exg_ratio": round(pos_exg_ratio * 100, 2),
            "skin_ratio": round(skin_ratio * 100, 2),
            "reason_en": "Human subject / face detected! This AI system is strictly trained for Guava leaf and plant disease diagnosis. Please point your camera at a guava tree leaf.",
            "reason_mr": "मानवी चेहरा किंवा व्यक्ती आढळली! ही प्रणाली केवळ पेरूच्या झाडाच्या पानांचे रोग ओळखण्यासाठी आहे. कृपया कॅमेरा पेरूच्या पानासमोर धरून फोटो काढा."
        }
        
    if pos_exg_ratio < 0.025:
        return False, "NON_PLANT_DETECTED", {
            "exg_ratio": round(pos_exg_ratio * 100, 2),
            "skin_ratio": round(skin_ratio * 100, 2),
            "reason_en": "No plant foliage detected! The image does not show guava leaves or plant tissue. Please upload a clear photo of a guava leaf.",
            "reason_mr": "झाडाचे पान आढळले नाही! हा फोटो खोली किंवा इतर वस्तूचा वाटत आहे. कृपया पेरूच्या झाडाच्या पानाचा स्पष्ट फोटो काढा."
        }
        
    return True, "VALID_PLANT", {
        "exg_ratio": round(pos_exg_ratio * 100, 2),
        "skin_ratio": round(skin_ratio * 100, 2)
    }
