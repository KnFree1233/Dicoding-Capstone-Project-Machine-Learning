import numpy as np
from tools import resize_mask

def predict_food(image, model):
    results =  model(image)
    if results[0].boxes is None or len(results[0].boxes) == 0:
        return None

    # Get food id and class name
    food_class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    food_class_names = [results[0].names[class_id] for class_id in food_class_ids]

    # Get food confidences
    food_confidences = results[0].boxes.conf.cpu().numpy()
    food_confidences = food_confidences.tolist()

    # Get food masks
    food_masks = results[0].masks.data.cpu().numpy()
    food_masks = ((food_masks > 0.5).astype(np.uint8)) * 255

    # Resize coin mask to original image size
    resize_food_masks = []
    h, w = results[0].orig_shape

    for food_mask in food_masks:
        convert_mask = resize_mask(food_mask, h, w)
        resize_food_masks.append(convert_mask)
    resize_food_masks = np.array(resize_food_masks)

    # Get food boxes
    food_boxes = results[0].boxes.xyxy.cpu().numpy()

    food_results = {
        'food_class_ids': food_class_ids,
        'food_class_names': food_class_names,
        'food_confidences': food_confidences,
        'food_masks': food_masks,
        "resize_food_masks": resize_food_masks,
        "food_boxes": food_boxes,
    }

    return food_results