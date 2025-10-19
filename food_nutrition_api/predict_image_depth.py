import torch
import numpy as np

def predict_image_depth(midas, transform, image):
    # Convertion from PIL to NumPy (format RGB)
    img = np.array(image)
    input_batch = transform(img).to("cpu")

    with torch.no_grad():
        prediction = midas(input_batch)

    # Resize back to original image size
    prediction = torch.nn.functional.interpolate(
        prediction.unsqueeze(1),
        size=img.shape[:2],
        mode="bicubic",
        align_corners=False,
    ).squeeze()

    depth_map = prediction.cpu().numpy()
    return depth_map