from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.cloud import secretmanager

import json
import base64
import requests
import PIL.Image as Image
import io

from img import img_64
from draw import draw_boxes

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    image: str

# GET request

@app.get("/")
async def root():
    return {"message": "Hello World"}


# POST request

@app.post("/demo")
# def receive_data( data: Data):
async def receive_data():

    # 1. Receive data from the client
    # image64 = data.image
    image64 = img_64.split(",")[1]

    # 2. Process the data
    count = 0
    result_b64 = "base64 image"

    # Create the Secret Manager client.
    # client = secretmanager.SecretManagerServiceClient()

    # Run inference on an image
    # api_key = client.access_secret_version(request={"name": "ULTRALYTICS_SECRET"})

    url = "https://api.ultralytics.com/v1/predict/ipyo4cywDcA7LgB4Zy1n"
    headers = {"x-api-key": "b72997cc481dfa7aa0c6c856c8532ecb301ef68f55"}

    data = {"size": 640, "confidence": 0.25, "iou": 0.45}

    # with open("path/to/image.jpg", "rb") as f:
    #     re = 1       
    
    img_decoded = io.BytesIO(base64.b64decode(image64))

    response = requests.post(url, headers=headers, data=data, files={"image": img_decoded})

    # Check for successful response
    response.raise_for_status()

    # Print inference results
    # print(json.dumps(response.json(), indent=2))

    # Draw bounding boxes and labels on image
    # result = response.json()
    img_decoded.seek(0)
    im = img_decoded.read()

    result = response.json()

    b64_result, w, h = draw_boxes(im, result)

    x, y, x2, y2 = response.json()["data"][0]['box'].values()

    # 3. Send some data back to the client
    return {
         "x": x,
        "y": y,
        "x2": x2,
        "y2": y2,
        "witdh" : w,
        "height" : h,
        "count": len(response.json()["data"]),
        "image": b64_result
    }