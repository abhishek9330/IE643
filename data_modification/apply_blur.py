import cv2
import os
import numpy as np


CLASS_MAP = {
    0: 'Person',
    1: 'Bicycle',
    2: 'Car',
    3: 'Motorcycle',
    4: 'Airplane',
    5: 'Bus',
    6: 'Train',
    7: 'Truck'
}


label_dir = './custom_dataset/labels/val'    
image_dir = './custom_dataset/images/val'    
target_dir = './blurred/'   

def apply_motion_blur(image, kernel_size=15):
    """Apply motion blur effect to an image."""
    kernel_motion_blur = np.zeros((kernel_size, kernel_size))
    kernel_motion_blur[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    kernel_motion_blur = kernel_motion_blur / kernel_size
    return cv2.filter2D(image, -1, kernel_motion_blur)

def process_image(label_file, image_file):
    """Process image according to the label file."""
    with open(label_file, 'r') as f:
        labels = f.readlines()

    
    contains_airplane = False
    valid_labels = []
    for label in labels:
        class_id = int(label.split()[0])
        if CLASS_MAP[class_id] == 'Airplane' and len(labels) == 1:
            contains_airplane = True
        else:
            valid_labels.append(label)
    
    if contains_airplane:
        print(f"Skipping image {image_file} - contains only airplane.")
        return
    
    
    image = cv2.imread(image_file)
    
    
    for label in valid_labels:
        class_id, x, y, w, h = map(float, label.split())
        class_id = int(class_id)

        if CLASS_MAP[class_id] != 'Person':
            
            img_h, img_w = image.shape[:2]
            x_center, y_center, width, height = x * img_w, y * img_h, w * img_w, h * img_h
            x_min = int(x_center - width / 2)
            y_min = int(y_center - height / 2)
            x_max = int(x_center + width / 2)
            y_max = int(y_center + height / 2)
            
            
            obj_roi = image[y_min:y_max, x_min:x_max]
            obj_blurred = apply_motion_blur(obj_roi)
            image[y_min:y_max, x_min:x_max] = obj_blurred
    
    
    image_name = os.path.basename(image_file)
    label_name = os.path.basename(label_file)
    cv2.imwrite(os.path.join(target_dir, 'images/val', image_name), image)

    with open(os.path.join(target_dir, 'labels/val', label_name), 'w') as f:
        f.writelines(labels)

def main():
    os.makedirs(os.path.join(target_dir, 'images/val'), exist_ok=True)
    os.makedirs(os.path.join(target_dir, 'labels/val'), exist_ok=True)

    
    for label_file in os.listdir(label_dir):
        if label_file.endswith('.txt'):
            image_file = os.path.join(image_dir, label_file.replace('.txt', '.jpg'))  
            label_path = os.path.join(label_dir, label_file)
            
            if os.path.exists(image_file):
                process_image(label_path, image_file)

if __name__ == '__main__':
    main()
