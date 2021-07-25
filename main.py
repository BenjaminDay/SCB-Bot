import pytesseract
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

"""
the plan:

Skip the interaction function for now and just have the program do theoretical calculations and tracking of inventory to see if it is able to do so, then once that is done it can start interaction with the game through the emulator.

This will likely save me a lot of trial and error hassle with the image recognition that I can impletement into a working framework instead.

Skip initial placement method on screen and setup,
do mainloop logic for item tracking and inventory control using some example pics.


Some other ideas:
Have a tracker for stat purposes to show how much the bot has made, sold and what special items it has found.
"""


#Constants
WIDTH, HEIGHT = 1920, 1080  #Will want to find a way to auto determine the borders of the game somehow later
SESSION = time.time()
RAW_IMAGES = ["metal", "wood", "plastic", "seeds", "minerals"]  #Raw items producable in the factories
CRAFT_IMAGES = ["nails", "planks", "hammer", "measuring tape", "shovel", "vegetables", "chairs"]  #Items that can be crafted in commercial buildings
SPECIAL_IMAGES = ["storage camera", "storage lock", "storage bar", "dozer exhaust", "dozer wheel", "dozer blade"]  #Special items like storage, land, beach etc.
ITEM_IMAGES = RAW_IMAGES + CRAFT_IMAGES + SPECIAL_IMAGES  #All item images that are related to inventories


#Globals
level = 11  #Constant atm but will need to check for later so not putting in constants (since it will need to be updated if level-up)
##Use level to extract the file names for the images used from a text file.
inv = {}  #Using a check for level maybe in conjuction with this?
simoleons = 0
#simcash = 0
#gold_keys = 0
#plat_keys = 0
#daily_chest = 0  #Value to be gotten from image rec for time remaining +60s for error buffer

#Displays an inputted image in a new window until keyboard interrupt or until specified delay
def display_img(img, title, delay=0):
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)  #Creates a window and autosizes it to the image once shown.
    cv2.imshow(title, img)  #Paints the image to the window
    cv2.waitKey(delay)  #Delay in seconds looking for a keyboard input (0 for no countdown)
    cv2.destroyAllWindows()  #Closes the window

#Takes an image, cleans it up and reads the numbers then returns them in integer format
def read_num(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #Converts the image to grayscale
    bfilter = cv2.bilateralFilter(gray, 5, 5, 5)  #Noise reduction
    edged = cv2.Canny(bfilter, 400, 600)  #Edge detection
    final = cv2.bitwise_not(edged)  #Inveting the image from black with white text to black text with a white backdrop
    try:
        return int(pytesseract.image_to_string(final, config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789'))  ##Config not working?
    except Exception:  #In case the image_to_string fails to filter out text chars.
        print("read_num - Text does not contain an integer!")
        return -1

#Gets the xy coords of a target image
def image_find(src, target, area = (0,0, 1920, 1080)):  #Source and target string are file paths, area is default 1920x1080 but needs to be changed
    r = pyautogui.locateOnScreen(src+target+".jpg", region=area, grayscale=True, confidence=0.95)  #Looks for first occurance of target
    if r != None:  #If result contains coordinates
        return (r.left, r.top, r.width, r.height)

#Interact with the screen to get camera vertical then using roads to square off orientation
def reset_cam_pos():
    pass

#Normal left mouse down up event
def click(xy):
    win32api.SetCursorPos(xy)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01) #This pauses the script for 0.01 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#Drags from start to finish
def drag_click(start, finish):
    win32api.SetCursorPos(start)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.01 seconds
    win32api.SetCursorPos(finish)
    time.sleep(0.1) #This pauses the script for 0.01 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#Gets the contents of the ingame inventory matching items to quantities using images
def get_inv(area = ()):  ##Need to determine the inventory screen size to reduce load on image_find

    cannot_find = True
    while cannot_find:
        print("Looking for inventory icon...")
        inv_pos = image_find("images/icons/", "storage icon", (0,0, 990, 570))  #Getting coords to the inventory button
        if inv_pos != None:
            x, y, w, h = inv_pos
            centered_inv = (x + w // 2, y + h // 2)  #Taking half the width and height and adding it to x and y coords
            cannot_find = False

            ##Clear up after debugging inventory
            print(f"Inventory Found at: {centered_inv}")
            cv2.rectangle(gamecapture, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)
        else:
            time.sleep(1)

    """
    ##Need to get the bot to click it now using coords
    print("clicking")
    time.sleep(0.5)
    click(centered_inv)
    print("dragging")
    time.sleep(0.5)
    drag_click((540, 342), (540, 63))"""


    inventory = {}
    boxes = []  ##Cleanup once debug done
    snips = []  ##Ditto

    for item in RAW_IMAGES+CRAFT_IMAGES:
        pos = image_find("images/items/production/", item, area)

        if pos != None:
            x, y, w, h = pos
            snippet_area = (x+50, y, 70, h)  #Sets the crop area for the quantity to be extracted from inventory panel

            snip = pyautogui.screenshot(region=snippet_area)  #Takes cropped screenshot
            converted = cv2.cvtColor(np.array(snip), cv2.COLOR_RGB2BGR)  #Converts it into usable image for cv2

            quantity = read_num(converted)  #Cropped image is read and a number is passed back for the item's inventory value
            inventory[item] = quantity  #Item name and value given to dictionary

            ##Cleanup and remove below and snips and boxes once debug complete
            #print(quantity)
            #display_img(final, "snip")
            snips.append((x+58, y+50, quantity))
            boxes.append((x, y, x+w, y+h))

    ##Can also be cleaned up once image rec is working well
    for square in boxes:
        cv2.rectangle(gamecapture, pt1=square[0:2], pt2=square[2:4], color=(0, 255, 0), thickness=2)
    for snip in snips:
        #cv2.rectangle(gamecapture, pt1=snip[0:2], pt2=snip[2:4], color=(0, 0, 255), thickness=2)  #Displays a border for inventory numbers
        cv2.putText(gamecapture, str(snip[2]), snip[0:2], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    return inventory



def main():
    mainloop = True
    while mainloop:
        global gamecapture
        gamecapture = pyautogui.screenshot(region=(0,0, 990, 570))
        gamecapture = cv2.cvtColor(np.array(gamecapture), cv2.COLOR_RGB2BGR)
        inv = get_inv()  #Obtains the inventory data
        ##Cleanup prints after debug
        print(inv)


        display_img(gamecapture, "screenshot")  #Paints window
        #cv2.imshow("title", gamecapture)


print("Executing in 2 seconds...")
time.sleep(1)
print("Executing in 1 seconds...")
time.sleep(1)
print("Executing.")

main()
