
import cv2
import numpy as np
import base64


def draw_boxes(bytes_image : bytes, result):

    nparr = np.frombuffer(bytes_image, np.uint8)

    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height, width, _ = img_cv.shape

    # Iterate over the detected objects
    for obj in result['data'][0:2]:
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