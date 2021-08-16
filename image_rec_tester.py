import pyautogui, cv2, time, win32gui, numpy as np

"""
This program tests image recognition and makes sure the images stored work as expected

Process:
Take file paths to images 1 and 2
Display image 1
Check for image 2 in image 1
image 3 = image 1
Draw rect of image 2 in image 3
Display image 1, 2, 3 - top left, top right and bottom centre respectively
Return pos
"""

#Gets the x and y coords of a needle image from a haystack parameter
def get_image_pos(filepath, needle, haystack)-> tuple:  #Returns (x1, y1, w, h)
    box = pyautogui.locateOnScreen(filepath + needle + ".jpg", region=haystack, grayscale=True, confidence=0.95)  #Returns (x1, y1, w, h) or None
    if box != None:
        return (box[0], box[1], box[2], box[3])

#Converts coords between (0, 0) reference frame and a window
def relative(point, reference, mode = "from00")-> tuple: #Returns same lenght tuple inputted as point
    if len(point) % 2 == 1:
        raise CustomError('relative - tuple point must have an even number of items')
    if len(point) > 2:
        return (relative(point[:2], reference, mode) + relative(point[2:], reference, mode))  #Recursive call if the length of point is more than 2 that then concatenates tuples on the way up
    if mode == "from00":  #Converts real point to be relative to reference
        return (point[0] - reference[0], point[1] - reference[1])  #e.g. point (110, 150) turns into (10, 25) with reference (100, 125)
    else:  #Converts a relative to be a real value relative to (0, 0)
        return (point[0] + reference[0], point[1] + reference[1])  #e.g. point (10, 25) turns into (110, 150) from reference (100, 125)


#Converts tuples from x2, y2 coords into width and height
def convert_xy_wh(coord, mode = "xy2wh")-> tuple:  #Returns (x1, y1, w, h) or (x1, y1, x2, y2) depending on mode
    if mode == "xy2wh":
        return coord[:2] + (coord[2] - coord[0], coord[3] - coord[1])
    else:
        return coord[:2] + (coord[2] + coord[0], coord[3] + coord[1])

def main(fp, image1, image2):
    #Read in images and prep
    img1 = cv2.imread(fp+image1+".jpg", cv2.IMREAD_COLOR)
    img2 = cv2.imread(fp+image2+".jpg", cv2.IMREAD_COLOR)
    cv2.imshow(image1, img1)
    cv2.setWindowProperty(image1,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty(image1,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
    cv2.moveWindow(image1, 100, 100)
    cv2.imshow(image2, img2)
    cv2.moveWindow(image2, 1500, 200)
    cv2.waitKey(1)

    #Get image 1 dim and location
    image1_xy = win32gui.GetWindowRect(win32gui.FindWindow(None, image1))  #x1, y1, x2, y2
    image1_xy = (image1_xy[0]+8, image1_xy[1]+30, image1_xy[2]-8, image1_xy[3]-8) #Adjusting for Windows invisible pixel border (8 pixels) and header bar (30 pixels)
    image1_wh = convert_xy_wh(image1_xy)
    print(f"image xy: {image1_xy} and wh: {image1_wh}")

    time.sleep(0.5)
    #Take a crop of image 1 +10 pixels in each direction
    sc_window = (image1_wh[0]-10, image1_wh[1]-40, image1_wh[2]+20, image1_wh[3]+50)
    screenshot = pyautogui.screenshot(region=sc_window)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  #Converting it for cv2

    rel_image1_xy = relative(image1_xy, sc_window[:2])  #Gets coords of image 1 edges relative to screenshot to draw outline rectangle as demo
    cv2.rectangle(screenshot, pt1=rel_image1_xy[:2], pt2=rel_image1_xy[2:], color=(0, 0, 255), thickness=2)  #Drawing outline of image 1

    #Find image 2 in image 1
    pos = get_image_pos(fp, image2, image1_wh)  #x1, y1, w, h
    if pos != None:
        #Draw image 2 outline onto image 3 (cropped screenshot)
        conv_pos = convert_xy_wh(pos, "wh2xy")
        rel_pos = relative(conv_pos, sc_window[:2])
        print(f"pos: {pos}\nconverted: {conv_pos}\nrelative: {rel_pos}")
        cv2.rectangle(screenshot, pt1=rel_pos[:2], pt2=rel_pos[2:], color=(0, 255, 0), thickness=2)

    time.sleep(0.5)
    #Show image 3
    cv2.imshow("screenshot", screenshot)
    cv2.moveWindow("screenshot", 500, 400)
    print("Press any key to quit...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    """Edit file path and image names below to test."""

    #Filepath
    fp = "images/misc/"
    #Image file names (images must be .jpg)
    image1 = "sample image"
    image2 = "house"

    main(fp, image1, image2)
