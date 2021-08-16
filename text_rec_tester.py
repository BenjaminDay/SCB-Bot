import time, pyautogui, cv2, imutils, easyocr, win32gui, numpy as np
from matplotlib import pyplot as plt
from image_rec_tester import get_image_pos, relative, convert_xy_wh

"""
This program tests text recognition and makes sure the text being read is correct and returns as expected

Process:
Take file path and image name
Display image
Take preset and crop image (if run outside of this program the preset is cropped from the screenshot of the screen instead)
Display crop in grayscale
Read text and return
"""

def get_text(preset, reference)-> str:  #preset is a tuple x1, y1, w, h for a region on the screen relative to the game window
    real_crop = relative(preset[:2], reference, "to00")+preset[2:]
    #Grab screenshot using the real_crop and convert for cv2 grayscale
    crop = pyautogui.screenshot(region=real_crop)
    grayscaled = cv2.cvtColor(np.array(crop), cv2.COLOR_BGR2GRAY)

    reader = easyocr.Reader(['en'])
    result = reader.readtext(grayscaled)
    return result[0][1]

def get_text_show(preset, reference)-> str:  #preset is a tuple x1, y1, w, h for a region on the screen relative to the game window
    real_crop = relative(preset[:2], reference, "to00")+preset[2:]
    #Grab screenshot using the real_crop and convert for cv2 grayscale
    crop = pyautogui.screenshot(region=real_crop)
    grayscaled = cv2.cvtColor(np.array(crop), cv2.COLOR_BGR2GRAY)

    reader = easyocr.Reader(['en'])
    return grayscaled, reader.readtext(grayscaled)

def main(fp, image, preset):
    #Read in image and prep
    img = cv2.imread(fp+image+".jpg", cv2.IMREAD_COLOR)
    cv2.imshow(image, img)
    cv2.setWindowProperty(image,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty(image,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
    cv2.moveWindow(image, 100, 100)
    cv2.waitKey(1)

    #Get image dim and location
    image_xy = win32gui.GetWindowRect(win32gui.FindWindow(None, image))  #x1, y1, x2, y2
    image_xy = (image_xy[0]+8, image_xy[1]+30, image_xy[2]-8, image_xy[3]-8) #Adjusting for Windows invisible pixel border (8 pixels) and header bar (30 pixels)
    image_wh = convert_xy_wh(image_xy)
    #print(f"image xy: {image_xy} and wh: {image_wh}")

    time.sleep(0.5)

    grayscaled, text = get_text_show(preset["placeholder"], image_xy)

    #Displaying the images
    cv2.imshow("grayscaled", grayscaled)
    cv2.moveWindow("grayscaled", 500, 400)
    print(text)

    print("Press any key to quit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    """Edit file path, image name and preset coords below to test."""

    example = 6

    if example == 1:
        #Filepath
        fp = "images/raw/"
        #Image file name (images must be .jpg)
        image = "claim"
        preset = {"placeholder": (30, 465, 145, 50)}
    elif example == 2:
        #Filepath
        fp = "images/raw/"
        #Image file name (images must be .jpg)
        image = "claimed"
        preset = {"placeholder": (60, 362, 80, 25)}
    elif example == 3:
        #Filepath
        fp = "images/raw/"
        #Image file name (images must be .jpg)
        image = "cargo 1"
        preset = {"placeholder": (118, 60, 30, 25)}
    elif example == 4:
        #Filepath
        fp = "images/raw/"
        #Image file name (images must be .jpg)
        image = "global 9"
        preset = {"placeholder": (60, 180, 28, 20)}
    elif example == 5:
        #Filepath
        fp = "images/raw/"
        #Image file name (images must be .jpg)
        image = "global 2"
        preset = {"placeholder": (210, 360, 150, 28)}
    elif example == 6:
        #Filepath
        fp = "images/todo/"
        #Image file name (images must be .jpg)
        image = "daily 2"
        preset = {"placeholder": (10, 240, 150, 60)}


    main(fp, image, preset)
