from flask import Flask, request, jsonify
from algorithm.object_detector import YOLOv7
from utils.detections import draw
import numpy as np
import cv2
import json
from paddleocr import PaddleOCR, draw_ocr
import imghdr
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
yolov7 = YOLOv7()
yolov7.load('best.weights', classes='classes.yaml', device='cpu')


file_path = "data.json"

with open(file_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)


def extract_strings(PaddleOCR_result):
    strings = []
    for element in PaddleOCR_result:
        if isinstance(element, str):
            strings.append(element)
        elif isinstance(element, list):
            strings += extract_strings(element)
        elif isinstance(element, tuple):
            strings += extract_strings(list(element))

    stringvar = " ".join(strings)
    string = stringvar.replace(' ', '')
    LicencePlateNumber = ' '.join([char for char in string])

    return LicencePlateNumber


def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)


def remove_borders(image):
    contours, heiarchy = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)


@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    image_data = file.read()

    # Detect the image format (JPEG or PNG) based on the file signature
    image_format = imghdr.what(None, image_data)

    # Check if the image format is supported (JPEG or PNG)
    if image_format not in ['jpeg', 'png']:
        return "Unsupported image format. Please upload a JPEG or PNG image."

    # Decode the image based on the detected format
    if image_format == 'jpeg':
        image = cv2.imdecode(np.fromstring(
            image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    else:
        # For PNG images, use the cv2.IMREAD_COLOR flag to load the image without alpha channel
        image = cv2.imdecode(np.fromstring(
            image_data, np.uint8), cv2.IMREAD_COLOR)
    detections = yolov7.detect(image)
    detected_image = draw(image, detections)
    retval, buffer = cv2.imencode('.jpg', detected_image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    json_data = json.dumps(detections)
    parsed_dict = json.loads(json_data)[0]
    x, y, width, height = parsed_dict["x"], parsed_dict["y"], parsed_dict["width"], parsed_dict["height"]

    cropped_image = image[y:y+height, x:x+width]
    res = cv2.resize(cropped_image, dsize=(270, 200),
                     interpolation=cv2.INTER_CUBIC)
    crop = res[80:200, 0:270]
    img = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = cv2.medianBlur(img, 1)  # Median blur to remove noise
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.medianBlur(img, 1)
    img = noise_removal(img)
    img = remove_borders(img)
    ocr = PaddleOCR(lang="ar")
    result = ocr.ocr(img)
    # print(result)
    # read, _ = result[0][0][1]
    read = extract_strings(result)
    text = " ".join(read.replace(" ", ""))
    print(text)
    # cv2.imshow("fg", detected_image)

    # cv2.imshow("crop", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    car_location = ""
    for ele in data['carsData']:
        if text == ele['plate']:
            print(ele['plate'], ele['location'])
            car_location = ele['location']
    if car_location == "":
        car_location = "not found in our cameras"
    mydata = {"response": image_base64,
              "car_location": car_location, "plate": text}
    return jsonify(mydata)


@app.route('/favicon.ico')
def favicon():
    return ''


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
