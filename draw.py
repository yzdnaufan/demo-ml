
import base64
import cv2
import io
import requests

import numpy as np
from PIL import Image

from firestore import GetImageFromFirestore
from main import url as u, headers as h, data as d

def draw_boxes(bytes_image : bytes, result):

    nparr = np.frombuffer(bytes_image, np.uint8)

    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height, width, _ = img_cv.shape

    # Iterate over the detected objects
    for obj in result['data']:
        # Get the bounding box coordinates
        x, xx, y, yy = obj['box'].values()

        # x1 = int(x) - int(w/2) if int(x) - int(w/2) > 0 else 0
        # y1 = int(y) - int(h/2) if int(y) - int(h/2) > 0 else 0

        # x2 = int(x) + int(w/2) if int(x) + int(w/2) < width else width
        # y2 = int(y) + int(h/2) if int(y) + int(h/2) < height else height

        # Draw the bounding box
        # cv2.rectangle(img_cv,(int(x),int(y)),(int(w), int(h)),  lineType=cv2.LINE_AA, color=(0, 255, 0), thickness=2)
        cv2.rectangle(img_cv,(int(x),int(y)),(int(xx), int(yy)),  lineType=cv2.LINE_AA, color=(0, 255, 0), thickness=2)

        # Optionally, add a label
        # label = obj['label']
        # cv2.putText(img_cv, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Assuming 'image' is your OpenCV image
    retval, buffer = cv2.imencode('.jpg', img_cv)

    # Convert to base64
    img_base64 = base64.b64encode(buffer).decode()

    # If you want to get a data URL
    img_data_url = 'data:image/jpeg;base64,' + img_base64
    
    return img_data_url, width, height

def draw_from_firestore(id):
    # Load image
    img_enc = GetImageFromFirestore(idRef=id).split(',')[1]
    img_decoded = io.BytesIO(base64.b64decode(img_enc))

    response = requests.post(u, headers=h, data=d, files={"image": img_decoded})

    # Check for successful response
    response.raise_for_status()

    # Print inference results
    # print(json.dumps(response.json(), indent=2))

    # Draw bounding boxes and labels on image
    # result = response.json()
    img_decoded.seek(0)
    im = img_decoded.read()

    result = response.json()

    b64_result, width, height = draw_boxes(im, result)

    # with open('./test/img.jpeg', "rb") as binary_file:
    #     binary_data = binary_file.read()
    #     encoded_data = base64.b64encode(binary_data).decode()

    data = { 'image' : b64_result, 'count' : len(response.json()["data"])}

    return data