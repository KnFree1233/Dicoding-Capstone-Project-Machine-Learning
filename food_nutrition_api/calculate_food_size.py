from tools import get_size_px, get_median_depth

FOOD_DENSITY = 1

def calculate_food_size(food_results, depth_map, size_cm_per_px):
    real_food_sizes = []
    for mask in food_results['resize_food_masks']:
        object_size = get_size_px(mask)
        object_depth = get_median_depth(mask, depth_map)
        object_size["depth"] = object_depth

        food_length = object_size["length"] * size_cm_per_px["cm_per_px_length"]
        food_width = object_size["width"] * size_cm_per_px["cm_per_px_width"]
        food_depth = object_size["depth"] * size_cm_per_px["cm_per_depth_unit"]
        food_area = food_length * food_width
        food_volume = food_length * food_width * food_depth
        food_weight = food_volume * FOOD_DENSITY
        real_food_sizes.append({
            "length": food_length,
            "width": food_width,
            "depth": food_depth,
            "area": food_area,
            "volume": food_volume,
            "weight": food_weight,
        })

    return real_food_sizes