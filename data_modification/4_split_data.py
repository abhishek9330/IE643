import os
import shutil
from pathlib import Path

blurred_images_dir = './blurred/images/train/'
blurred_labels_dir = './blurred/labels/train/'
original_images_dir = './custom_dataset/images/train/'
base_output_dir = './T'

blurred_labels = sorted(Path(blurred_labels_dir).glob('*.txt'))
def copy_data(labels_list, images_dir, dest_images_dir, dest_labels_dir):
    for label_path in labels_list:
        image_name = label_path.stem + '.jpg' 
        image_path = images_dir / image_name
        
    
        dest_image_path = dest_images_dir / image_name
        dest_label_path = dest_labels_dir / label_path.name
        
    
        shutil.copy(image_path, dest_image_path)
        shutil.copy(label_path, dest_label_path)
        print("Done, ", label_path.name)

split_size = len(blurred_labels) // 10
splits = [blurred_labels[i * split_size:(i + 1) * split_size] for i in range(10)]

for i in range(10):

    output_dir = Path(base_output_dir) / f'T{i+1}'
    output_images_dir = output_dir / 'images/train'
    output_labels_dir = output_dir / 'labels/train'
    
    output_images_dir.mkdir(parents=True, exist_ok=True)
    output_labels_dir.mkdir(parents=True, exist_ok=True)
    
    if (i + 1) % 2 == 0: 
        copy_data(splits[i], Path(original_images_dir), output_images_dir, output_labels_dir)
    else: 
        copy_data(splits[i], Path(blurred_images_dir), output_images_dir, output_labels_dir)

print("Datasets T1-T10 created with alternating blurred and original images.")
