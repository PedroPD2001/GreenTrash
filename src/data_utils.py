import cv2
import numpy as np
import hashlib
import os
from collections import Counter

def load_images_from_folder(folder_path, class_name):
    images = []
    if not os.path.exists(folder_path):
        return images
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.avif')
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                img = cv2.imread(file_path)
                if img is not None:
                    images.append((img, class_name))
            except Exception as e:
                pass
    
    return images

def calculate_image_hash(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (8, 8))
    avg = resized.mean()
    binary = (resized > avg).astype(np.uint8)
    hash_str = ''.join(str(b) for b in binary.flatten())
    return hashlib.md5(hash_str.encode()).hexdigest()

def detect_duplicates(images_with_labels):
    seen_hashes = {}
    duplicates = []
    unique_images = []
    
    for idx, (img, label) in enumerate(images_with_labels):
        img_hash = calculate_image_hash(img)
        if img_hash in seen_hashes:
            duplicates.append(idx)
        else:
            seen_hashes[img_hash] = idx
            unique_images.append((img, label))
    
    return unique_images, duplicates

def assess_image_quality(image):
    if image is None or image.size == 0:
        return 0.0
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    brightness = np.mean(gray)
    brightness_score = 1.0 - abs(brightness - 127.5) / 127.5
    
    contrast = np.std(gray) / 255.0
    
    quality_score = (laplacian_var / 100.0) * 0.5 + brightness_score * 0.25 + contrast * 0.25
    return min(1.0, max(0.0, quality_score))

def filter_low_quality(images_with_labels, min_quality=0.3):
    filtered = []
    removed = []
    
    for idx, (img, label) in enumerate(images_with_labels):
        quality = assess_image_quality(img)
        if quality >= min_quality:
            filtered.append((img, label))
        else:
            removed.append((idx, quality))
    
    return filtered, removed

def augment_image(image, augmentation_type='flip'):
    if augmentation_type == 'flip':
        return cv2.flip(image, 1)
    elif augmentation_type == 'rotate_light':
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), np.random.uniform(-15, 15), 1.0)
        return cv2.warpAffine(image, M, (w, h))
    elif augmentation_type == 'brightness':
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] = np.clip(hsv[:,:,2] * np.random.uniform(0.8, 1.2), 0, 255)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    elif augmentation_type == 'contrast':
        alpha = np.random.uniform(0.9, 1.1)
        beta = np.random.uniform(-10, 10)
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return image

def balance_classes_with_augmentation(images_with_labels, target_samples_per_class=None):
    if len(images_with_labels) == 0:
        return images_with_labels
    
    class_counts = Counter([label for _, label in images_with_labels])
    
    if target_samples_per_class is None:
        target_samples_per_class = max(class_counts.values())
    
    augmented_data = []
    augmentation_types = ['flip', 'rotate_light', 'brightness', 'contrast']
    
    for class_name in class_counts:
        current_count = class_counts[class_name]
        class_images = [(img, label) for img, label in images_with_labels if label == class_name]
        
        if current_count < target_samples_per_class and current_count > 0:
            needed = target_samples_per_class - current_count
            augment_per_image = max(1, min(needed // current_count, 2))
            
            for img, label in class_images:
                for _ in range(augment_per_image):
                    aug_type = np.random.choice(augmentation_types)
                    aug_img = augment_image(img.copy(), aug_type)
                    augmented_data.append((aug_img, label))
    
    return images_with_labels + augmented_data

