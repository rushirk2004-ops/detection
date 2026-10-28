import torch
import torch.nn as nn
from torchvision.models import efficientnet_b3, EfficientNet_B3_Weights

def get_efficientnetb3(num_classes=5):
    """
    Returns a pre-trained EfficientNet-B3 model, modified for the specific number of classes.
    """
    # Load pre-trained weights
    weights = EfficientNet_B3_Weights.IMAGENET1K_V1
    model = efficientnet_b3(weights=weights)
    
    # Freeze the base parameters for transfer learning (optional, depending on fine-tuning strategy)
    # for param in model.parameters():
    #     param.requires_grad = False
        
    # Replace the classifier layer
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    
    return model

if __name__ == "__main__":
    model = get_efficientnetb3(num_classes=5)
    print(f"Model architecture configured. Classifier out features: {model.classifier[1].out_features}")
