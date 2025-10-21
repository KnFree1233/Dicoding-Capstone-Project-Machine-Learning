import numpy as np
import cv2
import uuid
import os
from PIL import ImageOps
from tools import resize_mask, resize_bbox


def create_detection_image(image, food_results, coin_result, output_dir):
    old_w, old_h = image.size

    # Delete EXIF
    image = ImageOps.exif_transpose(image)

    target_height = 640
    target_width = int(target_height * 3 / 4)
    image = image.resize((target_width, target_height))
    img = np.array(image)

    food_masks_resize = []
    for food_mask in food_results['food_masks']:
        food_masks_resize.append(resize_mask(food_mask, target_height, target_width))
    food_masks_resize = np.array(food_masks_resize)

    food_bboxes_resize = []
    for food_bboxes in food_results['food_boxes']:
        food_bboxes_resize.append(resize_bbox(food_bboxes, old_w, old_h, target_width, target_height))
    food_bboxes_resize = np.array(food_bboxes_resize)

    coin_mask_resize = resize_mask(coin_result["coin_mask"], target_height, target_width)
    coin_bboxes_resize = resize_bbox(coin_result["coin_box"], old_w, old_h, target_width, target_height)

    coin_box = np.expand_dims(coin_bboxes_resize, axis=0)
    coin_mask = np.expand_dims(coin_mask_resize, axis=0)

    combine_boxes = np.concatenate((food_bboxes_resize, coin_box), axis=0)
    combine_masks = np.concatenate((food_masks_resize, coin_mask), axis=0)
    combine_class_name = np.concatenate([food_results["food_class_names"], [coin_result["coin_class_name"]]], axis=0)
    combine_confidences = np.concatenate([food_results["food_confidences"], [coin_result["coin_confidence"]]], axis=0)

    # Loop combine result
    for i in range(len(combine_boxes)):
        box = combine_boxes[i]
        mask = combine_masks[i]
        cls_name = combine_class_name[i]
        conf = combine_confidences[i]

        # Coloring each object
        color = tuple(np.random.randint(0, 255, 3).tolist())

        # --- Draw Mask ---
        mask_resized = cv2.resize(mask.astype(np.uint8), (img.shape[1], img.shape[0]))
        img[mask_resized > 0.5] = (
                img[mask_resized > 0.5] * 0.5 + np.array(color) * 0.5
        ).astype(np.uint8)

        # --- Draw Bounding Box ---
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # --- Draw Label ---
        label = f"{cls_name} {conf:.2f}"
        font_scale = 1.2
        font_thickness = 3
        text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_w, text_h = text_size

        # Background for texts
        cv2.rectangle(img, (x1, y1 - text_h - 10), (x1 + text_w + 5, y1), color, -1)
        cv2.putText(
            img, label, (x1 + 2, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness
        )

    filename = f"{uuid.uuid4().hex}.jpg"
    save_path = os.path.join(output_dir, filename)

    cv2.imwrite(save_path, img)

    return filename