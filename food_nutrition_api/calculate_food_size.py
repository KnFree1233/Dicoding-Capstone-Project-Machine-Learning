import numpy as np
from tools import get_size_px, get_median_depth

FOOD_DENSITY = 1

def calculate_food_size(food_results, depth_map, size_cm_per_px):
    real_food_sizes = []
    for mask in food_results['resize_food_masks']:
        # Calculate food height
        mask_depth = depth_map[mask > 0]
        depth_value_top = np.min(mask_depth)
        depth_value_bottom = np.max(mask_depth)
        object_height = abs(depth_value_bottom - depth_value_top)

        # Get pixel area from mask
        object_pixel_area = np.count_nonzero(mask)

        food_height = object_height * size_cm_per_px["cm_per_depth_unit"]
        food_area = object_pixel_area * (size_cm_per_px["cm_per_px_length"] ** 2)
        food_volume = food_area * food_height
        food_weight = food_volume * FOOD_DENSITY
        real_food_sizes.append({
            "height": food_height,
            "area": food_area,
            "volume": food_volume,
            "weight": food_weight,
        })

    return real_food_sizes