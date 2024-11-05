import os
import shutil


classes_of_interest = [0, 1, 2, 3, 4, 5, 6, 7]  


input_labels_dir = '../Project/yoloData/yoloData/labels/val'  
input_images_dir = '../Project/yoloData/yoloData/images/val'  
output_labels_dir = './custom_dataset/labels/val'  
output_images_dir = './custom_dataset/images/val'  


os.makedirs(output_labels_dir, exist_ok=True)
os.makedirs(output_images_dir, exist_ok=True)


for label_file in os.listdir(input_labels_dir):
    if label_file.endswith('.txt'):
        label_path = os.path.join(input_labels_dir, label_file)
        
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        
        filtered_lines = [line for line in lines if int(line.split()[0]) in classes_of_interest]
        
        if filtered_lines:
            
            output_label_path = os.path.join(output_labels_dir, label_file)
            image_file = label_file.replace('.txt', '.jpg')  
            input_image_path = os.path.join(input_images_dir, image_file)
            output_image_path = os.path.join(output_images_dir, image_file)
            
            
            with open(output_label_path, 'w') as f:
                f.writelines(filtered_lines)
            
            
            if os.path.exists(input_image_path):
                shutil.copy(input_image_path, output_image_path)
            else:
                print(f"Image file {image_file} not found!")

print("Processing complete.")
