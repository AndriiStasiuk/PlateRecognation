import cv2
import pytesseract

from image_gw_api.cascade_classifiers import DEFAULT_CLASSIFIER
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"/usr/local/Cellar/tesseract/4.1.1/bin/tesseract"


class ImageProcessor:

    def __init__(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.car_plate_cascade_classifier = DEFAULT_CLASSIFIER
        self.car_plate = None

    def _extract_car_plate(self):
        car_plate_rects = self.car_plate_cascade_classifier.detectMultiScale(
            self.image, scaleFactor=1.1, minNeighbors=5
        )
        car_plate_img = None

        for x, y, w, h in car_plate_rects:
            car_plate_img = self.image[y + 15:y + h - 10, x + 15:x + w - 20]

        return car_plate_img

    @staticmethod
    def _enlarge_img(image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image

    def process_image(self):
        car_plate_img = self._enlarge_img(self._extract_car_plate(), 150)
        car_plate_gray = cv2.cvtColor(car_plate_img, cv2.COLOR_RGB2GRAY)
        blurred_car_plate = cv2.medianBlur(car_plate_gray, 3)

        binary_image = cv2.threshold(blurred_car_plate, 130, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        inverted_bin = cv2.bitwise_not(binary_image)

        kernel = np.ones((2, 2), np.uint8)
        processed_img = cv2.erode(inverted_bin, kernel, iterations=1)
        processed_img = cv2.dilate(processed_img, kernel, iterations=1)

        self.car_plate = pytesseract.image_to_string(
            processed_img, config=f'--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЯЧСМИТЬ'
                                  f'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ).rstrip("\n\f")

        return self.car_plate

