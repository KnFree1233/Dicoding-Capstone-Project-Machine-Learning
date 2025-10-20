import requests

url = "https://muticous-loralee-formlessly.ngrok-free.dev/predict/"
files = {'file': open(r"sample/food-coin-13.jpg", 'rb')}
res = requests.post(url, files=files)
print(res.json())