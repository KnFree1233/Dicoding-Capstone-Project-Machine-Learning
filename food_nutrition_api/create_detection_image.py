import numpy as np
import cv2
import uuid
import os

def create_detection_image(image, food_results, coin_result, output_dir):
    img = np.array(image)
    coin_box = coin_result["coin_box"].reshape(1, 4)
    coin_mask = coin_result["coin_mask"].reshape(1, 640, 480)

    combine_boxes = np.concatenate((food_results["food_boxes"], coin_box), axis=0)
    combine_masks = np.concatenate((food_results["food_masks"], coin_mask), axis=0)
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