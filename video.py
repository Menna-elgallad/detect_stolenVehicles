from algorithm.object_detector import YOLOv7
from utils.detections import draw
from tqdm import tqdm
from paddleocr import PaddleOCR
import cv2
import re
import json

yolov7 = YOLOv7()


ocr = PaddleOCR(use_angle_cls=True, lang="arabic")
yolov7.load('best.weights', classes='classes.yaml',
            device='cpu')


def check_validty(text):
    if (len(text.replace(" ", "")) == 6 or len(text.replace(" ", "")) == 7):
        arabic_pattern = re.compile(
            r'[\u0600-\u06FF]+')  # Matches Arabic letters
        number_pattern = re.compile(r'\d+')  # Matches numbers (digits)

        contains_arabic = arabic_pattern.search(text) is not None
        contains_numbers = number_pattern.search(text) is not None

        return contains_arabic and contains_numbers
    else:
        return False


final_data = {'carsData': []}
videos = ['street 2.mp4', 'street 1.mp4', 'street 3.mp4']
for v in videos:
    video = cv2.VideoCapture(v)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frames_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv2.VideoWriter('output6.mp4', fourcc, fps, (width, height))

    if video.isOpened() == False:
        print('[!] error opening the video')

    print('[+] started reading text on the video...\n')
    pbar = tqdm(total=frames_count, unit=' frames',
                dynamic_ncols=True, position=0, leave=True)
    texts = {}

    alltext = []
    try:
        while video.isOpened():
            ret, frame = video.read()
            if ret == True:
                # Detect text with PaddleOCR

                detections = yolov7.detect(frame)
                detected_frame = draw(frame, detections)
                output.write(detected_frame)
                pbar.update(1)
                result = ocr.ocr(frame)
                print(result)
                for sublist in result:
                    for subsublist in sublist:
                        arabic = subsublist[1][0]
                        is_arabic = all('\u0600' <= char <= '\u06FF' or '\u0750' <=
                                        char <= '\u077F' for char in arabic if char != ' ')
                        if is_arabic:
                            print(arabic)
                            alltext.append(arabic)
                # text = [item[1][0] for sublist in result for item in sublist]

                # all.append(text)
                # # for item in result:
                #     print("item", item)
            else:
                break
                pbar.update(1)
    except KeyboardInterrupt:
        pass

    pbar.close()
    video.release()
    output.release()
    yolov7.unload()

    # print(alltext)

    my_data = []
    for x in alltext:
        if check_validty(x) == True:
            my_data.append(" ".join(x.replace(" ", "")))

    my_set = set(my_data)
    print(my_set)
    for x in my_set:
        final_data['carsData'].append(
            {'plate': x, "location": v.replace(".mp4", "")})


# print(data)
file_path = "data.json"

with open(file_path, "w", encoding="utf-8") as json_file:
    json.dump(final_data, json_file, ensure_ascii=False)

print("Data has been written to", file_path)
