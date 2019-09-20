import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import urllib
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def ExtractNumbers(List):
    for index, Row in List.iterrows():
        getimage = urllib.request.urlopen(Row[0])
        myImg = np.array(Image.open(getimage))
        Images.append(myImg)
        xt = Row[1][0]['x'] * myImg.shape[1]
        yt = Row[1][0]['y'] * myImg.shape[0]
        xb = Row[1][1]['x'] * myImg.shape[1]
        yb = Row[1][1]['y'] * myImg.shape[0]
        origImage = Image.fromarray(myImg)
        plateImage = origImage.crop((xt, yt, xb, yb))
        Plates.append(np.array(plateImage))
        plateImage.save('image.png')
        img = cv2.imread('image.png')
        img = cv2.resize(img, (int(img.shape[1] * 4), int(img.shape[0] * 4)))
        Num = pytesseract.image_to_string(img)
        print(Num)
        Numbers.append(Num)
Images = []
Plates = []
Numbers = []
if __name__ == "__main__":
    List = pd.read_json('Indian_Number_plates.json', lines=True)
    pd.set_option('display.max_colwidth', -1)
    del List['extras']
    List['points'] = List.apply(lambda Row: Row['annotation'][0]['points'], axis=1)
    del List['annotation']
    ExtractNumbers(List)
