import numpy as np
from tools import resize_mask

def predict_coin(image, model):
    results =  model(image)
    if results[0].boxes is None or len(results[0].boxes) == 0:
        return None

    # Get food confidences
    coin_confidences = results[0].boxes.conf.cpu().numpy()
    coin_confidences = coin_confidences.tolist()

    # Get coin with best confidence
    best_idx = np.argmax(coin_confidences)
    best_coin_conf = coin_confidences[best_idx]

    # Get food id and class name
    coin_class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    coin_class_id = coin_class_ids[best_idx]
    coin_class_name = results[0].names[coin_class_id]

    # Get food masks
    coin_mask = results[0].masks.data[best_idx].cpu().numpy()
    coin_mask = ((coin_mask > 0.5).astype(np.uint8)) * 255

    # Resize coin mask to original image size
    h, w = results[0].orig_shape
    resize_coin_mask = resize_mask(coin_mask, h, w)

    # Get coin box
    coin_box = results[0].boxes.xyxy[best_idx].cpu().numpy()

    coin_result = {
        "coin_class_id": coin_class_id,
        "coin_class_name": coin_class_name,
        "coin_confidence": best_coin_conf,
        "coin_mask": coin_mask,
        "resize_coin_mask": resize_coin_mask,
        "coin_box": coin_box,
    }

    return coin_result