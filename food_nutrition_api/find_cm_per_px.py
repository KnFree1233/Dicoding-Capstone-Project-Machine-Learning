import cv2
import numpy as np
from tools import get_size_px, get_median_depth

# Value in cm
REAL_COIN_DIAMETER = 2.41
REAL_COIN_THICKNESS = 0.16

def find_cm_per_px(coin_mask, depth_map):
    coin_size = get_size_px(coin_mask)
    coin_depth = get_median_depth(coin_mask, depth_map)

    # Get cm/px for length and width
    length_pixel = coin_size["length"]
    width_pixel = coin_size["width"]
    cm_per_px_length = REAL_COIN_DIAMETER / length_pixel
    cm_per_px_width = REAL_COIN_DIAMETER / width_pixel

    # Get background mask depth score around coin mask
    bg_only = (coin_mask == 0)
    near_coin = cv2.dilate(coin_mask, np.ones((25, 25), np.uint8))  # add padding around coin mask
    ring_bg = np.logical_and(near_coin, bg_only)
    bg_depth = np.median(depth_map[ring_bg])

    # Get cm/depth unit for depth
    depth_difference = abs(coin_depth - bg_depth)
    cm_per_depth_unit = REAL_COIN_THICKNESS / depth_difference

    result = {"cm_per_px_length": cm_per_px_length,
              "cm_per_px_width": cm_per_px_width,
              "cm_per_depth_unit": cm_per_depth_unit}
    return result