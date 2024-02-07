import os
import json
import logging

import cv2
import torch
from paddleocr import PaddleOCR


class Updater:
    def __init__(self):
        ocr_logger = logging.getLogger('ppocr')
        ocr_logger.setLevel(logging.WARN)

        gpu = True if torch.cuda.is_available() else False
        self.ocr_engine = PaddleOCR(use_angle_cls=True, lang='en', use_gpu = gpu, use_space_char =True, ocr_version = 'PP-OCRv4')


    def ocr(self, image, x1, y1, x2, y2):
        cropped_image = image[x2:y2, x1:y1]

        result = self.ocr_engine.ocr(cropped_image, cls=True)

        try:
            page_txt_list = []
            for t in result[0]:
                page_txt_list.append(t[1][0])

            return " ".join(page_txt_list)
        except:
            print(x1, x2, y1, y2)
            cv2.imwrite(f"{x1}_{x2}_{y1}_{y2}.jpg", cropped_image)
            return ""
    

    def update(self, image_path, json_path, new_json_path):
        os.makedirs(new_json_path, exist_ok=True)

        for js in os.listdir(json_path):
            json_file_path = os.path.join(json_path, js)

            print(json_file_path)
            
            with open(json_file_path, 'r') as f:
                data = json.load(f)

            image_file_path = os.path.join(image_path, js.replace('json', 'jpg'))
            image = cv2.imread(image_file_path)

            for i in range(len(data["words"])):
                x1, y1, x2, y2 = data["words"][i]["rect"]["x1"], data["words"][i]["rect"]["x2"], data["words"][i]["rect"]["y1"], data["words"][i]["rect"]["y2"]
                new_ocr_value = self.ocr(image, x1, y1, x2, y2)
                data["words"][i]["value"] = new_ocr_value

            with open(os.path.join(new_json_path, js), 'w') as f:
                json.dump(data, f)
            
            break