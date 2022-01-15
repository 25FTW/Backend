#   ------25FTW Project------
#   ------pips------
import cv2
#   from google.colab.patches import cv2_imshow
#   from google.colab import files
#   from googletrans import Translator
#   import pyttsx3 as txt
#   from PIL import Image
import pytesseract
import numpy as np
from string import digits
'''python - m pip install pytesseract
python - m pip install pyttsx3
sudo apt install tesseract-ocr
python - m pip install - -upgrade pip
python - m pip install - -upgrade Pillow'''

#   ------libraries------

# ---enter image here---
#   ------extra:------img = Image.open('a.jpg')  ------


def runOCR(filename):
    img = cv2.imread(filename, -1)  # PUT IMAGE HERE instead of a.jpg

    rgb_planes = cv2.split(img)

    #   ------removing noise and shadows------
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(
            diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
            dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    print(result_planes)
    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    _,img = cv2.threshold(result_norm, 195, 255, cv2.THRESH_TOZERO)
    #   cv2.imshow('frame', img)
    #   cv2.waitKey(0)
    #   ------conversion------
    fileNametmp = "D:/Program Files/Tesseract-OCR/tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = fileNametmp
    result = pytesseract.image_to_string(img, lang="eng", config='--psm 6')

    print(result)  # image to text successful

    #   ------itemization of text-----
    ress = result.split('\n')
    item = []
    price = []
    for i in ress:
        res1 = True if next(
            (chr for chr in i if chr.isdigit()), None) else False
        res2 = True if next(
            (chr for chr in i if chr.isalpha()), None) else False
        if "total" in i.lower():
            break
        if res1 and res2:
            o = i.split(' ')
            price.append(o[-1])
            remove_digits = str.maketrans('', '', digits)
            it = " ".join(o[:-1]).translate(remove_digits)  
            item.append(it)

    #       ------Item and price list  ------
    print(item, price)
    return [item, price]


#   runOCR('sample.jpeg')
