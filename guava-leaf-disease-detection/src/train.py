import torch
import torch.nn as nn
import torch.optim as optim
import os
import argparse
from data_loader import get_data_loaders
from models.efficientnetb3_model import get_efficientnetb3
from models.resnet50_model import get_resnet50

def train_model(model_name, data_dir, epochs=5, batch_size=16, learning_rate=0.0003):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_loader, val_loader, test_loader, class_names = get_data_loaders(data_dir, batch_size=batch_size)
    num_classes = len(class_names)
    print(f"Classes: {class_names}")

    if model_name.lower() == 'efficientnet':
        model = get_efficientnetb3(num_classes)
    elif model_name.lower() == 'resnet50':
        model = get_resnet50(num_classes)
    else:
        raise ValueError("Model not supported. Choose 'efficientnet' or 'resnet50'")

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_acc = 0.0
    save_dir = '../models/saved_models'
    os.makedirs(save_dir, exist_ok=True)
    
    # Simple training loop
    for epoch in range(epochs):
        print(f'Epoch {epoch}/{epochs - 1}')
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
                dataloader = train_loader
            else:
                model.eval()
                dataloader = val_loader

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloader:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloader.dataset)
            epoch_acc = running_corrects.double() / len(dataloader.dataset)

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                torch.save(model.state_dict(), os.path.join(save_dir, f'{model_name.lower()}_best.pt'))

    print(f'Best val Acc: {best_acc:4f}')
    return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Guava Disease Detection Model')
    parser.add_argument('--model', type=str, default='resnet50', help='Model to train (resnet50 or efficientnet)')
    parser.add_argument('--epochs', type=int, default=5, help='Number of epochs')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size')
    parser.add_argument('--data_dir', type=str, default='../data', help='Data directory')
    args = parser.parse_args()
    
    train_model(args.model, args.data_dir, args.epochs, args.batch_size)
