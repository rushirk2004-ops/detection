import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights

def get_resnet50(num_classes=5):
    """
    Returns a pre-trained ResNet-50 model, modified for the specific number of classes.
    """
    weights = ResNet50_Weights.IMAGENET1K_V2
    model = resnet50(weights=weights)
    
    # Replace the final fully connected layer
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    
    return model

if __name__ == "__main__":
    model = get_resnet50(num_classes=5)
    print(f"Model architecture configured. Classifier out features: {model.fc.out_features}")
