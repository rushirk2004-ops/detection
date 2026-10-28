import os
import shutil
import random
from pathlib import Path

def split_data(raw_dir, target_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, seed=42):
    random.seed(seed)
    
    raw_path = Path(raw_dir)
    target_path = Path(target_dir)
    
    train_dir = target_path / 'train'
    val_dir = target_path / 'val'
    test_dir = target_path / 'test'
    
    # Define categories
    categories = ['canker', 'dot', 'mummification', 'rust', 'healthy']
    
    for cat in categories:
        (train_dir / cat).mkdir(parents=True, exist_ok=True)
        (val_dir / cat).mkdir(parents=True, exist_ok=True)
        (test_dir / cat).mkdir(parents=True, exist_ok=True)
        
        cat_path = raw_path / cat
        if not cat_path.exists():
            print(f"Skipping {cat}, not found in raw data.")
            continue
            
        images = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)
        
        train_end = int(len(images) * train_ratio)
        val_end = int(len(images) * (train_ratio + val_ratio))
        
        train_imgs = images[:train_end]
        val_imgs = images[train_end:val_end]
        test_imgs = images[val_end:]
        
        def copy_imgs(img_list, dest_dir):
            for img in img_list:
                shutil.copy2(cat_path / img, dest_dir / img)
                
        copy_imgs(train_imgs, train_dir / cat)
        copy_imgs(val_imgs, val_dir / cat)
        copy_imgs(test_imgs, test_dir / cat)
        
        print(f"{cat}: {len(train_imgs)} train | {len(val_imgs)} val | {len(test_imgs)} test")

if __name__ == '__main__':
    raw_dir = 'data/raw'
    target_dir = 'data'
    print("Splitting dataset into train, val, and test...")
    split_data(raw_dir, target_dir)
    print("Data splitting complete!")
