import io
import torch
import os
from mimetypes import guess_type
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
from starlette.responses import JSONResponse
from ultralytics import YOLO
from food_segmentation import predict_food
from coin_segmentation import predict_coin
from predict_image_depth import predict_image_depth
from find_cm_per_px import find_cm_per_px
from calculate_food_size import calculate_food_size
from nutrition_estimation import nutrition_estimation
from create_detection_image import create_detection_image

torch.hub.set_dir("model/midas")
food_model = None
coin_model = None
midas = None
transform = None
status = False

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global food_model, coin_model, midas, transform, status
    status = False
    print("Initialization model...")
    food_model = YOLO("model/yolo_food_segmentation_model/best.pt")
    coin_model = YOLO("model/yolo_coin_segmentation_model/best.pt")
    midas = torch.hub.load("intel-isl/MiDaS", "DPT_Large")
    transform = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = transform.dpt_transform
    status = True
    print("Server Ready!")
    yield
    print("Server Shutdown!")
    status = False

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": f"Server {'Active' if status else 'Inactive'}"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not status:
        return {"message": "Server Inactive"}

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        print(f"Error reading image: {e}")
        return JSONResponse(status_code=400, content={"error": "Invalid image file"})

    food_results = predict_food(image, food_model)
    if food_results is None:
        return {"message": "No food detected"}
    coin_result = predict_coin(image, coin_model)
    if coin_result is None:
        return {"message": "No coin detected"}

    depth_map = predict_image_depth(midas, transform, image)
    size_cm_per_px = find_cm_per_px(coin_result["resize_coin_mask"], depth_map)
    real_food_sizes = calculate_food_size(food_results, depth_map, size_cm_per_px)

    food_nutrition_results = nutrition_estimation(food_results, real_food_sizes)
    img_filename =  create_detection_image(image, food_results, coin_result, OUTPUT_DIR)

    return {
        "message": "Success",
        "food_nutrition_results": food_nutrition_results,
        "image_filename": img_filename,
    }

@app.get("/result/{filename}")
async def get_result_image(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    mime_type, _ = guess_type(path)
    return FileResponse(path, media_type=mime_type or "application/octet-stream")