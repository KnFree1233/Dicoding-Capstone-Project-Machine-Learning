# Dicoding-Capstone-Project-Machine-Learning
This project was developed as part of the Machine Learning Capstone Project for Dicoding Indonesia’s Machine Learning Batch 8 program

# Food Nutrition API
To host the API, first need to run this command:<br>
pip install fastapi uvicorn torch torchvision torchaudio ultralytics timm Pillow starlette opencv-python matplotlib

# Dataset
The dataset used in this project:<br>
- Food Segmentation from Robotflow<br>
https://universe.roboflow.com/yolov11-food-image-segmentation/yolov11-instance-seg-seismiks
- Coin Segmentation from Robotflow<br>
https://universe.roboflow.com/myimages-ikmlt/coins-segmentation-4cqs9
- Coin Segmentation from manual photo 1000 rupiah

# Classes
The dataset for food segmentation consists of 18 classes, as listed below:
- 0 - Ayam Goreng - Dada
- 1 - Ayam Goreng - Paha
- 2 - Ayam Goreng - Sayap
- 3 - French Fries
- 4 - Jagung
- 5 - Lalapan
- 6 - Lele Goreng
- 7 - Mashed Potato
- 8 - Nasi Putih
- 9 - Pisang
- 10 - Pizza
- 11 - Roti Putih
- 12 - Sambal
- 13 - Saus Tomat
- 14 - Steak Sapi
- 15 - Tahu Goreng
- 16 - Telor Ceplok
- 17 - Tempe

The dataset for coin segmentation consists of 1 class, as listed below:
- 0 - coin

# Food Nutrition per Gram
This nutritional information was obtained with the help of ChatGPT and may not be fully accurate
| No | Food Name           | Calories (g)  | Protein (g) | Carbs (g)       | Fat (g)   |
| -- | ------------------- | ------------- | ----------- | --------------- | --------- |
| 1  | Ayam Goreng - Dada  | 1.87          | 0.334       | 0.005           | 0.047     |
| 2  | Ayam Goreng - Paha  | 1.79          | 0.25        | 0.000           | 0.082     |
| 3  | Ayam Goreng - Sayap | 2.03          | 0.305       | 0.000           | 0.081     |
| 4  | French Fries        | 2.74          | 0.035       | 0.357           | 0.141     |
| 5  | Jagung              | 0.96          | 0.034       | 0.190           | 0.015     |
| 6  | Lalapan             | 0.25          | 0.015       | 0.040           | 0.003     |
| 7  | Lele Goreng         | 2.75          | 0.180       | 0.000           | 0.190     |
| 8  | Mashed Potato       | 2.00          | 0.045       | 0.330           | 0.080     |
| 9  | Nasi Putih          | 1.30          | 0.027       | 0.280           | 0.003     |
| 10 | Pisang              | 0.89          | 0.011       | 0.230           | 0.003     |
| 11 | Pizza               | 2.66          | 0.110       | 0.330           | 0.100     |
| 12 | Roti Putih          | 2.65          | 0.090       | 0.490           | 0.032     |
| 13 | Sambal              | 0.80          | 0.015       | 0.120           | 0.050     |
| 14 | Saus Tomat          | 0.90          | 0.015       | 0.210           | 0.002     |
| 15 | Steak Sapi          | 2.50          | 0.270       | 0.000           | 0.160     |
| 16 | Tahu Goreng         | 1.80          | 0.100       | 0.030           | 0.120     |
| 17 | Telor Ceplok        | 1.55          | 0.130       | 0.011           | 0.110     |
| 18 | Tempe               | 2.10          | 0.190       | 0.090           | 0.115     |

