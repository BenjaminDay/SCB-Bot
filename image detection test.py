import pytesseract
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import cv2

mainloop = True
"""
while mainloop:
    locate = pyautogui.locateOnScreen('images/storage icon.png', region=(0,0,1920,1080), grayscale=True, confidence=0.8)
    if locate != None:
        print(locate)
        print(type(locate))
        print((locate.left, locate.top, locate.width, locate.height))
        time.sleep(0.5)
    else:
        print("I am unable to see it")
        time.sleep(0.5)
"""

def display_img(img, title):
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

img=cv2.imread(r'images\sampleinv.jpg')
#display_img(img, "source")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#display_img(gray, "grayscale")
bfilter = cv2.bilateralFilter(gray, 5, 5, 5) #Noise reduction
display_img(bfilter, "bilateralFilter")
edged = cv2.Canny(bfilter, 500, 700) #Edge detection
display_img(edged, "edged")
result=pytesseract.image_to_string(gray)

print(result)
#input()
