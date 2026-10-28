import os
import shutil
from pathlib import Path

# Define standard categories to map to
CATEGORIES = ['canker', 'dot', 'mummification', 'rust', 'healthy']

def normalize_category_name(folder_name):
    """
    Tries to map a folder name to one of the standard categories.
    E.g. 'Guava Canker' -> 'canker', 'healthy leaves' -> 'healthy'
    """
    folder_name_lower = folder_name.lower()
    for cat in CATEGORIES:
        if cat in folder_name_lower:
            return cat
    return None

def merge_datasets(source_dirs, target_dir):
    """
    Reads from multiple source datasets and copies all images category-wise
    into the target directory.
    """
    target_path = Path(target_dir)
    
    # Create target category folders if they don't exist
    for cat in CATEGORIES:
        (target_path / cat).mkdir(parents=True, exist_ok=True)
        
    total_copied = 0
    
    for source_dir in source_dirs:
        print(f"\nProcessing dataset: {source_dir}")
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"Warning: Source directory '{source_dir}' does not exist.")
            continue
            
        # Walk through the source directory
        for root, dirs, files in os.walk(source_path):
            current_folder = Path(root).name
            category = normalize_category_name(current_folder)
            
            if category:
                # Filter for image files
                images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if not images:
                    continue
                    
                print(f"  Found {len(images)} images in '{current_folder}' -> mapping to '{category}'")
                
                target_cat_dir = target_path / category
                for img in images:
                    src_file = Path(root) / img
                    
                    # To prevent filename collisions, prefix with parent folder name and a counter
                    # or just use a unique name
                    unique_filename = f"{source_path.name}_{current_folder}_{img}"
                    dst_file = target_cat_dir / unique_filename
                    
                    shutil.copy2(src_file, dst_file)
                    total_copied += 1
            else:
                # If it doesn't match a category, but contains images, warn the user
                images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    print(f"  Warning: Found {len(images)} images in '{current_folder}' but could not map it to a standard category.")

    print(f"\nDone! Copied a total of {total_copied} images to {target_dir}")

if __name__ == "__main__":
    # Add paths to your downloaded datasets here
    # Example:
    # source_datasets = [
    #     '../archive/Guava Disease Dataset/train',
    #     '../archive/Guava Disease Dataset/val',
    #     '../archive/Guava Disease Dataset/test',
    #     '../archive/Another_Dataset_Folder'
    # ]
    
    source_datasets = [
        'archive/Guava Disease Dataset'
    ]
    
    # We will merge everything into data/raw first, and then we can split them later
    target_directory = 'data/raw'
    
    merge_datasets(source_datasets, target_directory)
