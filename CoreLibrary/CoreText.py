import cv2
import io
import os
from PIL import Image
import pytesseract
import numpy as np

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./private/GoogleVision-0b272261a65c.json"

def google_ocr(src_path):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), src_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    full_text = texts[0].description
    result = []

    for text in texts[0:-1]:
        result.append(text.description)
    return result, full_text

def simple_img2text(src_path):
    img = Image.open(src_path)
    text = pytesseract.image_to_string(img, lang="eng")
    return text

def img2text(src_path, write_path):
    #read image with opencv
    img = cv2.imread(src_path)

    #covert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #apply dilation and erosion to remove noise
    kernel = np.ones((1,1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    #apply threshold
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # img = cv2.Canny(img, 100, 200)
    # img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, (5, 5))
    cv2.imwrite(os.path.join(write_path, "thres.png"), img)

    #recognize text
    result = pytesseract.image_to_string(Image.open(os.path.join(write_path, "thres.png")))
    return result


