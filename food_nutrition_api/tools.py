import numpy as np
import cv2

FOODS_NUTRITION_PER_GRAM = {
    "Ayam Goreng - Dada": {"calories": 1.87, "protein": 0.334, "carbs": 0.005, "fat": 0.047},
    "Ayam Goreng - Paha": {"calories": 1.79, "protein": 0.25, "carbs": 0.0, "fat": 0.082},
    "Ayam Goreng - Sayap": {"calories": 2.03, "protein": 0.305, "carbs": 0.0, "fat": 0.081},
    "French Fries": {"calories": 2.74, "protein": 0.035, "carbs": 0.357, "fat": 0.141},
    "Jagung": {"calories": 0.96, "protein": 0.034, "carbs": 0.19, "fat": 0.015},
    "Lalapan": {"calories": 0.25, "protein": 0.015, "carbs": 0.04, "fat": 0.003},
    "Lele Goreng": {"calories": 2.75, "protein": 0.18, "carbs": 0.0, "fat": 0.19},
    "Mashed Potato": {"calories": 2.0, "protein": 0.045, "carbs": 0.33, "fat": 0.08},
    "Nasi Putih": {"calories": 1.3, "protein": 0.027, "carbs": 0.28, "fat": 0.003},
    "Pisang": {"calories": 0.89, "protein": 0.011, "carbs": 0.23, "fat": 0.003},
    "Pizza": {"calories": 2.66, "protein": 0.11, "carbs": 0.33, "fat": 0.10},
    "Roti Putih": {"calories": 2.65, "protein": 0.09, "carbs": 0.49, "fat": 0.032},
    "Sambal": {"calories": 0.80, "protein": 0.015, "carbs": 0.12, "fat": 0.05},
    "Saus Tomat": {"calories": 0.90, "protein": 0.015, "carbs": 0.21, "fat": 0.002},
    "Steak Sapi": {"calories": 2.50, "protein": 0.27, "carbs": 0.0, "fat": 0.16},
    "Tahu Goreng": {"calories": 1.80, "protein": 0.10, "carbs": 0.03, "fat": 0.12},
    "Telor Ceplok": {"calories": 1.55, "protein": 0.13, "carbs": 0.011, "fat": 0.11},
    "Tempe": {"calories": 2.10, "protein": 0.19, "carbs": 0.09, "fat": 0.115}
}

def resize_mask(mask, h, w):
    convert_mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
    return convert_mask

def get_size_px(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=cv2.contourArea)
    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
    length_px = np.linalg.norm(np.array(leftmost) - np.array(rightmost))
    width_px = np.linalg.norm(np.array(topmost) - np.array(bottommost))
    object_size = {"length": length_px, "width": width_px}

    return object_size

def get_median_depth(mask, depth_map):
    object_depth = np.median(depth_map[mask > 0])
    return object_depth

def get_food_nutrition_per_gram():
    return FOODS_NUTRITION_PER_GRAM