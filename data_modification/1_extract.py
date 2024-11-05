import json
import os

with open('annotations.json', 'r') as f:
    coco_data = json.load(f)

output_dir = 'labels'
os.makedirs(output_dir, exist_ok=True)

category_id_to_class = {category['id']: idx for idx, category in enumerate(coco_data['categories'])}

image_id_to_dimensions = {img['id']: (img['width'], img['height']) for img in coco_data['images']}

for ann in coco_data['annotations']:
    image_id = ann['image_id']
    category_id = ann['category_id']
    
    if category_id not in category_id_to_class or image_id not in image_id_to_dimensions:
        continue

    class_id = category_id_to_class[category_id]
    
    x, y, width, height = ann['bbox']
    img_width, img_height = image_id_to_dimensions[image_id]

    x_center = (x + width / 2) / img_width
    y_center = (y + height / 2) / img_height
    norm_width = width / img_width
    norm_height = height / img_height

    yolo_annotation = f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}\n"

    label_file_path = os.path.join(output_dir, f"{image_id}.txt")
    with open(label_file_path, 'a') as file:
        file.write(yolo_annotation)

print("YOLO annotations saved to", output_dir)


# TXT format:  class(1) bb coordinates(4)
# Multiple rows in case of multiple objects
 
# sample entry:   1 0.23 0.24 0.543 0.532