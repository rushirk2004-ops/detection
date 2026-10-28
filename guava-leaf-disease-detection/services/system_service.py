"""
System Monitoring and Health Service
Inspects real hardware resources, GPU/CUDA acceleration, memory, and model storage status.
"""
import os
import sys
import shutil
import platform
import torch
import psutil
from typing import Dict, Any

from core.model_loader import get_model_info, MODEL_REGISTRY

def get_system_health() -> Dict[str, Any]:
    """Returns real operational metrics of the system."""
    # CPU & RAM
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_cores = psutil.cpu_count(logical=True)
    memory = psutil.virtual_memory()
    
    # Disk
    drive = os.path.splitdrive(os.path.abspath(__file__))[0] or "/"
    disk = shutil.disk_usage(drive)
    
    # PyTorch & Device
    cuda_available = torch.cuda.is_available()
    cuda_device_name = torch.cuda.get_device_name(0) if cuda_available else "N/A (Using CPU)"
    cuda_device_count = torch.cuda.device_count() if cuda_available else 0
    
    # Checkpoints
    models_info = {}
    for name in MODEL_REGISTRY:
        models_info[name] = get_model_info(name)
        
    return {
        "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
        "python_version": sys.version.split()[0],
        "pytorch_version": torch.__version__,
        "cuda_available": cuda_available,
        "cuda_device_name": cuda_device_name,
        "cuda_device_count": cuda_device_count,
        "cpu_percent": cpu_percent,
        "cpu_cores": cpu_cores,
        "ram_total_gb": round(memory.total / (1024**3), 2),
        "ram_used_gb": round(memory.used / (1024**3), 2),
        "ram_percent": memory.percent,
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "models": models_info
    }
